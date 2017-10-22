from http.server import BaseHTTPRequestHandler, HTTPServer
#class webserverHandler
def main():
    try:
        port = 8080
        server = HTTPServer(('',port), webserverHandler)
