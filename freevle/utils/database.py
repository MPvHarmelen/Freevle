import re

def validate_slug(self, key, slug):
    if type(slug) != str:
        raise TypeError('Expected string, got {}'.format(type(slug)))
    if re.match("^[\w\d_-]*$", slug):
        return slug.lower()
    else:
        raise ValueError("A slug must only contain alphanumeric characters"
                         ", - (dash) and _ (underscore).")
