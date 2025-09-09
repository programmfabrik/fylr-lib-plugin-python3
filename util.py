# encoding: utf-8

from datetime import datetime
import json
import sys
import traceback
import requests


# helper functions


def write_tmp_file(
    name: str,
    lines: list[str],
    new_file: bool = False,
    skip_datetime: bool = False,
    dir: str = '/tmp/',
):
    if not isinstance(lines, list):
        lines = [lines]

    if not skip_datetime:
        lines = ['// ' + str(datetime.now())] + lines

    if not dir.endswith('/'):
        dir += '/'
    with open(dir + name, 'w' if new_file else 'a') as tmp:
        tmp.writelines(map(lambda l: dumpjs(l) + '\n', lines))


def handle_exceptions(func):
    def func_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            exc_info = sys.exc_info()
            stack = traceback.extract_stack()
            tb = traceback.extract_tb(exc_info[2])
            full_tb = stack[:-1] + tb
            exc_line = traceback.format_exception_only(*exc_info[:2])

            trace = [str(repr(e))] + traceback.format_list(full_tb) + exc_line

            return_error_response('\n'.join(trace))

    return func_wrapper


def get_json_value(
    js: dict,
    path: str,
    split_char: str = '.',
    expected: bool = False,
    default=None,
):
    current = js
    path_parts = []
    current_part = ''

    for i in range(len(path)):
        if path[i] != split_char:
            current_part += path[i]
            if i == len(path) - 1:
                path_parts.append(current_part)
            continue

        if i > 0 and path[i - 1] == '\\':
            current_part += path[i]
            continue

        if len(current_part) > 0:
            path_parts.append(current_part)
            current_part = ''

    for path_part in path_parts:
        path_part = path_part.replace('\\' + split_char, split_char)

        if not isinstance(current, dict) or path_part not in current:
            if expected:
                raise Exception('expected: ' + path_part)
            else:
                return default

        current = current[path_part]

    return current


def dumpjs(js, indent: int = 4) -> str:
    return json.dumps(js, indent=indent)


def join_url_path(path_elements: list) -> str:
    cleaned_path_elements = []
    for p in path_elements:
        p = str(p).strip()
        while p.startswith('/'):
            p = p[1:]
        while p.endswith('/'):
            p = p[:-1]
        if p == '':
            continue

        cleaned_path_elements.append(p)

    return '/'.join(cleaned_path_elements)


# plugin response functions


def stdout(line: str, log_in_tmp_file: bool = False):
    if log_in_tmp_file:
        write_tmp_file('stdout.json', [line], new_file=True)
    sys.stdout.write(line)
    sys.stdout.write('\n')


def stderr(line: str, log_in_tmp_file: bool = False):
    if log_in_tmp_file:
        write_tmp_file('stderr.json', [line], new_file=True)
    sys.stderr.write(line)
    sys.stderr.write('\n')


def return_response(response: dict, log_in_tmp_file: bool = False):
    if log_in_tmp_file:
        write_tmp_file('return_response.json', [dumpjs(response)], new_file=True)
    stdout(dumpjs(response))
    exit(0)


def return_error_response(error: str, log_in_tmp_file: bool = False):
    if log_in_tmp_file:
        write_tmp_file('return_error_response.json', [error], new_file=True)
    stderr(error)
    exit(1)


def return_error_response_with_parameters(
    error: str,
    parameters: dict = {},
    statuscode: int = 400,
    log_in_tmp_file: bool = False,
):
    error_payload = {
        'code': error,
        'statuscode': statuscode,
        'parameters': parameters,
    }
    if log_in_tmp_file:
        write_tmp_file(
            'return_error_response.json',
            [dumpjs(error_payload)],
            new_file=True,
        )
    stdout(dumpjs(error_payload))
    exit(statuscode)


def return_empty_objects():
    # special helper method: used when no changes on any objects can or should be done
    # fylr only checks and updates objects that are returned by the plugin
    # empty object array in response => nothing to do
    return_response(
        {
            'objects': [],
        }
    )


# fylr api functions


def fylr_api_headers(access_token: str) -> dict:
    return {
        'authorization': 'Bearer ' + access_token,
    }


def get_from_api(
    api_url: str,
    path: str,
    access_token: str,
    log_in_tmp_file: bool = False,
) -> tuple[str, int]:

    if log_in_tmp_file:
        write_tmp_file(
            'get_from_api.json',
            [
                '// api_url: ' + api_url,
                '// path: ' + path,
            ],
            new_file=True,
        )

    resp = requests.get(
        url=join_url_path([api_url, path]),
        headers=fylr_api_headers(access_token),
    )

    if log_in_tmp_file:
        write_tmp_file(
            'get_from_api.json',
            [
                '// status_code: ' + str(resp.status_code),
                resp.text,
            ],
            new_file=False,
        )

    return resp.text, resp.status_code


def post_to_api(
    api_url: str,
    path: str,
    access_token: str,
    payload: str = '',
    log_in_tmp_file: bool = False,
) -> tuple[str, int]:

    if log_in_tmp_file:
        write_tmp_file(
            'post_to_api.json',
            [
                '// api_url: ' + api_url,
                '// path: ' + path,
                '// payload:',
                payload,
            ],
            new_file=True,
        )

    resp = requests.post(
        url=join_url_path([api_url, path]),
        headers=fylr_api_headers(access_token),
        data=payload if payload else None,
    )

    if log_in_tmp_file:
        write_tmp_file(
            'post_to_api.json',
            [
                '// status_code: ' + str(resp.status_code),
                resp.text,
            ],
            new_file=False,
        )

    return resp.text, resp.status_code


def get_config_from_api(
    api_url: str,
    access_token: str,
    path: str = '',
    log_in_tmp_file: bool = False,
) -> dict:
    content, status_code = get_from_api(
        api_url=api_url,
        path=join_url_path(['config', path]),
        access_token=access_token,
        log_in_tmp_file=log_in_tmp_file,
    )
    if status_code != 200:
        raise Exception(f'request failed: {status_code}: {content}')
    try:
        return json.loads(content)
    except Exception as je:
        raise Exception(f'request body parsing failed: {str(je)}: {content}')


# ------------------------------------


class TagFilter:

    _any: list[int]
    _all: list[int]
    _not: list[int]

    def __init__(self):
        self.reset()

    def __str__(self):
        if self.is_empty():
            return '[empty]'

        s = []
        for c in [
            ('any', self._any),
            ('all', self._all),
            ('not', self._not),
        ]:
            if len(c[1]) == 0:
                continue
            s.append(f'{c[0]}: {c[1]}')

        return ', '.join(s)

    def reset(self):
        self._any = []
        self._all = []
        self._not = []

    def is_empty(self) -> bool:
        """
        returns true if no valid tag ids are set
        """
        for c in [
            self._any,
            self._all,
            self._not,
        ]:
            if len(c) > 0:
                return False
        return True

    def parse(self, tagfilter_js: dict) -> bool:
        """
        parses the tagfilter json, returns true if the tagfilter is empty
        """

        self.reset()

        if not isinstance(tagfilter_js, dict):
            return False

        for c in [
            ('any', self._any),
            ('all', self._all),
            ('not', self._not),
        ]:
            _js = tagfilter_js.get(c[0])
            if not isinstance(_js, list):
                continue
            for _id in _js:
                if not isinstance(_id, int):
                    continue
                c[1].append(_id)

        return self.is_empty()

    def match(self, tags: list[dict]) -> bool:
        if self.is_empty():
            return True

        # collect all tag ids
        tag_ids: set[int] = set()
        for tag in tags:
            tag_id = tag.get('_id')
            if isinstance(tag_id, int):
                tag_ids.add(tag_id)

        # if any of the tags in 'not' is in the list: does not match
        for tag_id in self._not:
            if tag_id in tag_ids:
                return False

        # if any of the tags in 'all' is not in the list: does not match
        for tag_id in self._all:
            if tag_id not in tag_ids:
                return False

        # if none of the tags in 'any' is in the list: does not match
        _any = len(self._any) == 0
        for tag_id in self._any:
            if tag_id in tag_ids:
                _any = True
                break
        if not _any:
            return False

        # else: does match
        return True
