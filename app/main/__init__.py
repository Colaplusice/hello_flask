from flask import Blueprint

from ..models.models import Permisson

main = Blueprint('main', __name__)


@main.app_context_processor
def inject_permission():
    return dict(Permisson=Permisson)
