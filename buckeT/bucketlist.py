from flask import Flask, jsonify, request, json
from flask_restful import Resource, reqparse
from database_models import User, BucketList, BucketListItem
from buckeT import db, app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import re

parser = reqparse.RequestParser()
parser.add_argument('q',type=str, help="Search word")
parser.add_argument('limit',type=int, help="Limit can only be a number")
parser.add_argument('page',type=int, help="Page value can only be a number")


class RegisterUser(Resource):
    """register a new user to the database"""

    def post(self):
        """post method for passing user credentials to the request"""
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('first_name', required=True, type=str,
                                help='please enter your first name.')
            parser.add_argument('second_name', required=True, type=str,
                                help='please enter your second name.')
            parser.add_argument('email', required=True, type=str,
                                help='please enter an email address.')
            parser.add_argument('password', required=True, type=str,
                                help='please enter a password.')
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
                return {
    'message': "Password should be longer than 8 characters!"}

            new_user = User(first_name=args['first_name'], second_name=args['second_name'],
                            email=args['email'], password=args['password'])

            if User.query.filter_by(email=args['email']).first():
                return {'message': 'User you are entering already exists!'}, 409

            else:
                if (re.match('[a-zA-Z]', args['first_name'])
                   and re.match('[a-zA-Z]', args['second_name'])):
                    new_user.save()
                    return {'message': 'Sucessfully registered new user!'}, 201
                else:
                    return {'message': 'first name or second name can not contain\
                                        special characters or numbers!'}, 409

        except:
            return {'message': 'User not registered due to errors!'}, 400

class LoginUser(Resource):
    """login a user"""

    def post(self):
        """Method is responsible for logging in a user."""

        parser = reqparse.RequestParser()
        parser.add_argument('email', required=True, type=str, help='please enter an email address!')
        parser.add_argument('password', required=True, type=str, help='please enter a password!')
        args = parser.parse_args()
        email, password = args['email'], args['password']
        user = User.query.filter_by(email=email).first()
        if user:
            if user.verify_password(password):
                token = {'access_token': create_access_token(identity=user.email)}
                return {'message': 'Successfully logged in', 'token': token }, 201
            else:
                return {'message': 'Wrong password!'}, 401
        else:
            return {'message': 'User does not exist!'}, 401

class SingleBucketlist(Resource):
    """Class responsible for fetching, editing and deleting a specific bucket
    list.
    """

    @jwt_required
    def get(self, ID):
        """method fetches a specific bucket list by its ID"""

        bucketlist = BucketList.query.filter_by(id=ID).first()
        if bucketlist:
            items = BucketListItem.query.filter_by(bucket_list_it_belongs_to=bucketlist.name).all()
            all_items = []
            for item in items:
                item_and_details = {
                    'id': item.id,
                    'name': item.name,
                    'date_created': item.date_created,
                    'date_modified': item.date_modified,
                    'done': False
                }
                all_items.append(item_and_details)

            bucket_and_details = {
                'id': bucketlist.id,
                'name': bucketlist.name,
                'items': all_items,
                'date_created': bucketlist.date_created,
                'date_modified': bucketlist.date_modified,
                'created_by': bucketlist.created_by
                }

            return jsonify({'bucket list': bucket_and_details}, 200)

        else:
            return {'message': 'No bucket list with that given ID.'}, 404

    @jwt_required
    def delete(self, ID):
        """Method deletes a specified bucket list"""

        bucketlist = BucketList.query.filter_by(id=ID).first()
        if bucketlist:
            bucketlist.delete()
            return {'message': 'Bucketlist deleted successfully'}, 200
        else:
            return {'message': 'No bucket list found with that ID'}, 404

    @jwt_required
    def put(self, ID):
        """Method edits a specified bucke list"""

        bucketlist = BucketList.query.filter_by(id=ID).first()
        if bucketlist:
            parser = reqparse.RequestParser()
            parser.add_argument('name', required=True, type=str,
                                help='please enter a bucket list name.')
            args = parser.parse_args()
            if args['name']:
                bucketlist.name = args['name']
                bucketlist.save()
                return {'message': 'Bucket list edit successful'}, 201

            else:
                return {'message': 'Please enter a name to replace the current one stored!'}, 200
        else:
            return {'message': 'No bucket list found with that ID'}, 404


class Bucketlist(Resource):
    """Create a bucket list"""

    @jwt_required
    def post(self):
        """method responsible for creating a bucket list."""

        user = User.query.filter_by(email=get_jwt_identity()).first()
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, type=str,
                            help='please enter a bucket list name.')
        args = parser.parse_args()
        if args['name']:
            if (re.match('[a-zA-Z]', args['name'])):
                try:
                    bucketlist = BucketList(name=args['name'], user_email=user.email)
                    bucketlist.save()
                    return {'message': '{} has been added to your pool of bucket\
                                        lists.'.format(args['name'])}, 201
                except:
                    return {'message': 'Bucket list already exists!'}
            else:
                    return {'message': 'Bucketlist name can not contain\
                                        special characters or numbers!'}, 409
        else:
            return {'message': 'Please provide a name for the bucket list.'}, 400

    @jwt_required
    def get(self):
        """method responsible for fetching all bucket lists."""

        args = parser.parse_args()
        limit = 20
        qword = None
        page = 1
        
        if args['limit']:
            limit = int(args['limit'])
            if limit < 1:
                limit = 20
            if limit > 100:
                limit = 100

        if args['q']:
            qword = args['q']
            if qword is None or qword =="":
                qword = None
        
        if args['page']:
            page = int(args['page'])
            if page < 1:
                page =1

        user = User.query.filter_by(email=get_jwt_identity()).first()
        page = (page - 1) * limit
        
        if qword:
            qword = "%{}%".format(qword)
            bucketlist = BucketList.query.filter(BucketList.name.ilike(qword)).filter(BucketList.created_by==user.email).offset(page).limit(limit).all()
        else:
            bucketlist = BucketList.query.filter_by(created_by=user.email).offset(page).limit(limit).all()
        output = {}
        if bucketlist:
            buckets = []
            for bucket in bucketlist:
                items = BucketListItem.query.filter_by(bucket_list_it_belongs_to=bucket.name).all()
                all_items = []
                for item in items:
                    item_and_details = {
                        'id': item.id,
                        'name': item.name,
                        'date_created': item.date_created,
                        'date_modified': item.date_modified,
                        'done': False
                    }
                    all_items.append(item_and_details)

                bucket_and_details = {
                    'id': bucket.id,
                    'name': bucket.name,
                    'items': all_items,
                    'date_created': bucket.date_created,
                    'date_modified': bucket.date_modified,
                    'created_by': bucket.created_by
                }

                buckets.append(bucket_and_details)

            return jsonify({'buckets': buckets}, 200)

        else:
            return {'message': 'No bucket lists at the moment!'}, 200


if __name__ == '__main__':
    app.run(debug=True)
