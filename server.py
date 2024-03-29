from http.server import BaseHTTPRequestHandler, HTTPServer
import time

class ChunkedResponseHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Transfer-Encoding', 'chunked')
        self.end_headers()

    def do_POST(self):
        data = "{\"success\":true, \"body\":\"ON\"}\r\n".encode('utf-8')
        self._set_headers()

        # Отправка данных чанками
        for i in range(0, len(data), 5):  # Отправляем чанками по 5 байт
            chunk = data[i:i+5]
            self.wfile.write(("%X\r\n" % len(chunk)).encode('utf-8'))
            self.wfile.write(chunk)
            self.wfile.write(b'\r\n')
            self.wfile.flush()  # Форсированная передача чанка
            time.sleep(2)

        self.wfile.write('0\r\n\r\n'.encode())  # Отправляем последний чанк


def run(server_class=HTTPServer, handler_class=ChunkedResponseHandler, port=1):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd on port %d...' % port)
    httpd.serve_forever()


if __name__ == "__main__":
    run()