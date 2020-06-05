from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(
	name='ckanext-grouphierarchy',
	version=version,
	description="CKAN group hierarchy - templates and configuration",
	long_description="""\
	""",
	classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
	keywords='',
	author='Mandana Moshrefzadeh',
	author_email='mandana.moshrefzadeh.com',
	url='',
	license='Affero General Public License (AGPL)',
	packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
	namespace_packages=['ckanext', 'ckanext.grouphierarchy'],
	include_package_data=True,
	zip_safe=False,
	install_requires=[
		# -*- Extra requirements: -*-
	],
	entry_points=\
	"""
        [ckan.plugins]
        display_group=ckanext.grouphierarchy.plugin:HierarchyDisplay
        form_group=ckanext.grouphierarchy.plugin:HierarchyForm
	""",
)
