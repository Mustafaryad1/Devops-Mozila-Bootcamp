import jwt
import datetime

from milestone import create_app as app, db, bcrypt

"""
    Models for Authentication and user management
"""
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    is_restaurant = db.Column(db.Boolean, nullable=False, default=False)
    auth = db.relationship('Auth', backref='user', uselist=False)
    logins_times = db.relationship('Logins', backref='user', uselist=False)
    restaurant = db.relationship('Restaurant', backref='user', uselist=False)
    orders = db.relationship('Order', backref='user')

    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e
    
    @staticmethod
    def decode_auth_token(auth_token):
        """
        Validates the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, config.get('SECRET_KEY'), algorithms =['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'
        
    def __repr__(self):
        return f"User('{self.username}', '{self.email}',)"


class Auth(db.Model):
    id =  db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
    hashed_password = db.Column(db.String(150), nullable=False)

    def __init__(self,user_id, password):
        self.user_id = user_id
        self.hashed_password = bcrypt.generate_password_hash(password).decode()
    
    @staticmethod
    def check_password(hashed_password, password):
        return bcrypt.check_password_hash(hashed_password, password)


class Logins(db.Model):
    id =  db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
    login_falid_times = db.Column(db.Integer, default=0)
    retry_time = db.Column(db.DateTime)


class Restaurant(db.Model):
    id =  db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
    menu = db.relationship('Menu', backref='restaurant', uselist=False)
    orders = db.relationship('Order', backref='restaurant')

    def to_json(self):
        data = {}
        data['restaurant_code'] = f'Restaurant #{self.id}'
        
        return data

class Menu(db.Model):
    id =  db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'),
        nullable=False)
    foods = db.relationship('Food', backref='menu')

    def to_json(self):
        data = {}
        data['restaurant'] = f'Restaurant#{self.restaurant_id}'
        data['foods'] = [item.to_json() for item in self.foods]

        return data

class Food(db.Model):
    id =  db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String(120), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'),
        nullable=False)
    order_item = db.relationship('OrderItem', backref='food')

    def to_json(self):
        data = {}
        data['name'] = self.name
        data['price'] = self.price
        
        return data

class OrderItem(db.Model):
    id =  db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'),
        nullable=False)
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'),
        nullable=False)
    quantity = db.Column(db.Integer,nullable=False)
    total_price = db.Column(db.Float, nullable=False)

    def to_json(self):
        data = {}
        data['food'] = self.food.name
        data['quantity'] = self.quantity
        data['total_price'] = self.total_price
        
        return data 

class Order(db.Model):
    id =  db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'),
        nullable=False)
    status = db.Column(db.Boolean, default=False)
    total_price = db.Column(db.Float, default=0.0, nullable=False)
    order_items = db.relationship('OrderItem', backref='menu')
    address = db.Column(db.String(120), nullable=False)

    def to_json(self):
        data = {}
        data['user'] = self.user.username
        data['order_items'] = [order_item.to_json() for order_item in self.order_items]
        data['total_price'] = self.total_price
        data['address'] = self.address
        data['status'] = "DELIVERED" if self.status else "PENDING"

        return data