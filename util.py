# encoding: utf-8

from datetime import datetime
import json
import sys
import traceback
import requests


# helper functions

def write_tmp_file(name, lines, new_file=False, dir='/tmp/'):
    if not isinstance(lines, list):
        lines = [lines]

    lines = [str(datetime.now()), ''] + lines

    if not dir.endswith('/'):
        dir += '/'
    with open(dir + name, 'w' if new_file else 'a') as tmp:
        tmp.writelines(map(lambda l: str(l) + '\n', lines))


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


def get_json_value(js, path, expected=False, split_char='.'):

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
                return None

        current = current[path_part]

    return current


def dumpjs(js, indent=4):
    return json.dumps(js, indent=indent)


# plugin response functions


def stdout(line):
    sys.stdout.write(line)
    sys.stdout.write('\n')


def stderr(line):
    sys.stderr.write(line)
    sys.stderr.write('\n')


def return_response(response):
    stdout(dumpjs(response))
    exit(0)


def return_error_response(error):
    stderr(error)
    exit(1)

# fylr api functions


def fylr_api_headers(access_token):
    return {
        'authorization': 'Bearer ' + access_token,
    }


def get_from_api(api_url, path, access_token):
    resp = requests.get(
        api_url + '/' + path,
        headers=fylr_api_headers(access_token))

    return resp.text, resp.status_code


def post_to_api(api_url, path, access_token, payload=None):
    resp = requests.post(
        api_url + '/' + path,
        headers=fylr_api_headers(access_token),
        data=payload)

    return resp.text, resp.status_code
