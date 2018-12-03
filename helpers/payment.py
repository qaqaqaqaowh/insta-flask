import braintree
import os

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id=os.environ.get("MERCHANT_ID"),
        public_key=os.environ.get("PUBLIC_KEY"),
        private_key=os.environ.get("PRIVATE_KEY")
    )
)


def bt_pay(nonce, amount):

    result = gateway.transaction.sale({
        "amount": f"{amount}",
        "payment_method_nonce": nonce,
        "options": {
            "submit_for_settlement": True
        }
    })
    return result
