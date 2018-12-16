import os

from flask import url_for, request, current_app, Response

from hello_flask_app.models import View_message, User_message
from .. import main


# 每次请求前进行统计pv
@main.before_app_request
def get_user_message():
    if not request.url_rule:
        return
    if request.url_rule.endpoint != "static":
        view_data = {
            "url": request.url[:255],
            "ip": request.remote_addr,
            "referrer": request.referrer,
            "req_method": request.method,
            "end_point": request.url_rule.endpoint,
            "user_agent": request.user_agent,
        }
        user_data = {"ip": request.remote_addr}
        if view_data.get("user_agent"):
            User_message.create_or_update_from_request(user_data)
            View_message.create_from_request(view_data)


# @main.after_app_request
# def after_request(response):
#     print(response)
#     for query in get_debug_queries():
#         if query.duration >= current_app.config['FLASKY_SLOW_DB_QUERY_TIME']:
#             current_app.logger.warning(
#                 '缓慢的语句:%s\n 参数:%s\n 持续时长:%fs\n,内容:%s\n'
#                 % (query.statement, query.parameters, query.duration,
#                    query.context)
#             )
#     return response


@main.route("/all_visit")
def all_visit():
    all = View_message.query.count()
    return Response(str(all))


@main.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == "static":
        filename = values.get("filename", None)
        if filename:
            file_path = os.path.join(current_app.root_path, endpoint, filename)
            values["q"] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)
