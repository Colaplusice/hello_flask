from flask import jsonify
from ..models.models import Comment
from . import api


@api.route("/comments/<int:id>")
def get_comment(id):
    comment = Comment.get_or_404(id)
    return jsonify(comment.to_json())
