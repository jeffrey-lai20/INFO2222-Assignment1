'''
    Our Model class
    This should control the actual "logic" of your website
    And nicely abstracts away the program logic from your page loading
    It should exist as a separate layer to any database or data structure that you might be using
    Nothing here should be stateful, if it's stateful let the database handle it
'''
import view
import random
from bottle import template, redirect

# Initialise our views, all arguments are defaults for the template
page_view = view.View()

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
    else:
        return page_view("valid", name="admin", page_title="Dashboard")
    #return redirect("/login")

#-----------------------------------------------------------------------------
# Login
#-----------------------------------------------------------------------------

def login_form():
    '''
        login_form
        Returns the view for the login_form
    '''
    return page_view("login", page_title="")

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

    # By default assume good creds
    login = True

    if username != "admin": # Wrong Username
        err_str = "Incorrect Username"
        login = False

    if password != "password": # Wrong password
        err_str = "Incorrect Password"
        login = False

    if login:
        return page_view("valid", name=username, page_title="Dashboard")
    else:
        return page_view("invalid", reason=err_str)

#-----------------------------------------------------------------------------
# Register
#-----------------------------------------------------------------------------

def register_form():
    '''
        login_form
        Returns the view for the login_form
    '''
    return page_view("register", page_title="")

#-----------------------------------------------------------------------------

def register_check(username, password, confirm_password):
    if password != confirm_password:
        return redirect("/register")
    return redirect("/login")

#-----------------------------------------------------------------------------
# About
#-----------------------------------------------------------------------------

def about():
    '''
        about
        Returns the view for the about page
    '''
    return page_view("about", garble=about_garble())

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

def info2222_homepage():
    return page_view("info2222", page_title = "INFO2222-Homepage")

def info2222_resource():
    return page_view("info2222_resource", page_title = "INFO2222-Resource")

def info2222_resource_upload():
    return page_view("info2222_resource_upload", page_title = "INFO2222-Resource")

def info2222_forum():
    return page_view("info2222_forum", page_title = "INFO2222-Forum")

def announcement_final():
    return page_view("announcement_final", page_title = "INFO2222-Forum")

def forum_new_thread():
    return page_view("forum_new_thread", page_title = "INFO2222-Forum")

def forum_new_thread_post():
    return page_view("forum_new_thread_post", page_title = "INFO2222-Forum")

def forum_answer():
    return page_view("forum_answer", page_title = "INFO2222-Forum")

def message():
    return page_view("message", page_title = "INFO2222-Message")
