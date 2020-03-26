# -*- coding: utf-8 -*-
import secrets
from datetime import datetime
from http.server import BaseHTTPRequestHandler

from logger_settings import logging_setup


class Server(BaseHTTPRequestHandler):

    log = logging_setup()

    def do_GET(self):
        self._req_handler()
        self._give_response()

    def do_POST(self):
        self._req_handler()
        self._give_response()

    def do_PUT(self):
        self._req_handler()
        self._give_response()

    def do_PATCH(self):
        self._req_handler()
        self._give_response()

    def do_DELETE(self):
        self._req_handler()
        pass

    def do_TRACE(self):
        self._req_handler()
        self._give_response()

    def do_HEAD(self):
        self._req_handler()
        self._give_response()

    def _give_response(self):
        self.send_response(200)
        self.end_headers()

    def _req_handler(self):
        """
        Функция обработки запросов, всех, для создания всех логов
        """
        # Эта штука создает метку события, по которой его можно однозначно идентифицировать
        req_stamp = f'{self.command}_{secrets.token_hex(5)}_{str(datetime.now())}'

        self._log_msg_creator(req_stamp, self.path)

        # Разделение пути и параметров
        path_lst = self.path.split('?')

        # Проверка на метод запроса
        if self.command != 'GET':
            self._log_msg_creator(req_stamp, path_lst[0], err_msg=True, err_type='Method error')

        # Проверка на путь
        if path_lst[0] != '/api':
            self._log_msg_creator(req_stamp, path_lst[0], err_msg=True, err_type='Path error')
        try:
            param = path_lst[1]
        except IndexError:
            pass
        else:
            # Проверка на параметры запроса
            if param != '':
                param_lst = param.split('&')
                self._log_msg_creator(
                    req_stamp,
                    path_lst[0],
                    err_msg=True,
                    err_type='Parameter error',
                    param_lst=param_lst
                )

    def _log_msg_creator(self, req_stamp, path, err_msg=False, err_type=None, param_lst=None):
        """
        Функция записи лога в файл
        :param req_stamp: Метка запроса
        :param path: Путь запроса
        :param err_msg: Это лог ошибки или нет
        :param err_type: Тип ошибки если это лог ошибки
        :param param_lst: Список параметров запроса
        """
        msg = f'Request stamp:{req_stamp}\n' \
              f'Method:{self.command}\n' \
              f'Path:{path}\n'

        msg_param = 'Params:\n'

        if param_lst:
            for item in param_lst:
                msg_param += f'{item}'

        if err_msg:
            msg_err = f'Type error:{err_type}\n'
            msg_result = f'{msg}{msg_err}{msg_param}'
            self.log.error(msg_result)
        else:
            msg_result = f'{msg}{msg_param}'
            self.log.info(msg_result)
