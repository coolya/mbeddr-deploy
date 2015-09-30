#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import json, os, requests

DEBUG = False
EXEC_CMD = os.getenv('EXEC_CMD', 'echo foo')

class GitAutoDeploy(BaseHTTPRequestHandler):
    def do_POST(self):
            self.handleStuff()

    def handleStuff(self):

            length = int(self.headers.getheader('content-length'))
            body = self.rfile.read(length)
            data = json.loads(body)

            self.send_response(200)
            self.end_headers()

            cburl = data['callback_url']
            ret = os.system(EXEC_CMD)
            if ret == 0:
                state = 'success'
                description = 'Deployment to build servers PASSED'
            else:
                state = 'error'
                description = 'Deployment to build servers FAILED'

            cbdata = {
                'state': state,
                'description': description,
                'context': "mbeddr build server deployment",
            }
            if DEBUG:
                print(json.dumps(data, sort_keys = False, indent = 4))
                print('callback url:')
                print(cburl)
            r = requests.post(cburl, data=json.dumps(cbdata))


def main():
    try:
        server = None
        print('Mbeddr deploy helper started')
        server = HTTPServer(('', 8001), GitAutoDeploy)
        server.handle_request()
    except(KeyboardInterrupt, SystemExit) as e:
        if server:
            server.socket.close()

if __name__ == '__main__':
    main()