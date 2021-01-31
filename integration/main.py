#!/usr/bin/env python3.9

"""
This is the entry point to run integration tests from.
At the moment, it expects the docker-compose system to be running,
and to have a clean DB at outset.
TODO: startup the docker-compose system from within this script.

We spin up a test http server which our jobs will make requests to.
"""

import asyncio

from aiohttp import web


async def start_test_http_server(req_q: asyncio.Queue):
    """
    Run a test http server.
    All requests are just passed back into a queue to be handled elsewhere.
    """
    async def base_handler(req):
        body = await req.text()
        req_q.put_nowait(body)
        return web.Response(text="TEST-OK")
    app = web.Application()
    app.add_routes([web.post("/", base_handler)])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 8080)
    await site.start()
    return


async def run_tests(req_q: asyncio.Queue):
    async def wait_next_req():
        return await req_q.get()
    # do tests here...
    return


async def main():
    req_q = asyncio.Queue()
    await asyncio.gather(*[
        start_test_http_server(req_q),
        run_tests(req_q),
    ])
    return


if __name__ == '__main__':
    asyncio.run(main())