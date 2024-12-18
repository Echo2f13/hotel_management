from db import init_db
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

#staff cred
STAFF_EMAIL = "staff@gmail.com"
STAFF_PASSWORD = "Staff@123"
cart_data = [
    {'dish_name': 'Chicken Biryani', 'price': 200, 'quantity': 2},
    {'dish_name': 'Samosa', 'price': 50, 'quantity': 4}
]
staff_data = []
# Updated menu data with Cool Drinks (Thums Up, Maaza, Pepsi)
menu_data = {
    'Biryani': [
        {'id': '1', 'name': 'Chicken Biryani', 'price': '₹250'},
        {'id': '2', 'name': 'Mutton Biryani', 'price': '₹400'},
        {'id': '3', 'name': 'Egg Biryani', 'price': '₹180'},
        {'id': '4', 'name': 'Tandoori Chicken Biryani', 'price': '₹300'},
        {'id': '5', 'name': 'Prawn Biryani', 'price': '₹250'}
    ],
    'Starters': [
        {'id': '6', 'name': 'Paneer Tikka', 'price': '₹150'},
        {'id': '7', 'name': 'Veg Pakora', 'price': '₹120'}
    ],
    'Curries': [
        {'id': '8', 'name': 'Butter Chicken', 'price': '₹350'},
        {'id': '9', 'name': 'Dal Makhani', 'price': '₹180'}
    ],
    'Desserts': [
        {'id': '10', 'name': 'Gulab Jamun', 'price': '₹100'},
        {'id': '11', 'name': 'Ras Malai', 'price': '₹120'},
        {'id': '12', 'name': 'Thums Up', 'price': '₹60'},
        {'id': '13', 'name': 'Maaza', 'price': '₹60'},
        {'id': '14', 'name': 'Pepsi', 'price': '₹60'}
    ]
}
@app.route("/staff-login", methods=["GET", "POST"])
def staff_login():
    error_message = ""
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        # Validate credentials
        if email == STAFF_EMAIL and password == STAFF_PASSWORD:
            return redirect(url_for('staff_dashboard'))
        else:
            error_message = "Incorrect credentials!"

    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Staff Login</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
                text-align: center;
            }}
            header {{
                background-color: #4CAF50;
                color: white;
                padding: 20px 0;
            }}
            header img {{
                vertical-align: middle;
                width: 50px;
                margin-right: 10px;
            }}
            header span {{
                font-size: 24px;
                font-weight: bold;
            }}
            .login-container {{
                margin-top: 100px;
                background-color: white;
                border-radius: 10px;
                padding: 30px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                width: 300px;
                margin-left: auto;
                margin-right: auto;
            }}
            .login-container input {{
                width: 100%;
                padding: 10px;
                margin: 10px 0;
                border: 1px solid #ccc;
                border-radius: 5px;
                font-size: 16px;
            }}
            .login-container button {{
                width: 100%;
                padding: 15px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 18px;
                cursor: pointer;
            }}
            .login-container button:hover {{
                background-color: #45a049;
            }}
            .error-message {{
                color: red;
                font-size: 14px;
                margin-top: 10px;
            }}
        </style>
    </head>
    <body>
        <header>
            <img src="/static/logo.jpg" alt="Hotel Logo">
            <span>Hotel Name</span>
        </header>
        <div class="login-container">
            <h2>Staff Login</h2>
            <form method="post">
                <input type="text" name="email" placeholder="Enter Email" required><br>
                <input type="password" name="password" placeholder="Enter Password" required><br>
                <button type="submit">Login</button>
            </form>
            <p class="error-message">{error_message}</p>
        </div>
    </body>
    </html>
    '''
@app.route("/staff-dashboard", methods=["GET", "POST"])
def staff_dashboard():
    global staff_data  

    if request.method == "POST":
        action = request.form['action']

        if action == 'Add Dish':
            category = request.form['category'].capitalize()
            dish_id = request.form['id']
            dish_name = request.form['name']
            dish_price = request.form['price']

            if category in menu_data:
                menu_data[category].append({'id': dish_id, 'name': dish_name, 'price': dish_price})
            else:
                menu_data[category] = [{'id': dish_id, 'name': dish_name, 'price': dish_price}]

        elif action == 'Delete Dish':
            category = request.form['category']
            dish_id = request.form['id']
            menu_data[category] = [dish for dish in menu_data[category] if dish['id'] != dish_id]

        elif action == 'Edit Dish':
            category = request.form['category']
            dish_id = request.form['id']
            new_name = request.form['new_name']
            new_price = request.form['new_price']
            for dish in menu_data[category]:
                if dish['id'] == dish_id:
                    dish['name'] = new_name
                    dish['price'] = new_price

        elif action == 'Add Staff':
            staff_id = request.form['staff_id']
            staff_name = request.form['staff_name']
            staff_role = request.form['staff_role']
            staff_age = request.form['staff_age']

            staff_data.append({
                'id': staff_id,
                'name': staff_name,
                'role': staff_role,
                'age': staff_age
            })

        elif action == 'Delete Staff':
            staff_id = request.form['staff_id']
            staff_data = [staff for staff in staff_data if staff['id'] != staff_id]

        return redirect('/staff-dashboard')

    menu_html = ""
    for category, dishes in menu_data.items():
        menu_html += f"<h3>{category}</h3>"
        menu_html += """
        <table border="1" style="width:100%; margin: 10px 0;">
            <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Price</th>
                <th>Actions</th>
            </tr>
        """
        for dish in dishes:
            menu_html += f"""
            <tr>
                <td>{dish['id']}</td>
                <td>{dish['name']}</td>
                <td>{dish['price']}</td>
                <td>
                    <form action="/staff-dashboard" method="POST" style="display:inline;">
                        <input type="hidden" name="category" value="{category}">
                        <input type="hidden" name="id" value="{dish['id']}">
                        <input type="submit" name="action" value="Delete Dish">
                    </form>
                    <form action="/staff-dashboard" method="POST" style="display:inline;">
                        <input type="hidden" name="category" value="{category}">
                        <input type="hidden" name="id" value="{dish['id']}">
                        <input type="text" name="new_name" placeholder="New Name" required>
                        <input type="text" name="new_price" placeholder="New Price" required>
                        <input type="submit" name="action" value="Edit Dish">
                    </form>
                </td>
            </tr>
            """
        menu_html += "</table>"


    staff_html = """
    <h3>Staff Members</h3>
    <table border="1" style="width:100%; margin: 10px 0;">
        <tr>
            <th>Staff ID</th>
            <th>Name</th>
            <th>Role</th>
            <th>Age</th>
            <th>Actions</th>
        </tr>
    """
    for staff in staff_data:
        staff_html += f"""
        <tr>
            <td>{staff['id']}</td>
            <td>{staff['name']}</td>
            <td>{staff['role']}</td>
            <td>{staff['age']}</td>
            <td>
                <form action="/staff-dashboard" method="POST" style="display:inline;">
                    <input type="hidden" name="staff_id" value="{staff['id']}">
                    <input type="submit" name="action" value="Delete Staff">
                </form>
            </td>
        </tr>
        """
    staff_html += "</table>"

    staff_html += """
    <h3>Add a New Staff Member</h3>
    <form action="/staff-dashboard" method="POST">
        <label for="staff_id">Staff ID:</label><br>
        <input type="text" id="staff_id" name="staff_id" required><br>
        <label for="staff_name">Name:</label><br>
        <input type="text" id="staff_name" name="staff_name" required><br>
        <label for="staff_role">Role:</label><br>
        <input type="text" id="staff_role" name="staff_role" required><br>
        <label for="staff_age">Age:</label><br>
        <input type="text" id="staff_age" name="staff_age" required><br>
        <input type="submit" name="action" value="Add Staff">
    </form>
    """

    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Staff Dashboard</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
            }}
            header {{
                background-color: #4CAF50;
                color: white;
                padding: 20px 0;
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 10px 50px;
            }}
            header img {{
                vertical-align: middle;
                width: 50px;
                margin-right: 10px;
            }}
            header span {{
                font-size: 24px;
                font-weight: bold;
            }}
            .buttons-container {{
                display: flex;
                justify-content: flex-end;
                padding: 20px;
            }}
            .buttons-container button {{
                padding: 10px 20px;
                font-size: 16px;
                margin-left: 15px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }}
            .buttons-container button:hover {{
                background-color: #45a049;
            }}
            .section {{
                display: none;
                background-color: white;
                padding: 20px;
                margin: 20px auto;
                width: 50%;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                border-radius: 10px;
            }}
            .section.active {{
                display: block;
            }}
        </style>
        <script>
            function showSection(sectionId) {{
                // Hide all sections
                document.querySelectorAll('.section').forEach(section => {{
                    section.style.display = 'none';
                }});
                // Show the selected section
                document.getElementById(sectionId).style.display = 'block';
            }}
        </script>
    </head>
    <body>
        <header>
            <div>
                <img src="/static/logo.jpg" alt="Hotel Logo">
                <span>Hotel Name</span>
            </div>
        </header>
        <div class="buttons-container">
            <button onclick="showSection('profile-section')">Profile</button>
            <button onclick="showSection('update-menu-form')">Update Menu</button>
            <button onclick="showSection('staff-section')">Staff Members</button>
            <button>Order Detail</button>
            <button onclick="window.location.href='/'">Logout</button>
        </div>

        <!-- Profile Section -->
        <div id="profile-section" class="section">
            <h3>Staff Profile</h3>
            <p><strong>ID:</strong> 224298</p>
            <p><strong>Name:</strong> Koushik</p>
            <p><strong>Date of Birth:</strong> 12-12-1999</p>
            <p><strong>Mobile Number:</strong> 1234567890</p>
        </div>

        <!-- Menu Update Section -->
        <div id="update-menu-form" class="section">
            <h3>Update Menu</h3>
            {menu_html}
            <h3>Add a New Dish</h3>
            <form action="/staff-dashboard" method="POST">
                <label for="category">Category:</label><br>
                <input type="text" id="category" name="category" required><br>
                <label for="id">Dish ID:</label><br>
                <input type="text" id="id" name="id" required><br>
                <label for="name">Dish Name:</label><br>
                <input type="text" id="name" name="name" required><br>
                <label for="price">Price:</label><br>
                <input type="text" id="price" name="price" required><br>
                <input type="submit" name="action" value="Add Dish">
            </form>
        </div>

        <!-- Staff Section -->
        <div id="staff-section" class="section">
            {staff_html}
        </div>
    </body>
    </html>
    '''



@app.route("/")
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Hotel Management System</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
            }
            header {
                background-color: #4CAF50;
                color: white;
                padding: 20px 0;
                font-size: 24px;
            }
            .container {
                display: flex;
                justify-content: space-around;
                align-items: center;
                margin: 50px auto;
                width: 80%;
            }
            .hotel-image {
                width: 40%;
            }
            .buttons {
                display: flex;
                flex-direction: column;
                gap: 20px;
            }
            .button {
                padding: 15px 30px;
                font-size: 16px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            .button:hover {
                background-color: #45a049;
            }
        </style>
    </head>
    <body>
        <header>
            <img src="/static/logo.jpg" alt="Hotel Logo" style="vertical-align: middle; width: 50px;">
            <span>Hotel Name</span>
        </header>
        <div class="container">
            <img src="/static/logo.jpg" alt="Hotel Picture" class="hotel-image">
            <div class="buttons">
                <button class="button" onclick="window.location.href='/staff-login'">Staff Login</button>
                <button class="button" onclick="window.location.href='/customer-login'">Customer Login</button>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route("/customer-login")
def customer_login():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Customer Dashboard</title>
    </head>
    <body>
        <h1 style="text-align:center;">Hotel Name</h1>
        <div style="text-align:center;">
            <img src="/static/logo.jpg" alt="Hotel Logo" style="width: 10%; margin-top: 20px;">
        </div>
        <div style="text-align:center; margin-top: 20px;">
            <h2>Customer Dashboard</h2>
        </div>
        <div style="display: flex; flex-direction: column; align-items: center; margin-top: 50px;">
            <button style="margin: 10px; padding: 10px 20px; background-color: #63a4ff; border: none; color: white;" onclick="window.location.href='/menu'">Show Menu</button>
            <button style="margin: 10px; padding: 10px 20px; background-color: #45b39d; border: none; color: white;">Review Items</button>
            <button style="margin: 10px; padding: 10px 20px; background-color: #28a745; border: none; color: white;" onclick="window.location.href='/'">Exit</button>
        </div>
    </body>
    </html>
    '''

@app.route("/menu")
def show_menu():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Menu</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
            }
            header {
                background-color: #4CAF50;
                color: white;
                padding: 20px 0;
                font-size: 24px;
            }
            .menu-container {
                display: flex;
                justify-content: space-between;
                margin: 30px;
            }
            .categories {
                width: 20%;
                text-align: left;
                padding-right: 20px;
            }
            .categories button {
                margin: 10px 0;
                padding: 15px 30px;
                font-size: 16px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                width: 100%;
            }
            .categories button:hover {
                background-color: #45a049;
            }
            .dish-grid {
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                gap: 20px;
                width: 75%;
            }
            .dish-card {
                width: 200px;
                padding: 10px;
                background-color: white;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
                border-radius: 10px;
                text-align: center;
            }
            .dish-card img {
                width: 100%;
                height: auto;
                border-radius: 5px;
            }
            .dish-card h3 {
                margin-top: 10px;
                font-size: 18px;
            }
            .dish-card p {
                margin-top: 5px;
                font-size: 16px;
            }
        </style>
    </head>
    <body>
        <header>
            <img src="/static/logo.jpg" alt="Hotel Logo" style="vertical-align: middle; width: 50px;">
            <span>Hotel Name</span>
        </header>
        <h2>Select a Category</h2>
        <div class="menu-container">
            <!-- Left-side categories -->
            <div class="categories">
                <button onclick="window.location.href='/category/biryani'">Biryani</button>
                <button onclick="window.location.href='/category/starters'">Starters</button>
                <button onclick="window.location.href='/category/curries'">Curries</button>
                <button onclick="window.location.href='/category/desserts'">Desserts</button>
            </div>
            
            <!-- Right-side dishes -->
            <div class="dish-grid">
                <!-- Dishes will be dynamically inserted here -->
            </div>
        </div>
    </body>
    </html>
    '''
@app.route("/category/<category_name>")
def category_page(category_name):
    category_data = menu_data.get(category_name.capitalize(), [])
    
    if not category_data:
        return f"<h2>No dishes found for category: {category_name}</h2>"
    
    dishes_html = ""
    for dish in category_data:
        dishes_html += f'''
        <div class="dish-card">
            <img src="/static/{dish['id']}.jpg" alt="{dish['name']}">
            <h3>{dish['name']}</h3>
            <p>{dish['price']} <br> ID: {dish['id']}</p>
            <button onclick="alert('Added {dish['name']} to cart')">Add</button>
        </div>
        '''
    
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>{category_name.capitalize()} - Menu</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                text-align: center;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
            }}
            header {{
                background-color: #4CAF50;
                color: white;
                padding: 20px 0;
                font-size: 24px;
                position: relative;
            }}
            .cart-button {{
                position: absolute;
                right: 20px;
                top: 20px;
                background-color: #FF5733;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 16px;
                cursor: pointer;
            }}
            .cart-button:hover {{
                background-color: #FF4500;
            }}
            .menu-container {{
                display: flex;
                justify-content: space-between;
                margin: 30px;
            }}
            .categories {{
                width: 20%;
                text-align: left;
                padding-right: 20px;
            }}
            .categories button {{
                margin: 10px 0;
                padding: 15px 30px;
                font-size: 16px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                width: 100%;
            }}
            .categories button:hover {{
                background-color: #45a049;
            }}
            .dish-grid {{
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                gap: 20px;
                width: 75%;
            }}
            .dish-card {{
                width: 200px;
                padding: 10px;
                background-color: white;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
                border-radius: 10px;
                text-align: center;
            }}
            .dish-card img {{
                width: 100%;
                height: auto;
                border-radius: 5px;
            }}
            .dish-card h3 {{
                margin-top: 10px;
                font-size: 18px;
            }}
            .dish-card p {{
                margin-top: 5px;
                font-size: 16px;
            }}
        </style>
    </head>
    <body>
        <header>
            <img src="/static/logo.jpg" alt="Hotel Logo" style="vertical-align: middle; width: 50px;">
            <span>Hotel Name</span>
            <button class="cart-button" onclick="window.location.href='/cart'">Cart</button>
        </header>
        <h2>{category_name.capitalize()}</h2>
        <div class="menu-container">
            <div class="categories">
                <button onclick="window.location.href='/category/biryani'">Biryani</button>
                <button onclick="window.location.href='/category/starters'">Starters</button>
                <button onclick="window.location.href='/category/curries'">Curries</button>
                <button onclick="window.location.href='/category/desserts'">Desserts</button>
            </div>
            <div class="dish-grid">
                {dishes_html}
            </div>
        </div>
    </body>
    </html>
    '''

@app.route("/cart")
def cart_page():
    total_price = 0
    cart_html = ""
    for index, item in enumerate(cart_data, start=1):
        total_price += item['price'] * item['quantity']
        cart_html += f'''
        <tr>
            <td>{index}</td>
            <td>{item['dish_name']}</td>
            <td>{item['price']}</td>
            <td>{item['quantity']}</td>
            <td>{item['price'] * item['quantity']}</td>
        </tr>
        '''
    
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Cart - Hotel</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                text-align: center;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
            }}
            header {{
                background-color: #4CAF50;
                color: white;
                padding: 20px 0;
                font-size: 24px;
                position: relative;
            }}
            .menu-container {{
                display: flex;
                justify-content: space-between;
                margin: 30px;
            }}
            .cart-table {{
                width: 80%;
                margin: 20px auto;
                border-collapse: collapse;
                text-align: left;
            }}
            .cart-table th, .cart-table td {{
                border: 1px solid #ddd;
                padding: 10px;
            }}
            .cart-table th {{
                background-color: #4CAF50;
                color: white;
            }}
            .total-price {{
                margin-top: 20px;
                font-size: 20px;
                font-weight: bold;
            }}
            .order-button {{
                margin-top: 30px;
                padding: 10px 20px;
                font-size: 18px;
                background-color: #FF5733;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }}
            .order-button:hover {{
                background-color: #FF4500;
            }}
        </style>
        <script>
            function placeOrder() {{
                const tableNumber = prompt('Please enter your table number:');
                if (tableNumber) {{
                    alert('Order placed successfully for Table ' + tableNumber);
                }}
            }}
        </script>
    </head>
    <body>
        <header>
            <img src="/static/logo.jpg" alt="Hotel Logo" style="vertical-align: middle; width: 50px;">
            <span>Hotel Name</span>
        </header>
        <h2>Cart</h2>
        <table class="cart-table">
            <thead>
                <tr>
                    <th>S.No</th>
                    <th>Dish Name</th>
                    <th>Price</th>
                    <th>Quantity</th>
                    <th>Total Price</th>
                </tr>
            </thead>
            <tbody>
                {cart_html}
            </tbody>
        </table>
        <div class="total-price">
            Total Price: {total_price}
        </div>
        <button class="order-button" onclick="placeOrder()">Order Now</button>
    </body>
    </html>
    '''

init_db()
if __name__ == "__main__":
    app.run(debug=True)