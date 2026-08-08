from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user')
})

user_create_model = api.inherit('UserCreate', user_model, {
    'password': fields.String(required=True, description='Password of the user'),
    'is_admin': fields.Boolean(description='Whether the new user is an admin', default=False)
})

user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(description='Email of the user (admin only)'),
    'password': fields.String(description='Password of the user (admin only)')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_create_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def post(self):
        """Register a new user (admin only)"""
        if not get_jwt().get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403

        user_data = api.payload

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload
        
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        try:
            new_user = facade.create_user(user_data)
        except ValueError as e:
            return {'error': str(e)}, 400

        return {'id': new_user.id, 'message': 'User successfully created'}, 201

        user_payload = dict(user_data)
        if 'password' not in user_payload or not user_payload['password']:
            user_payload['password'] = 'default-password'

        try:
            new_user = facade.create_user(user_payload)
        except ValueError as e:
            return {'error': str(e)}, 400

        return {'id': new_user.id, 'first_name': new_user.first_name, 'last_name': new_user.last_name, 'email': new_user.email}, 201
    
    @api.response(200, 'List of users successfully retrieved')
    def get(self):
        """Retrieve a list of all users"""
        users = facade.get_users()
        return [{'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email} for user in users], 200

    
@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}, 200

    @api.expect(user_update_model, validate=True)
    @api.response(200, 'User successfully updated')
    @api.response(404, 'User not found')
    @api.response(403, 'Unauthorized action')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, user_id):
        """Update user information"""
        current_user_id = get_jwt_identity()
        is_admin = get_jwt().get('is_admin', False)

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        user_data = dict(api.payload)

        if not is_admin:
            if current_user_id != user_id:
                return {'error': 'Unauthorized action'}, 403
            if 'email' in user_data or 'password' in user_data:
                return {'error': 'You cannot modify email or password.'}, 400
        elif 'email' in user_data:
            existing_user = facade.get_user_by_email(user_data['email'])
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email already in use'}, 400

        new_password = user_data.pop('password', None)
        try:
            facade.update_user(user_id, user_data)
            if new_password:
                user.hash_password(new_password)
            return {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}, 200
        except ValueError as e:
            return {'error': str(e)}, 400
    
    @api.expect(user_model, validate=True)
    @api.response(200, 'User successfully updated')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    def put(self, user_id):
        """Update user information"""
        user_data = api.payload
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        try:
            updated_user = facade.update_user(user_id, user_data)
            return {'id': updated_user.id, 'first_name': updated_user.first_name, 'last_name': updated_user.last_name, 'email': updated_user.email}, 200
        except ValueError as e:
            return {'error': str(e)}, 400
            
