from . import plugin_info_json


def init_info_json() -> plugin_info_json.PluginCallbackInfo:
    info_json = plugin_info_json.PluginCallbackInfo(
        plugin_name='fylr-plugin-linked-object-use-once'
    )
    info_json.parse(
        raw_info_json="""
            {
                "info": {
                    "api_url": "http://localhost:8080",
                    "api_user": {
                        "_basetype": "user",
                        "user": {
                            "_generated_displayname": "root",
                            "_id": 1,
                            "_version": 4,
                            "frontend_language": "de-DE",
                            "type": "system"
                        }
                    },
                    "api_user_access_token": "ory_at_123accesstoken456",
                    "config": {
                        "plugin": {
                            "fylr-plugin-linked-object-use-once": {
                                "config": {
                                    "tan_settings": {
                                        "linked_settings": [
                                            {
                                                "main_objecttype": "objekt",
                                                "main_objecttype:info": {
                                                    "is_default": false
                                                },
                                                "tag_after": 2,
                                                "tag_after:info": {
                                                    "is_default": false
                                                },
                                                "tag_before": 1,
                                                "tag_before:info": {
                                                    "is_default": false
                                                },
                                                "tan_objecttype": "tan_objekt",
                                                "tan_objecttype:info": {
                                                    "is_default": false
                                                }
                                            }
                                        ],
                                        "linked_settings:info": {
                                            "is_default": false
                                        }
                                    }
                                }
                            }
                        },
                        "system": {
                            "config": {
                                "languages": {
                                    "database": [
                                        {
                                            "date_format": "de",
                                            "date_format:info": {
                                                "is_default": false
                                            },
                                            "number_format": "de",
                                            "number_format:info": {
                                                "is_default": false
                                            },
                                            "time_format": "de",
                                            "time_format:info": {
                                                "is_default": false
                                            },
                                            "value": "de-DE",
                                            "value:info": {
                                                "is_default": false
                                            }
                                        },
                                        {
                                            "date_format": "us",
                                            "date_format:info": {
                                                "is_default": false
                                            },
                                            "number_format": "us",
                                            "number_format:info": {
                                                "is_default": false
                                            },
                                            "time_format": "us",
                                            "time_format:info": {
                                                "is_default": false
                                            },
                                            "value": "en-US",
                                            "value:info": {
                                                "is_default": false
                                            }
                                        }
                                    ],
                                    "database:info": {
                                        "is_default": true
                                    },
                                    "frontend": [
                                        "de-DE",
                                        "en-US"
                                    ],
                                    "frontend:info": {
                                        "is_default": true
                                    }
                                }
                            }
                        }
                    },
                    "external_url": "http://localhost:8085",
                    "request": {
                        "header": {
                            "Accept": [
                                "*/*"
                            ],
                            "Accept-Language": [
                                "en-US,en;q=0.5"
                            ],
                            "Authorization": [
                                "Bearer ory_at_123accesstoken456"
                            ],
                            "Cache-Control": [
                                "no-cache"
                            ],
                            "Connection": [
                                "keep-alive"
                            ],
                            "Content-Length": [
                                "469"
                            ],
                            "Content-Type": [
                                "application/json; charset=utf-8"
                            ],
                            "Cookie": [
                                "fylr-browser-id=eyJVVUlEIjoiMTZmMjBiYTktMjcxNi00MjNmLTk5MDYtN2MyYjI4ZDY5YjA1IiwiTGFuZ3VhZ2UiOiJkZS1ERSJ9"
                            ],
                            "Origin": [
                                "http://localhost:8085"
                            ],
                            "Pragma": [
                                "no-cache"
                            ],
                            "Priority": [
                                "u=0"
                            ],
                            "Referer": [
                                "http://localhost:8085/search/"
                            ],
                            "Sec-Fetch-Dest": [
                                "empty"
                            ],
                            "Sec-Fetch-Mode": [
                                "cors"
                            ],
                            "Sec-Fetch-Site": [
                                "same-origin"
                            ],
                            "User-Agent": [
                                "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:142.0) Gecko/20100101 Firefox/142.0"
                            ],
                            "X-Fylr-Authorization": [
                                "Bearer ory_at_123accesstoken456"
                            ]
                        },
                        "host": "localhost:8085",
                        "method": "POST",
                        "query": {
                            "confirmTransition": [
                                "78f27eca682f76ff2b05196c14345b31"
                            ],
                            "format": [
                                "long"
                            ],
                            "priority": [
                                "2"
                            ]
                        },
                        "url": {
                            "ForceQuery": false,
                            "Fragment": "",
                            "Host": "",
                            "OmitHost": false,
                            "Opaque": "",
                            "Path": "/api/v1/db/objekt",
                            "RawFragment": "",
                            "RawPath": "",
                            "RawQuery": "priority=2&format=long&progress_uuid=8b911c3d-58e0-4313-89cc-66b3d4e3c00e&confirmTransition=78f27eca682f76ff2b05196c14345b31",
                            "Scheme": "",
                            "User": null
                        }
                    }
                },
                "objects": [
                    {
                        "_best_mask": false,
                        "_callback_context": {
                            "hash": "93a6de1a-0fa7-4c7b-a3c5-cf55ef97a6a5",
                            "original_mask": "objekt__mask"
                        },
                        "_collections": [],
                        "_comment": "",
                        "_create_user": null,
                        "_current": null,
                        "_format": "long",
                        "_has_children": false,
                        "_latest_version": false,
                        "_mask": "_all_fields",
                        "_mask_display_name": {
                            "und": "_all_fields"
                        },
                        "_objecttype": "objekt",
                        "_objecttype_display_name": {
                            "de-DE": "Objekt"
                        },
                        "_owner": null,
                        "_published": [],
                        "_published_count": 0,
                        "_standard": {
                            "1": {},
                            "eas": {
                                "1": null
                            },
                            "geo": {}
                        },
                        "_system_object_id": 0,
                        "_tags": [],
                        "_uuid": "",
                        "objekt": {
                            "_id": 0,
                            "_version": 1
                        }
                    }
                ]
            }
        """
    )
    return info_json


def test_jsoninfo_get_access_token():
    info_json = init_info_json()
    assert info_json.get_access_token() == 'ory_at_123accesstoken456'


def test_jsoninfo_get_external_url():
    info_json = init_info_json()
    assert info_json.get_external_url() == 'http://localhost:8085'


def test_jsoninfo_get_api_url():
    info_json = init_info_json()
    assert info_json.get_api_url() == 'http://localhost:8080'


def test_jsoninfo_get_main_objecttype():
    info_json = init_info_json()
    assert info_json.get_main_objecttype() == 'objekt'


def test_jsoninfo_get_objects():
    info_json = init_info_json()
    assert len(info_json.get_object_list()) == 1


def test_get_query_parameter():
    info_json = init_info_json()
    assert info_json.get_query_parameter('unknown') == ''
    assert (
        info_json.get_query_parameter('confirmTransition')
        == '78f27eca682f76ff2b05196c14345b31'
    )


def test_get_from_plugin_config():
    info_json = init_info_json()
    linked_settings = info_json.get_list_from_plugin_config(
        'tan_settings.linked_settings'
    )
    assert isinstance(linked_settings, list)
    assert len(linked_settings) == 1
    assert linked_settings[0].get('tan_objecttype') == 'tan_objekt'
