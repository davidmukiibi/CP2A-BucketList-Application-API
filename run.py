import os
from buckeT import app, api
from buckeT.bucketlist import RegisterUser, LoginUser

config_name = os.getenv('APP_SETTINGS') # config_name = "development"



api.add_resource(RegisterUser, '/auth/register/')
api.add_resource(LoginUser, '/auth/login/')


if __name__ == '__main__':
    app.run()