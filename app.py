from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)


orders = []
feedback_list = []
checkin_records = []
checkout_records = []


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


@app.route('/checkin', methods=['GET', 'POST'])
def checkin():
    if request.method == 'POST':
        checkin_data = {
            'guest_name': request.form.get('guest_name'),
            'email': request.form.get('email'),
            'phone': request.form.get('phone'),
            'arrival_date': request.form.get('arrival_date'),
            'departure_date': request.form.get('departure_date'),
            'room_preference': request.form.get('room_preference'),
            'special_requests': request.form.get('special_requests'),
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        
        room_number = f"{len(checkin_records) + 101}"
        checkin_data['room_number'] = room_number
        
        checkin_records.append(checkin_data)
        
        
        confirmation = {
            'message': f"Check-in successful! Your room number is {room_number}",
            'room_number': room_number,
            'guest_name': checkin_data['guest_name']
        }
        return render_template('checkin_confirmation.html', confirmation=confirmation)
    
    return render_template('checkin.html')


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        checkout_data = {
            'room_number': request.form.get('room_number'),
            'guest_name': request.form.get('guest_name'),
            'checkout_date': request.form.get('checkout_date'),
            'payment_method': request.form.get('payment_method'),
            'feedback': request.form.get('feedback'),
            'room_rating': request.form.get('room_rating'),
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        checkout_records.append(checkout_data)
        
       
        for record in checkin_records:
            if (record['room_number'] == checkout_data['room_number'] and 
                record['guest_name'].lower() == checkout_data['guest_name'].lower()):
                checkin_records.remove(record)
                break
        
        return redirect(url_for('checkout_confirmation'))
    
    return render_template('checkout.html')


@app.route('/checkout-confirmation')
def checkout_confirmation():
    return render_template('checkout_confirmation.html')


@app.route('/admin/records')
def view_records():
    return render_template('admin_records.html',
                         checkins=checkin_records,
                         checkouts=checkout_records,
                         orders=orders,
                         feedback=feedback_list)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html'), 500


@app.route('/check-availability', methods=['GET', 'POST'])
def check_availability():
    if request.method == 'POST':
        check_date = request.form.get('check_date')
        room_type = request.form.get('room_type')
        
       
       
        available = True 
        
        return render_template('availability.html',
                             available=available,
                             date=check_date,
                             room_type=room_type)
    
    return render_template('check_availability.html')

if __name__ == '__main__':
    app.config['SECRET_KEY'] = 'your-secret-key-here'  
    app.run(debug=True, host='0.0.0.0', port=8080)  

