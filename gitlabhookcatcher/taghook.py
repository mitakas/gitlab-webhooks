# Copyright 2014 Sebastian Jordan

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from BaseHTTPServer import (HTTPServer,
                            BaseHTTPRequestHandler)
import SocketServer
import os
import subprocess
import tempfile
from shutil import rmtree
from hook import HookHandler


class TagHookHandler(HookHandler):
    """Request handler to handle the tag web hook

    You need to specify a pypi repository for the hook handler to
    work.  You do that by setting the pypirepo field of the class:
    HookHandler.pypirepo = "yourrepo".

    Notice that the repo name you specify has to appear in the .pypirc
    of the user running server.
    """
    def do_POST(self):
        
        # send ok
        if self.checkIP():
            self.send_response(200)
        else:
            self.send_response(403)
            return

        # parse json
        print("Parse JSON...")
        data = self.getJSON()
        if data is None:
            print("... JSON not valid!")
            return
        print("... JSON okay")

        ref = data['ref']
        repo = data['repository']['url']

        print("Check repository URL...")
        if not self.checkRepoURL(repo):
            print("... URL not allowed")
            return
        print("... URL okay")

        # handle tag
        handle_tag(repository=repo, reference=ref, pypi=self.pypirepo)

    pypirepo = ""


def handle_tag(repository, reference, pypi):
    
    # get current directory
    current_dirname = os.getcwd()
    # create a temporary directory
    tempdir_name = tempfile.mkdtemp()

    # change to temporary directory
    os.chdir(tempdir_name)
    # pull repository and checkout the reference
    subprocess.call(['git','clone',repository,'-n','.'])
    subprocess.call(['git','checkout',reference])

    if os.path.exists('setup.py'):
        subprocess.call(['python','setup.py','sdist','upload','-r',pypi])

    # change back to current directory
    os.chdir(current_dirname)
    # delete temporary directory
    rmtree(tempdir_name)
    
        
def run_server(port, klass=TagHookHandler):
    server_address = ('', port)
    httpd = HTTPServer(server_address, klass)
    print("Start Webserver on port %i" % port)
    print("Hit CTL-C to shut down the server")
    print("Upload new releases to pypi repository \"%s\""\
          % TagHookHandler.pypirepo)
    # start web server
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.socket.close()
