from flask import request
from flask_restful import Resource

from common.validation import apply

success = {"code": "0", "message": "OK"}


class BaseResource(Resource):
    request_models = {}

    def _get_valid_request_object(self, method):
        object_type = self.request_models[method]
        obj = object_type()  # initialize the object

        all_attrs = obj.__dir__()
        attrs = [attr for attr in all_attrs if not attr.__contains__("_")]

        json = request.get_json()
        for attr in attrs:
            request_value = json.get(attr)
            apply(obj, attr, request_value)

        return obj

    def dispatch_request(self, *args, **kwargs):
        method = request.method.lower()
        if method in self.request_models:
            request_obj = self._get_valid_request_object(method)
            kwargs['request'] = request_obj

        return super().dispatch_request(*args, **kwargs)
