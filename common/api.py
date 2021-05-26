import logging

from flask import jsonify
from flask_restful import Api

from common.exception import HttpException


class BaseApi(Api):
    def handle_error(self, err: Exception):
        if isinstance(err, HttpException):
            logging.error('Http exception captured, err: %s', err)
            return err.get_body(), err.http_status

        # if exception is not httpException that means it is unknown exception
        # so we need to return unknown error and we should log this
        logging.exception('Unknown exception captured, err: %s', err)
        return jsonify({'code': '999999', 'message': 'UNKNOWN ERROR'}), 500
