from django.db.models import fields
from django.db.models import Avg, Max

class OrderField(fields.IntegerField):
	"""Ignores the incoming value and instead gets the maximum plus one of the field."""
	def pre_save(self, model_instance, value):
		# if the model is new and not an update
		if model_instance.pk is None:
			records = model_instance.__class__.objects.aggregate(Max(self.name))
			if records['%s__max' % self.name]:
				# get the maximum attribute from the first record and add 1 to it
				value = records['%s__max' % self.name]	+ 1
			else:
				value = 1
		# otherwise the model is updating, pass the attribute value through
		else:
			value = getattr(model_instance, self.attname)
		return value

	
	# prevent the field from being displayed in the admin interface
	def formfield(self, **kwargs):
		return None 
		

