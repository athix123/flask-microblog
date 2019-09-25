from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm
from flask import jsonify

@app.route('/')
@app.route('/index')
def index():
	user = {'username': 'athix'}
	posts = [
		{
			'author': {'username': 'John'},
			'body': 'Beautiful day in Malang!'
		},
		{
			'author': {'username': 'Susan'},
			'body': 'One Piece movie was so cool!'
		}
	]
	return render_template('index.html', title='Home', user=user, posts=posts)
	#return jsonify(user)


@app.route('/login', methods=['GET', 'POST'])
def login():
		form = LoginForm()
		if form.validate_on_submit():
			flash('Login requested for user {}, remember_me={}'.format(
				form.username.data, form.remember_me.data))
			return redirect('/index')
		return render_template('login.html', title='Sign-In', form=form)
