'''
    This is a file that configures how your server runs
    You may eventually wish to have your own explicit config file
    that this reads from.

    For now this should be sufficient.

    Keep it clean and keep it simple, you're going to have
    Up to 5 people running around breaking this constantly
    If it's all in one file, then things are going to be hard to fix

    If in doubt, `import this`
'''

#-----------------------------------------------------------------------------

import sys
from bottle import get, post, request, static_file, error, Bottle, template,ServerAdapter, route, run, server_names
import bottle.ext.sqlite
import model
import argparse
import bottle
from beaker.middleware import SessionMiddleware
import os
from cheroot import wsgi
from cheroot.ssl.builtin import BuiltinSSLAdapter

import ssl
import crypt
import pwd

#-----------------------------------------------------------------------------
# You may eventually wish to put these in their own directories and then load
# Each file separately

# For the template, we will keep them together

import model
import view
import controller

#-----------------------------------------------------------------------------
# import configurations
configs = {}
try:
    import configs
    configs = configs.configs
    default_configs  = False
except ImportError:
    default_configs = True
    pass

# It might be a good idea to move the following settings to a config file and then load them
# Change this to your IP address or 0.0.0.0 when actually hosting
host = '0.0.0.0' if default_configs else configs["web"]["host"]

# Test port, change to the appropriate port to host
port = 8080 if default_configs else configs["web"]["port"]

# Turn this off for production
debug = True

# Turn this off for production
fast = False if default_configs else configs["app"]["fast"]


################################################################################################################
#Resource part
@get('/resource')
def do_index():
    """List all uploaded files"""
    model.aaa.require(fail_redirect='/login')
    root = '%s/' % bottle.request.environ.get('SCRIPT_NAME')
    return bottle.template('templates/resource.html', files=os.listdir(app.config['file_upload.dir']), root=root, **model.current_user_data())
    #return model.page_view('resource', page_title="Resource", files=os.listdir(app.config['file_upload.dir']), root=root)

@get('/resource/download/<filename>')
def do_download(filename):
    model.aaa.require(fail_redirect='/login')
    """Return a static file from the files directory"""
    return bottle.static_file(filename, root=app.config['file_upload.dir'])

@post('/resource/upload')
def do_upload():
    model.aaa.require(fail_redirect='/login')
    """Upload a file if it's missing"""
    upload = bottle.request.files.get('upload') # pylint: disable-msg=E1101
    try:
        upload.save(app.config['file_upload.dir'])
    except IOError as io_error:
        return bottle.HTTPError(409, io_error)

    root = '%s/' % bottle.request.environ.get('SCRIPT_NAME')
    bottle.redirect('/resource')

@get('/resource/delete/<filename>')
def do_delete(filename):
    model.aaa.require(fail_redirect='/login')
    if model.aaa.current_user.role == "user":
        return
    os.remove("files/" + filename)
    bottle.redirect('/resource')

def create_files_dir(path):
    """Create a directory to upload files to if it's missing."""
    if not os.path.isdir(path):
        os.mkdir(path)

################################################################################################################
app = bottle.app()

class SSLCherryPyServer(ServerAdapter):

    def run(self, handler):
        server = wsgi.Server((self.host, self.port), handler)
        server.ssl_adapter = BuiltinSSLAdapter("server.crt", "server.key")

        server.ssl_adapter.context.options |= ssl.OP_NO_TLSv1
        server.ssl_adapter.context.options |= ssl.OP_NO_TLSv1_1

        try:
            server.start()
        finally:
            server.stop()

def run_server():
    '''
        run_server
        Runs a bottle server
    '''
    # app = bottle.app()


    # add bottle-sqlite plugin
    # link to sqlite3 database
    plugin=bottle.ext.sqlite.Plugin(dbfile='./database/info2222.db')
    app.install(plugin)

    session_opts = {
        'session.cookie_expires': True,
        'session.encrypt_key': 'please use a random key and keep it secret!',
        'session.httponly': True,
        'session.timeout': 3600 * 24,  # 1 day
        'session.type': 'cookie',
        'session.validate_key': True,
    }

################################################################################################################

    # bottle.route('/resource', 'GET', do_index)
    # bottle.route('/resource/download/<filename>', 'GET', do_download)
    # bottle.route('/resource/upload', 'POST', do_upload)

    # Change working directory so relative paths (and template lookup) work
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    app.config.setdefault('file_upload.dir', 'files')

    if os.path.exists('file_upload.conf'):
        app.config.load_config('file_upload.conf')
    create_files_dir(app.config['file_upload.dir'])

################################################################################################################

    appp = SessionMiddleware(app, session_opts)
    run(app=appp, host=host, port=port, server=SSLCherryPyServer, fast=fast)


#-----------------------------------------------------------------------------
# Optional SQL support
# Comment out the current manage_db function, and
# uncomment the following one to load an SQLite3 database

def manage_db():
    '''
        Blank function for database support, use as needed
    '''
    pass

"""
import sql

def manage_db():
    '''
        manage_db
        Starts up and re-initialises an SQL databse for the server
    '''
    database_args = ":memory:" # Currently runs in RAM, might want to change this to a file if you use it
    sql_db = sql.SQLDatabase(database_args=database_args)

    return
"""

#-----------------------------------------------------------------------------

# What commands can be run with this python file
# Add your own here as you see fit

command_list = {
    'manage_db' : manage_db,
    'server'       : run_server
}

# The default command if none other is given
default_command = 'server'

def run_commands(args):
    '''
        run_commands
        Parses arguments as commands and runs them if they match the command list

        :: args :: Command line arguments passed to this function
    '''
    commands = args[1:]

    # Default command
    if len(commands) == 0:
        commands = [default_command]

    for command in commands:
        if command in command_list:
            command_list[command]()
        else:
            print("Command '{command}' not found".format(command=command))

#-----------------------------------------------------------------------------

def app_instance():
    app=bottle.default_app()
    plugin=bottle.ext.sqlite.Plugin(dbfile='./database/info2222.db')
    app.install(plugin)

    session_opts={
        'session.cookie_expires': True,
        'session.encrypt_key': 'please use a random key and keep it secret!',
        'session.httponly': True,
        'session.timeout': 3600 * 24,  # 1 day
        'session.type': 'cookie',
        'session.validate_key': True,
    }
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    app.config.setdefault('file_upload.dir', 'files')

    if os.path.exists('file_upload.conf'):
        app.config.load_config('file_upload.conf')
    create_files_dir(app.config['file_upload.dir'])

    appp=SessionMiddleware(app, session_opts)
    return appp

#-----------------------------------------------------------------------------

if __name__ == '__main__':
  run_commands(sys.argv)
else:
  app = application = app_instance();