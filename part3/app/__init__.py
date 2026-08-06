from flask import Flask, redirect
from flask_restx import Api
<<<<<<< HEAD
=======
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

jwt = JWTManager()
bcrypt = Bcrypt()

>>>>>>> 79c8a994356ac45caeae564088e16f54114a8726
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
<<<<<<< HEAD


def create_app():
    app = Flask(__name__)
=======
from app.api.v1.auth import api as auth_ns


def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)
    jwt.init_app(app)
    bcrypt.init_app(app)
>>>>>>> 79c8a994356ac45caeae564088e16f54114a8726
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='Swagger documentation for the HBnB application APIs',
        doc='/docs'
    )

    api.add_namespace(users_ns, path='/api/v1/users/')
    api.add_namespace(amenities_ns, path='/api/v1/amenities/')
    api.add_namespace(places_ns, path='/api/v1/places/')
    api.add_namespace(reviews_ns, path='/api/v1/reviews/')
<<<<<<< HEAD
=======
    api.add_namespace(auth_ns, path='/api/v1/auth/')
>>>>>>> 79c8a994356ac45caeae564088e16f54114a8726

    def index():
        return redirect('/docs')

    app.view_functions['root'] = index

    return app