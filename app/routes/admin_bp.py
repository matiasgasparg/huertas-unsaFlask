from flask import Blueprint

from ..controllers.admin_controller import adminController

admin_bp = Blueprint('admin_bp', __name__)

admin_bp.route('/', methods=['POST'])(adminController.login) #'/user'


