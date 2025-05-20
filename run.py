from flask import Flask, render_template
import pymysql
import os

pymysql.install_as_MySQLdb()

app = Flask(__name__)

# Import routes correctly using `app.routes`
from app.routes.bas_routes import bas_routes
from app.routes.bill_routes import bill_routes
from app.routes.cash_flow_routes import cash_flow_routes
from app.routes.company_routes import company_routes
from app.routes.financial_routes import financial_routes
from app.routes.invoice_routes import invoice_routes
from app.routes.ledger_routes import ledger_routes
from app.routes.payroll_routes import payroll_routes
from app.routes.purchase_order_routes import purchase_order_routes
from app.routes.quote_routes import quote_routes
from app.routes.report_routes import report_routes
from app.routes.transaction_routes import transaction_routes

# Register Blueprints
app.register_blueprint(bas_routes)
app.register_blueprint(bill_routes)
app.register_blueprint(cash_flow_routes)
app.register_blueprint(company_routes)
app.register_blueprint(financial_routes)
app.register_blueprint(invoice_routes)
app.register_blueprint(ledger_routes)
app.register_blueprint(payroll_routes)
app.register_blueprint(purchase_order_routes)
app.register_blueprint(quote_routes)
app.register_blueprint(report_routes)
app.register_blueprint(transaction_routes)

@app.route('/')
def home():
    return render_template("index.html")  # ✅ Now properly loads the homepage!

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
