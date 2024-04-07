from flask import Blueprint

from ..controllers.img_controller import imgController

img_bp = Blueprint('img_bp', __name__)

img_bp.route('/', methods=['POST'])(imgController.upload_image) 
img_bp.route('/<descripcion>', methods=['GET'])(imgController.get) 
img_bp.route('/crear', methods=['POST'])(imgController.create) 
img_bp.route('/<descripcion>', methods=['DELETE'])(imgController.delete) 
