#!/usr/bin/env python
# coding: utf-8
"""
    exceptions.py
    ~~~~~~~~~~

"""


class ApiUtilsException(Exception):
    def __init__(self, code, message):
        self.__code = code
        self.__message = message

    def __str__(self):
        return u"ApiUtilsException<code:{}, message:{}>".format(self.__code, self.__message)


class ApiUtilsValidationError(Exception):
    pass


