from .base import *
from .dev import *
from .production import *
from .test import *

config = {
    "development": DevelopementConfig,
    "testing": TestConfig,
    "production": ProductionConfig,
    "default": ProductionConfig,
}
