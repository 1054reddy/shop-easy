from flask import Flask, render_template, jsonify, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set this to a secure key in a real application

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="230001054",
    password="raja@1054",
    database="fashionwebsite"
)

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Products page route
@app.route('/products')
def products_page():
    category = request.args.get('category')
    cursor = db.cursor(dictionary=True)
    
    if category:
        # Query to get products based on the category
        cursor.execute("""
            SELECT p.* 
            FROM Products p
            JOIN Categories c ON p.category_id = c.category_id
            WHERE c.category_name = %s
        """, (category,))
    else:
        # Query to get all products
        cursor.execute("SELECT * FROM Products")

    products = cursor.fetchall()
    cursor.close()
    return render_template('products.html', products=products, selected_category=category)


# Product details route with dynamic product_id
@app.route('/product-details/<int:product_id>', methods=['GET'])
def product_details(product_id):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Products WHERE product_id = %s", (product_id,))
    product = cursor.fetchone()
    cursor.execute("SELECT size FROM Product_Sizes WHERE product_id = %s", (product_id,))
    sizes = cursor.fetchall()
    cursor.close()
    if product:
        return render_template('product-details.html', product=product, sizes=sizes)  # Pass sizes to template
    else:
        return "Product not found", 404

# API endpoint to fetch all products
@app.route('/get_products', methods=['GET'])
def get_products():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Products")
    products = cursor.fetchall()  # Consistent naming
    cursor.close()
    return jsonify(products)

# Route to add item to cart
@app.route('/add_to_cart_initial', methods=['POST'])
def add_to_cart_initial():
    product_id = request.form['product_id']
    size = request.form['size']
    quantity = request.form.get('quantity', 1)
    # Add logic to insert these details into the Cart_Items table
    # Assuming `user_id` is handled via session or a similar approach
    return jsonify({'status': 'success', 'message': 'Added to cart'})

# Helper function to get or create a cart for a user
def get_or_create_cart(user_id):
    cursor = db.cursor()
    cursor.execute("SELECT cart_id FROM Carts WHERE user_id = %s", (user_id,))
    cart = cursor.fetchone()
    
    if not cart:
        cursor.execute("INSERT INTO Carts (user_id) VALUES (%s)", (user_id,))
        db.commit()
        cart_id = cursor.lastrowid
    else:
        cart_id = cart[0]
    
    cursor.close()
    return cart_id

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    user_id = session.get('user_id')  # Assumes user_id is stored in session
    product_id = request.form.get('product_id')
    product_size_id = request.form.get('product_size_id')
    
    # Set a default value of 1 if 'quantity' is not provided or is None
    quantity = request.form.get('quantity')
    if quantity is None:
        quantity = 1
    else:
        quantity = int(quantity)  # Convert to integer

    if not user_id:
        return jsonify({"status": "failure", "message": "User not logged in"}), 401
    
    cart_id = get_or_create_cart(user_id)
    
    cursor = db.cursor()
    # Check if item already exists in cart
    cursor.execute("""
        SELECT quantity FROM Cart_Items 
        WHERE cart_id = %s AND product_id = %s AND product_size_id = %s
    """, (cart_id, product_id, product_size_id))
    existing_item = cursor.fetchone()

    if existing_item:
        # Update quantity if item exists
        new_quantity = existing_item[0] + quantity
        cursor.execute("""
            UPDATE Cart_Items SET quantity = %s
            WHERE cart_id = %s AND product_id = %s AND product_size_id = %s
        """, (new_quantity, cart_id, product_id, product_size_id))
    else:
        # Insert new item into cart
        cursor.execute("""
            INSERT INTO Cart_Items (cart_id, product_id, product_size_id, quantity, price)
            VALUES (%s, %s, %s, %s, 
                (SELECT price FROM Products WHERE product_id = %s))
        """, (cart_id, product_id, product_size_id, quantity, product_id))

    db.commit()
    cursor.close()
    return jsonify({"status": "success", "message": "Item added to cart"})


@app.route('/update_cart_item', methods=['POST'])
def update_cart_item():
    user_id = session.get('user_id')
    product_id = request.form.get('product_id')
    product_size_id = request.form.get('product_size_id')
    quantity = int(request.form.get('quantity'))

    if not user_id:
        return jsonify({"status": "failure", "message": "User not logged in"}), 401
    
    cart_id = get_or_create_cart(user_id)
    cursor = db.cursor()

    if quantity > 0:
        # Update quantity in cart
        cursor.execute("""
            UPDATE Cart_Items SET quantity = %s 
            WHERE cart_id = %s AND product_id = %s AND product_size_id = %s
        """, (quantity, cart_id, product_id, product_size_id))
    else:
        # Remove item from cart if quantity is zero
        cursor.execute("""
            DELETE FROM Cart_Items 
            WHERE cart_id = %s AND product_id = %s AND product_size_id = %s
        """, (cart_id, product_id, product_size_id))

    db.commit()
    cursor.close()
    return jsonify({"status": "success", "message": "Cart item updated"})

@app.route('/get_cart_items', methods=['GET'])
def get_cart_items():
    user_id = session.get('user_id')  # Assumes user_id is stored in session

    if not user_id:
        return jsonify({"status": "failure", "message": "User not logged in"}), 401

    cart_id = get_or_create_cart(user_id)  # Fetch or create the cart

    cursor = db.cursor()
    cursor.execute("""
        SELECT p.name, p.price, ci.quantity, ps.size 
        FROM Cart_Items ci
        JOIN Products p ON ci.product_id = p.product_id
        LEFT JOIN Product_Sizes ps ON ci.product_size_id = ps.product_size_id
        WHERE ci.cart_id = %s
    """, (cart_id,))

    cart_items = cursor.fetchall()
    cursor.close()

    # Convert the result into a list of dictionaries to return as JSON
    cart_items_data = [
        {
            'name': item[0],
            'price': item[1],
            'quantity': item[2],
            'size': item[3]
        }
        for item in cart_items
    ]

    return jsonify({"status": "success", "cart_items": cart_items_data})

@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    user_id = session.get('user_id')  # Assumes user_id is stored in session
    product_id = request.form.get('product_id')
    product_size_id = request.form.get('product_size_id')

    if not user_id:
        return jsonify({"status": "failure", "message": "User not logged in"}), 401

    cart_id = get_or_create_cart(user_id)  # Get or create the cart
    cursor = db.cursor()

    # Delete the item from Cart_Items table
    cursor.execute("""
        DELETE FROM Cart_Items 
        WHERE cart_id = %s AND product_id = %s AND product_size_id = %s
    """, (cart_id, product_id, product_size_id))

    db.commit()
    cursor.close()

    return jsonify({"status": "success", "message": "Item removed from cart"})



@app.route('/checkout', methods=['POST'])
def checkout():
    user_id = session.get('user_id')
    
    if not user_id:
        return redirect(url_for('login'))
    
    cart_id = get_or_create_cart(user_id)
    cursor = db.cursor()
    
    # Check if the cart has any items
    cursor.execute("SELECT COUNT(*) FROM Cart_Items WHERE cart_id = %s", (cart_id,))
    cart_item_count = cursor.fetchone()[0]
    
    if cart_item_count == 0:
        return jsonify({"status": "failure", "message": "Your cart is empty."}), 400

    # Step 0: Check if there is sufficient stock for each item in the cart
    cursor.execute("""
        SELECT ci.product_size_id, ci.quantity, ps.stock_quantity
        FROM Cart_Items ci
        JOIN Product_Sizes ps ON ci.product_size_id = ps.product_size_id
        WHERE ci.cart_id = %s AND ps.stock_quantity < ci.quantity
    """, (cart_id,))

    # If any results are returned, there is insufficient stock for one or more items
    insufficient_stock = cursor.fetchall()
    if insufficient_stock:
        return jsonify({
            "status": "failure",
            "message": "Insufficient stock for one or more items.",
            "details": [{"product_size_id": row[0], "requested": row[1], "available": row[2]} for row in insufficient_stock]
        }), 400
    
    try:
        # Start transaction
        db.autocommit = False

        # Step 1: Create new order
        cursor.execute("""
            INSERT INTO Orders (user_id, order_date, total_amount)
            SELECT %s, NOW(), SUM(ci.quantity * ci.price) 
            FROM Cart_Items ci WHERE ci.cart_id = %s
        """, (user_id, cart_id))
        order_id = cursor.lastrowid

        # Step 2: Copy cart items to order items
        cursor.execute("""
            INSERT INTO Order_Items (order_id, product_id, product_size_id, quantity, price)
            SELECT %s, ci.product_id, ci.product_size_id, ci.quantity, ci.price
            FROM Cart_Items ci WHERE ci.cart_id = %s
        """, (order_id, cart_id))

        # Step 3: Update stock for each product size
        cursor.execute("""
            UPDATE Product_Sizes ps
            JOIN Cart_Items ci ON ps.product_size_id = ci.product_size_id
            SET ps.stock_quantity = ps.stock_quantity - ci.quantity
            WHERE ci.cart_id = %s
        """, (cart_id,))
        
        # Step 4: Clear cart items after successful stock update
        cursor.execute("DELETE FROM Cart_Items WHERE cart_id = %s", (cart_id,))
        
        # Commit transaction
        db.commit()
        
        return jsonify({"status": "success", "message": "Checkout successful"})
    
    except mysql.connector.Error as err:
        # Rollback on error
        db.rollback()
        return jsonify({"status": "failure", "message": str(err)})
    
    finally:
        cursor.close()
        db.autocommit = True  # Reset autocommit to default


@app.route('/search', methods=['GET'])
def search_products():
    query = request.args.get('query', '').strip()
    page = int(request.args.get('page', 1))
    per_page = 10
    offset = (page - 1) * per_page

    if not query:
        return render_template('search_results.html', results=[], query=query, page=1, total_pages=1)

    cursor = db.cursor(dictionary=True)

    try:
        # Count total results
        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM Products
            WHERE MATCH(name, description) AGAINST(%s IN NATURAL LANGUAGE MODE)
        """, (query,))
        total_results = cursor.fetchone()['total']
        total_pages = (total_results + per_page - 1) // per_page

        # Fetch paginated and relevant results
        cursor.execute("""
            SELECT product_id, name, description, price,
                   MATCH(name, description) AGAINST(%s IN NATURAL LANGUAGE MODE) AS relevance
            FROM Products
            WHERE MATCH(name, description) AGAINST(%s IN NATURAL LANGUAGE MODE)
            HAVING relevance > 0.5
            LIMIT %s OFFSET %s
        """, (query, query, per_page, offset))
        results = cursor.fetchall()

        return render_template('search_results.html', results=results, query=query, page=page, total_pages=total_pages)
    finally:
        cursor.close()

@app.route('/search-suggestions', methods=['GET'])
def search_suggestions():
    term = request.args.get('term', '').strip()

    if not term:
        return jsonify([])

    cursor = db.cursor()

    try:
        # Use a LIKE query for partial matches
        cursor.execute("""
            SELECT DISTINCT name
            FROM Products
            WHERE name LIKE %s
            LIMIT 10
        """, (f"%{term}%",))
        suggestions = [row[0] for row in cursor.fetchall()]  # Extract names from results
        return jsonify(suggestions)
    finally:
        cursor.close()



# Categories page route
@app.route('/categories', methods=['GET'])
def categories_page():
    return render_template('categories.html')

# Cart page route
@app.route('/cart', methods=['GET'])
def cart_page():
    return render_template('cart.html')

# Profile page route
@app.route('/profile')
def profile_page():
    user_id = session.get('user_id')
    
    if not user_id:
        return redirect(url_for('login'))  # Redirect if not logged in

    # Fetch user details from the database
    cursor = db.cursor()
    cursor.execute("SELECT name, email, mobile_no FROM Users WHERE user_id = %s", (user_id,))
    user_info = cursor.fetchone()
    cursor.close()

    if user_info:
        user_data = {
            'name': user_info[0],
            'email': user_info[1],
            'mobile_no': user_info[2]
        }
    else:
        user_data = {}

    return render_template('profile.html', user=user_data)


@app.route('/order-history', methods=['GET'])
def order_history_page():
    user_id = session.get('user_id')  # Assuming the user is logged in and session stores user_id

    if not user_id:
        return jsonify({"status": "failure", "message": "User not logged in"}), 401
    
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT order_id, order_date, total_amount 
        FROM Orders 
        WHERE user_id = %s 
        ORDER BY order_date DESC
    """, (user_id,))
    orders = cursor.fetchall()
    cursor.close()
    
    return render_template('order_history.html', orders=orders)

@app.route('/api/order-history', methods=['GET'])
def get_order_history():
    user_id = session.get('user_id')

    if not user_id:
        return jsonify({"status": "failure", "message": "User not logged in"}), 401

    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT order_id, order_date, total_amount 
        FROM Orders 
        WHERE user_id = %s 
        ORDER BY order_date DESC
    """, (user_id,))
    orders = cursor.fetchall()
    cursor.close()

    return jsonify(orders)



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        print("Form submission detected")
        name = request.form['name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        address = request.form['address']
        mobile_no = request.form['mobile_no']
        gender = request.form['gender']
        age = request.form['age']

        print("Form data collected:", name, email, address, mobile_no, gender, age)

        cursor = db.cursor()
        try:
            cursor.execute("""INSERT INTO Users (name, email, password, address, mobile_no, gender, age)
                              VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                           (name, email, password, address, mobile_no, gender, age))
            db.commit()
            print("Data inserted successfully")
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except mysql.connector.Error as err:
            db.rollback()
            print("Database error:", err)  # Logs the error
            flash(f'Error: {err}', 'danger')
        finally:
            cursor.close()

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor = db.cursor()
        cursor.execute("SELECT user_id, name, password FROM Users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()

        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            session['username'] = user[1]
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password. Please try again.', 'danger')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))
if __name__ == '__main__':
    app.run(debug=True)
