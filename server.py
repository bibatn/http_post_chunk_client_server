from http.server import BaseHTTPRequestHandler, HTTPServer
import time

class ChunkedResponseHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Transfer-Encoding', 'chunked')
        # self.send_header('Content-Length', '31')
        self.end_headers()

    def do_POST(self):
        data = "{\"success\":true, \"body\":\"ON\"}"
        self._set_headers()

        # Отправка данных чанками
        for i in range(0, len(data), 5):  # Отправляем чанками по 5 байт
            chunk = data[i:i+5]
            tosend = "%X\r\n%s\r\n" % (len(chunk), chunk)
            bytes = tosend.encode('utf-8')
            self.wfile.write(bytes)
            self.wfile.flush()  # Форсированная передача чанка

        self.wfile.write('0\r\n\r\n'.encode())  # Отправляем последний чанк


def run(server_class=HTTPServer, handler_class=ChunkedResponseHandler, port=1):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd on port %d...' % port)
    httpd.serve_forever()


if __name__ == "__main__":
    run()