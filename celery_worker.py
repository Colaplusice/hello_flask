import os
from hello_flask_app import celery, create_app

app = create_app(os.getenv("FLASK_CONFIG") or "default")
app.app_context().push()
