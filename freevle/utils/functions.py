"""Functions that come in handy"""

import re
from math import ceil
from unicodedata import normalize
from markdown import Markdown

from flask import request
from werkzeug.exceptions import NotFound

from freevle import app

markdown = Markdown(output_format='html5', safe_mode='escape', lazy_ol=False).convert

heading_tag = re.compile(r'<h(\d+).*>(.*)</h\1>')
def headles_markdown(text):
    text = markdown(text)
    return heading_tag.sub(r'<p>\2</p>', text)

image_tag = re.compile(r'<p><img alt=".*" src=".*"( title=".*")?></p>')
def imageles_markdown(text):
    text = headles_markdown(text)
    return image_tag.sub('<p>No inline images allowed</p>', text)

first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')
def camel_to_underscore(name):
    s1 = first_cap_re.sub(r'\1_\2', name)
    return all_cap_re.sub(r'\1_\2', s1).lower()

_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')
def slugify(text, delim='-'):
    """
    Generates an ASCII-only slug.
    Snippet from http://flask.pocoo.org/snippets/5/
    """
    result = []
    for word in _punct_re.split(text.lower()):
        word = normalize('NFKD', word).encode('ascii', 'ignore')
        if word:
            result.append(word)
    return delim.join(result)

def paginate(all_items, items_per_page=10, extra_function=lambda a: a):
    try:
        page = int(request.args.get('page', 1))
    except ValueError as e:
        if not app.config['DEBUG']:
            raise NotFound
        else:
            raise NotFound(e)
    # if page < 0:
    #     raise NotFound
    if page > 0:
        page -= 1 # Make 'page' zero based

    # list slicing lesson:
    # >>> li = [0,1,2,3,4,5,6,7,8,9]
    # >>> li[-2]
    # 8
    # >>> li[-2:0]
    # []
    # >>> li[-2:]
    # [8, 9]
    # >>> li[-2:None]
    # [8, 9]
    # Those last two results are what we're looking for.
    # That's why the if statement is in there.
    max_page = int(ceil(len(all_items) / items_per_page))
    items = all_items[
        items_per_page * page :
        items_per_page * (page + 1) if page != -1 else None
    ]
    if page < 0:
        # Make negative lookup positive again
        page += max_page
    if (max_page != 0 and abs(page) > max_page)\
       or abs(page) > max_page + 1:
        raise NotFound
    # Make 'page' one based again
    page += 1
    return extra_function(items), page, max_page
