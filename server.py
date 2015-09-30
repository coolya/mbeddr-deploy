#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import json, os, hmac, hashlib

DEBUG = False
EXEC_CMD = os.getenv('EXEC_CMD', 'echo foo')

class GitAutoDeploy(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            self.handleStuff()
        except:
            pass

    def log_message(self, format, *args):
        return

    def handleStuff(self):
        try:
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
        except:
            print("Error")

def main():
    try:
        server = None
        print('KurzDNS GitHub Autodeploy Service Thing v1.0.1-ultrastable started.')
        server = HTTPServer(('', 8001), GitAutoDeploy)
        server.handle_one_request()
    except(KeyboardInterrupt, SystemExit) as e:
        if server:
            server.socket.close()

if __name__ == '__main__':
    main()