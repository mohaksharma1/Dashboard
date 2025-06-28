import base64
import datetime,subprocess, sys
import os
import shutil
import sqlite3


from flask import Flask, request, send_from_directory, render_template
from updater import check_update

database = 'orders.db'

def getTotalPurchase():
    conn = sqlite3.connect(database, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Purchase ")
    items = cursor.fetchall()
    # print(items)
    total_purchase=0
    for purchase_item in items:
        total_purchase= total_purchase + float(str(purchase_item[2]).replace(",",""))
    conn.commit();
    conn.close()
    gtotal_purchase=total_purchase
    return total_purchase

def getTotalSale():
    conn = sqlite3.connect(database, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Sales")
    items = cursor.fetchall()
    # print(items)
    total_purchase=0
    for purchase_item in items:
        total_purchase= total_purchase + float(str(purchase_item[2]).replace(",",""))
    conn.commit();
    conn.close()
    gtotal_purchase=total_purchase
    return total_purchase

def get_order(order_id):
    conn = sqlite3.connect(database, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT product_name, quantity, price FROM OrderDetails WHERE order_id=?", (order_id,))
    order_items = cursor.fetchall()
    print(order_items)
    cursor.execute("SELECT order_id, order_date, customer_name, mobile_no, place, remarks FROM Orders WHERE order_id=?",
                   (order_id,))
    orderss = cursor.fetchall()
    conn.commit()
    conn.close()
    # print(orderss)
    return order_items, orderss


app = Flask(__name__, static_folder="static")


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.static_folder, 'favicon.ico')


@app.route('/bill.png')
def bill():
    return send_from_directory(app.static_folder, 'bill.png')


@app.route('/icon.png')
def icon():
    return send_from_directory(app.static_folder, 'icon.png')


@app.route('/')
def welcome():
    msg=" "
    if getTotalSale()> getTotalPurchase():
        msg=f"Net Profit is <b>₹ {getTotalSale()-getTotalPurchase()} </b>"
    else:
        msg=f"Net Loss is <b>₹ {getTotalSale()-getTotalPurchase()} </b>"
    upd=""
    if check_update()==1:
        upd="Update Availble"

    return '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Silver Scissors Admin Dashboard</title>
    <style>
        /* Basic CSS styling for a clean and beautiful admin page */
        body {
            font-family: Arial, sans-serif;
            background-color: #f8f9fa;
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            width: 80%;
            max-width: 800px;
            padding: 20px;
            background-color: #ffffff;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            border-radius: 8px;
            text-align: center;
        }
        h1 {
            color: #4a4a4a;
            margin-bottom: 20px;
        }
        .section-title {
            font-size: 1.2em;
            margin-top: 20px;
            color: #007bff;
            border-bottom: 2px solid #007bff;
            display: inline-block;
            padding-bottom: 5px;
        }
        .button-container {
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            justify-content: center;
            margin-top: 10px;
        }
        .button {
            padding: 15px 20px;
            font-size: 16px;
            color: #ffffff;
            background-color: #007bff;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            text-decoration: none;
            width: 180px;
            text-align: center;
            transition: background-color 0.3s;
        }
        .button:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>

<div class="container">
    <h1>Welcome to Silver Scissors Admin Dashboard</h1>
    <p>Manage orders, ledger, and status efficiently with categorized tools.</p>
    '''+f'''<p>{msg}</p>
    <p>{upd}</p>
    '''+'''
    
    <!-- Orders Section -->
    <h2 class="section-title">Orders</h2>
    <div class="button-container">
        <a href="/form" class="button">Place Order</a>
        <a href="/setOrder" class="button">Edit Order</a>
        <a href="/review" class="button">View All Orders</a>
    </div>

    <!-- Ledger Section -->
    <h2 class="section-title">Ledger</h2>
    <div class="button-container">
        <a href="/setBill" class="button">Get Bill</a>
        <a href="/putpurchase" class="button">Insert Purchase</a>
        <a href="/getpurchase" class="button">View All Purchases</a>
        <a href="/putsale" class="button">Insert Sale</a>
        <a href="/getsales" class="button">View All Sales</a>
    </div>

    <!-- Status Section -->
    <h2 class="section-title">Status</h2>
    <div class="button-container">
        <a href="/setstatus" class="button">Update Status</a>
        <a href="/getstatusall" class="button">View All Status</a>
    </div>
</div>

</body>
</html>

    '''


@app.route('/home')
def home():
    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <link rel="icon" type="image/png" href="icon.png">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Silver Scissors</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            margin: 0;
            padding: 0;
            background-color: #f2f2f2;
        }
        .container {
            margin-top: 100px;
        }
        h1 {
            color: #333;
        }
        button {
            background-color: #4CAF50;
            color: white;
            padding: 15px 30px;
            margin: 20px;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
        }
        button:hover {
            background-color: #45a049;
        }
    </style>
</head>
<body>

    <div class="container">
        <h1>Welcome to Silver Scissors</h1>
        <button onclick="placeOrder()">Place Order</button>
        <button onclick="reviewOrder()">List Orders</button>
        <button onclick="getBill()">Get Bill</button>
        <button onclick="editOrder()">Edit order</button>
        <button onclick="getStatus()">View Status</button>
        <button onclick="setStatus()">Edit Status</button>
        <button onclick="getSales()">Sales</button>
        <button onclick="window.location.href = 'putsale'">New Sale</button>
        <button onclick="getPurchase()">Purchase</button>
        <button onclick="window.location.href = 'putpurchase'">New Purchase</button>
    </div>

    <script>
    
    function getPurchase() {
            window.location.href = 'getpurchase';
        }
    function getSales() {
            window.location.href = 'getsales';
        }
    
    function getStatus() {
            window.location.href = 'getstatusall';
        }
        
        function setStatus() {
            window.location.href = 'setstatus';
        }
    
        function placeOrder() {
            window.location.href = 'form';
        }

        function reviewOrder() {
            
            window.location.href = 'review';
        }
        
        function getBill() {
            
            window.location.href = 'setBill';
        }
        
        function editOrder() {
            
            window.location.href = 'setOrder';
        }
    </script>

</body>
</html>
'''


@app.route('/setBill')
def setBill():
    return '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>SILVER SCISSORS</title>
        </head>
        <body>

            <h2>SILVER SCISSORS BILLING SERVICE (Live)</h2>
            <form action="/getBill" method="POST">
            
                <label >ORDER NO :  </label>
                <input type="text" id="orderno" name="orderno" required><br><br>
            
                <input type="submit" value="Submit">
            </form>
           
            <br><br>
            <button onclick="back()">Back</button>
        <script>
        function back(){
            window.location.href = '/';
        }
        </script>
        </body>
        </html>
        '''


# Route to handle form submission
@app.route('/getBill', methods=['POST'])
def getBill():
    order_date = ""
    total = 0
    order_no = int(request.form['orderno'])
    order_items, orderss = get_order(order_no)
    table = ''' '''
    for order in orderss:
        if order:
            order_date = datetime.datetime.strptime(order[1], "%Y-%m-%d").strftime("%d %B %Y")
            name = order[2]
            place = order[4]
            phone = order[3]
    for product_name, quantity, price in order_items:
        amount = int(quantity) * int(price)
        table = table + f'''<tr>
                <td>{product_name.upper()}</td>
                <td>{quantity}</td>
                <td>₹{price}</td>
                <td>₹{amount}</td>
            </tr>
            '''
        total = total + amount

    return '''
   <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Silver Scissors Company Bill</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 600px;
            background-color: white;
            padding: 20px;
            margin: 0 auto;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        
        .container2 {
 display: grid;
 align-items: center; 
 grid-template-columns: 1fr 1fr 1fr;
 column-gap: 5px;
}
        
        h2 {
            text-align: center;
            color: #333;
            margin-bottom: 20px;
        }
        .bill-info {
            display: flex;
            justify-content: space-between;
            margin-bottom: 20px;
            color: #555;
        }
        .bill-info div {
            width: 48%;
        }
        .bill-info label {
            font-weight: bold;
            color: #333;
        }
        .items-table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }
        .items-table th, .items-table td {
            border: 1px solid #ddd;
            padding: 10px;
            text-align: left;
        }
        .items-table th {
            background-color: #f2f2f2;
            font-weight: bold;
            color: #555;
        }
        .items-table td {
            background-color: #fcfcfc;
        }
        .total-section {
            text-align: right;
            margin-top: 20px;
        }
        .total-section label {
            font-size: 18px;
            font-weight: bold;
            color: #333;
        }
        .total-section span {
            font-size: 20px;
            color: #28a745;
        }
        .print-button {
            display: block;
            width: 100%;
            padding: 10px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 5px;
            text-align: center;
            cursor: pointer;
            font-size: 16px;
        }
        .print-button:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>
<div id="capture">
<div class="container">
''' + f'''
<div class="container2">
<div class="image">
        <img src="icon.png" height="100" width="100">
      </div>
     <h2>Silver Scissors</h2>
     </div>
    <h2>INVOICE</h2>
    
    <!-- Bill Information -->
    <div class="bill-info">
        <div>
            <label>Order Number:</label>
            <p>{order_no}</p>
        </div>
        <div>
            <label>Date of Order:</label>
            <p>{order_date}</p>
        </div>
    </div>
    
    <div class="bill-info">
        <div>
            <label>Customer Name:</label>
            <p>{name.upper()}</p>
        </div>
        <div>
            <label>Place:</label>
            <p>{place}</p>
        </div>
    </div>

    <!-- Items Table -->
    <table class="items-table">
        <thead>
            <tr>
                <th>Item Description</th>
                <th>Quantity</th>
                <th>Price</th>
                <th>Amount</th>
            </tr>
        </thead>
        <tbody>''' + table + f'''
        </tbody>
    </table>

    <!-- Total Amount -->
    <div class="total-section">
        <label>Total: </label>
        <span>₹ {total}</span>
    </div>

    
</div>
</div>''' + '''
<button id="capture-btn">Share on Whatsapp</button>

    <script>

        document.getElementById('capture-btn').addEventListener('click', function() {
            html2canvas(document.querySelector("#capture")).then(canvas => {
                              
                const form = document.createElement('form');

        // Set the form's attributes
        form.action = 'testsubmit'; // Replace with your action URL
        form.method = 'POST'; // or 'GET', depending on your needs

        // Create an input element
        const input = document.createElement('input');
        input.type = 'hidden'; // use 'hidden' to keep it out of view
        input.name = 'imgdata'; // Name of the input
        input.value = canvas.toDataURL(); // Value to send

        // Append the input to the form
        form.appendChild(input);
        
        const input2 = document.createElement('input');
        input2.type = 'hidden'; // use 'hidden' to keep it out of view
        input2.name = 'phone'; // Name of the input
        input2.value = ''' + phone + ''' // Value to send
        form.appendChild(input2);

        // Append the form to the body (optional)
        document.body.appendChild(form);

        // Submit the form
        form.submit();
            });
        });
    </script>
</body>
</html>

'''


@app.route('/review', methods=['GET'])
def review():
    db = sqlite3.connect(database)  # Connect to the database
    db.row_factory = sqlite3.Row
    rows = db.execute('SELECT * FROM Orders').fetchall()
    rows2 = db.execute('SELECT * FROM OrderDetails').fetchall()
    db.close()
    return render_template('view.html', rows=rows, rows2=rows2)


# Route to display the form
@app.route('/form', methods=['GET'])
def form():
    return '''
        <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Silver Scissors </title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f5f5f5;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 600px;
            background-color: white;
            padding: 20px;
            margin: 0 auto;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        h2 {
            text-align: center;
            color: #333;
        }
        label {
            display: block;
            margin: 15px 0 5px;
            color: #555;
        }
        input, textarea, select {
            width: 100%;
            padding: 10px;
            margin: 5px 0;
            border: 1px solid #ccc;
            border-radius: 5px;
            box-sizing: border-box;
        }
        textarea {
            height: 100px;
        }
        .form-group {
            margin-bottom: 15px;
        }
        button {
            display: block;
            width: 100%;
            padding: 10px;
            background-color: #28a745;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover {
            background-color: #218838;
        }
         .object {
            border: 1px solid #ccc;
            padding: 10px;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
''' + f'''
<div class="container">
        <h2>Silver Scissors Order service</h2>
<form action="/submitOrder" method="POST">

        <!-- Name of Customer -->
        <div class="form-group">
            <label for="customer-name">Name of Customer</label>
                <input type="text" id="name" name="name" required>
        </div>
        
        <!-- Name of Customer -->
        <div class="form-group">
            <label for="phone">PHONE NO</label>
                <input type="text" id="phone" name="phone" >
        </div>
        
        <!-- Address -->
        <div class="form-group">
            <label for="place">Place</label>
                <input type="text" id="place" name="place" required>
        </div>

        <!-- Date of Order -->
        <div class="form-group">
            <label for="order-date">Date of Order</label>
                <input type="date" id="date" name="date" required>
        </div>

        
        <div id="objects-container">
            <div class="object">
                <label for="item">Item Name:</label>
                <input type="text" name="item[]" required><br><br>

                <label for="quantity">Quantity:</label>
                <input type="number" name="quantity[]" required><br><br>

                <label for="price">Price:</label>
                <input type="number" name="price[]" required><br><br>
            </div>
        </div>
        
        <button type="button" id="add-object">Add Items</button>

        <!-- Remarks -->
        <div class="form-group">
            <label for="remarks">Remarks</label>
                <textarea id="remarks" name="remarks" rows="4" cols="50" required></textarea>
        </div>

        <!-- Submit Button -->
        <button type="submit">Submit Order</button>
    </form>
</div>
''' + '''
<script>
        document.getElementById('add-object').addEventListener('click', function() {
            // Clone the first object container
            var firstObject = document.querySelector('.object');
            var newObject = firstObject.cloneNode(true);

            // Clear input values in the cloned object
            var inputs = newObject.querySelectorAll('input');
            inputs.forEach(function(input) {
                input.value = '';
            });

            // Append the new object to the objects container
            document.getElementById('objects-container').appendChild(newObject);
        });
    </script>

</body>
</html>

    '''


# Route to handle form submission
@app.route('/submitOrder', methods=['POST'])
def submitOrder():
    conn = sqlite3.connect(database, check_same_thread=False)
    cursor = conn.cursor()
    # Parse the form data
    date = str(request.form['date'])
    cursor.execute("INSERT INTO Orders (order_date, customer_name, mobile_no, place, remarks) VALUES (?, ?, ?, ?, ?)",
                   (date, request.form['name'], request.form['phone'], request.form['place'], request.form['remarks']))
    orderno = cursor.lastrowid
    cursor.execute(
        "INSERT INTO orderStatus (order_id, order_date, customer_name,ready,amt_recvd,dispatched) VALUES (?, ?, ?,?,?,?)",
        (orderno, date, request.form['name'], "false", "false", "false",))
    items = request.form.getlist('item[]')
    qtys = request.form.getlist('quantity[]')
    prices = request.form.getlist('price[]')

    for item, qty, price in zip(items, qtys, prices):
        cursor.execute("INSERT INTO OrderDetails (order_id, product_name, quantity, price) VALUES (?, ?, ?, ?)",
                       (orderno, item, qty, price))
    conn.commit()

    now = datetime.datetime.now()
    date_now = now.strftime("%Y-%m-%d %H:%M:%S")
    log = f"{date_now} : Order No {orderno} - {request.form} \n"
    msg = f"Thank you '{request.form['name']}'. We have recieved your Order. Your order number is {orderno}"

    print(log)
    with open("log.txt", "a") as myfile:
        myfile.write(log)
    conn.close()
    # Display or process the form data
    return '''
    <html>
    <body >
    <script>
    window.onload = function(){
    window.location.href = ''' + f'''"https://wa.me/91{request.form['phone']}/?text={msg}"''' + '''
    }
</script>
''' + f'<a href="https://wa.me/91{request.form['phone']}/?text={msg}">{msg}</a>' + '''
</body>
</html>
'''


@app.route('/setstatus')
def setStatus():
    return '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>SILVER SCISSORS</title>
        </head>
        <body>

            <h2>SILVER SCISSORS BILLING SERVICE (Live)</h2>
            <form action="/getstatus" method="POST">

                <label >ORDER NO :  </label>
                <input type="text" id="orderno" name="orderno" required><br><br>

                <input type="submit" value="Submit">
            </form>

            <br><br>
            <button onclick="back()">Back</button>
        <script>
        function back(){
            window.location.href = '/';
        }
        </script>
        </body>
        </html>
        '''


@app.route('/getstatus', methods=['POST'])
def getStatus():
    conn = sqlite3.connect(database, check_same_thread=False)
    cursor = conn.cursor()
    orderno = request.form["orderno"]
    cursor.execute("SELECT * FROM orderStatus WHERE order_id = ?", (orderno,))
    items = cursor.fetchall()
    for status_items in items:
        if status_items[3] in ['true']:
            ready = "checked"
        else:
            ready = ""
        if status_items[4] in ['true']:
            amt_recvd = "checked"
        else:
            amt_recvd = ""
        if status_items[5] in ['true']:
            dispatched = "checked"
        else:
            dispatched = ""

    conn.commit()
    conn.close()
    return '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Boolean Toggle Form</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .form-container {
            background-color: #fff;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            width: 300px;
            text-align: center;
        }
        h2 {
            margin-bottom: 20px;
        }
        .toggle {
            display: inline-block;
            position: relative;
            width: 60px;
            height: 30px;
        }
        .toggle input {
            display: none;
        }
        .slider {
            position: absolute;
            cursor: pointer;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: #ccc;
            transition: .4s;
            border-radius: 30px;
        }
        .slider:before {
            position: absolute;
            content: "";
            height: 22px;
            width: 22px;
            left: 4px;
            bottom: 4px;
            background-color: white;
            transition: .4s;
            border-radius: 50%;
        }
        input:checked + .slider {
            background-color: #4CAF50;
        }
        input:checked + .slider:before {
            transform: translateX(30px);
        }
        .submit-btn {
            padding: 10px 20px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        .submit-btn:hover {
            background-color: #45a049;
        }
         table {
            width: 75%;
            border-collapse: collapse;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            background-color: white;
        }
        th, td {
            padding: 30px;
            text-align: center;
            font-size: 1.1em;
        }
        th {
            background-color: #4CAF50;
            color: white;
        }
        td {
            color: black;
            font-weight: bold;
        }
    </style>
</head>
<body>

<div class="form-container">
    <h2>Update Order Status</h2>
    
    <form action="/updatestatus" method="post">
       <table>
        <thead>
        <tr>
        <th>Order No</th>
        <th>Order Date</th>
        <th>Name</th>
        <th>Ready</th>
        <th>Amount Recieved</th>
        <th>Dispatched</th>
        </tr>
        </thead>
        
        <tbody>''' + f'''
        <tr>
                <td>{status_items[0]}</td>
                <input type="hidden" name="orderno" id="orderno" value="{status_items[0]}">
                <td>{status_items[1]}</td>
                <td>{status_items[2]}</td>
                <td> <label class="toggle">
            <input type="checkbox" name="ready" {ready}>
            <span class="slider"></span>
        </label></td>
                <td><label class="toggle">
            <input type="checkbox" name="amt_recvd" {amt_recvd}>
            <span class="slider"></span>
        </label></td>
                <td><label class="toggle">
            <input type="checkbox" name="dispatched" {dispatched}>
            <span class="slider"></span>
        </label></td>
            </tr> 
        
        </tbody>
        </table>
        
        
        <button type="submit" class="submit-btn">Submit</button>
    </form>
</div>

</body>
</html>

    '''


@app.route('/updatestatus', methods=['POST'])
def updateStatus():
    conn = sqlite3.connect(database, check_same_thread=False)
    cursor = conn.cursor()
    orderno = request.form["orderno"]
    ready = 'true' if request.form.get('ready') else 'false'
    amt_recvd = 'true' if request.form.get('amt_recvd') else 'false'
    dispatched = 'true' if request.form.get('dispatched') else 'false'
    cursor.execute("UPDATE orderStatus SET ready=?, amt_recvd=?, dispatched = ? WHERE order_id = ?",
                   (ready, amt_recvd, dispatched, orderno,))
    conn.commit();
    conn.close()
    return '''
        <script>
        alert("STATUS UPDATED")
        </script>
        '''


@app.route('/getpurchase')
def getpurchase():
    conn = sqlite3.connect(database, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Purchase ")
    items = cursor.fetchall()
    # print(items)
    total_purchase=0
    table = ''''''
    for purchase_item in items:
        total_purchase= total_purchase + float(str(purchase_item[2]).replace(",",""))
        table = table + f'''
        <tr>
                <td>{purchase_item[0]}</td>
                <td>{purchase_item[1].upper()}</td>
                <td>{purchase_item[2]}</td>
            </tr> 
'''
    conn.commit();
    conn.close()
    gtotal_purchase=total_purchase
    return '''
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sales</title>
    <style>
    .center-container{
            display: flex;
            justify-content: center; /* Center horizontally */
            align-items: center;
            height: 100vh;
            width:100%
    }
    .table-container {
            
            width: 100%; /* Adjust width as needed */
            max-height: 700px; /* Set your desired height */
            overflow-y: auto; /* Enable vertical scroll */
            border: 1px solid #ddd; /* Optional: adds a border around the table */
        }
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        table {
            width: 50%;
            border-collapse: collapse;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            background-color: white;
        }
        th, td {
            padding: 15px;
            text-align: center;
            font-size: 1.1em;
        }
        th {
            background-color: #4CAF50;
            color: white;
        }
        td {
            color: black;
            font-weight: bold;
        }
        .true {
            background-color: #28a745; /* Green */
        }
        .false {
            background-color: #dc3545; /* Red */
        }
    </style>
</head>''' + f'''
<body>
<h1>Total Purchase is ₹{str(total_purchase)}</h1>
<div class="center-container">
<div class="table-container">

    <table border="1">
        <thead>
            <tr>
                <th>Date</th>
                <th>Item Description</th>
                <th>Amount</th>
            </tr>
        </thead>
        <tbody>
        ''' + table + '''

        </tbody>
    </table>
    </div>
    </div>

</body>
</html>

    '''


@app.route('/getsales')
def getsales():
    conn = sqlite3.connect(database, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Sales ")
    items = cursor.fetchall()
    # print(items)
    total_sale=0
    table = ''''''
    for sale_item in items:
        total_sale= total_sale + float(str(sale_item[2]).replace(",",""))
        table = table + f'''
        <tr>
                <td>{sale_item[0]}</td>
                <td>{sale_item[1]}</td>
                <td>{sale_item[2]}</td>
            </tr> 
'''
    conn.commit();
    conn.close()
    gtotal_sale=total_sale
    return '''
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sales</title>
    <style>
    .table-container {
            width: 100%; /* Adjust width as needed */
            max-height: 700px; /* Set your desired height */
            overflow-y: auto; /* Enable vertical scroll */
            border: 1px solid #ddd; /* Optional: adds a border around the table */
        }
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        table {
            width: 50%;
            border-collapse: collapse;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            background-color: white;
        }
        th, td {
            padding: 15px;
            text-align: center;
            font-size: 1.1em;
        }
        th {
            background-color: #4CAF50;
            color: white;
        }
        td {
            color: black;
            font-weight: bold;
        }
        .true {
            background-color: #28a745; /* Green */
        }
        .false {
            background-color: #dc3545; /* Red */
        }
    </style>
</head>''' + f'''
<body>

<h1>Total Sale is ₹{str(total_sale)}</h1>

<div class="table-container">

    <table border="1">
        <thead>
            <tr>
                <th>Date</th>
                <th>Item Description</th>
                <th>Amount</th>
            </tr>
        </thead>
        <tbody>
        ''' + table + '''

        </tbody>
    </table>
    </div>

</body>
</html>

    '''


@app.route('/getstatusall')
def getStatusAll():
    conn = sqlite3.connect(database, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orderStatus ")
    items = cursor.fetchall()
    print(items)
    table = ''''''
    for status_items in items:
        table = table + f'''
        <tr>
                <td>{status_items[0]}</td>
                <td>{status_items[1]}</td>
                <td>{status_items[2]}</td>
                <td class="{status_items[3]}"></td>
                <td class="{status_items[4]}"></td>
                <td class="{status_items[5]}"></td>
            </tr> 
'''
    conn.commit();
    conn.close()
    return '''
   <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sales</title>
    <style>
    .center-container{
            display: flex;
            justify-content: center; /* Center horizontally */
            align-items: center;
            height: 100vh;
            width:100%
    }
    .table-container {
            
            width: 100%; /* Adjust width as needed */
            max-height: 700px; /* Set your desired height */
            overflow-y: auto; /* Enable vertical scroll */
            border: 1px solid #ddd; /* Optional: adds a border around the table */
        }
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        table {
            width: 50%;
            border-collapse: collapse;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            background-color: white;
        }
        th, td {
            padding: 15px;
            text-align: center;
            font-size: 1.1em;
        }
        th {
            background-color: #4CAF50;
            color: white;
        }
        td {
            color: black;
            font-weight: bold;
        }
        .true {
            background-color: #28a745; /* Green */
        }
        .false {
            background-color: #dc3545; /* Red */
        }
    </style>
</head>''' + f'''
<body>
<div class="center-container">
<div class="table-container">

    <table border="1">
        <thead>
            <tr>
                <th>Order No</th>
                <th>Customer Name</th>
                <th>Order Date</th>
                <th>Ready</th>
                <th>Amount Received</th>
                <th>Dispatched</th>
            </tr>
        </thead>
        <tbody>
        ''' + table + '''

        </tbody>
    </table>
    </div>
    </div>

</body>
</html>

    '''


@app.route('/setOrder')
def setOrder():
    return '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>SILVER SCISSORS</title>
        </head>
        <body>

            <h2>SILVER SCISSORS BILLING SERVICE (Live)</h2>
            <form action="/getOrder" method="POST">

                <label >ORDER NO :  </label>
                <input type="text" id="orderno" name="orderno" required><br><br>

                <input type="submit" value="Submit">
            </form>

            <br><br>
            <button onclick="back()">Back</button>
        <script>
        function back(){
            window.location.href = '/';
        }
        </script>
        </body>
        </html>
        '''


@app.route('/getOrder', methods=['POST'])
def getOrder():
    order_no = int(request.form['orderno'])
    order_items, orderss = get_order(order_no)
    table = ''' '''
    for order in orderss:
        if order:
            order_date = order[1]
            name = order[2]
            place = order[4]
            phone = order[3]
            remarks = order[5]
    for product_name, quantity, price in order_items:
        table = table + f'''
        <div class="object">
                <label for="item">Item Name:</label>
                <input type="text" name="item[]" value="{product_name}" required><br><br>

                <label for="quantity">Quantity:</label>
                <input type="number" name="quantity[]" value="{quantity}" required><br><br>

                <label for="price">Price:</label>
                <input type="number" name="price[]" value="{price}" required><br><br>
            </div>
'''
    return '''
        <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Silver Scissors </title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f5f5f5;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 600px;
            background-color: white;
            padding: 20px;
            margin: 0 auto;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        h2 {
            text-align: center;
            color: #333;
        }
        label {
            display: block;
            margin: 15px 0 5px;
            color: #555;
        }
        input, textarea, select {
            width: 100%;
            padding: 10px;
            margin: 5px 0;
            border: 1px solid #ccc;
            border-radius: 5px;
            box-sizing: border-box;
        }
        textarea {
            height: 100px;
        }
        .form-group {
            margin-bottom: 15px;
        }
        button {
            display: block;
            width: 100%;
            padding: 10px;
            background-color: #28a745;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover {
            background-color: #218838;
        }
         .object {
            border: 1px solid #ccc;
            padding: 10px;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
''' + f'''
<div class="container">
        <h2>Silver Scissors Order service</h2>
<form action="/editOrder" method="POST">

        <!-- Name of Customer -->
        <div class="form-group">
            <label for="customer-name">Name of Customer</label>
                <input type="text" id="order" name="order"  value="{order_no}" readonly required>
        </div>
        <!-- Name of Customer -->
        <div class="form-group">
            <label for="customer-name">Name of Customer</label>
                <input type="text" id="name" name="name"  value="{name}" required>
        </div>
        
        <!-- Name of Customer -->
        <div class="form-group">
            <label for="phone">PHONE NO</label>
                <input type="text" id="phone" name="phone" value="{phone}" >
        </div>
        
        <!-- Address -->
        <div class="form-group">
            <label for="place">Place</label>
                <input type="text" id="place" name="place" value="{place}" required>
        </div>

        <!-- Date of Order -->
        <div class="form-group">
            <label for="order-date">Date of Order</label>
                <input type="date" id="date" name="date" value="{order_date}" required>
        </div>

        
        <div id="objects-container">
            ''' + table + f'''
            </div>
        
        <button type="button" id="add-object">Add Items</button>

        <!-- Remarks -->
        <div class="form-group">
            <label for="remarks">Remarks</label>
                <textarea id="remarks" name="remarks" rows="4" cols="50" value="{remarks}" required></textarea>
        </div>

        <!-- Submit Button -->
        <button type="submit">Submit Order</button>
    </form>
</div>
''' + '''
<script>
        document.getElementById('add-object').addEventListener('click', function() {
            // Clone the first object container
            var firstObject = document.querySelector('.object');
            var newObject = firstObject.cloneNode(true);

            // Clear input values in the cloned object
            var inputs = newObject.querySelectorAll('input');
            inputs.forEach(function(input) {
                input.value = '';
            });

            // Append the new object to the objects container
            document.getElementById('objects-container').appendChild(newObject);
        });
    </script>

</body>
</html>
    '''


@app.route('/editOrder', methods=['POST'])
def editOrder():
    conn = sqlite3.connect(database, check_same_thread=False)
    cursor = conn.cursor()
    # Parse the form data
    orderno = request.form['order']
    date = str(request.form['date'])
    cursor.execute(
        "UPDATE Orders SET order_date = ?, customer_name = ?, mobile_no = ?, place = ?, remarks = ? WHERE order_id = ?",
        (date, request.form['name'], request.form['phone'], request.form['place'], request.form['remarks'], orderno,))

    items = request.form.getlist('item[]')
    qtys = request.form.getlist('quantity[]')
    prices = request.form.getlist('price[]')
    cursor.execute("DELETE FROM OrderDetails WHERE order_id = ?",
                   (orderno,))

    for item, qty, price in zip(items, qtys, prices):
        cursor.execute("INSERT INTO OrderDetails (order_id, product_name, quantity, price) VALUES (?, ?, ?, ?)",
                       (orderno, item, qty, price))
    conn.commit()

    now = datetime.datetime.now()
    date_now = now.strftime("%Y-%m-%d %H:%M:%S")
    log = f"{date_now} : Order No {orderno} - {request.form} \n"
    msg = f"Thank you '{request.form['name']}'. We have recieved your Order. Your order number is {orderno}"

    print(log)
    with open("log2.txt", "a") as myfile:
        myfile.write(log)
    conn.commit();
    conn.close()
    # Display or process the form data
    return '''
        <html>
        <body >
        <script>
        window.onload = function(){
        window.location.href = ''' + f'''"https://wa.me/91{request.form['phone']}/?text={msg}"''' + '''
        }
    </script>
    ''' + f'<a href="https://wa.me/91{request.form['phone']}/?text={msg}">{msg}</a>' + '''
    </body>
    </html>
    '''


# Route to display the form
@app.route('/putpurchase', methods=['GET'])
def putpurchase():
    return '''
        <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Silver Scissors </title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f5f5f5;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 600px;
            background-color: white;
            padding: 20px;
            margin: 0 auto;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        h2 {
            text-align: center;
            color: #333;
        }
        label {
            display: block;
            margin: 15px 0 5px;
            color: #555;
        }
        input, textarea, select {
            width: 100%;
            padding: 10px;
            margin: 5px 0;
            border: 1px solid #ccc;
            border-radius: 5px;
            box-sizing: border-box;
        }
        textarea {
            height: 100px;
        }
        .form-group {
            margin-bottom: 15px;
        }
        button {
            display: block;
            width: 100%;
            padding: 10px;
            background-color: #28a745;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover {
            background-color: #218838;
        }
         .object {
            border: 1px solid #ccc;
            padding: 10px;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
''' + f'''
<div class="container">
        <h2>New Purchase</h2>
<form action="/submitpurchase" method="POST">

       

        
        <!-- Date of Order -->
        <div class="form-group">
            <label for="order-date">Date of Order</label>
                <input type="date" id="date" name="date" required>
        </div>
        <div class="form-group">
            <label for="item">Item</label>
                <input type="text" id="item" name="item" required>
        </div>
        <div class="form-group">
            <label for="amount">Amount</label>
                <input type="number" id="amount" name="amount" required>
        </div>


       

        <!-- Submit Button -->
        <button type="submit">Submit</button>
    </form>
</div>

</body>
</html>

    '''


# Route to handle form submission
@app.route('/submitpurchase', methods=['POST'])
def submitpurchase():
    conn = sqlite3.connect(database, check_same_thread=False)
    cursor = conn.cursor()
    # Parse the form data

    cursor.execute("INSERT INTO Purchase (date, item, amount) VALUES (?, ?, ?)",
                   (request.form["date"], request.form["item"], request.form["amount"]))
    conn.commit()

    conn.close()
    # Display or process the form data
    return '''
    <html>
    <body >
    <script>
    window.onload = function(){
    alert("Updated")
    window.location.href = "/"
    }
</script>

</body>
</html>
'''


# Route to display the form
@app.route('/putsale', methods=['GET'])
def putsale():
    return '''
        <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Silver Scissors </title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f5f5f5;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 600px;
            background-color: white;
            padding: 20px;
            margin: 0 auto;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        h2 {
            text-align: center;
            color: #333;
        }
        label {
            display: block;
            margin: 15px 0 5px;
            color: #555;
        }
        input, textarea, select {
            width: 100%;
            padding: 10px;
            margin: 5px 0;
            border: 1px solid #ccc;
            border-radius: 5px;
            box-sizing: border-box;
        }
        textarea {
            height: 100px;
        }
        .form-group {
            margin-bottom: 15px;
        }
        button {
            display: block;
            width: 100%;
            padding: 10px;
            background-color: #28a745;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover {
            background-color: #218838;
        }
         .object {
            border: 1px solid #ccc;
            padding: 10px;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
''' + f'''
<div class="container">
        <h2>New Purchase</h2>
<form action="/submitsale" method="POST">




        <!-- Date of Order -->
        <div class="form-group">
            <label for="order-date">Date of Order</label>
                <input type="date" id="date" name="date" required>
        </div>
        <div class="form-group">
            <label for="item">Item</label>
                <input type="text" id="item" name="item" required>
        </div>
        <div class="form-group">
            <label for="amount">Amount</label>
                <input type="number" id="amount" name="amount" required>
        </div>




        <!-- Submit Button -->
        <button type="submit">Submit</button>
    </form>
</div>

</body>
</html>

    '''


# Route to handle form submission
@app.route('/submitsale', methods=['POST'])
def submitsale():
    conn = sqlite3.connect(database, check_same_thread=False)
    cursor = conn.cursor()
    # Parse the form data

    cursor.execute("INSERT INTO Sales (date, item, amount) VALUES (?, ?, ?)",
                   (request.form["date"], request.form["item"], request.form["amount"]))
    conn.commit()

    conn.close()
    # Display or process the form data
    return '''
    <html>
    <body >
    <script>
    window.onload = function(){
    alert("Updated")
    window.location.href = "/"
    }
</script>

</body>
</html>
'''


@app.route('/quit')
def exitor():
    sys.exit()
    return "Exiting....."

@app.route('/upgrade')
def testHtml():
    try:
        subprocess.run([sys.executable, "updateMe.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error while running script: {e}")
    finally:
        # Exit the runner script
        sys.exit()
    return "Updating..."


@app.route('/testsubmit', methods=['POST'])
def submit():
    base64_string = request.form['imgdata']
    # print(base64_string)
    # Decode the Base64 string
    image_data = base64.b64decode(base64_string.split(",")[1])

    # Write the decoded data to a PNG file
    with open('bill.png', 'wb') as image_file:
        image_file.write(image_data)

    source_file = 'bill.png'  # Replace with your source file path
    destination_folder = 'static'  # Replace with your destination folder path

    # Create the destination folder if it doesn't exist
    os.makedirs(destination_folder, exist_ok=True)
    #
    # # Move the file to the subfolder
    shutil.move(source_file, os.path.join(destination_folder, os.path.basename(source_file)))
    msg = "http://192.168.1.8:5000/bill.png"
    return '''
    <html>
    <body >

''' + f'<a href="{msg}" download="bill.png">Download bill</a>' + '''

   <button id="shareBtn">Share Image</button>

    <script>
        document.getElementById("shareBtn").addEventListener("click", function() {
            if (typeof Android !== "undefined" && Android.shareImage) {
                Android.shareImage("http://192.168.1.8:5000/bill.png"); // Replace with actual image URL
            } else {
                console.error("Android interface not found!");
            }
        });
    </script>







</body>
</html>
'''


if __name__ == '__main__':
    # Start the Flask app
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)
