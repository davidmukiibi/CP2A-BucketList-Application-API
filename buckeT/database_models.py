from buckeT import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)


class User(db.Model):
    """Creating the users table. This table will hold all users in the system."""
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(32), nullable=False)
    second_name = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(32), nullable=False, unique=True)
    password_hash = db.Column(db.String, nullable=False, unique=True)
    bucketlist_name = db.relationship('BucketList', backref='Users', lazy='dynamic')


    # def generate_token(self, expiration = 600):
    #     s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
    #     return s.dumps({ 'id': self.id })

    # @staticmethod
    # def verify_token(token):
    #     s = Serializer(app.config['SECRET_KEY'])
    #     try:
    #         data = s.loads(token)
    #     except SignatureExpired:
    #         return None # valid token, but expired
    #     except BadSignature:
    #         return None # invalid token
    #     user = User.query.get(data['id'])
    #     return user


    @property
    def password(self):
        """Show an error message when a user tries to edit the password field in the database."""
        raise AttributeError('Password field is a write-only field, can not be changed!')

    @password.setter
    def password(self, password):
        """Creates a hashed password."""
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """Compare password hashes with that saved in the user table."""
        return check_password_hash(self.password_hash, password)


    def __repr__(self):
        return '<User {}>'.format(self.email)


    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete():
        db.session.delete()
        db.session.commit()

    def get_all():
        return User.query.all()


class BucketList(db.Model):
    """creating the bucketlists table. This table will hold all bucket lists created."""
    __tablename__ = 'bucketlists'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bucketlist_identifier = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(32), nullable=False, unique=True)
    date_created = db.Column(db.DateTime, default=db.func.now())
    date_modified = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    created_by = db.Column(db.String(30), db.ForeignKey('Users.email'))


    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<BucketList {}>'.format(self.name)

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete():
        db.session.delete()
        db.session.commit()

    def get_all():
        return Bucketlist.query.all()


class BucketListItem(db.Model):
    """Creating the Bucketlist Items table. This table will hold all items in all bucket lists."""
    __tablename__ = 'Bucketlist Items'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32), nullable=False)
    bucket_list_item_identifier = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.now())
    bucket_list_it_belongs_to = db.Column(db.String(30), db.ForeignKey('bucketlists.name'), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Bucket_list_Item {}>'.format(self.name)

    def save(self):
        db.session.add()
        db.session.commit()

    def delete():
        db.session.delete()
        db.session.commit()

    def get_all():
        return BucketListItem.query.all()

