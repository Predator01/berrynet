# -*- coding: utf-8 -*-

from os import path

from flask import Blueprint, render_template, request

from core.query import Query
from core.settings import BASE_DIR

bp = Blueprint('default', __name__)


@bp.route('/', methods=['GET'], strict_slashes=False)
def index():
    """Returns the index interface."""
    return render_template('index.html')


@bp.route('/analyze', methods=['GET'], strict_slashes=False)
def query():
    """Returns the query results."""
    db_url = path.join(BASE_DIR, "berrynet.db")
    template_variables = {}
    book_url = request.args.get('url', '')
    e, r, t = None, None, None
    with Query(None, db_url, book_url, should_download=True) as query:
        e, r = query.results()
        t = query.top(500)
    template_variables['e'] = e
    template_variables['r'] = r
    template_variables['t'] = t
    # print "template variables = %s" % str(template_variables)
    return render_template('result.html', **template_variables)
    