from flask import Blueprint
from flask_restx import Api

from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns

blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(blueprint, version='1.0', title='HBnB API', description='HBnB Application API')

api.add_namespace(users_ns, path='/users')
api.add_namespace(amenities_ns, path='/amenities')