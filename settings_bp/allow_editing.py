from flask import Blueprint
import auth
import glb
import json

editing_allowed_bp = Blueprint('/allow_editing', __name__,)

@editing_allowed_bp.route("/", methods=['GET'])
@auth.is_authorized
def get_allowed_scopes():
    try:
        return json.dumps(glb.settings["editing_perm_scopes"])
    except Exception as e:
        return str(e), 500

@editing_allowed_bp.route("/", methods=['DELETE'])
@auth.is_authorized
@auth.is_teacher
def remove_all_scopes():
    try:
        glb.update_settings("editing_perm_scopes", [])
        return json.dumps(glb.settings["editing_perm_scopes"])
    except Exception as e:
        return str(e), 500

@editing_allowed_bp.route("/<scope>", methods=['PUT'])
@auth.is_authorized
@auth.is_teacher
def add_allowed_scope(scope):
    scope_to_add = "nbscmanlys-h:" + scope
    try:
        current_allowed_scopes = glb.settings["editing_perm_scopes"]
        if scope_to_add not in current_allowed_scopes:
            current_allowed_scopes.append(scope_to_add)
            glb.update_settings("editing_perm_scopes", current_allowed_scopes)
        return json.dumps(glb.settings["editing_perm_scopes"])
    except Exception as e:
        return str(e), 500

@editing_allowed_bp.route("/<scope>", methods=['DELETE'])
@auth.is_authorized
@auth.is_teacher
def remove_allowed_scope(scope):
    scope_to_add = "nbscmanlys-h:" + scope
    try:
        current_allowed_scopes = glb.settings["editing_perm_scopes"]
        if scope_to_add in current_allowed_scopes:
            current_allowed_scopes.remove(scope_to_add)
            glb.update_settings("editing_perm_scopes", current_allowed_scopes)
        return json.dumps(glb.settings["editing_perm_scopes"])
    except Exception as e:
        return str(e), 500