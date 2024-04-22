from flask import Blueprint

from ..controllers.user_controller import userController

user_bp = Blueprint('user_bp', __name__)

user_bp.route('/<int:idhuertas>', methods=['GET'])(userController.get) #'/user'
user_bp.route('/<int:idhuertas>/<int:id_practica>', methods=['GET'])(userController.get_asistencia) #'/user/<int:id_usuario>'
user_bp.route('/crear/<int:idhuertas>', methods=['POST'])(userController.create) #'/user'
user_bp.route('/<int:id_usuario>/<int:id_practica>', methods=['POST'])(userController.asistencia) #'/user/<int:id_usuario>'
user_bp.route('/<int:id_usuario>', methods=['DELETE'])(userController.delete) #'/user/<int:id_usuario>'
user_bp.route('/login', methods=['POST'])(userController.login)
user_bp.route('/logout/<int:id_usuario>', methods=['POST'])(userController.logout)


