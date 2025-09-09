# encoding: utf-8


import json
import sys


from . import util

# helper class with functions to parse the info json block from fylr


class PluginCallbackInfo:

    __plugin_name: str
    __access_token: str
    __external_url: str
    __api_url: str
    __query: dict
    __plugin_config: dict
    __objects: list

    def __init__(self, plugin_name: str):
        self.__plugin_name = plugin_name

    def __get(self, js: dict, path: str, default=None):
        return util.get_json_value(
            js=js,
            path=path,
            default=default,
        )

    def parse_from_stdin(self):
        self.parse(sys.stdin.read())

    def parse(self, raw_info_json: str):
        __info_json = json.loads(raw_info_json)
        self.__access_token = str(
            self.__get(__info_json, 'info.api_user_access_token', '')
        )
        self.__external_url = str(self.__get(__info_json, 'info.external_url', ''))
        self.__api_url = str(self.__get(__info_json, 'info.api_url', ''))

        __query = self.__get(__info_json, 'info.request.query', None)
        if isinstance(__query, dict):
            self.__query = __query
        else:
            self.__query = {}

        __plugin_config = self.__get(
            __info_json, f'info.config.plugin.{self.__plugin_name}.config', None
        )
        if isinstance(__plugin_config, dict):
            self.__plugin_config = __plugin_config
        else:
            self.__plugin_config = {}

        __objects = self.__get(__info_json, 'objects', None)
        if isinstance(__objects, list):
            self.__objects = __objects
        else:
            self.__objects = []

    def get_access_token(self) -> str:
        return self.__access_token

    def get_external_url(self) -> str:
        return self.__external_url

    def get_api_url(self) -> str:
        return self.__api_url

    def get_object_list(self) -> list:
        if not isinstance(self.__objects, list):
            return []
        return self.__objects

    def get_main_objecttype(self) -> str:
        if not self.__objects:
            return ''
        return self.__objects[0].get('_objecttype')

    def get_query_parameter(self, parameter: str) -> str:
        params = self.__get(self.__query, parameter, default=[])
        if not params or not isinstance(params, list):
            return ''
        return params[0]

    def get_list_from_plugin_config(self, path: str, default=[]) -> list:
        l = self.__get(self.__plugin_config, path, default=default)
        if isinstance(l, list):
            return l
        return default

    def get_dict_from_plugin_config(self, path: str, default={}) -> dict:
        d = self.__get(self.__plugin_config, path, default=default)
        if isinstance(d, dict):
            return d
        return default

    def get_str_from_plugin_config(self, path: str, default='') -> str:
        s = self.__get(self.__plugin_config, path, default=default)
        if isinstance(s, str):
            return s
        return default

    def get_int_from_plugin_config(self, path: str, default=0) -> int:
        i = self.__get(self.__plugin_config, path, default=default)
        if isinstance(i, int):
            return i
        return default

    def get_bool_from_plugin_config(self, path: str, default=False) -> bool:
        b = self.__get(self.__plugin_config, path, default=default)
        if isinstance(b, bool):
            return b
        return default
