from flask import Flask, render_template, request

app = Flask(__name__)

# Список товарів
products = [
    {'id': 1, 'name': 'Піца Маргарита', 'price': 200, 'image': 'product1.jpg'},
    {'id': 2, 'name': 'Бургер з куркою', 'price': 150, 'image': 'product2.jpg'},
    {'id': 3, 'name': 'Суші Роли', 'price': 250, 'image': 'product3.jfif'},
    {'id': 4, 'name': 'Салат Цезар', 'price': 120, 'image': 'product4.jpg'},
    {'id': 5, 'name': 'Лимонад', 'price': 50, 'image': 'product5.jpg'}
]

# Список замовлень
orders = []

@app.route("/", methods=["GET", "POST"])
def index():
    receipt = None
    thank_you_message = None
    if request.method == "POST":
        product_id = int(request.form['product_id'])
        quantity = int(request.form['quantity'])
        customer_type = request.form['customer_type']

        # Знайдемо товар за ID
        product = next((p for p in products if p['id'] == product_id), None)

        if product:
            total_price = product['price'] * quantity
            discount = 0
            if customer_type == 'wholesale':
                discount = total_price * 0.20  # 20% знижка для оптовиків
            total_price -= discount

            receipt = {
                'product_name': product['name'],
                'quantity': quantity,
                'customer_type': customer_type,
                'discount': discount,
                'total_price': total_price
            }

            # Якщо кнопка "Замовити" натиснута, збережемо замовлення
            if 'order' in request.form:
                orders.append(receipt)
                thank_you_message = "Дякуємо за покупку!"

    return render_template("index.html", products=products, receipt=receipt, thank_you_message=thank_you_message)

@app.route("/orders")
def orders_page():
    return render_template("orders.html", orders=orders)

@app.route("/catalog")
def catalog():
    return render_template("catalog.html", products=products)

@app.route("/contacts")
def contacts():
    return render_template("contacts.html")

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)
