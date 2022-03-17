import sqlite3
from flask import Flask, render_template, request, redirect, session
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = 'alkjaslkgjwleakhg lkwhlhwlklkhw'
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


def is_logged_in():
    """
    A function to return whether the user is logged in or not
    """
    if session.get("email") is None:
        print("Not logged in")
        return False
    else:
        return True


@app.route('/')
def render_homepage():
    return render_template('home.html', logged_in=is_logged_in())


@app.route('/menu')
def render_menu_page():
    con = create_connection(DATABASE)

    query = "SELECT name, description, volume, price, image FROM product"
    cur = con.cursor()  # creates a courser to write the query
    cur.execute(query)
    product_list = cur.fetchall()
    con.close()
    return render_template('menu.html', products=product_list, logged_in=is_logged_in())


@app.route('/contact')
def render_contact_page():
    return render_template('contact.html', logged_in=is_logged_in())


@app.route('/login', methods=["GET", "POST"])
def render_login_page():
    if is_logged_in():
        return redirect('/')
    print(request.form)
    if request.method == "POST":
        email = request.form.get('email').lower().strip()
        password = request.form.get('password')

        con = create_connection(DATABASE)
        query = "SELECT id, fname, password FROM customer WHERE email=?"
        cur = con.cursor()
        cur.execute(query, (email,))
        user_data = cur.fetchall()
        con.close()

        try:
            user_id = user_data[0][0]
            first_name = user_data[0][1]
            db_password = user_data[0][2]
            # set up a session for this login
        except IndexError:
            return redirect("/login?error=Invalid+email+or+password")
        if not bcrypt.check_password_hash(db_password, password):
            return redirect("/login?error=Invalid+email+or+password")

        session["email"] = email
        session["user_id"] = user_id
        session["fname"] = first_name
        session["cart"] = []
        return redirect('/menu')

    error = request.args.get('error')
    return render_template('login.html', logged_in=is_logged_in(), error=error)


@app.route('/logout')
def render_logout_page():
    print(list(session.keys()))
    [session.pop(key) for key in list(session.keys())]
    print(list(session.keys()))
    return redirect('/')


@app.route('/signup', methods=["GET", "POST"])
def render_signup_page():
    if is_logged_in():
        return redirect('/')
    if request.method == "POST":
        print(request.form)
        fname = request.form.get('fname').title().strip()
        lname = request.form.get('lname').title().strip()
        email = request.form.get('email').lower().strip()
        password = request.form.get('password')
        password2 = request.form.get('password2')

        if len(password) < 8:
            return redirect('signup?error=Password+must+be+at+least+8+Characters')

        if password != password2:
            return redirect('signup?error=Passwords+do+not+match')

        hashed_password = bcrypt.generate_password_hash(password)
        con = create_connection(DATABASE)

        query = "INSERT INTO customer (fname, lname, email, password) VAlUES (?, ?, ?, ?)"

        cur = con.cursor()
        cur.execute(query, (fname, lname, email, hashed_password))
        con.commit()
        con.close()
        return redirect('/login')

    error = request.args.get('error')
    if error is None:
        error = ''
    return render_template('signup.html', error=error)


app.run(host='0.0.0.0', debug=True)