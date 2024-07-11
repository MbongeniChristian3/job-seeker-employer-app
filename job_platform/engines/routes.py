#!/usr/bin/python3
"""
Contains the RoutesDocs classes
"""
from flask import render_template, url_for, flash, redirect, request
from app import app, db, bcrypt
from forms import RegistrationForm, LoginForm, JobPostForm, JobSearchForm, JobApplyForm
from models import User, Job, Application
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
@app.route("/home")
def home():
    """ returns html home page """
    return render_template('home.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    """ returns url link for home page if user is authenticated """
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, user_type=form.user_type.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    """ logs out from the home page """
    return redirect(url_for('home'))

@app.route("/dashboard")
@login_required
def dashboard():
    if current_user.user_type == 'employer':
        jobs = Job.query.filter_by(employer_id=current_user.id).all()
    else:
        jobs = Job.query.all()
        """ returns all available jobs """
    return render_template('dashboard.html', title='Dashboard', jobs=jobs)

@app.route("/job/new", methods=['GET', 'POST'])
@login_required
def new_job():
    form = JobPostForm()
    if form.validate_on_submit():
        job = Job(title=form.title.data, description=form.description.data, employer_id=current_user.id)
        db.session.add(job)
        db.session.commit()
        flash('Your job has been created!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('job_post.html', title='New Job', form=form)

@app.route("/job/search", methods=['GET', 'POST'])
def search_job():
    form = JobSearchForm()
    jobs = []
    if form.validate_on_submit():
        jobs = Job.query.filter(Job.title.contains(form.keyword.data) | Job.description.contains(form.keyword.data)).all()
        """ searches for jobs available """
    return render_template('job_search.html', title='Search Jobs', form=form, jobs=jobs)

@app.route("/job/<int:job_id>/apply", methods=['GET', 'POST'])
@login_required
def apply_job(job_id):
    form = JobApplyForm()
    job = Job.query.get_or_404(job_id)
    if form.validate_on_submit():
        application = Application(job_id=job.id, applicant_id=current_user.id)
        db.session.add(application)
        db.session.commit()
        flash('You have successfully applied for this job.', 'success')
        """ def apply for a job """
        return redirect(url_for('dashboard'))
    return render_template('job_apply.html', title='Apply Job', form=form, job=job)
