def parse_request(data: bytes):
    parsed_answer = {}
    str_data = data.decode('utf-8')
    header, body = str_data.split('\r\n\r\n', 1)
    arr = header.split('\r\n')
    request = arr[0].split(' ')
    parsed_answer['method'] = request[0]
    parsed_answer['path'] = request[1]
    parsed_answer['version'] = request[2]
    parsed_answer['headers'] = {}
    for i in range(1, len(arr)):
        key, value = arr[i].split(':', 1)
        parsed_answer['headers'][key] = value.strip()
    parsed_answer['body'] = body
    return parsed_answer

if __name__ == '__main__':
    ret_ans = parse_request(b'GET /index.html HTTP/1.1\r\nHost: localhost:8080\r\nUser-Agent: curl/8.19.0\r\nAccept: */*\r\n\r\n')
    print(ret_ans)