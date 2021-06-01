from typing import Any, Callable, Mapping
from flask import request


def str_is_none(is_none, val: str):
    if is_none:
        return val is None
    return val is not None


def str_min_len(min_len, val):
    print("min_len: %d, val: %s" % (min_len, val))
    if len(val) < min_len:
        raise ValueError()
    return None


def str_max_len(max_len, val):
    print("max_len: %d, val: %s" % (max_len, val))
    if len(val) > max_len:
        return ValueError()
    return None


_constraint_container: Mapping[str, Callable[[Any], None or Exception]] = {
    'str-is-none': str_is_none,
    'str-min_len': str_min_len,
    'str-max_len': str_max_len,
}


class Validator:
    def __init__(self, _type, parameters: Mapping[str, Any]) -> None:
        self.type = _type
        self.parameters = parameters
        self.is_report_ready = False
        self.general_validation_report = []

    def validate(self, field_value: Any):
        self.is_report_ready = True
        for key, constraint_value in self.parameters.items():
            constraint = '%s-%s' % (self.type, key)
            if constraint in _constraint_container:
                validator = _constraint_container[constraint]
                validation_response = validator(constraint_value, field_value)
                self.general_validation_report.append(validation_response)

    def is_valid(self):
        if not self.is_report_ready:
            raise Exception("report is not ready yet, first run validate")

        for report in self.general_validation_report:
            if report is not None:
                return False
        return True

    def raise_error_stack(self):
        raise Exception(self.general_validation_report)

    def apply(self, value):
        """
        First it will run the validate method, if it is not ran yet 
        If there is an error in the report it will raise whole errors
        otherwise it will return the incoming value.
        """
        if not self.is_report_ready:
            self.validate(value)

        if not self.is_valid():
            self.raise_error_stack()

        return value


class Field:
    @classmethod
    def __get_clean_params(self, params):
        return {key: val for key, val in params.items() if val is not None and key != 'self'}

    @classmethod
    def String(self, is_none=None, is_blank=None, is_empty=None, is_email=None, pattern=None, min_len=None, max_len=None):
        return Validator('str', self.__get_clean_params(locals()))

    @classmethod
    def Integer(self, min=None, max=None):
        return Validator('int', self.__get_clean_params(locals()))

    @classmethod
    def Float(self, min=None, max=None):
        return Validator('float', self.__get_clean_params(locals()))

    @classmethod
    def Object(self):
        return Validator('object', self.__get_clean_params(locals()))

    @classmethod
    def Custom(self, name, **kwargs):
        return Validator('custom', self.__get_clean_params(locals()))


def apply(obj: Any, field_name: str, field_value: Any):

    attr = None
    try:
        attr = obj.__getattribute__(field_name)
    except Exception as ex:
        print("unexpected value captured, err: ", ex)
        return

    if not isinstance(attr, Validator):
        print(
            "current field is not defined as a validator, so processing this field is risky")
        return

    # Raise meaningful http exception, here is the failing scenario of the validation
    try:
        # returns the new value or raise exception
        value = attr.apply(field_value)
        obj.__setattr__(field_name, value)
    except Exception as ex:
        print("error occurred at validation process, err: ", ex)
        raise ValueError()
