import os
import json
import click

import ckan.lib.navl.dictization_functions as dict_fns
import ckan.plugins.toolkit as tk
import ckan.model as model

from ckan.cli import error_shout


NotFound = tk.ObjectNotFound
NotAuthorized = tk.NotAuthorized
ValidationError = tk.ValidationError

HERE = os.path.dirname(__file__)
_site_url = tk.config.get('ckan.site_url')


@click.group("grouphierarchy", short_help="Grouphierarchy commands")
def grouphierarchy():
    pass


@grouphierarchy.command("init_data")
def init_data():
    print(_site_url)
    data = []
    # ckanext.grouphierarchy.init_data = example.json
    # make sure the .json file is inside grouphierarchy directory,
    # otherwise it won't work
    filepath = tk.config.get("ckanext.grouphierarchy.init_data", None)
    # if the .json file is not set in the .ini it would fall to the default one
    if not filepath:
        filepath = "init_data.json"

    with open(os.path.join(HERE, filepath), encoding='utf-8') as f:
        data = json.load(f)

    user = tk.get_action('get_site_user')({'ignore_auth': True})

    for group in data:
        context = {
            "model": model,
            "session": model.Session,
            "user": user['name'],
            "return_id_only": True
        }
        if group.get('image_url'):
            group['image_url'] = _site_url + group.get('image_url')
            print(group['image_url'])

        try:
            tk.get_action('group_create')(context, group)
        except (NotFound, NotAuthorized) as e:
            error_shout(e)
            raise click.Abort()
        except dict_fns.DataError:
            error_shout('Integrity Error')
            raise click.Abort()
        except ValidationError as e:
            error_shout(e)
            raise click.Abort()
    click.secho(
        "Successfully created the initial Groups",
        fg="green",
        bold=True
    )


def get_commands():
    return [grouphierarchy]
