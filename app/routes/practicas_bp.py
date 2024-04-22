from flask import Blueprint

from ..controllers.practicas_controller import practicasController

practicas_bp = Blueprint('practicas_bp', __name__)

practicas_bp.route('/<int:idhuertas>', methods=['GET'])(practicasController.get) 
practicas_bp.route('/crear/<int:idhuertas>', methods=['POST'])(practicasController.create) 
practicas_bp.route('/<int:idpractica>', methods=['PUT'])(practicasController.update)
practicas_bp.route('/<int:idpractica>', methods=['DELETE'])(practicasController.delete) 


