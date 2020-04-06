'''
    This file will handle our typical Bottle requests and responses
    You should not have anything beyond basic page loads, handling forms and
    maybe some simple program logic
'''

from bottle import route, get, post, request, static_file, error

import model

global login
login = 0
#-----------------------------------------------------------------------------
# Static file paths
#-----------------------------------------------------------------------------

# Allow image loading
@route('/img/<picture:path>')
def serve_pictures(picture):
    '''
        serve_pictures

        Serves images from static/img/

        :: picture :: A path to the requested picture

        Returns a static file object containing the requested picture
    '''
    return static_file(picture, root='static/img/')

#-----------------------------------------------------------------------------

# Allow CSS
@route('/css/<css:path>')
def serve_css(css):
    '''
        serve_css

        Serves css from static/css/

        :: css :: A path to the requested css

        Returns a static file object containing the requested css
    '''
    return static_file(css, root='static/css/')

#-----------------------------------------------------------------------------

# Allow javascript
@route('/js/<js:path>')
def serve_js(js):
    '''
        serve_js

        Serves js from static/js/

        :: js :: A path to the requested javascript

        Returns a static file object containing the requested javascript
    '''
    return static_file(js, root='static/js/')

#-----------------------------------------------------------------------------
# Pages
#-----------------------------------------------------------------------------

# Redirect to login
@get('/')
@get('/home')
def get_index():
    '''
        get_index

        Serves the index page
    '''
    global login
    return model.index(login)

#-----------------------------------------------------------------------------

# Display the login page
@get('/login')
def get_login_controller():
    '''
        get_login

        Serves the login page
    '''
    global login
    login = 1
    return model.login_form()

#-----------------------------------------------------------------------------

# Attempt the login
@post('/login')
def post_login():
    '''
        post_login

        Handles login attempts
        Expects a form containing 'username' and 'password' fields
    '''

    # Handle the form processing
    username = request.forms.get('username')
    password = request.forms.get('password')

    # Call the appropriate method
    return model.login_check(username, password)


# -----------------------------------------------------------------------------

# Display the register page
@get('/register')
def get_register_controller():
    '''
        get_register

        Serves the register page
    '''
    return model.register_form()


# -----------------------------------------------------------------------------

# Attempt the register
@post('/register')
def post_register():
    '''
        post_register

        Handles Register attempts
        Expects a form containing 'username' and 'password' fields
    '''

    # Handle the form processing
    username = request.forms.get('username')
    password = request.forms.get('password')
    confirm_password = request.forms.get('confirm_password')

    # Call the appropriate method
    return model.register_post(username, password, confirm_password)


# -----------------------------------------------------------------------------

# Logout
@get('/logout')
def get_logout_controller():
    '''
        get_login

        Serves the login page
    '''
    global login
    login = 0
    return model.logout()

#-----------------------------------------------------------------------------

@get('/about')
def get_about():
    '''
        get_about

        Serves the about page
    '''
    return model.about()

#-----------------------------------------------------------------------------

@get('/invalid')
def get_invalid():
    '''
        get_invalid

        Serves the invalid page
    '''
    reason = request.query['reason']
    return model.invalid(reason)


#-----------------------------------------------------------------------------

@get('/dashboard')
def get_dashboard():
    '''
        get_dashboard

        Serves the dashboard page
    '''
    return model.dashboard()

#-----------------------------------------------------------------------------

@error(404)
def error404(error):
    return model.error404()

#-----------------------------------------------------------------------------

# Subject's Homepage
@get('/info2222')
def info2222_homepage():
    return model.info2222_homepage()


#-----------------------------------------------------------------------------

# info2222 Resource page
@get('/resource')
def info2222_resource():
    return model.info2222_resource()

#-----------------------------------------------------------------------------
# info2222 Resouce Submit
@post('/resource')
def post_resource():
    return model.info2222_resource_upload()

#-----------------------------------------------------------------------------

@get('/info2222_resource_delete')
def info2222_resource_delete():
    return model.info2222_resource_delete()

@get('/forum')
def info2222_forum():
    return model.info2222_forum()

#-----------------------------------------------------------------------------

@get('/announcement_final')
def announcement_final():
    return model.announcement_final()

#-----------------------------------------------------------------------------

@get('/forum_new_thread')
def forum_new_thread():
    return model.forum_new_thread()

#-----------------------------------------------------------------------------

@get('/forum_new_thread_post')
def forum_new_thread_post():
    return model.forum_new_thread_post()

#-----------------------------------------------------------------------------

@get('/forum_answer')
def forum_answer():
    return model.forum_answer()

#-----------------------------------------------------------------------------

@get('/message')
def message():
    return model.message()

@get('/profile')
def profile():
    return model.profile()
