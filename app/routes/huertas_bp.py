from flask import Blueprint

from ..controllers.huertas_controller import huertasController

huertas_bp = Blueprint('huertas_bp', __name__)

huertas_bp.route('/', methods=['GET'])(huertasController.get_all) 
huertas_bp.route('/<int:idhuertas>', methods=['GET'])(huertasController.get) 
huertas_bp.route('/crear', methods=['POST'])(huertasController.create) 
huertas_bp.route('/<int:idhuertas>', methods=['PUT'])(huertasController.update)
huertas_bp.route('/<int:idhuertas>', methods=['DELETE'])(huertasController.delete) 



