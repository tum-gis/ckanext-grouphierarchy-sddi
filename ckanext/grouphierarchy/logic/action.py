import logging

import ckan.plugins as p
import ckan.logic as logic
import ckan.model as model
from ckanext.grouphierarchy.model import GroupTreeNode_g

log = logging.getLogger(__name__)
_get_or_bust = logic.get_or_bust


@logic.side_effect_free
def group_tree_g(context, data_dict):
    '''Returns the full group tree hierarchy.

    :returns: list of top-level GroupTreeNodes
    '''
    group_type = data_dict.get('type', 'group')
    return [_group_tree_branch_g(group, type=group_type)
            for group in model.Group.get_top_level_groups(type=group_type)]


@logic.side_effect_free
def group_tree_section_g(context, data_dict):
    '''Returns the section of the group tree hierarchy which includes the given
    group, from the top-level group downwards.

    :param id: the id or name of the group to include in the tree
    :param include_parents: if false, starts from given group
    :returns: the top GroupTreeNode of the tree section

    '''
    group = _group_tree_check_g(data_dict)
    if not data_dict.get('include_parents', True):
        root_group = group
    else:
        root_group = (group.get_parent_group_hierarchy(type=group.type) or [group])[0]
    return _group_tree_branch_g(root_group, highlight_group_name=group.name,
                              type=group.type)

@logic.side_effect_free
def group_tree_children_g(context, data_dict):
    '''Returns a flat list of groups of the children of the group
    identified by parameter id in data_dict.

    :param id: the id or name of the parent group.
    :param type: "group"
    :returns: list of children GroupTreeNodes

    '''
    root_group = _group_tree_check_g(data_dict)
    children = root_group.get_children_group_hierarchy(type=root_group.type)
    children = [{'id': id, 'name': name, 'title': title}
                for id, name, title, _ in children]
    return children


def _group_tree_check_g(data_dict):
    group_name_or_id = _get_or_bust(data_dict, 'id')
    group = model.Group.get(group_name_or_id)
    if group is None:
        raise p.toolkit.ObjectNotFound
    group_type = data_dict.get('type', 'groups')
    if group.type != group_type:
        how_type_was_set = ('was specified' if data_dict.get('type')
                            else 'is filtered by default')
        raise p.toolkit.ValidationError(
            'Group type is "{}" not "{}" that {}'
            .format(group.type, group_type, how_type_was_set))
    return group
    
def _group_tree_branch_g(root_group, highlight_group_name=None, type='groups'):
    '''Returns a branch of the group tree hierarchy, rooted in the given group.

    :param root_group: group object at the top of the part of the tree
    :param highlight_group_name: group name that is to be flagged 'highlighted'
    :returns: the top GroupTreeNode of the tree
    '''
    nodes = {}  # group_id: GroupTreeNode()
    root_node = nodes[root_group.id] = GroupTreeNode_g(
        {'id': root_group.id,
         'name': root_group.name,
         'title': root_group.title})
    if root_group.name == highlight_group_name:
        nodes[root_group.id].highlight_g()
        highlight_group_name = None
    for group_id, group_name, group_title, parent_id in \
            root_group.get_children_group_hierarchy(type=type):
        node = GroupTreeNode_g({'id': group_id,
                              'name': group_name,
                              'title': group_title})
        nodes[parent_id].add_child_node_g(node)
        if highlight_group_name and group_name == highlight_group_name:
            node.highlight_g()
        nodes[group_id] = node
    return root_node
