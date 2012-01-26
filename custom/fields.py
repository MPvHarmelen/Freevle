import re
from django.forms import fields
from django.forms import ValidationError
from django.utils.encoding import smart_unicode

class HexColorField(fields.Field):
	
	default_error_messages = {
		'hex_error': u'This is an invalid color code. It must be a html hex color code e.g. #000000'
	}

	def clean(self, value):
		
		super(HexColorField, self).clean(value)
		
		if value in fields.EMPTY_VALUES:
			return u''
		
		value = smart_unicode(value)
		value_length = len(value)
		
		if value_length != 7 or not re.match('^\#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$', value):
			raise ValidationError(self.error_messages['hex_error'])
		
		return value

	def widget_attrs(self, widget):
		if isinstance(widget, (fields.TextInput)):
			return {'maxlength': str(7)}
