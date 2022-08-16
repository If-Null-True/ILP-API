from flask import Blueprint
from settings_bp import allow_editing

settings_bp = Blueprint('/settings', __name__,)

settings_bp.register_blueprint(allow_editing.editing_allowed_bp, url_prefix='/allow_editing')