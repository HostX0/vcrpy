import asyncio

import pytest

pytest.importorskip("aiohttp")

from vcr.request import Request
from vcr.stubs.aiohttp_stubs import build_response


def test_replayed_aiohttp_content_stream_keeps_cursor_state():
    async def read_lines():
        response = build_response(
            Request("GET", "https://example.com/", None, {}),
            {
                "status": {"code": 200, "message": "OK"},
                "headers": {},
                "body": {"string": b"first\nsecond\n"},
            },
            [],
        )

        content = response.content
        assert response.content is content
        assert await response.content.readline() == b"first\n"
        assert await response.content.readline() == b"second\n"
        assert await response.content.readline() == b""

    asyncio.run(read_lines())
