# ckanext-grouphierarchy
## Overview
This extension is based on the [ckanext-hierarchy](https://github.com/ckan/ckanext-hierarchy) extension.
The `ckanext-grouphierarchy-sddi` extension **requires** [ckanext-hierarchy](https://github.com/ckan/ckanext-hierarchy) extension. The `ckanext-grouphierarchy-sddi` extension is tested with v1.2.0 of the [ckanext-hierarchy](https://github.com/ckan/ckanext-hierarchy) extension.

The `ckanext-grouphierarchy` provides a new field on the group edit form to select a parent group. This new hierarchical arrangement of groups is displayed
using templates in this extension, instead of the usual list. An group
page also displays the section of the tree.
This version (0.2) of this extension also supports the group labeling on the dataset page and on the search page where the datasets are listed. Please note the labeling is only for the main group [id='main-categories'] including 9 sub-groups/children.

Forms (hierachy_form plugin):

* /group/new
* /group/edit/{id}

Templates (hierarchy_display plugin):

* /group - now shows the group hierarchy instead of list
* /group/about/{id} - now also shows the relevant part of the hierarchy

Please note that the categories of groups are hard coded.
github.com/tum-gis/ckanext-grouphierarchy-sddi/blob/master/ckanext/grouphierarchy/templates/group/snippets/group_list.html

Snippets (used by hierarchy_display and ckanext-scheming):

* /scheming/form_snippets/group_hierarchy.html

You can use this extension with CKAN as it is, enabling both plugins. Or if you
use an extension to customise the form already with an IGroupForm, then you
will want to only use the hierarchy_display plugin, and copy bits of the
hierarchy_form into your own. If you have your own templates then you can use
the snippets (or logic functions) that this extension provides to display the
trees.

In order to make hierarchy works with ckanext-scheming you need to enable just
hierarchy_display and then use corresponding form_snippet in your org_schema.
For example, you may add next field:

```json
{
    "field_name": "not_used",
    "label": "Parent group",
    "display_snippet": null,
    "form_snippet": "group_hierarchy.html",
    "validators": "ignore_missing"
}
```

New users are added automatically to the parent groups, which allows them to create datasets linked to these groups. Alls children groups are inherited from the parent groups.

## Functionality

### Main Categories and Topics

With the extension by default, it will be installed two parent Groups and their children groups:

* Main Category / Hauptkategorie:
  * Datensatz und Dokumente
  * Digitaler Zwilling
  * Geoobjekt
  * Gerät / Ding
  * Methode
  * Online-Anwendung
  * Online-Dienst
  * Projekt
  * Software
* Topics / Themen:
  * Arbeiten
  * Bauen
  * Bildung
  * Energie
  * Gesundheit
  * Gewerbe / Handwerk
  * Handel
  * Informations-Technologie
  * Kultur
  * Landwirtschaft
  * Mobilität
  * Stadtplanung
  * Tourismus & Freizeit
  * Umwelt
  * Verwaltung
  * Wohnen

The following image is showing how is it realized in the catalog.

![categorie-1](https://github.com/tum-gis/ckanext-grouphierarchy-sddi/assets/93824048/854d1a78-3bbf-42cf-b153-2225d59e28d4)

The `init_data.json` file is by default located in `ckanext-grouphierarchy-sddi/ckanext/grouphierarchy/` and this file is going to be used for installation of default main categories, topics, and organisations.
By default, there are 9 main categories, 16 topics and 18 Organizations. In the following `.json` file you can see default values:
`https://github.com/tum-gis/ckanext-grouphierarchy-sddi/blob/main/ckanext/grouphierarchy/init_data.json`.

The default 9 main categories and 16 topics are mandatory for SDDI and are the result of [long research](https://www.asg.ed.tum.de/en/gis/projects/smart-district-data-infrastructure/). They should not be changed when the catalog is used in SDDI context. Organisations can be modified. The default organizations defined in the file `init_data.json` are predefined within the [TwinBy project](https://twinby.bayern/de/startseite).

The file is possible to define in `production.ini` as a variable:

```text
ckanext.grouphierarchy.init_data=/path/to/init_data.json
```

The default setting is:

```text
ckanext.grouphierarchy.init_data=init_data.json
```

If the file is located in `ckanext-grouphierarchy-sddi/ckanext/grouphierarchy`, just the file name needs to be set, e.g.:

`ckanext-grouphierarchy-sddi/ckanext/grouphierarchy/my_init_data.json`:

```text
ckanext.grouphierarchy.init_data=my_init_data.json
```

The file can also be specified as an URL:

```text
ckanext.grouphierarchy.init_data=https://url/to/init_data.json
```

The `.json` file **must** have the following structure:

```json
{
    "groups": [
        {
            "title": "Hauptkategorien",
            "name": "main-categories"
        },
        {
            "title": "Category 1",
            "name": "category1",
            "groups": [
                {
                    "capacity": "public",
                    "name": "main-categories"
                }
            ]
        },
        {
            "title": "Themen",
            "name": "topics"
        },
        {
            "title": "Topic 1",
            "name": "topic1",
            "groups": [
                {
                    "capacity": "public",
                    "name": "topics"
                }
            ]
        }
    ],
    "organizations": [
        {
            "title": " Organisation",
            "name": "organisation"
        }
    ]
}
```

Personalized `.json` file **must contain** `"groups": [ "Hauptkategorien", "Themen" ]`. `"organizations": []` are optional.

To have parent/child relations between organizations, the structure must be as follows:

```json
{
    "organizations": [
        {
            "title": "Parent Organisation",
            "name": "parent-organisation",
            "image_url": "/base/images/organisation_icons/parent-organisation_logo.png"
        },
        {
            "title": "Child Organisation",
            "name": "child-organisation",
            "image_url": "/base/images/organisation_icons/child-organisation_logo.png",
            "groups": [
                {
                    "capacity": "public",
                    "name": "parent-organisation"
                }
            ]
        }
    ]
}
```

The values which have to be filled in have the following interpretation:

* `title` is presenting titel of the main category/topic/organisation which is going to be shown in the running instance

* `name` is defining the name od the main category/topic/organisation  which is going to be stored in database and for defyning URL of the dataset

* `image_url` is defining location where the logo of the main category/topic/organisation is. This is optional value.

* `"groups": [{"capacity": "public", "name": "parent-organisation"}]` - if the main category/topic/organisation needs to be defined as child, here should be defined parent `name`. This value is required only for parent-child relation.

The `init_data.json` is loaded at first initialization of a fresh instance. If is required to change values defined in `init_data.json` the "old" values should be first removed from the database.


### Main Page Personalization

The personalization of the SDDI CKAN catalog can be done either via variables or later in the running instance.

#### Personalisation via variables

The configuration which are enabling personalization should be added in the `production.ini`. For example:

```
ckan.site_intro_paragraph = "Here is example for Intro Paragraph"
ckan.background_image = ../base/images/hero.jpg
ckan.site_intro_text = "Here is example for Intro Text."
```

With the `ckan.site_intro_paragraph` is possible to define intro paragraph text on the main page, `ckan.background_image` is defining the background image on the main page, `ckan.site_intro_text` is defining the intro text on the main page.

![variables](https://github.com/tum-gis/ckanext-grouphierarchy-sddi/assets/93824048/4c309aa3-dd0d-4bdd-9b86-bf80ca916ce1)

If the configuration via variables is going to be used, the `ckan.background_image` can be defined ether as a path to the image or as URL.

#### Personalisation in the running instance

Only user with `admin` rights can change and apply perionalization settings.
This settings are possible to find in the `config` tab of `Systemadmin settings` (As shown in the following image).

![Personalisation](https://github.com/tum-gis/ckanext-grouphierarchy-sddi/assets/93824048/1df24bd5-a66d-4fd7-8195-6abcf0cf98d7)

As shown on the image, in In `config` tab is possible to change the Intro text on main page of your running instance (`Intro Text`), Paragraph under intro text on main page (`Intro Paragraph`) and to add or upload the background image in the main page (`Background image`).
If the (`Background image`) is not defined (as in this example), it will be used the `hero.jpg` image (`ckanext-grouphierarchy-sddi/ckanext/grouphierarchy/public/base/images/hero.jpg`).

By default, the intro text is defined as `ckan.site_intro_text="This is the intro to my CKAN instance."`. The `ckan.site_intro_paragraph` is not defined.
For background image  `hero.png` is used with the default location `https://github.com/tum-gis/ckanext-grouphierarchy-sddi/blob/main/ckanext/grouphierarchy/public/base/images/hero.jpg`
In the following image is possible to see the main page of one running instance with default settings.

![image](https://github.com/tum-gis/ckanext-grouphierarchy-sddi/assets/93824048/801a2685-9398-4f13-b881-a14a2eb25bb5)

### Personalization of the license list

The personalised SDDI licences list is by default located here: `ckanext-grouphierarchy-sddi/ckanext/grouphierarchy
/licenses_SDDI.json`. 

By default CKAN will use list of licenses avaliable [here](https://licenses.opendefinition.org/licenses/groups/ckan.json). 

To add personalised file to your CKAN instance `licenses_group_url` must be defined in production.ini file.

Example:

```
licenses_group_url = file:///path/to/my/local/json-list-of-licenses.json
licenses_group_url = http://licenses.opendefinition.org/licenses/groups/od.json
```
More informations about [Internationalisation Settings](https://docs.ckan.org/en/2.9/maintaining/configuration.html#internationalisation-settings) and `licenses_group_url` variable is possible to find in [official CKAN documentation](https://docs.ckan.org/en/2.9/maintaining/configuration.html#licenses-group-url).

### Compatibility

This extension has been tested with CKAN v2.8.0, CKAN v2.9.0 or later.

## Installation

Install the extension in your python environment.

```console
$ . /usr/lib/ckan/default/bin/activate
(pyenv) $ cd /usr/lib/ckan/default/src
(pyenv) $ pip install -e "git+https://tum-gis/ckanext-grouphierarchy-sddi.git#egg=ckanext-grouphierarchy-sddi"
```

Then change your CKAN ini file (e.g. development.ini or production.ini).  Note that display_group
should come before form_group

```text
ckan.plugins = stats text_view recline_view ... display_group
```

## Copyright & License
This module is Crown Copyright 2013 and openly licensed with AGPLv3 - see LICENSE file.

The `ckanext-grouphierarchy-sddi` extension is based on the [ckanext-hierarchy](https://github.com/ckan/ckanext-hierarchy) extension which is openly licensed with AGPLv3 and the Copyright belongs to commit authors.
