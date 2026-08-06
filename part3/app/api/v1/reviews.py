from flask_restx import Namespace, Resource, fields
<<<<<<< HEAD
=======
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
>>>>>>> 79c8a994356ac45caeae564088e16f54114a8726
from app.services import facade

api = Namespace('reviews', description='Review operations')

<<<<<<< HEAD
# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new review"""
        review_data = api.payload
        place = facade.get_place(review_data['place_id'])
        if not place:
            return {'error': 'Place not found'}, 400
        user = facade.get_user(review_data['user_id'])
        if not user:
            return {'error': 'User not found'}, 400
        if place.owner.id == user.id:
            return {'error': 'User cannot review their own place'}, 400
        try:
            new_review = facade.create_review(review_data)
            return new_review.to_dict(), 201
        except Exception as e:
=======
# Model used to create a review. user_id is not accepted here - it is
# derived from the authenticated user's JWT identity.
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'place_id': fields.String(required=True, description='ID of the place')
})

# Model used to update a review. All fields optional to support partial updates.
review_update_model = api.model('ReviewUpdate', {
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new review"""
        current_user = get_jwt_identity()
        review_data = dict(api.payload)

        place = facade.get_place(review_data.get('place_id'))
        if not place:
            return {'error': 'Place not found'}, 400

        if place.owner_id == current_user:
            return {'error': 'You cannot review your own place.'}, 400

        if any(review.user_id == current_user for review in place.reviews):
            return {'error': 'You have already reviewed this place.'}, 400

        review_data['user_id'] = current_user
        try:
            new_review = facade.create_review(review_data)
            return new_review.to_dict(), 201
        except (ValueError, TypeError, KeyError) as e:
>>>>>>> 79c8a994356ac45caeae564088e16f54114a8726
            return {'error': str(e)}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        return [review.to_dict() for review in facade.get_all_reviews()], 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return review.to_dict(), 200

<<<<<<< HEAD
    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        review_data = api.payload
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        
        try:
            facade.update_review(review_id, review_data)
            return {'message': 'Review updated successfully'}, 200
        except Exception as e:
=======
    @api.expect(review_update_model, validate=True)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(403, 'Unauthorized action')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, review_id):
        """Update a review's information"""
        current_user = get_jwt_identity()
        is_admin = get_jwt().get('is_admin', False)
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        if not is_admin and review.user_id != current_user:
            return {'error': 'Unauthorized action'}, 403

        review_data = api.payload
        try:
            facade.update_review(review_id, review_data)
            return {'message': 'Review updated successfully'}, 200
        except (ValueError, TypeError) as e:
>>>>>>> 79c8a994356ac45caeae564088e16f54114a8726
            return {'error': str(e)}, 400

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
<<<<<<< HEAD
    def delete(self, review_id):
        """Delete a review"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        
=======
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        current_user = get_jwt_identity()
        is_admin = get_jwt().get('is_admin', False)
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        if not is_admin and review.user_id != current_user:
            return {'error': 'Unauthorized action'}, 403

>>>>>>> 79c8a994356ac45caeae564088e16f54114a8726
        try:
            facade.delete_review(review_id)
            return {'message': 'Review deleted successfully'}, 200
        except Exception as e:
<<<<<<< HEAD
            return {'error': str(e)}, 400
=======
            return {'error': str(e)}, 400
>>>>>>> 79c8a994356ac45caeae564088e16f54114a8726
