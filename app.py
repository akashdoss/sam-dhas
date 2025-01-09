from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# Temporary storage for orders
orders = []

@app.route('/')
def home():
    return render_template('index.html', orders=orders)

@app.route('/order', methods=['POST'])
def order():
    service = request.form.get('service')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    orders.append({'service': service, 'timestamp': timestamp})
    return redirect(url_for('home'))

@app.route('/cancel', methods=['POST'])
def cancel():
    order_to_cancel = request.form.get('order')
    orders[:] = [order for order in orders if order['service'] != order_to_cancel]
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
