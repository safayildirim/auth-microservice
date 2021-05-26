import logging

from flask import request
from flask_restful import Resource
from flask_restful.utils import unpack, OrderedDict
from werkzeug.wrappers import Response as ResponseBase

try:
    from collections.abc import Mapping
except ImportError:
    from collections import Mapping

success = {"code": "0", "message": "OK"}


class BaseResource(Resource):
    representations = None
    method_decorators = []

    def dispatch_request(self, *args, **kwargs):
        # Taken from flask
        # noinspection PyUnresolvedReferences
        logging.info('Request method %s', request.method.lower())

        meth = getattr(self, request.method.lower(), None)
        if meth is None and request.method == 'HEAD':
            meth = getattr(self, 'get', None)
        assert meth is not None, 'Unimplemented method %r' % request.method

        logging.info('decorators %s', self.method_decorators)
        if isinstance(self.method_decorators, Mapping):
            decorators = self.method_decorators.get(request.method.lower(), [])
        else:
            decorators = self.method_decorators

        for decorator in decorators:
            meth = decorator(meth)
        logging.info('after running decorators')

        resp = meth(*args, **kwargs)
        logging.info("response: %s", resp)

        if isinstance(resp, ResponseBase):  # There may be a better way to test
            return resp

        representations = self.representations or OrderedDict()

        # noinspection PyUnresolvedReferences
        mediatype = request.accept_mimetypes.best_match(representations, default=None)
        if mediatype in representations:
            data, code, headers = unpack(resp)
            resp = representations[mediatype](data, code, headers)
            resp.headers['Content-Type'] = mediatype
            return resp

        return resp
