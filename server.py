# coding=utf-8
from __future__ import division, print_function

import logging
import os
from werkzeug.middleware.proxy_fix import ProxyFix

from virtual.web import app

logging.basicConfig(level=logging.INFO)
logging.getLogger("rasterio._base").setLevel(logging.WARNING)
LOG = logging.getLogger(__name__)


app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8000)), debug=True)
