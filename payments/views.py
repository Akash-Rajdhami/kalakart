import uuid
import requests

from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction

from cart.models import Cart
from orders.models import Order
from products.models import Product


@login_required
def PaymentView(request):

    cart_items = Cart.objects.filter(user=request.user)

    if not cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect("cart")

    total = 0

    for item in cart_items:
        total += item.product.price * item.quantity

    if request.method == "POST":

        # Khalti requires amount in paisa
        amount_paisa = int(total * 100)

        # Create a unique order ID
        purchase_order_id = "KK-" + uuid.uuid4().hex[:10]

        # Save payment information in session
        request.session["purchase_order_id"] = purchase_order_id
        request.session["payment_amount"] = amount_paisa

        payload = {
            "return_url": request.build_absolute_uri(
                "/payment/success/"
            ),
            "website_url": request.build_absolute_uri("/"),
            "amount": amount_paisa,
            "purchase_order_id": purchase_order_id,
            "purchase_order_name": "KalaKart Order",
            "customer_info": {
                "name": request.user.get_full_name()
                or request.user.username,
                "email": request.user.email,
                "phone": request.user.phone_number or "",
            },
        }

        headers = {
            "Authorization": f"Key {settings.KHALTI_SECRET_KEY}",
            "Content-Type": "application/json",
        }

        try:

            response = requests.post(
                "https://dev.khalti.com/api/v2/epayment/initiate/",
                json=payload,
                headers=headers,
                timeout=10,
            )

            data = response.json()

            # Temporary debugging information
            print("KHALTI STATUS:", response.status_code)
            print("KHALTI RESPONSE:", data)

            if response.status_code == 200 and data.get("payment_url"):

                request.session["khalti_pidx"] = data["pidx"]

                return redirect(data["payment_url"])

            messages.error(
                request,
                f"Khalti error: {data}"
            )

        except requests.RequestException:

            messages.error(
                request,
                "Unable to connect to Khalti. Please try again."
            )

    context = {
        "cart_items": cart_items,
        "total": total,
    }

    return render(
        request,
        "payments/payment.html",
        context
    )



@login_required
def PaymentSuccessView(request):

    pidx = request.GET.get("pidx")

    if not pidx:
        messages.error(request, "Payment information was not received.")
        return redirect("payment-failed")

    # Verify this callback matches the payment initiated in this session.
    if pidx != request.session.get("khalti_pidx"):
        messages.error(request, "Invalid payment session.")
        return redirect("payment-failed")

    amount_paisa = request.session.get("payment_amount")

    if not amount_paisa:
        messages.error(request, "Payment session has expired.")
        return redirect("payment-failed")

    headers = {
        "Authorization": f"Key {settings.KHALTI_SECRET_KEY}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(
            "https://dev.khalti.com/api/v2/epayment/lookup/",
            json={"pidx": pidx},
            headers=headers,
            timeout=10,
        )
        data = response.json()

    except (requests.RequestException, ValueError):
        messages.error(request, "Unable to verify payment with Khalti.")
        return redirect("payment-failed")

    if not (
        response.status_code == 200
        and data.get("status") == "Completed"
        and data.get("total_amount") == amount_paisa
    ):
        messages.error(request, "Payment was not completed or could not be verified.")
        return redirect("payment-failed")

    try:
        with transaction.atomic():

            cart_items = list(
                Cart.objects.filter(user=request.user)
                .select_related("product")
                .order_by("product_id")
            )

            if not cart_items:
                messages.error(request, "Your cart is empty.")
                return redirect("payment-failed")

            # Lock and check every product before creating orders.
            locked_products = {}

            for item in cart_items:
                if item.product_id not in locked_products:
                    product = Product.objects.select_for_update().get(
                        pk=item.product_id
                    )
                    locked_products[item.product_id] = product

                product = locked_products[item.product_id]

                if item.quantity < 1 or product.stock < item.quantity:
                    messages.error(
                        request,
                        f"Insufficient stock for {product.name}. "
                        "Your payment was completed, so please contact "
                        "the store administrator about your payment/refund."
                    )
                    return redirect("payment-failed")

            # Create orders and deduct stock exactly once in this transaction.
            for item in cart_items:
                product = locked_products[item.product_id]

                Order.objects.create(
                    user=request.user,
                    product=product,
                    quantity=item.quantity,
                    price=product.price,
                    total_price=product.price * item.quantity,
                )

                product.stock -= item.quantity
                product.save(update_fields=["stock"])

            Cart.objects.filter(user=request.user).delete()

    except Product.DoesNotExist:
        messages.error(
            request,
            "A product in your cart is no longer available. "
            "Please contact the store administrator about your payment."
        )
        return redirect("payment-failed")

    # Clear payment information after a successful order.
    request.session.pop("khalti_pidx", None)
    request.session.pop("purchase_order_id", None)
    request.session.pop("payment_amount", None)

    messages.success(
        request,
        "Payment successful! Your order has been placed."
    )

    return render(
        request,
        "payments/payment_success.html",
        {"transaction_id": data.get("transaction_id")},
    )


@login_required
def PaymentFailedView(request):

    return render(
        request,
        "payments/payment_failed.html"
    )