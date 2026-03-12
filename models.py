from flask_login import UserMixin
from mongoengine import Document, StringField, IntField, BooleanField, DateTimeField, FloatField, ReferenceField
CASCADE = 2
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin, Document):
    meta = {'collection': 'users'}
    
    email = StringField(unique=True, required=True)
    password_hash = StringField(required=True)
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    phone = StringField()
    location = StringField()
    role = StringField(default='user')
    career_break_years = IntField()
    previous_role = StringField()
    desired_role = StringField()
    skills = StringField()
    bio = StringField()
    profile_picture = StringField()
    is_active = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.utcnow)
    last_login = DateTimeField()
    
    # Mentor Fields
    company = StringField()
    job_title = StringField()
    experience_years = IntField()
    company_verified = BooleanField(default=False)
    is_verified_mentor = BooleanField(default=False)
    
    # 2FA Fields
    otp = StringField()
    otp_expiry = DateTimeField()

    # Password helpers
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_progress_percentage(self):
        return 0

    # Required for Flask-Login with MongoEngine
    def get_id(self):
        return str(self.id)

class Assessment(Document):
    meta = {'collection': 'assessments'}
    
    user = ReferenceField(User, reverse_delete_rule=CASCADE, required=True)
    assessment_type = StringField()
    score = FloatField()
    result_data = StringField()
    completed_at = DateTimeField(default=datetime.utcnow)

class Course(Document):
    meta = {'collection': 'courses'}
    
    title = StringField(required=True)
    description = StringField()
    category = StringField()
    difficulty = StringField()
    duration_hours = IntField()
    skills_covered = StringField()
    video_url = StringField()
    resources = StringField()
    is_free = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.utcnow)

class UserCourse(Document):
    meta = {'collection': 'user_courses'}
    
    user = ReferenceField(User, reverse_delete_rule=CASCADE, required=True)
    course = ReferenceField(Course, reverse_delete_rule=CASCADE, required=True)
    progress = FloatField(default=0.0)
    completed = BooleanField(default=False)
    enrolled_at = DateTimeField(default=datetime.utcnow)
    completed_at = DateTimeField()

class MentorConnection(Document):
    meta = {'collection': 'mentor_connections'}
    
    mentor = ReferenceField(User, reverse_delete_rule=CASCADE, required=True)
    mentee = ReferenceField(User, reverse_delete_rule=CASCADE, required=True)
    status = StringField(default='pending')
    created_at = DateTimeField(default=datetime.utcnow)
    last_interaction = DateTimeField()

class Job(Document):
    meta = {'collection': 'jobs'}
    
    title = StringField(required=True)
    company = StringField(required=True)
    location = StringField()
    job_type = StringField()
    description = StringField()
    requirements = StringField()
    skills_required = StringField()
    salary_range = StringField()
    is_active = BooleanField(default=True)
    posted_by = ReferenceField(User)
    posted_at = DateTimeField(default=datetime.utcnow)
    expires_at = DateTimeField()

class JobApplication(Document):
    meta = {'collection': 'job_applications'}
    
    job = ReferenceField(Job, reverse_delete_rule=CASCADE, required=True)
    user = ReferenceField(User, reverse_delete_rule=CASCADE, required=True)
    status = StringField(default='applied')
    applied_at = DateTimeField(default=datetime.utcnow)
    resume_url = StringField()
    cover_letter = StringField()

class CommunityPost(Document):
    meta = {'collection': 'community_posts'}
    
    author = ReferenceField(User, reverse_delete_rule=CASCADE, required=True)
    title = StringField()
    content = StringField()
    category = StringField()
    likes = IntField(default=0)
    comments_count = IntField(default=0)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField()

class Comment(Document):
    meta = {'collection': 'comments'}
    
    post = ReferenceField(CommunityPost, reverse_delete_rule=CASCADE, required=True)
    author = ReferenceField(User, reverse_delete_rule=CASCADE, required=True)
    content = StringField()
    created_at = DateTimeField(default=datetime.utcnow)
