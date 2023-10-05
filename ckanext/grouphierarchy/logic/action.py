import logging
import json

import ckan.plugins as p
import ckan.logic as logic
import ckan.model as model
import ckan.plugins.toolkit as tk
import ckan.logic.schema as schema_


log = logging.getLogger(__name__)

_get_or_bust = logic.get_or_bust


@logic.side_effect_free
def group_tree_children_g(context, data_dict):
    """Returns a flat list of groups of the children of the group
    identified by parameter id in data_dict.

    :param id: the id or name of the parent group.
    :param type: "group"
    :returns: list of children GroupTreeNodes

    """
    root_group = _group_tree_check_g(data_dict)
    children = root_group.get_children_group_hierarchy(type=root_group.type)
    children = [
        {"id": id, "name": name, "title": title} for id, name, title, _ in children
    ]
    return children


def _group_tree_check_g(data_dict):
    group_name_or_id = _get_or_bust(data_dict, "id")
    group = model.Group.get(group_name_or_id)
    if group is None:
        raise p.toolkit.ObjectNotFound
    group_type = data_dict.get("type", "groups")
    if group.type != group_type:
        how_type_was_set = (
            "was specified" if data_dict.get("type") else "is filtered by default"
        )
        raise p.toolkit.ValidationError(
            'Group type is "{}" not "{}" that {}'.format(
                group.type, group_type, how_type_was_set
            )
        )
    return group


def user_create(context, data_dict):
    group_list = p.toolkit.get_action("group_list")({}, {})
    site_user = p.toolkit.get_action("get_site_user")({"ignore_auth": True}, {})
    user = logic.action.create.user_create(context, data_dict)

    role = p.toolkit.config.get("ckan.userautoadd.organization_role", "member")
    context["user"] = site_user.get("name")

    for group in group_list:
        try:
            p.toolkit.get_action("group_show")(
                context,
                {
                    "id": group,
                },
            )
        except logic.NotFound:
            return user

        p.toolkit.get_action("group_member_create")(
            context,
            {
                "id": group,
                "username": user["name"],
                "role": role,
            },
        )

    return user


@tk.chained_action
def user_update(next, context, data_dict):
    last_attempt_time = data_dict.get("last_attempt_time")
    if last_attempt_time:
        not_empty = tk.get_validator("not_empty")
        unicode_safe = tk.get_validator("unicode_safe")
        schema = context.get("schema") or schema_.default_update_user_schema()
        schema["last_attempt_time"] = [not_empty, unicode_safe]

        plugin_extras = {
            "sddi": {
                "last_attempt_time": json.dumps(
                    last_attempt_time, indent=4, sort_keys=True, default=str
                )
            }
        }

        data_dict = dict(data_dict, plugin_extras=plugin_extras)
        return next(context, data_dict)

    return next(context, data_dict)
