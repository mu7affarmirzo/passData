from django.db import models

from django.db.models.signals import pre_save, post_delete
from django.utils.timezone import now
from django.utils.text import slugify
from django.dispatch import receiver
from django.utils import timezone
from django.conf import settings
from datetime import datetime 
from uuid import uuid4
import random as r

def upload_location(instance, filename):
	ext = filename.split('.')[-1]
	file_path = 'static/detectall/imgs/{filename}'.format(
		filename='{}.{}'.format(uuid4().hex, ext)
	)
	return file_path

class PassportDataModel(models.Model):
	class Meta:
		verbose_name = "Passport"
		verbose_name_plural = "Passport danniylar"

	pass_img = models.ImageField(upload_to=upload_location, null=True, blank=True)

	# def location_f(self):
	# 	loc = self.pass_img.url
	# 	return loc

	def __str__(self):
		return str(self.pass_img)