import logging

import ckan.plugins as p
import ckan.logic as logic
import ckan.model as model


log = logging.getLogger(__name__)

_get_or_bust = logic.get_or_bust


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


def user_create(context, data_dict):

    group_list = p.toolkit.get_action('group_list')({}, {})
    site_user = p.toolkit.get_action('get_site_user')({'ignore_auth': True}, {})
    user = logic.action.create.user_create(context, data_dict)

    role = p.toolkit.config.get('ckan.userautoadd.organization_role', 'member')
    context['user'] = site_user.get('name')

    for group in group_list:
        try:
            p.toolkit.get_action('group_show')(
                context, {
                    'id': group,
                }
            )
        except logic.NotFound:
            return user

        p.toolkit.get_action('group_member_create')(
            context, {
                'id': group,
                'username': user['name'],
                'role': role,
            }
        )

    return user
