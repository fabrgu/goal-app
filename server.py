from jinja2 import StrictUndefined
from flask import (Flask, render_template, redirect, request, flash,
                   session)
from flask_debugtoolbar import DebugToolbarExtension
from model import User, Goal, connect_to_db, db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This instead raises an error.
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def index():
    """Go to login page if user is not logged in"""
    if session.get('user_id'):
        return redirect("/goals")
    else:
        return render_template('login.html')


@app.route('/registration')
def show_registration_form():
    """Show user registration form"""

    return render_template('registration.html')


@app.route('/registration', methods=['POST'])
def register():
    """Create user if email not in use."""

    email = request.form.get('email')
    user_confirmed = User.query.filter(User.email == email).first()
    
    if not user_confirmed:
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        password = request.form.get('password')

        user = User(email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password=generate_password_hash(password),
                    created_on=datetime.today())

        db.session.add(user)
        db.session.commit()
        flash('User successfully created')
    else:
        flash('User not created. Email associated with another user.')

    return redirect('/')


@app.route('/logout')
def logout():
    """ log user out of session"""

    flash('You are logged out.')

    if session.get('user_id'):
        del session['user_id']
    return redirect('/')


@app.route('/login', methods=['POST'])
def login():
    """Logs in existing user."""

    email = request.form.get('email')
    unhashed_password = request.form.get('password')

    user = User.query.filter(User.email == email,
                                      User.password == password).first()
    if user and check_password_hash(user.password, unhashed_password):
        session['user_id'] = user.user_id
        flash('Logged in')
        return redirect('/')
    else:
        flash('User does not exist. Please create an account.')
        return redirect('/registration')


@app.route('/goals/<int:user_id>')
def goal_list(user_id):
    """Show list of goals for user. """

    goals = Goal.query.filter_by(user_id=user_id).all()

    return render_template('goal_list.html', goals=goals)


@app.route('/goal/<int:goal_id>')
def movie_details(goal_id):
    """ Show details about goal."""

    goal = Goal.query.get(goal_id)

    return render_template('goal_details.html', goal=goal)


@app.route('/add_goal', methods=['POST'])
def add_goal():
    """Add new goal """
    description = request.form.get('description')
    name = request.form.get('name')

    new_goal = Goal(description=description, 
                    name=name,
                    created_on=datetime.today(),
                    modified_on=datetime.today())
    db.session.add(new_goal)
    db.session.commit()
    
    flash('Your goal has been added!')

    return redirect('/goals')

@app.route('/update_goal/<int:goal_id>', methods=['POST'])
def update_goal(goal_id):
    """ Update existing goal for existing users """

    user_id = session['user_id']
    description = request.form.get('description')
    name = request.form.get('name')

    goal = Goal.query.filter_by(goal_id=goal_id).first()

    if goal is not None:
        goal.description = description
        goal.name = name
        goal.modified_on = datetime.today()
        db.session.commit()
        flash('Your goal has been updated!')

    return redirect(f'/goal/{goal_id}')


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Uncomment to use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')