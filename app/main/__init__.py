from flask import Blueprint

from ..models import Permisson
main=Blueprint('main',__name__)

from . import views,errors

@main.app_context_processor
def inject_permission():
    return dict(Permisson=Permisson)
