import sqlite3
from flask import Flask, render_template

app = Flask(__name__)
DATABASE = r"C:\Users\18217\OneDrive - Wellington College\13DTS\Smile\smile.db"


def create_connection(db_file):
    """
    Create a connection with the database
    parameter: name of the database file
    returns: a connection to the file
    """
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except sqlite3.Error as e:
        print(e)
        return None


@app.route('/')
def render_homepage():
    return render_template('home.html')


@app.route('/menu')
def render_menu_page():
    con = create_connection(DATABASE)

    query = "SELECT name, description, volume, price, image FROM product"
    cur = con.cursor()  # creates a courser to write the query
    cur.execute(query)
    product_list = cur.fetchall()
    con.close()
    return render_template('menu.html', products=product_list)


@app.route('/contact')
def render_contact_page():
    return render_template('contact.html')


@app.route('/login', methods=["GET", "POST"])
def render_login_page():
    return render_template('login.html')


@app.route('/signup', methods=["GET", "POST"])
def render_signup_page():
    return render_template('signup.html')


app.run(host='0.0.0.0', debug=True)
