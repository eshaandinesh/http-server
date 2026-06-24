def build_response(status_code, body, content_type):
    response = 'HTTP/1.1 ' + str(status_code) + ' '
    if status_code == 200:
        response += 'OK'
    elif status_code == 404:
        response += 'Not Found'
    elif status_code == 500:
        response += 'Internal Server Error'
    response += '\r\nContent-Type: ' + content_type + '\r\nContent-Length: ' + str(len(body)) + '\r\n\r\n' + body

    return response.encode('utf-8')