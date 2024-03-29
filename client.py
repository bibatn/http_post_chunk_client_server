import http.client

def print_chunks(host, port):
    conn = http.client.HTTPConnection(host, port)
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    body = "data=example_data"
    conn.request("POST", "/", body, headers)
    response = conn.getresponse()
    if response.status == 200:
        # chunk = response.readline()
        # print(chunk)
        while True:
            chunk_size_hex = response.fp.read(1)
            if not chunk_size_hex:
                break
            chunk_size = int(chunk_size_hex, 16)
            response.fp.read(2)  # Consume CRLF before chunk
            chunk = response.fp.read(chunk_size)
            print(chunk.decode('utf-8'))
            response.fp.read(2)  # Consume CRLF after chunk

    conn.close()

if __name__ == "__main__":
    print_chunks('localhost', 1)