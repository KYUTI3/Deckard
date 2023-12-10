# Import all important libraries
from flask import *
from flask_session import Session
import sqlite3


# generate event attendance table
def generate_event_table(cursor, eventName, eventCode):
    # create table of attendance for this event
    table = """ CREATE TABLE IF NOT EXISTS %s(
                User CHAR(25) NOT NULL
            );
             """ % eventName
    cursor.execute(table)
    cursor.execute('SELECT * FROM Events WHERE Name ="%s"' % eventName)
    event = cursor.fetchone()

    # add event to table of events
    if event is None:
        cursor.execute("INSERT INTO Events VALUES ('%s', '%s')" % (eventName, eventCode))

# initialize flask
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# initialize database tables if not already created
connection = sqlite3.connect('data.db')
cursor_obj = connection.cursor()
#cursor_obj.execute("DROP TABLE IF EXISTS attend")

table = """ CREATE TABLE IF NOT EXISTS Users(
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

# example event
generate_event_table(cursor_obj, "Hackathon", 1234)

connection.commit()
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
        cursor.execute('SELECT * FROM Users WHERE Email ="%s" AND Password = "%s"' % (email, password))
        user = cursor.fetchone()
        connection.close()

        # if email and password are correct
        if user:
            session["name"] = user[0]
            session["email"] = email
            session["password"] = password
            session["score"] = user[3]
            # todo redirect to attend (done)
            return render_template('user.html', message=message, score=session["score"])
        else:
            message = 'Please enter correct email / password !'
    return render_template('login.html', message=message)


# Make function attendance
@app.route('/attend', methods=['GET', 'POST'])
def attend():
    message = ''
    # make sure user is logged in
    if session["name"] is None:
        return redirect(url_for('login'))
    else:
        # check that form data is available
        if request.method == 'POST' and 'Name' in request.form and 'Code' in request.form:
            eventName = request.form['Name']
            eventCode = request.form['Code']

            # verify event name and code
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM Events WHERE Name ="%s" AND Code = "%s"' % (eventName, eventCode))
            event = cursor.fetchone()
            # check if event name and code are valid
            if event:
                # check if person is already registered in the event
                cursor.execute('SELECT * FROM %s WHERE User ="%s"' % (eventName, session['name']))
                person = cursor.fetchone()
                print(person)
                if person is None:
                    # add person into event attendance and update their score
                    cursor.execute("INSERT INTO %s VALUES ('%s')" % (eventName, session["name"]))
                    cursor.execute('''UPDATE Users SET Score = %s WHERE User = "%s";''' % (session["score"]+1, session["name"]))
                    connection.commit()
                    session["score"] = session["score"] + 1
                    connection.close()
                    message = "success"
                    return render_template('user.html', message=message, score=session["score"])
                else:
                    message = 'You have already attended this event'
                    return render_template('user.html', message = message, score=session["score"])
            else:
                connection.close()
                message = "Event name or password incorrect"
                return render_template('attend.html', message=message)
        return render_template('attend.html', message=message)


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

        cursor.execute('SELECT * FROM Users WHERE Email ="%s"' % (email))
        user = cursor.fetchone()

        # if user has account redirect to login
        if user:
            message = 'you already have an account, please login'
            render_template('login.html', message=message)

        # add user account
        else:
            cursor.execute("INSERT INTO Users VALUES ('%s', '%s', '%s', 0)" % (userName, email, password))
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
