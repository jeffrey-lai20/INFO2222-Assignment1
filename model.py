'''
    Our Model class
    This should control the actual "logic" of your website
    And nicely abstracts away the program logic from your page loading
    It should exist as a separate layer to any database or data structure that you might be using
    Nothing here should be stateful, if it's stateful let the database handle it
'''
import view
import random
from bottle import template, redirect, static_file, request
import bottle
from beaker.middleware import SessionMiddleware
from cork import Cork
from datetime import datetime, timedelta
import logging
import json
from html import escape, unescape

global name
name = ""
# Use users.json and roles.json in the local example_conf directory
aaa = Cork('example_conf', email_sender='federico.ceratto@gmail.com', smtp_url='smtp://smtp.magnet.ie')

LOG_FILENAME = 'example.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)



# Initialise our views, all arguments are defaults for the template
page_view = view.View()

#-----------------------------------------------------------------------------
# Current User Data
#-----------------------------------------------------------------------------
def current_user_data():
    """Show current user role"""
    session = bottle.request.environ.get('beaker.session')
    aaa.require(fail_redirect='/login')
    return { 'user_email': aaa.current_user.email_addr, 'user_role': aaa.current_user.role, 'username':aaa.current_user.username};

def all_user_data():
    session = bottle.request.environ.get('beaker.session')
    aaa.require(fail_redirect='/login')
    return { 'users': aaa._store.users};

def user_is_anonymous():
    if aaa.user_is_anonymous:
        return 'True'

    return 'False'

#-----------------------------------------------------------------------------
# Index
#-----------------------------------------------------------------------------

def index(login):
    '''
        index
        Returns the view for the index
    '''
    if login == 0:
        return page_view("home", page_title="")
    return redirect("/login")

#-----------------------------------------------------------------------------
# Login
#-----------------------------------------------------------------------------

def login_form():
    '''
        login_form
        Returns the view for the login_form
    '''
    if aaa.user_is_anonymous:
        return page_view("login", page_title="")
    else:
        return redirect("/dashboard")


#-----------------------------------------------------------------------------

# Check the login credentials
def login_check(username, password):
    '''
        login_check
        Checks usernames and passwords

        :: username :: The username
        :: password :: The password

        Returns either a view for valid credentials, or a view for invalid credentials
    '''

    # check login status and user permission
    global name
    name = username
    aaa.login(username, password, success_redirect='/dashboard', fail_redirect='/invalid?reason=Sorry,%20These%20credentials%20do%20not%20match%20our%20records.%20Please%20Check!')


#-----------------------------------------------------------------------------
# Register
#-----------------------------------------------------------------------------

def register_form():
    '''
        register_form
        Returns the view for the register_form
    '''
    if aaa.user_is_anonymous:
        return page_view("register", page_title="")
    else:
        return redirect("/dashboard")

#-----------------------------------------------------------------------------

# Process a register request
def register_post(username, password, confirm_password):

    reason = ""
    if username == "" or password == "": # Wrong Username
        reason = "Username and password could not be empty!"
    if username in aaa._store.users:
        reason = "User is already existing."
    if password != confirm_password:
        reason = "Password are not matching."

    if reason != "":
        return redirect("/invalid?reason=" + reason)

    try:
        aaa._store.users[username] = {
            "role": "user",
            "username": username,
            "hash": aaa._hash(username=username, pwd=password),
            "email_addr": "",
            "desc": "",
            "creation_date": str(datetime.utcnow()),
            "last_login": str(datetime.utcnow()),
            "muted" : 0,
        }
        aaa._store.save_users()
    except Exception as e:
        reason = 'Caught this server error: ' + repr(e)

    else:
        return redirect("/login?redirect_msg=Registered%20successfully!%20Please%20Login.")

#-----------------------------------------------------------------------------
# Invalid
#-----------------------------------------------------------------------------
def invalid(reason):
    '''
        Invalid
        Returns the view for the invalid page
    '''
    return page_view("invalid", reason=reason, page_title="")


#-----------------------------------------------------------------------------
# Dashboard
#-----------------------------------------------------------------------------
def dashboard():
    '''
        Dashboard
        Returns the view for the dashboard page
    '''
    aaa.require(fail_redirect='/login')
    return page_view("dashboard", page_title="Dashboard", **current_user_data())


#-----------------------------------------------------------------------------
# About
#-----------------------------------------------------------------------------

def about():
    '''
        about
        Returns the view for the about page
    '''
    return page_view("about", garble=about_garble(), page_title="About")

#-----------------------------------------------------------------------------
# 404
#-----------------------------------------------------------------------------

def error404():
    '''
        404
        Returns the view for the 404 page
    '''
    # return page_view("error404", page_title="404 Not Found")
    return template("templates/error404")

#-----------------------------------------------------------------------------
# logout
#-----------------------------------------------------------------------------
def logout():
    '''
        logout
    '''
    aaa.logout(success_redirect='/home')

# Returns a random string each time
def about_garble():
    '''
        about_garble
        Returns one of several strings for the about page
    '''
    garble = ["leverage agile frameworks to provide a robust synopsis for high level overviews.",
    "iterate approaches to corporate strategy and foster collaborative thinking to further the overall value proposition.",
    "organically grow the holistic world view of disruptive innovation via workplace diversity and empowerment.",
    "bring to the table win-win survival strategies to ensure proactive domination.",
    "ensure the end of the day advancement, a new normal that has evolved from generation X and is on the runway heading towards a streamlined cloud solution.",
    "provide user generated content in real-time will have multiple touchpoints for offshoring."]
    return garble[random.randint(0, len(garble) - 1)]

#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------

def message(db):
    aaa.require(fail_redirect='/login')
    current_user = aaa.current_user.username
    from_mes = query_db(db, 'SELECT * from messages where from_user=?', (current_user,))
    to_mes = query_db(db, 'SELECT * from messages where to_user=?', (current_user,))
    message_ids = [x["id"] for x in from_mes] + [x["id"] for x in to_mes]


    format_strings=','.join(['?'] * len(message_ids))
    r_sql = 'SELECT * FROM replies where message_id in (%s)' % format_strings
    replies = query_db(db, r_sql,
                   tuple(message_ids))

    # print('SELECT * FROM replies from message_id in (?)' % format_strings)
    return page_view("message", page_title = "Message", from_me_messages = json.dumps(from_mes),
                     to_me_messages = json.dumps(to_mes), replies = json.dumps(replies), **current_user_data())

def message_post(db):
    result ={'error': 1}
    if aaa.user_is_anonymous:
        result['msg'] = 'Please Login!'
        return json.dumps(result)

    from_user = aaa.current_user.username
    to_user = request.forms.get('to_user')
    subject = request.forms.get('subject')
    body = request.forms.get('body')

    # simple from validation
    if (not to_user) or (not subject) or (not body):
        result['msg'] = 'Please complete the form!'
        return json.dumps(result)
    if not aaa.user(to_user):
        result['msg'] = '"To" user cannot be found! Please check.'
        return json.dumps(result)
    if to_user == from_user:
        result['msg'] = 'You cannot send message to yourself!'
        return json.dumps(result)

    # input filter for security purpose
    subject=escape(repr(subject)[1:-1])
    body=escape(repr(body)[1:-1])

    try:
        db.execute(
            """INSERT INTO messages(from_user, to_user, subject, body, create_at) VALUES (?,?,?,?,?)""",
            (from_user, to_user, subject, body, datetime.now().strftime('%Y-%m-%d-%H:%M:%S')))
    except Exception as e:
        result['msg'] = 'Database error! Please contact the administrator!'
        print(e)
        return json.dumps(result)

    result['error'] = 0
    result['msg'] = 'Message has been sent successfully!'
    return json.dumps(result)

def message_delete(message_id, db):
    result={'error': 1}
    if aaa.user_is_anonymous:
        result['msg'] = 'Please Login!'
        return json.dumps(result)

    current_user = aaa.current_user.username;

    try:
        db.execute(
            """DELETE FROM messages WHERE id=? AND (from_user=? OR to_user=?)""",
            (message_id, current_user, current_user,))
        db.execute(
            """DELETE FROM replies WHERE message_id=?""",
            (message_id,))
    except Exception as e:
        result['msg'] = 'Database error! Please contact the administrator!'
        print(e)
        return json.dumps(result)

    result['error'] = 0
    result['msg'] = 'Message has been deleted successfully!'
    return json.dumps(result)

def message_reply_post(db):
    result={'error': 1}
    if aaa.user_is_anonymous:
        result['msg'] = 'Please Login!'
        return json.dumps(result)

    current_user = aaa.current_user.username
    from_user = current_user
    body = request.forms.get('replay')
    body = escape(repr(body)[1:-1])
    message_id = request.forms.get('msg_id')
    try:
        db.execute(
            """INSERT INTO replies(from_user, message_id, body, create_at) VALUES (?,?,?,?)""",
            (from_user, message_id, body, datetime.now().strftime('%Y-%m-%d-%H:%M:%S')))
    except Exception as e:
        result['msg'] = 'Database error! Please contact the administrator!'
        print(e)
        return json.dumps(result)

    result['error'] = 0
    result['msg'] = 'The Reply has been sent successfully!'
    return json.dumps(result)

def profile():
    aaa.require(fail_redirect='/login')
    return template("templates/profile.html", **current_user_data())
    #return page_view("profile", page_title = "Profile", **current_user_data())
def manage_user():
    aaa.require(fail_redirect='/login')
    if aaa.current_user.role=='user':
        return error404()
    else:
        return template("templates/manage_user.html", **all_user_data())

def reset_password():
    aaa.require(fail_redirect='/login')
    return page_view("reset_password", page_title = "Reset Password", **current_user_data())

def reset_password_post(old_password, new_password, confirm_password):

    result ={'error': 1}
    if aaa.user_is_anonymous:
        result['msg'] = 'Please Login!'
        return json.dumps(result)

    reason = ""
    current_user = aaa.current_user

    if old_password == "" or new_password == "" or confirm_password == "": # Wrong Username
        reason = "Please complete the form!"
    salted_hash = aaa._store.users[current_user.username]["hash"]
    if hasattr(salted_hash, "encode"):
        salted_hash=salted_hash.encode("ascii")
    authenticated=aaa._verify_password(current_user.username, old_password, salted_hash)
    if not authenticated:
        reason = "Old password is not valid! Please check."
    if new_password != confirm_password:
        reason = "Password are not matching."

    if reason != "":
        return redirect("/invalid?reason=" + reason)

    try:
        """Change password"""
        aaa.reset_password(aaa._reset_code(current_user.username, current_user.email_addr), new_password)
    except Exception as e:
        reason = 'Caught this server error: ' + repr(e)

    if reason != "":
        return redirect("/invalid?reason=" + reason)
    else:
        return aaa.logout(success_redirect="/invalid?reason=Your%20password%20has%20been%20changed,%20please%20login%20in%20again!")

# util functions
def convert_to_json(cursor):
    return json.dumps([dict(zip([column[0] for column in cursor.description], row))
             for row in cursor.fetchall()])
def query_db(db, query, args=(), one=False):
    cur = db.cursor()
    cur.execute(query, args)
    r = [dict((cur.description[i][0], value) \
               for i, value in enumerate(row)) for row in cur.fetchall()]
    return (r[0] if r else None) if one else r
