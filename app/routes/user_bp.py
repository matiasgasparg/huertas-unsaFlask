from flask import Blueprint

from ..controllers.user_controller import userController

user_bp = Blueprint('user_bp', __name__)

user_bp.route('/', methods=['GET'])(userController.get_all) #'/user'
user_bp.route('/<int:id_usuario>', methods=['GET'])(userController.get) #'/user/<int:id_usuario>'
user_bp.route('/crear', methods=['POST'])(userController.create) #'/user'
user_bp.route('/<int:id_usuario>', methods=['PUT'])(userController.update) #'/user/<int:id_usuario>'
user_bp.route('/<int:id_usuario>', methods=['DELETE'])(userController.delete) #'/user/<int:id_usuario>'
user_bp.route('/login', methods=['POST'])(userController.login)
user_bp.route('/logout/<int:id_usuario>', methods=['POST'])(userController.logout)


