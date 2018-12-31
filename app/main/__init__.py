from flask import Blueprint

from app.models.models import Permission

main = Blueprint("main", __name__)

from .views import user_view, errors_view


@main.app_context_processor
def inject_permission():
    return dict(Permisson=Permission)
