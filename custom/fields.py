# HexColorField
import re
from django.forms import fields
from django.forms import ValidationError
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext_lazy as _

class HexColorField(fields.Field):
    
    default_error_messages = {
        'hex_error': _('This is an invalid color code. It must be a html hex color code e.g. #000000')
    }

    def clean(self, value):
        
        super(HexColorField, self).clean(value)
        
        if value in fields.EMPTY_VALUES:
            return ''
        
        value = smart_unicode(value)
        value_length = len(value)
        
        if value_length != 7 or not re.match('^\#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$', value):
            raise ValidationError(self.error_messages['hex_error'])
        
        return value

    def widget_attrs(self, widget):
        if isinstance(widget, (fields.TextInput)):
            return {'maxlength': str(7)}

# ResizedImageField
from PIL import Image

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from django.db.models.fields.files import ImageField, ImageFieldFile
from django.core.files.base import ContentFile


def _update_ext(filename, new_ext):
    parts = filename.split('.')
    parts[-1] = new_ext
    return '.'.join(parts)


class ResizedImageFieldFile(ImageFieldFile):
    
    def save(self, name, content, save=True):
        new_content = StringIO()
        content.file.seek(0)

        img = Image.open(content.file)
        img.thumbnail((
            self.field.max_width, 
            self.field.max_height
            ), Image.ANTIALIAS)
        img.save(new_content, format=self.field.format)

        new_content = ContentFile(new_content.getvalue())
        new_name = _update_ext(name, self.field.format.lower())

        super(ResizedImageFieldFile, self).save(new_name, new_content, save)


class ResizedImageField(ImageField):
    
    attr_class = ResizedImageFieldFile

    def __init__(self, max_width=100, max_height=100, format='PNG', *args, **kwargs):
        self.max_width = max_width
        self.max_height = max_height
        self.format = format
        super(ResizedImageField, self).__init__(*args, **kwargs)

