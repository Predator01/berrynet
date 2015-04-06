# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request


bp = Blueprint('default', __name__)


@bp.route('/', methods=['GET'], strict_slashes=False)
def index():
    """Returns the index interface."""
    return render_template('index.html')


@bp.route('/analyze', methods=['GET'], strict_slashes=False)
def query():
    """Returns the query results."""
    query = request.args.get('query', '')
    return render_template('restult.html')
    