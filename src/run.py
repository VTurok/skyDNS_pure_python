# -*- coding: utf-8 -*-
import http.server
from sys import argv

import server


def port_validator(data):
    try:
        port = int(data)
    except TypeError:
        print('Введено некорректное значение порта.')
        port = 8001

    return port


def run(port=8001, handler=server.Server):
    server_param = ('', port)

    with http.server.HTTPServer(server_param, handler) as httpd:
        print('Server starting...')
        print(f'Port: {port}')
        httpd.serve_forever()

    print('Server stopping...')


if __name__ == '__main__':

    if len(argv) == 2:
        run(port=port_validator(argv[1]))
    else:
        run()
