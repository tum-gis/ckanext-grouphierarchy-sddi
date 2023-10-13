import logging
import json
from datetime import datetime, timedelta

import ckan.plugins.toolkit as tk
from ckan.common import request


log = logging.getLogger(__name__)
_INTERVAL = int(tk.config.get("ckanext.sddi.last_attempt_time_interval", 60))


def user_cannot_send_reset(plugin_extras):
    if plugin_extras and "last_attempt_time" in plugin_extras["sddi"]:
        lst_att = json.loads(plugin_extras["sddi"]["last_attempt_time"])
        lst_att_obj = datetime.strptime(
            lst_att, "%Y-%m-%d %H:%M:%S.%f"
        )

        if datetime.now() - lst_att_obj < timedelta(seconds=_INTERVAL):
            return True

        return False


def ckanext_before_request():
    if request.endpoint == "user.request_reset" and request.method == "POST":
        id = request.form.get("user")
        site_user = tk.get_action("get_site_user")({"ignore_auth": True}, {})
        context = {"user": site_user["name"]}
        data_dict = {"id": id}

        if "@" in id:
            user_list = tk.get_action(u'user_list')(context, {
                u'email': id, "all_fields": False
            })
            if len(user_list) == 1:
                data_dict = {"id": user_list[0]}

        try:
            user_dict = tk.get_action("user_show")(
                context, dict(data_dict, include_plugin_extras=True)
            )
            if user_cannot_send_reset(user_dict["plugin_extras"]):
                return tk.abort(429)

            last_attempt_time = datetime.now()
            tk.get_action("user_update")(
                context, dict(user_dict, last_attempt_time=last_attempt_time)
            )
        except tk.ObjectNotFound:
            tk.abort(404, tk._("User not found"))
