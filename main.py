# Import all important libraries
from flask import *
from flask_session import Session
import sqlite3


# generate event attendance table
def generate_event_table(cursor, EventName):
    table = """ CREATE TABLE IF NOT EXISTS %s(
                User CHAR(25) NOT NULL,
            );
             """ % EventName
    cursor.execute(table)

# initialize flask
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# initialize database tables if not already created
connection = sqlite3.connect('data.db')
cursor_obj = connection.cursor()
#cursor_obj.execute("DROP TABLE IF EXISTS attend")

table = """ CREATE TABLE IF NOT EXISTS users(
            User CHAR(25) NOT NULL,
            Email VARCHAR(255) NOT NULL,
            Password CHAR(25) NOT NULL,
            Score INT
        );
         """
cursor_obj.execute(table)

table = """ CREATE TABLE IF NOT EXISTS Events(
            Name CHAR(25) NOT NULL,
            Code VARCHAR(255) NOT NULL
        );
         """
cursor_obj.execute(table)

connection.commit()

# example event
generate_event_table(cursor_obj, "hackathon")
connection.close()


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM users WHERE Email ="%s" AND Password = "%s"' % (email, password))
        user = cursor.fetchone()
        connection.close()

        # if email and password are correct
        if user:
            session["name"] = user[0]
            session["email"] = email
            session["password"] = password
            # todo redirect to attend
            return render_template('user.html', message=message)
        else:
            message = 'Please enter correct email / password !'
    return render_template('login.html', message=message)


# Make function attendance
@app.route('/attend')
def attend():
    session["name"] = None
    session["email"] = None
    session["password"] = None
    return redirect(url_for('login'))


# Make function for logout session
@app.route('/logout')
def logout():
    session["name"] = None
    session["email"] = None
    session["password"] = None
    return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form:
        userName = request.form['name']
        password = request.form['password']
        email = request.form['email']
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        cursor.execute('SELECT * FROM users WHERE Email ="%s"' % (email))
        user = cursor.fetchone()

        # if user has account redirect to login
        if user:
            message = 'you already have an account, please login'
            return redirect(url_for('login'))

        # add user account
        else:
            cursor.execute("INSERT INTO users VALUES ('%s', '%s', '%s', 0)" % (userName, email, password))
            message = "done registering, please login"
        connection.commit()
        connection.close()
        return render_template('login.html', message=message)
    elif request.method == 'POST':
        message = 'Please fill out the form !'
    return render_template('register.html', message=message)

# run code in debug mode
if __name__ == "__main__":
    app.run(debug=True)