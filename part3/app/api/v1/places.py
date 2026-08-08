from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('places', description='Place operations')

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'amenities': fields.List(fields.String, description="List of amenities ID's")
})


place_update_model = api.model('PlaceUpdate', {
    'title': fields.String(description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(description='Price per night'),
    'latitude': fields.Float(description='Latitude of the place'),
    'longitude': fields.Float(description='Longitude of the place'),
    'amenities': fields.List(fields.String, description="List of amenities ID's")
})

place_amenities_model = api.model('PlaceAmenities', {
    'amenities': fields.List(fields.String, required=True, description="List of amenity IDs to add")
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Create a new place"""
        current_user = get_jwt_identity()
        place_data = dict(api.payload)
        place_data['owner_id'] = current_user

        try:
            new_place = facade.create_place(place_data)
            return new_place.to_dict(), 201
        except (ValueError, TypeError, KeyError) as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        return [place.to_dict() for place in places], 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return place.to_dict(), 200

    @api.expect(place_update_model, validate=True)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(403, 'Unauthorized action')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, place_id):
        """Update a place's information"""
        current_user = get_jwt_identity()
        is_admin = get_jwt().get('is_admin', False)
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        if not is_admin and place.owner_id != current_user:
            return {'error': 'Unauthorized action'}, 403

        place_data = api.payload
        try:
            facade.update_place(place_id, place_data)
            return {'message': 'Place updated successfully'}, 200
        except (ValueError, TypeError) as e:
            return {'error': str(e)}, 400

@api.route('/<place_id>/amenities')
class PlaceAmenities(Resource):
    @api.expect(place_amenities_model, validate=True)
    @api.response(200, 'Amenities added successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self, place_id):
        """Add amenities to a place"""
        current_user = get_jwt_identity()
        is_admin = get_jwt().get('is_admin', False)

        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        if not is_admin and place.owner_id != current_user:
            return {'error': 'Unauthorized action'}, 403

        amenity_ids = api.payload.get('amenities', [])
        if not amenity_ids:
            return {'error': 'Invalid input data'}, 400

        try:
            for amenity_id in amenity_ids:
                facade.add_amenity_to_place(place_id, amenity_id)
        except KeyError as e:
            return {'error': str(e)}, 400

        return {'message': 'Amenities added successfully'}, 200

@api.route('/<place_id>/reviews/')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return [review.to_dict() for review in place.reviews], 200
