from flask_restx import Namespace, Resource, fields
<<<<<<< HEAD
=======
from flask_jwt_extended import jwt_required, get_jwt
>>>>>>> 79c8a994356ac45caeae564088e16f54114a8726
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

@api.route('/')
class AmenityList(Resource):
    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        amenities = facade.get_all_amenities()
        return [amenity.to_dict() for amenity in amenities], 200

    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
<<<<<<< HEAD
    def post(self):
        """Register a new amenity"""
=======
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def post(self):
        """Register a new amenity (admin only)"""
        if not get_jwt().get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403

>>>>>>> 79c8a994356ac45caeae564088e16f54114a8726
        amenity_data = api.payload
        try:
            new_amenity = facade.create_amenity(amenity_data)
            return new_amenity.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return amenity.to_dict(), 200

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
<<<<<<< HEAD
    def put(self, amenity_id):
        """Update an amenity's information"""
=======
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def put(self, amenity_id):
        """Update an amenity's information (admin only)"""
        if not get_jwt().get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403

>>>>>>> 79c8a994356ac45caeae564088e16f54114a8726
        amenity_data = api.payload
        try:
            updated_amenity = facade.update_amenity(amenity_id, amenity_data)
            if not updated_amenity:
                return {'error': 'Amenity not found'}, 404
            return updated_amenity.to_dict(), 200
        except ValueError as e:
            return {'error': str(e)}, 400