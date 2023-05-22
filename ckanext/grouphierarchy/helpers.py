import ckan.model as model

from ckan.plugins import toolkit as tk

from ckanext.hierarchy import helpers


# def groups():
#     query = model.Group.all(group_type='group')

#     def convert_to_dict(user):
#         out = {}
#         for k in ['id', 'name', 'title']:
#             out[k] = getattr(user, k)
#         return out

#     out = map(convert_to_dict, query.all())
#     return out


def group_tree_g(organizations=[], type_="groups"):
    full_tree_list = tk.get_action("group_tree_g")({}, {"type": type_})

    if not organizations:
        return full_tree_list
    else:
        filtered_tree_list = helpers.group_tree_filter(organizations, full_tree_list)
        return filtered_tree_list


def group_tree_section_g(id_, type_="groups", include_parents=True):
    return tk.get_action("group_tree_section")(
        {}, {"id": id_, "type": type_, "include_parents": include_parents}
    )


def group_tree_crumbs(id_):
    """Returns list of dicts with
      + either shortname (if available) or title (alternatively) and
      + id and
      + url
    for <id_> and all parents.

    """
    tree_node = tk.get_action("group_show")({}, {"id": id_})
    crumbs = [
        {
            "crumbname": tree_node.get("shortname") or tree_node.get("title"),
            "id": id_,
            "url": tk.url_for(controller="group", action="read", id=id_),
        }
    ]
    if tree_node["groups"]:
        id_parent = tree_node["groups"][0]["name"]
        return group_tree_crumbs(id_parent) + crumbs
    else:
        return crumbs


def get_allowable_children_groups(group_id):
    if group_id:
        group = model.Group.get(group_id)
        if group == None:
            return []
        allowable_parent_groups = group.get_children_group_hierarchy(type="group")
    else:
        allowable_parent_groups = model.Group.all(group_type="group")
    print(allowable_parent_groups)

    return allowable_parent_groups


def get_selected_group(groups, parent_group):
    """Return a list of groups selected for a datase."""

    group_list = get_allowable_children_groups(parent_group)

    group_name = []
    for gr in group_list:
        group_name.append(gr[1])

    category_gr = []
    for name in group_name:
        for selected_gr in groups:
            print(selected_gr)
            if selected_gr["name"] == name:
                # category_gr.append(selected_gr['title'])
                category_gr.append(selected_gr)

    return category_gr


def group_tree_get_longname_g(id_, default="", type_="groups"):
    tree_node = tk.get_action("group_show")({}, {"id": id_})
    longname = tree_node.get("longname", default)
    if not longname:
        return default
    return longname


def get_group_image(group_id):
    if group_id:
        group = model.Group.get(group_id)
        return group.image_url
    return


def get_recently_modified_group(_type):
    num = int(tk.config.get("ckanext.grouphierachy.homepage.group_show", 4))

    allowed_groups = get_names_in_main_category()
    action = f'{_type}_list'
    groups = tk.get_action(action)(
        {},
        {
            "type": _type,
            "sort": "package_count",
            "groups": allowed_groups,
        },
    )

    sorted_groups = []
    _groups = []
    if groups:
        for group in groups:
            groupobj = model.Session.query(model.Group).filter_by(name=group).first()
            _groups.append(groupobj)
        sorted_groups = sorted(
            _groups,
            key=lambda grp: [pkg.metadata_modified for pkg in grp.packages() if pkg],
            reverse=True,
        )
    return sorted_groups[:num]


def get_names_in_main_category():
    data = get_init_data()
    get_all_groups = [group for group in data if group.get('groups')]
    get_all_groups_in_main = (
        [group['name'] for group in get_all_groups 
        if group.get('groups')[0]['name'] == 'main-categories']
    )
    return get_all_groups_in_main


def get_init_data():
    import os
    import json

    HERE = os.path.dirname(__file__)
    # ckanext.grouphierarchy.init_data = example.json
    # make sure the .json file is inside grouphierarchy directory,
    # otherwise it won't work
    # if the .json file is not set in the .ini it would fall to the default one
    filepath = tk.config.get("ckanext.grouphierarchy.init_data", "init_data.json")
    with open(os.path.join(HERE, filepath), encoding='utf-8') as f:
        data = json.load(f)

    return data
