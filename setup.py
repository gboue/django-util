#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os,sys

from django_util  import VERSION

setup(name='django_util',
      version=".".join(map(str, VERSION)),
      description="Usefull tools for a django project",
      long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
      classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        ], 
      keywords='django tool',
      author='Guillaume Boue',
      author_email='guillaumeboue@gmail.com',
      url='http://github.com/gboue/django-util',
      license='BSD',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=[],
      )


