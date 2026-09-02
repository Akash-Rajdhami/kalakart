import uuid
import requests

from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from cart.models import Cart
from orders.models import Order


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
        messages.error(
            request,
            "Payment information was not received."
        )
        return redirect("payment-failed")

    amount_paisa = request.session.get("payment_amount")

    if not amount_paisa:
        messages.error(
            request,
            "Payment session has expired."
        )
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

    except requests.RequestException:

        messages.error(
            request,
            "Unable to verify payment with Khalti."
        )
        return redirect("payment-failed")

    # Payment must be completed and amount must match
    if (
        response.status_code == 200
        and data.get("status") == "Completed"
        and data.get("total_amount") == amount_paisa
    ):

        cart_items = Cart.objects.filter(
            user=request.user
        )

        if not cart_items.exists():
            messages.error(
                request,
                "Your cart is empty."
            )
            return redirect("payment-failed")

        for item in cart_items:

            Order.objects.create(
                user=request.user,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
                total_price=item.product.price * item.quantity,
            )

        cart_items.delete()

        # Remove payment information from session
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
            {
                "transaction_id": data.get("transaction_id"),
            }
        )

    messages.error(
        request,
        "Payment was not completed."
    )

    return redirect("payment-failed")


@login_required
def PaymentFailedView(request):

    return render(
        request,
        "payments/payment_failed.html"
    )