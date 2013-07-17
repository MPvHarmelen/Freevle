import re

def validate_slug(self, key, slug):
    if re.match("^[\w\d-_]*$", slug):
        return slug
    else:
        raise ValueError("A slug may only contain alphanumeric characters"
                         ", - (dash) and _ (underscore)."