import logging

import ckan.plugins as p

import ckanext.grouphierarchy.cli as cli
from ckanext.grouphierarchy.logic import action
from ckanext.grouphierarchy import helpers


log = logging.getLogger(__name__)

# This plugin is designed to work only these versions of CKAN
p.toolkit.check_ckan_version(min_version='2.0')


class HierarchySDDIDisplay(p.SingletonPlugin):
    p.implements(p.IConfigurer, inherit=True)
    p.implements(p.IActions, inherit=True)
    p.implements(p.ITemplateHelpers, inherit=True)
    p.implements(p.IPackageController, inherit=True)
    p.implements(p.IClick)


    # IConfigurer

    def update_config(self, config_):
        p.toolkit.add_template_directory(config_, 'templates')
        p.toolkit.add_public_directory(config_, 'public')
        p.toolkit.add_resource('public/scripts/vendor/jstree', 'jstree')
        p.toolkit.add_resource('fanstatic', 'grouphierarchy')

    # IActions

    def get_actions(self):
        return {
            "group_tree_children_g": action.group_tree_children_g,
            "user_create": action.user_create
            }

    def update_config_schema(self, schema):
        ignore_missing = p.toolkit.get_validator(u'ignore_missing')
        unicode_safe = p.toolkit.get_validator(u'unicode_safe')

        schema.update({
            u'ckan.site_intro_paragraph': [ignore_missing, unicode_safe],
            u'ckan.background_image': [ignore_missing, unicode_safe],
        })
        return schema

    # ITemplateHelpers

    def get_helpers(self):
        return {
            "get_selected_group": helpers.get_selected_group,
            "get_allowable_children_groups": helpers.get_allowable_children_groups,
            "get_group_image": helpers.get_group_image,
            "group_tree_crumbs": helpers.group_tree_crumbs,
            "group_tree_section_g": helpers.group_tree_section_g,
            "get_recently_modified_group": helpers.get_recently_modified_group
        }

    # IClick

    def get_commands(self):
        return cli.get_commands()
