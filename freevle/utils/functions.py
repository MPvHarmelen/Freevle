"""Functions that come in handy"""

import re
from unicodedata import normalize
from markdown import Markdown

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
