from app.api import api
from app.api.users import RoleView

api.add_url_rule("/roles", view_func=RoleView.as_view(name="roles"), methods=["GET"])
