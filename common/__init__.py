from common.validation import apply
import logging

from flask import request
from flask_restful import Resource

success = {"code": "0", "message": "OK"}


class BaseResource(Resource):
    request_models = {}

    def _get_valid_request_object(self, method):
        object_type = self.request_models[method]
        obj = object_type()  # initialize the object

        json = request.get_json()
        for key, value in json.items():
            apply(obj, key, value)

        return obj

    def dispatch_request(self, *args, **kwargs):
        method = request.method.lower()
        if method in self.request_models:
            request_obj = self._get_valid_request_object(method)
            kwargs['request'] = request_obj

        return super().dispatch_request(*args, **kwargs)
