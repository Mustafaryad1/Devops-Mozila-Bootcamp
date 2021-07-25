import datetime

from flask import Blueprint, request, make_response, jsonify, redirect

from milestone import db
from milestone.models import Logins, Restaurant, Menu, User, Auth

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

@auth_blueprint.route('/login', methods=['POST'])
def login():
        # get the post data
        post_data = request.get_json()
        try:
            # fetch the user data
            user = User.query.filter_by(
                email=post_data.get('email')
            ).first()
            if user and user.auth.check_password(
                user.auth.hashed_password, post_data.get('password')):
                auth_token = user.encode_auth_token(user.id)
                
                if auth_token:
                    logins = Logins.query.filter_by(user_id=1).first()
                    if user.is_restaurant:
                        if logins:
                            now = datetime.datetime.now()
                            if logins.retry_time:
                                if now < logins.retry_time:
                                    response = {
                                    'status': 'fail',
                                    'message': f'Your account has been banned for {logins.retry_time - now }'
                                    }
                                    return make_response(jsonify(response)), 400
                        
                    response = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        'auth_token': auth_token
                    }
                    return make_response(jsonify(response)), 200
            else:
                if user.is_restaurant:
                    logins = Logins.query.filter_by(user_id=user.id).first()
                    if not logins:
                        logins = Logins(user_id=1,login_falid_times=1)
                    elif logins.login_falid_times < 2:
                        logins.login_falid_times +=1
                    elif logins.retry_time:
                        now = datetime.datetime.now()
                        if now < logins.retry_time:
                            response = {
                            'status': 'fail',
                            'message': f'Your account has been banned for {logins.retry_time - now }'
                            }
                            return make_response(jsonify(response)), 400
                        else:
                            logins.login_falid_times = 1
                            logins.retry_time = None    
                    else:
                        logins.retry_time = datetime.datetime.now() + datetime.timedelta(minutes=5)
                
                    db.session.add(logins)
                    db.session.commit()

                response = {
                    'status': 'fail',
                    'message': 'User does not exist.'
                }
                return make_response(jsonify(response)), 404
        except Exception as e:
            print(e)
            response = {
                'status': 'fail',
                'message': 'Try again'
            }
            return make_response(jsonify(response)), 500