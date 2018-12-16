import celery


class Celery(celery.Celery):
    def init_app(self, app):
        self.config_from_object(app.config.get_namespace("CELERY_"))


#
# def buses_route(name, args, kwargs, options, task):
#     if name.startswith('buses.'):
#         hello_flask_app = get_current_app()
#         conf = hello_flask_app.config.get_namespace('CELERY_')
#         return {
#             'queue': conf['task_buses_queue'],
#             'exchange': conf['task_buses_exchange'],
#             'exchange_type': conf['task_buses_exchange_type'],
#             'routing_key': name
#         }
#     return None
