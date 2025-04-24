import os
import requests
from flask import Flask, request, render_template, redirect, url_for
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# PayPal API credentials
PAYPAL_CLIENT_ID = os.getenv("AS65CQOi1NgNfqFsEdrSWxOww7AOiV6EtR3A2H8BVQisHBQ7ratHjABN7mI4s3XHC_UcZwRREMXZE4I6")
PAYPAL_CLIENT_SECRET = os.getenv("EHnAi6d-XyQDKXAB-pjL0IljAohrRbfUjSE10q7h7uDx04MZspfsxtBbL04j5_ezx6NuaGCeLwp0pPxc")
PAYPAL_API_BASE = "https://api-m.sandbox.paypal.com"

# Simple in-memory store
invoices = {}
freelancer_earnings = {"total_received": 0.0, "tax_saved": 0.0}


def get_paypal_access_token():
    response = requests.post(
        f"{PAYPAL_API_BASE}/v1/oauth2/token",
        auth=(PAYPAL_CLIENT_ID, PAYPAL_CLIENT_SECRET),
        headers={"Accept": "application/json"},
        data={"grant_type": "client_credentials"},
    )
    return response.json()["access_token"]


@app.route("/")
def dashboard():
    return render_template("dashboard.html", invoices=invoices, earnings=freelancer_earnings)


@app.route("/invoice/new", methods=["GET", "POST"])
def create_invoice():
    if request.method == "POST":
        email = request.form["email"]
        amount = request.form["amount"]

        access_token = get_paypal_access_token()

        invoice_payload = {
            "detail": {"currency_code": "USD", "note": "Freela Invoice"},
            "invoicer": {"name": {"given_name": "Ana", "surname": "Vargas"}},
            "primary_recipients": [{"billing_info": {"email_address": email}}],
            "items": [{
                "name": "Freelance Work",
                "quantity": "1",
                "unit_amount": {"currency_code": "USD", "value": amount}
            }]
        }

        response = requests.post(
            f"{PAYPAL_API_BASE}/v2/invoicing/invoices",
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {access_token}"},
            json=invoice_payload,
        )

        invoice = response.json()
        invoice_id = invoice["id"]
        href = f"{invoice['href']}"

        # Send the invoice
        requests.post(
            f"{PAYPAL_API_BASE}/v2/invoicing/invoices/{invoice_id}/send",
            headers={"Authorization": f"Bearer {access_token}"}
        )

        invoices[invoice_id] = {
            "email": email,
            "amount": float(amount),
            "status": "SENT",
            "paypal_url": f"https://www.sandbox.paypal.com/invoice/payerView/details/{invoice_id}",
        }

        return redirect(url_for("dashboard"))

    return render_template("invoice_form.html")


@app.route("/webhook", methods=["POST"])
def paypal_webhook():
    data = request.json
    if data["event_type"] == "INVOICING.INVOICE.PAID":
        invoice_id = data["resource"]["id"]
        if invoice_id in invoices:
            invoices[invoice_id]["status"] = "PAID"
            amount = invoices[invoice_id]["amount"]
            tax_saved = round(amount * 0.20, 2)
            freelancer_earnings["total_received"] += amount
            freelancer_earnings["tax_saved"] += tax_saved
    return "", 200


if __name__ == "__main__":
    app.run(debug=True,port=5010)
