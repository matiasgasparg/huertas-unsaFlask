from flask import Blueprint

from ..controllers.noticia_controller import notController

not_bp = Blueprint('not_bp', __name__)

not_bp.route('/', methods=['GET'])(notController.get_all) 
not_bp.route('/<int:idnoticias>', methods=['GET'])(notController.get) 
not_bp.route('/crear', methods=['POST'])(notController.create) 
not_bp.route('/<int:idnoticias>', methods=['PUT'])(notController.update)
not_bp.route('/<int:idnoticias>', methods=['DELETE'])(notController.delete) 


