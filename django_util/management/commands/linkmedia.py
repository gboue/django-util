# -*- coding: utf-8 -*-
#!/usr/bin/python

import os
import sys

from django.conf import settings
from django.core.management.base import NoArgsCommand
from django.core.exceptions import ImproperlyConfigured
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
		
		
		print "MEDIA_ROOT %s" % (settings.MEDIA_ROOT)	
		
		if not os.path.isdir(settings.MEDIA_ROOT):
			raise ImproperlyConfigured('MEDIA_ROOT %s improprly configured' % (settings.MEDIA_ROOT))
			
		for app in settings.INSTALLED_APPS:
		    try:
		        mod = import_module(app)
		    except ImportError, e:
		        raise ImproperlyConfigured('ImportError %s: %s' % (app, e.args[0]))
		    app_media_dir = os.path.join(os.path.dirname(mod.__file__), 'media')
		    if os.path.isdir(app_media_dir):
				
				source_dir = app_media_dir
				sub_media_dir = os.path.join(app_media_dir, mod.__name__)
				
				if os.path.isdir(sub_media_dir):
					source_dir = sub_media_dir
					print "%s exist" % (sub_media_dir)
				else:
					print "%s will be used" % (app_media_dir)	
			
				link_to = os.path.join(settings.MEDIA_ROOT, mod.__name__)
			
				try:
					os.symlink(source_dir, link_to)
					print "%s ==> %s OK " % (link_to,source_dir,)
				except Exception, e:
					print e
			
		
		