# -*- coding:utf-8 -*-

import sys
import uuid

from os import path
from flask import Blueprint, render_template, request

from core.query import Query
from core.settings import BASE_DIR, TEMP_DIR

bp = Blueprint('default', __name__)


@bp.route('/', methods=['GET'], strict_slashes=False)
def index():
    """Returns the index interface."""
    return render_template('index.html')


@bp.route('/analyze', methods=['GET'], strict_slashes=False)
def query():
    """Returns the query results."""
    reload(sys)
    sys.setdefaultencoding("utf-8")
    template_variables = {}
    db_url = path.join(BASE_DIR, "berrynet.db")
    text = request.args.get('text', '')
    filename = str(uuid.uuid4())
    book_url = path.join(TEMP_DIR, filename)
    e, r, t = None, None, None

    with open(book_url, 'w') as text_file:
        text_file.write(text)

    with Query(None, db_url, book_url, should_download=False) as query:
        e, r = query.results()
        t = query.top(500)

    template_variables['elizabethan'] = e
    template_variables['romantic'] = r
    template_variables['top'] = t
    print "template variables = %s" % str(template_variables)
    return render_template('result.html', **template_variables)
    