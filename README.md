# goal-app
A web application that allows users to view, save, and edit goals they want to achieve. Users should be able to log in. They should only be able to see their own goals.

# How to Run locally
Have the following installed in your machine:
 * Python version 3.6.9
 * Pip version 20.0.2 (pip3)
 * Git
 * PostgreSQL

Steps:
  Navigate to the goal-app directory on the command line after cloning from github.

```
cd goal-app
```
 
 Create the facebook-clone PostgreSQL db by running on the command line:

```
createdb goal-proj
```

Create the tables in the db by running on the command line:

```
 python3 -i model.py
```
Then in python interactive mode run
```
Connected to DB.
>>> db.create_all()
```
 Install virtualenv if it's not available on your machine already.

 ```
 pip3 install virtualenv
 ```

 Create a virtual environment and install all the python libraries required 
 by the project.

 ```
 virtualenv env
 ```
 
 ```
 source env/bin/activate
 ```

 ```
 pip3 install -r requirements.txt
 ```

Now you can run the app locally by running on the command line:

```
python3 server.py
```