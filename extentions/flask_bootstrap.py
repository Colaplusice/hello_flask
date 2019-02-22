from wtforms import HiddenField


class Bootstrap:
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.jinja_env.globals['bootstrap_is_hidden_field'] = \
            self.is_hidden_field_filter

    def is_hidden_field_filter(self, field):
        return isinstance(field, HiddenField)
