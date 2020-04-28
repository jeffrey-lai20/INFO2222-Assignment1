'''
    Our Model class
    This should control the actual "logic" of your website
    And nicely abstracts away the program logic from your page loading
    It should exist as a separate layer to any database or data structure that you might be using
    Nothing here should be stateful, if it's stateful let the database handle it
'''
import view
import random
from bottle import template, redirect, static_file
import bottle
from beaker.middleware import SessionMiddleware
from cork import Cork
from datetime import datetime, timedelta
import logging

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
    return { 'user_email': aaa.current_user.email_addr, 'user_role': aaa.current_user.role };

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
    if username != confirm_password:
        reason = "Password are not matching."

    try:
        aaa._store.users[username] = {
            "role": "user",
            "hash": aaa._hash(username=username, pwd=password),
            "email_addr": "",
            "desc": "",
            "creation_date": str(datetime.utcnow()),
            "last_login": str(datetime.utcnow()),
        }
        aaa._store.save_users()
    except Exception as e:
        reason = 'Caught this server error: ' + repr(e)

    if reason != "":
        return redirect("/invalid?reason=" + reason)
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
    return page_view("error404", page_title="404 Not Found")

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

def info2222_homepage():
    aaa.require(fail_redirect='/login')
    return page_view("info2222", page_title = "INFO2222-Homepage" , **current_user_data())

def info2222_forum():
    aaa.require(fail_redirect='/login')
    return page_view("info2222_forum", page_title = "INFO2222-Forum", **current_user_data())

def announcement_final():
    aaa.require(fail_redirect='/login')
    return page_view("announcement_final", page_title = "INFO2222-Forum", **current_user_data())

def forum_new_thread():
    aaa.require(fail_redirect='/login')
    return page_view("forum_new_thread", page_title = "INFO2222-Forum", **current_user_data())

def forum_new_thread_post():
    aaa.require(fail_redirect='/login')
    return page_view("forum_new_thread_post", page_title = "INFO2222-Forum", **current_user_data())

def forum_answer():
    aaa.require(fail_redirect='/login')
    return page_view("forum_answer", page_title = "INFO2222-Forum", **current_user_data())

def message():
    aaa.require(fail_redirect='/login')
    return page_view("message", page_title = "INFO2222-Message", **current_user_data())

def profile():
    aaa.require(fail_redirect='/login')
    return page_view("profile", page_title = "Profile", **current_user_data())
