'''
    This file will handle our typical Bottle requests and responses
    You should not have anything beyond basic page loads, handling forms and
    maybe some simple program logic
'''

from bottle import route, get, post, request, static_file, error, Bottle, template, redirect
import os
import argparse
import model
import bottle
import sqlite3

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

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

# @get('/forum')
# def info2222_forum():
#     return model.info2222_forum()



#list all Threads
@get('/forum')
def get_forum(thread_name = None):
    model.aaa.require(fail_redirect='/login')
    conn = sqlite3.connect('forum.db')
    c = conn.cursor()
    threads = []
    cursor = c.execute("SELECT name, role, topic, reply, content, id, reply_id from FORUM")
    for row in cursor:
        threads.append(row)
    threads.reverse()
    conn.close()
    return model.template("templates/forum.html", threads = threads, thread_name = thread_name, **model.current_user_data(), muted = model.all_user_data()['users'][model.current_user_data()['username']]['muted'])

@get('/forum/new')
def forum_new(thread_name = None):
    model.aaa.require(fail_redirect='/login')
    conn = sqlite3.connect('forum.db')
    c = conn.cursor()
    threads = []
    cursor = c.execute("SELECT name, role, topic, reply, content, id, reply_id from FORUM")
    for row in cursor:
        threads.append(row)
    threads.reverse()
    conn.close()
    return model.template("templates/forum_new.html", threads = threads, thread_name = thread_name, muted = model.all_user_data()['users'][model.current_user_data()['username']]['muted'])

@post('/forum/new')
def receive_forum_new(thread_name = None):
    model.aaa.require(fail_redirect='/login')
    thread_name = request.forms.get('topic')
    content = request.forms.get('content')
    conn = sqlite3.connect('forum.db')
    c = conn.cursor()


#     c.execute("SELECT count(*) FROM FORUM WHERE topic='"+thread_name+"'")
#
# #if the count is 1, then table exists
#     if c.fetchone()[0]>=1 :
#     	c.execute("UPDATE FORUM set content = '"+content+"' where topic='"+thread_name+"' and reply = 'no'")
#     else :
    c.execute("INSERT INTO FORUM (name,role,topic,reply,content) \
      VALUES ('"+model.aaa.current_user.username+"', '"+model.aaa.current_user.role+"', '"+thread_name+"', 'no', '"+content+"')")
    conn.commit()
    conn.close()
    return get_forum()

@get('/forum/read/<thread_name>')
def get_forum_by_name(thread_name):
    model.aaa.require(fail_redirect='/login')
    return get_forum(thread_name)

@post('/forum/read/<thread_name>')
def get_reply(thread_name):
    model.aaa.require(fail_redirect='/login')
    reply = request.forms.get('reply')
    conn = sqlite3.connect('forum.db')
    c = conn.cursor()
    c.execute("INSERT INTO FORUM (name,role,topic,reply,content,id) \
          VALUES ('"+model.aaa.current_user.username+"', '"+model.aaa.current_user.role+"', '"+"reply"+"', 'yes', '"+reply+"', '"+thread_name+"')")
    conn.commit()
    conn.close()
    return get_forum(thread_name)

@get('/forum/delete/<info>')
def get_delete(info):
    model.aaa.require(fail_redirect='/login')
    reply = request.forms.get('reply')
    conn = sqlite3.connect('forum.db')
    c = conn.cursor()
    if len(info.split('_y_')) == 2:
        info = info.split('_y_')
        c.execute("DELETE FROM FORUM WHERE reply_id = '"+info[0]+"'")
        conn.commit()
        conn.close()
        return get_forum(info[1])
    elif len(info.split('_n_')) == 2:
        # print(info)
        info = info.split('_n_')
        # print(info)
        # c.execute("DELETE FROM FORUM WHERE topic = '"+info[0]+"' and reply = 'no'")
        # c.execute("DELETE FROM FORUM WHERE topic = '"+info[0]+"' and reply = 'yes'")
        c.execute("DELETE FROM FORUM WHERE id = '"+info[0]+"'")
        conn.commit()
        conn.close()
        return get_forum(None)


    # model.aaa.require(fail_redirect='/login')
    # conn = sqlite3.connect('forum.db')
    # c = conn.cursor()
    # threads = []
    # cursor = c.execute("SELECT name, role, topic, content  from FORUM")
    # for row in cursor:
    #     threads.append(row)
    # threads.reverse()
    # return model.template("templates/forum.html", threads = threads, thread_name = thread_name)

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

@get('/manage_user')
def manage_user():
    return model.manage_user()

@get('/delete/<user_name>')
def delete_user(user_name):
    model.aaa.require(fail_redirect='/login')
    if model.aaa.current_user.role=='user':
        return model.error404()
    del model.all_user_data()['users'][user_name]
    return bottle.redirect('/manage_user')

@get('/promote/<user_name>')
def promote(user_name):
    model.aaa.require(fail_redirect='/login')
    if model.aaa.current_user.role=='user':
        return model.error404()
    model.all_user_data()['users'][user_name]['role'] = 'staff'
    return bottle.redirect('/manage_user')

@get('/profile/reset_password')
def reset_password():
    model.aaa.require(fail_redirect='/login')
    return

@get('/mute/<user>')
def mute_user(user):
    model.aaa.require(fail_redirect='/login')
    if model.aaa.current_user.role=='user':
        return model.error404()
    model.all_user_data()['users'][user]['muted'] = 1
    return bottle.redirect('/manage_user')

@get('/unmute/<user>')
def unmute_user(user):
    model.aaa.require(fail_redirect='/login')
    if model.aaa.current_user.role=='user':
        return model.error404()
    model.all_user_data()['users'][user]['muted'] = 0
    return bottle.redirect('/manage_user')

##########################################################################################
