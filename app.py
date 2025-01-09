from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

orders = []  
feedback_list = []  

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/history')
def history():
    return render_template('history.html', orders=orders)

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        
        feedback_data = {
            'room': request.form.get('room'),
            'name': request.form.get('name'),
            'email': request.form.get('email'),
            'phone': request.form.get('phone'),
            'category': request.form.get('category'),
            'feedback': request.form.get('feedback'),
            'rating': request.form.get('rating'),
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        feedback_list.append(feedback_data)
        return redirect(url_for('thank_you'))
    return render_template('contact.html')

@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')

@app.route('/order', methods=['POST'])
def order():
    service = request.form['service']
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    orders.append({'service': service, 'timestamp': timestamp})
    return redirect(url_for('home'))

@app.route('/cancel', methods=['POST'])
def cancel():
    service = request.form['order']
    orders[:] = [order for order in orders if order['service'] != service]
    return redirect(url_for('history'))

if __name__ == '__main__':
    app.run(debug=True)
