from flask_login import current_user, login_user, logout_user
from app.login import bp
from app.login.UserForms import LoginForm,RegistrationForm;
from flask import render_template,flash,url_for,request,redirect;
from app.models import User;
from app import db;


@bp.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/index');
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first(); #query the from user from the data base
        print(form.password.data)
        if user is None or not user.check_password(form.password.data):
            flash('invalid username or password');
            return redirect('/login');
        login_user(user, remember=form.remember_me.data); 
        next_page = request.args.get('next');
        if not next_page or url_parse(next_page).netloc !='':
            next_page = '/index';
        return redirect(next_page);
    return render_template('login/Login.html',title='sign in',form=form);

@bp.route('/logout', methods=['GET'])
def logout():
    logout_user();
    return redirect('/login');

@bp.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/index');
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data);
        user.set_password(form.password.data);
        db.session.add(user);
        db.session.commit();
        flash('congratulations, you have successfully registered');
        return redirect('/login');
    else:
        return  render_template('login/registration.html',title='Register', form=form);


@bp.route('/reset_password_request',methods=['GET','POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect('/index');
    form = ResetPasswordRequestForm();
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first();
        if user:
            send_password_reset_email(user);
            return redirect('/login');
        else:
            return redirect('/register');
    return render_template('login/reset_password_request.html',form=form,title='Reset Password Request');

@bp.route('/reset_password/<token>',methods=['GET','POST'])
def reset_password(token):
    user = User.validate_reset_password_token(token);
    print(user);
    if not user:
        return redirect('/index');
    form = ResetPasswordForm();
    if form.validate_on_submit():
        user.set_password(form.password.data);
        db.session.commit();
        return redirect('/login');
    return render_template('login/reset_password.html',title='Reset Passowrd', form=form);
    
