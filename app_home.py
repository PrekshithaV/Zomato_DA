from flask import Flask, request, jsonify, render_template
import mysql.connector

app = Flask(__name__)

def create_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='zomato'
    )

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/place_order', methods=['POST'])
def place_order():
    connection = None
    cursor = None
    try:
        biriyani_quantity = request.form.get('biriyani_quantity', 0)
        paneer_quantity = request.form.get('paneer_quantity', 0)
        butter_chicken_quantity = request.form.get('butter_chicken_quantity', 0)
        address = request.form.get('address')

        cart = []
        if int(biriyani_quantity) > 0:
            cart.append(('Biriyani', int(biriyani_quantity)))
        if int(paneer_quantity) > 0:
            cart.append(('Paneer', int(paneer_quantity)))
        if int(butter_chicken_quantity) > 0:
            cart.append(('Butter Chicken', int(butter_chicken_quantity)))

        if not cart or not address:
            return jsonify({"error": "Cart is empty or address is missing."}), 400

        connection = create_connection()
        cursor = connection.cursor()

        for item_name, quantity in cart:
            cursor.execute("SELECT item_id FROM items WHERE item_name = %s", (item_name,))
            result = cursor.fetchone()

            if not result:
                return jsonify({"error": f"Item {item_name} not found."}), 400

            item_id = result[0]
            user_id = 1

            sql = """
                INSERT INTO orders (user_id, item_id, quantity, delivery_address)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (user_id, item_id, quantity, address))

        connection.commit()
        return jsonify({"message": "Order placed successfully!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

if __name__ == '__main__':
    app.run(debug=True)