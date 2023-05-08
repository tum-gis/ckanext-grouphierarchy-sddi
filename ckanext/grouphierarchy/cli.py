import os
import json
import click

import ckan.lib.navl.dictization_functions as dict_fns
import ckan.plugins.toolkit as tk
import ckan.model as model

from ckan.cli import error_shout

from ckanext.grouphierarchy.helpers import get_init_data


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

    data = get_init_data()
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
