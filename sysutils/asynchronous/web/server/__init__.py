"""
JUST A (little bit updated) COPY of original web.Application
"""

import asyncio


def run_app(app, *,
            host='0.0.0.0',
            port=None,
            shutdown_timeout=60.0,
            ssl_context=None,
            print=print,
            backlog=128,
            tasks=()):
    """Run an app locally"""
    if port is None:
        if not ssl_context:
            port = 8080
        else:
            port = 8443

    loop = app.loop

    handler = app.make_handler()
    server = loop.create_server(handler, host, port, ssl=ssl_context,
                                backlog=backlog)
    srv, startup_res = loop.run_until_complete(asyncio.gather(server,
                                                              app.startup(),
                                                              loop=loop))

    scheme = 'https' if ssl_context else 'http'
    print("======== Running on {scheme}://{host}:{port}/ ========\n"
          "(Press CTRL+C to quit)".format(scheme=scheme, host=host, port=port))

    try:
        loop.run_forever()
    except KeyboardInterrupt:  # pragma: no cover
        pass
    finally:
        srv.close()
        for t in tasks:
             t.cancel()
        loop.run_until_complete(srv.wait_closed())
        loop.run_until_complete(app.shutdown())
        #loop.run_until_complete(handler.finish_connections(shutdown_timeout))
        loop.run_until_complete(app.cleanup())
    loop.close()

