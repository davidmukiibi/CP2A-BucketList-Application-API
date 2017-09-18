# BucketList API in Flask microframework.

[![David Mukiibi](https://img.shields.io/badge/DAVID%20MUKIIBI-BUCKETLIST%20API-green.svg)]()
[![Coverage Status](https://coveralls.io/repos/github/davidmukiibi/CP2A-BucketList-Application-API/badge.svg?branch=develop)](https://coveralls.io/github/davidmukiibi/CP2A-BucketList-Application-API?branch=develop)
[![CircleCI](https://img.shields.io/circleci/project/github/RedSparr0w/node-csgo-parser.svg)]()

API Documentation: http://docs.mybucketlist1.apiary.io/#reference/0/login/login-a-user?console=1

## What is a Bucketlist?

Simply put, it is a list of goals, one wishes to accomplish during their life time.
One who intends to accomplish the goals is one who creates it.

## The Bucketlist API

In this project, I set out to create a web API that will create, update, delete and edit bucketlists.
The API is deveoped in flask with help from FlaskRestful.

## API Functionality Scope

|Method | Endpoint | Usage |
| ---- | ---- | --------------- |
|POST| `/api/v1/auth/register/` |  Registering a user. |
|POST| `/api/v1/auth/login/` | Logging in a user.|
|POST| `/api/v1/bucketlists/` | Creates a new bucketlist. |
|POST| `/api/v1/bucketlists/<int:ID>/items/` | Adds a new item to the given bucketlist with the give ID. |
|GET| `/api/v1/bucketlists/` | Retrieves all the created bucketlists created by a given user. |
|GET| `/api/v1/bucketlists/<int:ID>` | Get a single bucketlist of the given ID. |
|GET| `/api/v1/bucketlists?limit=` | This Paginates the results to get the required number of bucketllists.|
|GET| `/api/v1/bucketlists?q=` | Searches through bucketlists with the given word given for the q value.
|PUT| `/api/v1/bucketlists/<int:ID>` | Updates a single bucketlist of the given ID. |
|DELETE|`/api/v1/bucketlists/<int:ID>` | Deletes a single bucketlist of the give ID. |

## With that, now we can start the installation.

## Installation and Setup.

1. Clone the project on github by copying and pasting this URL in your terminal: git clone https://github.com/davidmukiibi/CP2A-BucketList-Application-API/tree/master

2. cd into the new created file folder.

3. You then Create a ***virtual environment*** and start the virtual environment.

4. Install the API dependencies with this command ```pip install -r requirements.txt``` in your new created folder.

4. Then you create a database.

Lets see how that is done below:


**Setup a Database:**

Install postgres ```brew install postgresql```

You can skip the above step if you already have postgresql installed.

1. In your terminal, run this command: ```psql postgres```

2. An interactive interface will open, once you are there, run this command: ```CREATE DATABASE jamaica;```
```note: the above command is case sensitive.```

3. There after, exit the postgres shell by typing this in the shell and hitting enter:```\q```

4. Then we run this in a normal terminal: ```source .env```

The next step is to run migrations and upgrades to setup the database tables.

**Run the Migrations**:
Run the following commands in your terminal.

1. ```python manage.py db init```

2. ```python manage.py db migrate```

3. ```python manage.py db upgrade```

By this stage we are almost done.

To run the application, run the below commands in the terminal.

```python run.py```

> The above command runs the application on:[http://127.0.0.1:5000] 

## Usage

For this step, since it's just an API and no User Interface, we need to install an app to help us use the API.

The given application of preference is Postman.

You can download it from here:
> https://www.getpostman.com/docs/postman/launching_postman/installation_and_updates

Then we need to start the database server too. I used pgAdmin to run mine:
> You can download pgAdmin from here: https://www.pgadmin.org
With that, we now have to create a database server and run it.
pgAdmin is friendly, so you can find where and how to create the server.

As of this point, we are done with setup, now lets open postman and start creating some bucketlists.

> Start the server in pgAdmin.

Open postman, and in the address bar, paste in this command:
> ```http://127.0.0.1:5000/```

First we need to register and login a user before we create any bucketlists.
> Append this ```auth/register/``` to the URL you have pasted in the postman address bar.

To create a user, you need to feed postman the following details in the ```body``` space of postman:
> New user's first name
> New user's second name
> New user's email address
> New user's password

To create a bucketlist or item, all you need is the bucketlist or item name.

Remember you need a user token everytime you want to create a bucketlist or an item.

And for that you will need to login first before we create a bucketlist, and then copy the token that is return and put it in the ```Headers``` field of postman.

The key will be ```Authorization``` and the value will be in this format: ```Bearer``` one space and then you paste the token you copied earlier.

## The following screenshots shows some examples on how to use the bucketlist API

- **Register a user.**

    ![alt text](postmanscreenshots/register.png)
    ```
        [POST] http://127.0.0.1:5000/api/v1/auth/register/
    ```
    ```first_name = david, second_name = mukiibi, email = 'david.mukiibi@gmail.com, password = 1234567890```

- **Login a user.**

    ![alt text](postmanscreenshots/login.png)
    ```
        [POST] http://127.0.0.1:5000/api/v1/auth/login/
    ```
    ```email = david.mukiibi@gmail.com, password = 1234567890```

 - **Create a bucketlist**

    To create a bucketlist, make a **POST** request to the following URI:
    **http://127.0.0.1:5000/api/v1/bucketlists/**

    ![alt text](postmanscreenshots/createbucketlist.png)
    ```
        [POST] http://127.0.0.1:5000/api/v1/bucketlists/
    ```    
    ```name = Got to jamaica```

- **Get all bucketlists**

    To list all bucketlists, make a **GET** request to the following URI:
    **http://127.0.0.1:5000/api/v1/bucketlists/**.

    ![alt text](postmanscreenshots/fetchbucketlists.png)

    ```
        [GET] http://127.0.0.1:5000/api/v1/bucketlists/

    ```
> Do not forget to put the token in the headers as up above.

- **Get a bucketlist by its id**

    To get a bucketlist by id , make a **GET** request to the following URI:
    **http://127.0.0.1:5000/api/v1/bucketlists/1**.

    ![alt text](postmanscreenshots/getbucketlist.png)

    ```
        [GET] http://127.0.0.1:5000/api/v1/bucketlists/1/

    ```

- **Delete a bucketlist by id**

    To delete a bucketlist, make a **DELETE** request to the following URI:
    **http://127.0.0.1:5000/api/v1/bucketlists/1**.

    ![alt text](postmanscreenshots/deletebucketlist.png)

    ```
        [DELETE] http://127.0.0.1:5000/api/v1/bucketlists/1/
    ```

- **Create a bucketlist Item**

    If you noticed we deleted the bucketlist we had, at this moment create another one and create an item on that as below.

    To create a bucketlist item, make a **POST** request to the following URI:
    **http://127.0.0.1:5000/api/v1/bucketlists/1/items/**.

    ![alt text](postmanscreenshots/createitems.png)

    ```
        [POST] http://127.0.0.1:5000/api/v1/bucketlists/1/items/
    ```    
    ```name = watch silicon valley```

I think by now you have gotten the hang of how to pass the CRUD commands, you can create the remaining methods.

## Testing
For the purpose of testing, cd into the root directory where you cloned the repo and then run the following commands:

```sh
$ nosetests --with-coverage
```
With the above command, it gives you the test coverage as well. If you do not want the coverage, do not add the
```--with-coverage```

Note: While running tests, you should have an internet connection, else the validate email test will fail with an IOERROR.
With that, you will be set to go.

cheers Enjoy using the API as your own.