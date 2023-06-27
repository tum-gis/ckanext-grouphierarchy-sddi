import logging
import six
import time

import ckan.plugins as p
import ckan.logic as logic
import ckan.model as model
import ckan.lib.uploader as uploader
import ckan.lib.helpers as h
import ckan.lib.app_globals as app_globals
import ckan.lib.navl.dictization_functions as dfunc

from ckan.common import config


log = logging.getLogger(__name__)

_check_access = logic.check_access
_get_or_bust = logic.get_or_bust
_validate = dfunc.validate


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


def config_option_update(context, data_dict):

    model = context['model']

    _check_access('config_option_update', context, data_dict)

    schema = logic.schema.update_configuration_schema()

    available_options = schema.keys()

    provided_options = data_dict.keys()

    unsupported_options = set(provided_options) - set(available_options)
    if unsupported_options:
        msg = 'Configuration option(s) \'{0}\' can not be updated'.format(
              ' '.join(list(unsupported_options)))

        raise logic.ValidationError(msg, error_summary={'message': msg})

    if data_dict['logo_upload'] or data_dict['clear_logo_upload']:
        upload = uploader.get_uploader('admin')
        upload.update_data_dict(data_dict, 'ckan.site_logo',
                                'logo_upload', 'clear_logo_upload')
        upload.upload(uploader.get_max_image_size())

    if data_dict['image_upload'] or data_dict['clear_image_upload']:
        upload_ = uploader.get_uploader('admin')
        upload_.update_data_dict(data_dict, 'ckan.background_image',
                                'image_upload', 'clear_image_upload')
        upload_.upload(uploader.get_max_image_size())
    
    data, errors = _validate(data_dict, schema, context)
    if errors:
        model.Session.rollback()
        raise logic.ValidationError(errors)

    for key, value in six.iteritems(data):

        # Set full Logo url
        if key in ['ckan.site_logo', 'ckan.background_image'] and value and not value.startswith('http')\
                and not value.startswith('/'):
            image_path = 'uploads/admin/'

            value = h.url_for_static('{0}{1}'.format(image_path, value))

        # Save value in database
        model.set_system_info(key, value)

        # Update CKAN's `config` object
        config[key] = value

        # Only add it to the app_globals (`g`) object if explicitly defined
        # there
        globals_keys = app_globals.app_globals_from_config_details.keys()
        if key in globals_keys:
            app_globals.set_app_global(key, value)

    # Update the config update timestamp
    model.set_system_info('ckan.config_update', str(time.time()))

    log.info('Updated config options: {0}'.format(data))

    return data
