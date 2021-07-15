from flask import Blueprint, request, make_response, jsonify, redirect

from milestone import db
from milestone.models import Restaurant, Menu, User, Auth

auth_blueprint = Blueprint('user', __name__, url_prefix='/user')

"""
    User Registration Resource
"""
@auth_blueprint.route('/register', methods=['POST'])
def register():
    # get the post data
    post_data = request.get_json()
    # check if user already exists
    
    if not post_data:
        response = {
                'status': 'fail',
                'message': 'Some error occurred. Please try again.'
            }
        return make_response(jsonify(response)), 401

    user = User.query.filter_by(email=post_data.get('email')).first()
    if not user:
        try:
            
            user = User(
                email=post_data.get('email'),
                username=post_data.get('username')
            )

            user_type = post_data.get('type')or 'user'
            if user_type.lower() == 'restaurant':
                user.is_restaurant = True
            elif user_type.lower() == 'admin':
                user.is_admin = True 
            
            # insert the user
            db.session.add(user)
            db.session.commit()

            auth = Auth(
                user_id=user.id,
                password=post_data.get('password')
            )

            db.session.add(auth)
            db.session.commit()
            # create restaurant data 
            restaurant = Restaurant(user_id=user.id)
            db.session.add(restaurant)
            db.session.commit()
            menu = Menu(restaurant_id=restaurant.id)
            db.session.add(menu)
            db.session.commit()
            # generate the auth token
            auth_token = user.encode_auth_token(user.id)
            response = {
                'status': 'success',
                'message': 'Successfully registered.',
                'auth_token': auth_token
            }
            return make_response(jsonify(response)), 201

        except Exception as e:
            print(e)
            response = {
                'status': 'fail',
                'message': 'Some error occurred. Please try again.'
            }
            return make_response(jsonify(response)), 401
    else:
        response = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return make_response(jsonify(response)), 202

