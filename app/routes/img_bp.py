from flask import Blueprint

from ..controllers.img_controller import imgController

img_bp = Blueprint('img_bp', __name__)

img_bp.route('/', methods=['POST'])(imgController.upload_image) 
img_bp.route('/<int:idhuertas>', methods=['GET'])(imgController.get_by_huerta) 
img_bp.route('/crear/<int:idhuertas>', methods=['POST'])(imgController.create) 
img_bp.route('/<int:idimagen>', methods=['DELETE'])(imgController.delete) 
