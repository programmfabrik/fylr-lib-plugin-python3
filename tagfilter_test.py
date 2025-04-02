from . import util


def test_tagfilter_initial_state():
    tag_filter = util.TagFilter()

    assert tag_filter.is_empty()
    assert str(tag_filter) == '[empty]'


def test_tagfilter_parse_valid():
    tag_filter = util.TagFilter()

    assert not tag_filter.parse(
        {
            'any': [
                1,
                2,
            ],
            'all': [
                3,
            ],
            'not': [
                4,
                5,
            ],
        }
    )
    assert tag_filter._any == [
        1,
        2,
    ]
    assert tag_filter._all == [
        3,
    ]
    assert tag_filter._not == [
        4,
        5,
    ]


def test_tagfilter_parse_invalid():
    tag_filter = util.TagFilter()

    assert not tag_filter.parse('invalid')
    assert not tag_filter.parse(
        [
            1,
            2,
            3,
        ]
    )
    assert not tag_filter.parse(None)


def test_tagfilter_parse_dirty():
    tag_filter = util.TagFilter()

    assert tag_filter.parse(
        {
            'any': [
                'x',
            ],
            'all': [
                'a',
                'b',
            ],
            'not': [
                None,
                'y',
            ],
            'xxx': [
                5,
                6,
            ],
        }
    )

    assert not tag_filter.parse(
        {
            'any': [
                'x',
                1,
                2,
            ],
            'all': [
                'y',
                3,
            ],
            'not': [
                None,
                4,
                None,
            ],
            'xxx': [
                5,
                6,
            ],
        }
    )
    assert tag_filter._any == [
        1,
        2,
    ]
    assert tag_filter._all == [
        3,
    ]
    assert tag_filter._not == [
        4,
    ]


def test_tagfilter_parse_empty():
    tag_filter = util.TagFilter()

    assert tag_filter.parse({})
    assert tag_filter.is_empty()


def test_tagfilter_str_representation():
    tag_filter = util.TagFilter()

    assert not tag_filter.parse(
        {
            'any': [
                1,
            ],
            'all': [
                2,
                3,
            ],
            'not': [
                4,
            ],
        }
    )
    assert str(tag_filter) == 'any: [1], all: [2, 3], not: [4]'

    tag_filter.parse({})
    assert str(tag_filter) == '[empty]'


def test_tagfilter_match_empty():
    tag_filter = util.TagFilter()

    assert tag_filter.parse({})
    assert tag_filter.match([])
    assert tag_filter.match(
        [
            {
                '_id': 1,
            },
            {
                '_id': 2,
            },
        ]
    )


def test_tagfilter_match_all():
    tag_filter = util.TagFilter()

    assert not tag_filter.parse(
        {
            'all': [
                1,
                2,
            ]
        }
    )
    assert not tag_filter.match(
        [
            {
                '_id': 1,
            },
            {
                '_id': 3,
            },
        ]
    )
    assert tag_filter.match(
        [
            {
                '_id': 1,
            },
            {
                '_id': 2,
            },
        ]
    )


def test_tagfilter_match_not():
    tag_filter = util.TagFilter()

    assert not tag_filter.parse(
        {
            'not': [
                1,
                2,
            ]
        }
    )
    assert not tag_filter.match(
        [
            {
                '_id': 1,
            },
        ]
    )
    assert not tag_filter.match(
        [
            {
                '_id': 1,
            },
            {
                '_id': 2,
            },
        ]
    )
    assert tag_filter.match([])
    assert tag_filter.match(
        [
            {
                '_id': 3,
            },
            {
                '_id': 4,
            },
        ]
    )


def test_tagfilter_match_any():
    tag_filter = util.TagFilter()

    assert not tag_filter.parse(
        {
            'any': [
                1,
                2,
            ]
        }
    )
    assert not tag_filter.match([])
    assert not tag_filter.match(
        [
            {
                '_id': 3,
            },
        ]
    )
    assert tag_filter.match(
        [
            {
                '_id': 2,
            },
            {
                '_id': 4,
            },
        ]
    )


def test_tagfilter_match_complex():
    tag_filter = util.TagFilter()

    assert not tag_filter.parse(
        {
            'all': [
                1,
                2,
            ],
            'not': [
                3,
            ],
            'any': [
                4,
                5,
            ],
        }
    )
    assert not tag_filter.match([])
    assert not tag_filter.match(
        [
            {
                '_id': 3,
            },
        ]
    )
    assert not tag_filter.match(
        [
            {
                '_id': 1,
            },
            {
                '_id': 2,
            },
            {
                '_id': 3,
            },
        ]
    )
    assert not tag_filter.match(
        [
            {
                '_id': 1,
            },
            {
                '_id': 2,
            },
        ]
    )
    assert not tag_filter.match(
        [
            {
                '_id': 1,
            },
            {
                '_id': 4,
            },
            {
                '_id': 5,
            },
        ]
    )

    assert tag_filter.match(
        [
            {
                '_id': 1,
            },
            {
                '_id': 2,
            },
            {
                '_id': 4,
            },
        ]
    )
    assert tag_filter.match(
        [
            {
                '_id': 1,
            },
            {
                '_id': 2,
            },
            {
                '_id': 5,
            },
        ]
    )
