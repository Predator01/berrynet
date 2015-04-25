# -*- coding: utf-8 -*-
"""

"""

from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware

from web.apps.website import Website

#import berrynet


website = Website()

application = DispatcherMiddleware(
    website.get_app(), {
    '/berrynet': website.get_app()
    }
)


if __name__ == "__main__":
    run_simple(
        '0.0.0.0',
        5000,
        application,
        use_reloader=True,
        use_debugger=True)
