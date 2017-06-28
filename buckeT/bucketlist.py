from flask import Flask, jsonify
from flask_restful import Resource, reqparse
from database_models import User, BucketList, BucketListItem
from buckeT import db, app
from flask_jwt_extended import create_access_token, jwt_required
import re


class RegisterUser(Resource):
    """register a new user to the database"""

    def post(self):
        """post method for passing user credentials to the request"""
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('first_name', required=True, type=str, help='please enter your first name.')
            parser.add_argument('second_name', required=True, type=str, help='please enter your second name.')
            parser.add_argument('email', required=True, type=str, help='please enter an email address.')
            parser.add_argument('password', required=True, type=str, help='please enter a password.')
            args = parser.parse_args()
            if not args['first_name']:
                return {'message': 'First name should not be empty!'}
            if not args['second_name']:
                return {'message': 'Second name should not be empty!'}
            if not args['email']:
                return {'message': 'Email should not be empty!'}
            if not args['password']:
                return {'message': 'Password should not be empty!'}
            if len(args['password']) < 8:
                return {'message': "Password should be longer than 8 characters!"}
            new_user = User(first_name=args['first_name'], second_name=args['second_name'], email=args['email'], password=args['password'])

            if User.query.filter_by(email=args['email']).first():
                return {'message': 'User you are entering already exists!'}, 409
            else:
                if (re.match('[a-zA-Z]', args['first_name']) and re.match('[a-zA-Z]', args['second_name'])):
                    new_user.save()
                    return {'message': 'Sucessfully registered new user!'}, 201
                else:
                    return {'message': 'first name or second name can not contain special characters or numbers!'}, 409

        except:
            return {'message': 'User not registered due to errors!'}, 400


if __name__ == '__main__':
    app.run(debug=True)