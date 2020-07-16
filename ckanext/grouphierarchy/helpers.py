from ckan.plugins import toolkit as tk
import ckan.model as model

def groups():
    query = model.Group.all(group_type='group')

    def convert_to_dict(user):
        out = {}
        for k in ['id', 'name', 'title']:
            out[k] = getattr(user, k)
        return out

    out = map(convert_to_dict, query.all())
    return out
    

def group_tree_g(organizations=[], type_='groups'):
    full_tree_list = tk.get_action('group_tree_g')({}, {'type': type_})
    
    if not organizations:
        return full_tree_list
    else:
        filtered_tree_list = group_tree_filter_g(organizations, full_tree_list)
        return filtered_tree_list
	

def group_tree_section_g(id_, type_='groups', include_parents=True):
    return tk.get_action('group_tree_section_g')(
        {}, {'id': id_, 'type': type_, 'include_parents': include_parents})

def group_tree_crumbs_g(id_):
    ''' Returns list of dicts with
      + either shortname (if available) or title (alternatively) and
      + id and
      + url
    for <id_> and all parents.

    '''
    tree_node =  tk.get_action('group_show')({},{'id':id_})
    crumbs = [{'crumbname': tree_node.get('shortname') or tree_node.get('title'),
               'id': id_,
               'url': tk.url_for(controller='group',
                                 action='read', id=id_)}]
    if (tree_node['groups']):
        id_parent = tree_node['groups'][0]['name']
        return group_tree_crumbs_g(id_parent) + crumbs
    else:
        return(crumbs)

    
def get_allowable_parent_groups_g(group_id):
    if group_id:
        group = model.Group.get(group_id)
        allowable_parent_groups = group.groups_allowed_to_be_its_parent(type='group')
    else:
        allowable_parent_groups = model.Group.all(
            group_type='group')
    return allowable_parent_groups



def get_allowable_children_groups_g(group_id):
    if group_id:
        group = model.Group.get(group_id)
        allowable_parent_groups = group.get_children_group_hierarchy_g(type='group')
    else:
        allowable_parent_groups = model.Group.all(
            group_type='group')
    print(allowable_parent_groups)

    return allowable_parent_groups



# Helper function from
# https://github.com/datagovuk/ckanext-dgu/blob/5fb78b354517c2198245bdc9c98fb5d6c82c6bcc/ckanext/dgu/lib/helpers.py
# for speedier rendering of organization-tree



def group_tree_filter_g(organizations, group_tree_list, highlight=False):
    # this method leaves only the sections of the tree corresponding to the list
    # since it was developed for the users, all children organizations from the 
    # organizations in the list are included
    def traverse_select_highlighted_g(group_tree, selection=[], highlight=False):
        # add highlighted branches to the filtered tree
        if group_tree['highlighted']:
            # add to the selection and remove highlighting if necessary
            if highlight:
                selection += [group_tree]
            else:
                selection += group_tree_highlight([], [group_tree])
        else:
            # check if there is any highlighted child tree
            for child in group_tree.get('children', []):
                traverse_select_highlighted_g(child, selection)

    filtered_tree=[]
    # first highlights all the organizations from the list in the three
    for group in group_tree_highlight(organizations, group_tree_list):
        traverse_select_highlighted_g(group, filtered_tree, highlight)

    return filtered_tree


def get_selected_group (groups, parent_group):
    '''Return a list of groups selected for a datase.'''
    
    group_list = get_allowable_children_groups_g(parent_group)
    
    group_name = []
    for gr in group_list:
        group_name.append(gr[1])
    
    category_gr = []    
    for name in group_name:
        for selected_gr in groups:
            print(selected_gr)
            if selected_gr['name'] == name:
               #category_gr.append(selected_gr['title'])
               category_gr.append(selected_gr)

    return category_gr


def group_tree_get_longname_g(id_, default="", type_='groups'):
     tree_node =  tk.get_action('group_show')({},{'id':id_})
     longname = tree_node.get("longname", default)
     if not longname:
         return default
     return longname


def group_tree_highlight_g(organizations, group_tree_list):

    def traverse_highlight_g(group_tree, name_list):
        if group_tree.get('name', "") in name_list:
            group_tree['highlighted'] = True
        else:
            group_tree['highlighted'] = False
        for child in group_tree.get('children', []):
            traverse_highlight_g(child, name_list)

    selected_names = [ o.get('name',None) for o in organizations]

    for group in group_tree_list:
        traverse_highlight_g(group, selected_names)
    return group_tree_list


