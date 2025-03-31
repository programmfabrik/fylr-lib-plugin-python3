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
        tmp.writelines(
            map(
                lambda l: (
                    dumpjs(l)
                    if (isinstance(l, dict) or isinstance(l, list))
                    else str(l)
                )
                + '\n',
                lines,
            )
        )


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
    js: dict[str],
    path: str,
    expected: bool = False,
    split_char: str = '.',
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
                return None

        current = current[path_part]

    return current


def dumpjs(js: dict[str], indent: int = 4) -> str:
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
        write_tmp_file('stdout.json', line, new_file=True)
    sys.stdout.write(line)
    sys.stdout.write('\n')


def stderr(line: str, log_in_tmp_file: bool = False):
    if log_in_tmp_file:
        write_tmp_file('stderr.json', line, new_file=True)
    sys.stderr.write(line)
    sys.stderr.write('\n')


def return_response(response: dict[str], log_in_tmp_file: bool = False):
    if log_in_tmp_file:
        write_tmp_file('return_response.json', dumpjs(response), new_file=True)
    stdout(dumpjs(response))
    exit(0)


def return_error_response(error: str, log_in_tmp_file: bool = False):
    if log_in_tmp_file:
        write_tmp_file('return_error_response.json', error, new_file=True)
    stderr(error)
    exit(1)


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


def fylr_api_headers(access_token: str) -> dict[str]:
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
    payload: str = None,
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
        data=payload,
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
) -> dict[str]:
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
