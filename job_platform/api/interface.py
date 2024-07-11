#!/usr/bin/python3
"""
holds api for the application.
"""

from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from app import app, db, bcrypt
from models import User, Job, Application
from flask_login import login_user, current_user, logout_user, login_required

api = Api(app)

class RegisterUser(Resource):
    def post(self):
        """
        registers new user 
        """
        data = request.get_json()
        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        user = User(username=data['username'], email=data['email'], password=hashed_password, user_type=data['user_type'])
        db.session.add(user)
        db.session.commit()
        return {'message': 'User created successfully'}, 201

class LoginUser(Resource):
    def post(self):
        """
        logs in already registered user in the web app
        """
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        if user and bcrypt.check_password_hash(user.password, data['password']):
            login_user(user, remember=True)
            return {'message': 'Login successful'}, 200
        return {'message': 'Invalid credentials'}, 401

class LogoutUser(Resource):
    @login_required
    def post(self):
        """
        allows user to log out from the system
        """
        logout_user()
        return {'message': 'Logout successful'}, 200

class JobResource(Resource):
    @login_required
    def post(self):
        """
        redirects user to the job resources,but user must provide with log in details
        """
        data = request.get_json()
        job = Job(title=data['title'], description=data['description'], employer_id=current_user.id)
        db.session.add(job)
        db.session.commit()
        return {'message': 'Job posted successfully'}, 201

    def get(self):
        """
        provides user with jobs with the following attributes
        * job.id
        * job.tittle
        * job.description
        * job.employer_id
        """

        jobs = Job.query.all()
        jobs_list = [{'id': job.id, 'title': job.title, 'description': job.description, 'employer_id': job.employer_id} for job in jobs]
        return jsonify(jobs_list)

class JobSearchResource(Resource):
    def get(self):
        """
        allos user to search for a job according to user id
        """
        parser = reqparse.RequestParser()
        parser.add_argument('keyword', required=True)
        args = parser.parse_args()
        keyword = args['keyword']
        jobs = Job.query.filter(Job.title.contains(keyword) | Job.description.contains(keyword)).all()
        jobs_list = [{'id': job.id, 'title': job.title, 'description': job.description, 'employer_id': job.employer_id} for job in jobs]
        return jsonify(jobs_list)

class ApplyJobResource(Resource):
    @login_required
    def post(self, job_id):
        """
        allows user to apply for a job according to user id
        """
        job = Job.query.get_or_404(job_id)
        application = Application(job_id=job.id, applicant_id=current_user.id)
        db.session.add(application)
        db.session.commit()
        return {'message': 'Applied for job successfully'}, 201

api.add_resource(RegisterUser, '/api/register')
api.add_resource(LoginUser, '/api/login')
api.add_resource(LogoutUser, '/api/logout')
api.add_resource(JobResource, '/api/jobs')
api.add_resource(JobSearchResource, '/api/jobs/search')
api.add_resource(ApplyJobResource, '/api/jobs/<int:job_id>/apply')

if __name__ == '__main__':
    app.run(debug=True,host '0.0.0.0', port=5000)
