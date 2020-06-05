import ckan.plugins as p
from ckanext.grouphierarchy.logic import action
from ckanext.grouphierarchy import helpers
from ckan.lib.plugins import DefaultGroupForm
import ckan.plugins.toolkit as tk
from lucparser import LucParser
import re
import logging
import pdb

log = logging.getLogger(__name__)

# This plugin is designed to work only these versions of CKAN
p.toolkit.check_ckan_version(min_version='2.0')


class HierarchyDisplay(p.SingletonPlugin):

    p.implements(p.IConfigurer, inherit=True)
    p.implements(p.IActions, inherit=True)
    p.implements(p.ITemplateHelpers, inherit=True)
    p.implements(p.IPackageController, inherit=True)

    # IConfigurer
    def update_config(self, config):
        p.toolkit.add_template_directory(config, 'templates')
        p.toolkit.add_template_directory(config, 'public')
        p.toolkit.add_resource('public/scripts/vendor/jstree', 'jstree')
        p.toolkit.add_resource('fanstatic', 'grouphierarchy')

    # IActions
    def get_actions(self):
        return {'group_tree_g': action.group_tree_g,
                'group_tree_section_g': action.group_tree_section_g,
                'group_tree_children_g':action.group_tree_children_g
                }

    # ITemplateHelpers
    def get_helpers(self):
        return {'groups': helpers.groups,
	           'group_tree_g': helpers.group_tree_g,
                'group_tree_section_g': helpers.group_tree_section_g,
                'group_tree_crumbs_g': helpers.group_tree_crumbs_g,
                'get_allowable_parent_groups_g': helpers.get_allowable_parent_groups_g,
		'group_tree_get_longname_g': helpers.group_tree_get_longname_g,
                'group_tree_highlight_g': helpers.group_tree_highlight_g,
		'get_allowable_children_groups_g': helpers.get_allowable_children_groups_g,
                }

    # IPackageController
    # Modify the search query to include the datasets from
    # the children organizations in the result list
    # HvW: Do this always
    def before_search(self, search_params):
        ''' If include children selected the query string is modified '''

        def _get_organizations_from_subquery_g(subquery):
            patall = '"?([\w-]+)"?'
            patwrong = 'AND|OR|NOT'
            patnot = 'NOT\s+("?([\w-]+)"?)'
            parentorgs = set(re.findall(patall, subquery))
            parentwrong = set(re.findall(patwrong, subquery))
            parentnot = set(re.findall(patnot, subquery))
            parentorgs = list(parentorgs - parentwrong - parentnot)
            return parentorgs
            
        lp = LucParser()
        for qtyp in ['fq', 'q']:
            query = search_params.get(qtyp, None)
            if query:
                queryterms = lp.deparse(query)
                for i, q in enumerate(queryterms):
                    if not isinstance(q, dict):
                        continue
                    fieldname = q.get('field')
                    if fieldname not in [ 'groups']:
                        continue
                    parentgroups = _get_organizations_from_subquery_g(q.get('term'))
                    
                    children = [tk.get_action('group_tree_children_g')
                                ({}, data_dict={'id': p, 'type':'group'})
                                for p in parentgroups]
                    childlist = [c[{'groups':
                                    'name'}[fieldname]] 
                                 for child in children for c in child]
                    if childlist:
                        childsearch = ' OR ' + ' OR '.join(childlist)
                        search_params[qtyp] = lp.add_to_query(
                            search_params[qtyp],
                            childsearch, fieldname=fieldname)
        return search_params


class HierarchyForm(p.SingletonPlugin, DefaultGroupForm):

    p.implements(p.IGroupForm, inherit=True)

    # IGroupForm

    def group_types(self):
        return ('group',)

    def group_controller(self):
        return 'group'

    def setup_template_variables(self, context, data_dict):
        from pylons import tmpl_context as c
        model = context['model']
        group_id = data_dict.get('id')
        c.allowable_parent_groups_g = helpers.get_allowable_parent_groups_g(group_id)
