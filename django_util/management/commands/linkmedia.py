# -*- coding: utf-8 -*-
#!/usr/bin/python

import os
import sys

from django.conf import settings
from django.core.management.base import NoArgsCommand
from django.utils._os import safe_join
from django.utils.importlib import import_module
import shutil

class Command(NoArgsCommand):
	help = "Link the media files from apps into the project media folder"

	def handle_noargs(self, **options):
		
		#from django.core.exceptions import ImproperlyConfigured
		#from django.template import TemplateDoesNotExist
		#from django.template.loader import BaseLoader
	
		# create the media directories into the media folder
		fs_encoding = sys.getfilesystemencoding() or sys.getdefaultencoding()
		
		for app in settings.INSTALLED_APPS:
		    try:
		        mod = import_module(app)
		    except ImportError, e:
		        raise ImproperlyConfigured('ImportError %s: %s' % (app, e.args[0]))
		    media_dir = os.path.join(os.path.dirname(mod.__file__), 'media')
		    if os.path.isdir(media_dir):
				sub_media_dir = os.path.join(media_dir, mod.__name__)
			
				if os.path.isdir(sub_media_dir):
					
					print "%s will be used" % (sub_media_dir)
				else:
					
					print "%s will be used" % (media_dir)					
			
		
		