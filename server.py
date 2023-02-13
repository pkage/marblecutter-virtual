# coding=utf-8
from __future__ import division, print_function

import logging
import os
from werkzeug.middleware.proxy_fix import ProxyFix

from virtual.web import app

logging.basicConfig(level=logging.INFO)
logging.getLogger("rasterio._base").setLevel(logging.WARNING)
LOG = logging.getLogger(__name__)

if 'FLASK_PROXY_DEPTH' in os.environ:
    proxy_depth = int(os.environ['FLASK_PROXY_DEPTH'])
    app.wsgi_app = ProxyFix(
        app.wsgi_app,
        x_for=proxy_depth,
        x_proto=proxy_depth,
        x_host=proxy_depth,
        x_prefix=proxy_depth
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8000)), debug=True)
