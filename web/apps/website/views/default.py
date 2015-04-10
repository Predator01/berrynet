# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request

from core.query import Query



bp = Blueprint('default', __name__)


@bp.route('/', methods=['GET'], strict_slashes=False)
def index():
    """Returns the index interface."""
    return render_template('index.html')


@bp.route('/analyze', methods=['GET'], strict_slashes=False)
def query():
    """Returns the query results."""
    template_variables = {}
    book_url = request.args.get('url', '')

    # with Query(None, db_url, book_url, should_download=True) as query:
    #     e, r = query.results()
    #     t = query.top(500)

    # template_variables['e'] = e
    # template_variables['r'] = r
    # template_variables['t'] = t
    return render_template('result.html', **template_variables)
    