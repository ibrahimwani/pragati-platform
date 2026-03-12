import os
import sqlite3
import json
from datetime import datetime
from mongoengine import connect
from models import User, Assessment, Course, UserCourse, MentorConnection, Job, JobApplication, CommunityPost, Comment
from flask import Flask
from database import db

# Initialize Flask app to get context if needed, but we can also just connect directly
app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://localhost:27017/pragati'
}
# Monkey patch flask.json if needed
import flask
try:
    from flask import json as flask_json
except ImportError:
    import json as flask_json
    flask.json = flask_json

def migrate():
    # connect directly using mongoengine
    connect(host='mongodb://localhost:27017/pragati')

    # SQLite Connection
    SQLITE_DB = 'instance/pragati.db' 
    if not os.path.exists(SQLITE_DB):
        SQLITE_DB = 'pragati.db'

    if not os.path.exists(SQLITE_DB):
        print(f"SQLite database not found at {SQLITE_DB}")
        return

    conn = sqlite3.connect(SQLITE_DB)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    print("Starting migration...")

    # Mapping for IDs (SQLite ID -> MongoDB Object)
    user_map = {}
    job_map = {}
    post_map = {}
    course_map = {}

    # Migrate Users
    cursor.execute("SELECT * FROM users")
    users = [dict(row) for row in cursor.fetchall()]
    for u in users:
        mongo_user = User(
            email=u['email'],
            password_hash=u['password_hash'],
            first_name=u['first_name'],
            last_name=u['last_name'],
            phone=u.get('phone'),
            location=u.get('location'),
            role=u.get('role', 'user'),
            career_break_years=u.get('career_break_years'),
            previous_role=u.get('previous_role'),
            desired_role=u.get('desired_role'),
            skills=u.get('skills'),
            bio=u.get('bio'),
            profile_picture=u.get('profile_picture'),
            is_active=bool(u.get('is_active', 1)),
            created_at=datetime.fromisoformat(u['created_at']) if u['created_at'] else datetime.utcnow(),
            company=u.get('company'),
            job_title=u.get('job_title'),
            experience_years=u.get('experience_years'),
            is_verified_mentor=bool(u.get('is_verified_mentor', 0)),
            otp=u.get('otp'),
            otp_expiry=datetime.fromisoformat(u['otp_expiry']) if u.get('otp_expiry') else None
        )
        mongo_user.save()
        user_map[u['id']] = mongo_user
    print(f"Migrated {len(users)} users.")

    # Migrate Assessments
    cursor.execute("SELECT * FROM assessments")
    assessments = [dict(row) for row in cursor.fetchall()]
    for a in assessments:
        if a['user_id'] in user_map:
            Assessment(
                user=user_map[a['user_id']],
                assessment_type=a.get('assessment_type'),
                score=a.get('score'),
                result_data=a.get('result_data'),
                completed_at=datetime.fromisoformat(a['completed_at']) if a['completed_at'] else datetime.utcnow()
            ).save()
    print(f"Migrated {len(assessments)} assessments.")

    # Migrate Courses
    cursor.execute("SELECT * FROM courses")
    courses = [dict(row) for row in cursor.fetchall()]
    for c in courses:
        mongo_course = Course(
            title=c['title'],
            description=c.get('description'),
            category=c.get('category'),
            difficulty=c.get('difficulty'),
            duration_hours=c.get('duration_hours'),
            skills_covered=c.get('skills_covered'),
            video_url=c.get('video_url'),
            resources=c.get('resources'),
            is_free=bool(c.get('is_free', 1)),
            created_at=datetime.fromisoformat(c['created_at']) if c.get('created_at') else datetime.utcnow()
        )
        mongo_course.save()
        course_map[c['id']] = mongo_course
    print(f"Migrated {len(courses)} courses.")

    # Migrate UserCourses
    cursor.execute("SELECT * FROM user_courses")
    user_courses = [dict(row) for row in cursor.fetchall()]
    for uc in user_courses:
        if uc['user_id'] in user_map and uc['course_id'] in course_map:
            UserCourse(
                user=user_map[uc['user_id']],
                course=course_map[uc['course_id']],
                progress=uc.get('progress', 0.0),
                completed=bool(uc.get('completed', 0)),
                enrolled_at=datetime.fromisoformat(uc['enrolled_at']) if uc['enrolled_at'] else datetime.utcnow(),
                completed_at=datetime.fromisoformat(uc['completed_at']) if uc.get('completed_at') else None
            ).save()
    print(f"Migrated {len(user_courses)} user courses.")

    # Migrate Jobs
    cursor.execute("SELECT * FROM jobs")
    jobs = [dict(row) for row in cursor.fetchall()]
    for j in jobs:
        mongo_job = Job(
            title=j['title'],
            company=j['company'],
            location=j.get('location'),
            job_type=j.get('job_type'),
            description=j.get('description'),
            requirements=j.get('requirements'),
            skills_required=j.get('skills_required'),
            salary_range=j.get('salary_range'),
            is_active=bool(j.get('is_active', 1)),
            posted_by=user_map.get(j.get('posted_by')),
            posted_at=datetime.fromisoformat(j['posted_at']) if j['posted_at'] else datetime.utcnow(),
            expires_at=datetime.fromisoformat(j['expires_at']) if j.get('expires_at') else None
        )
        mongo_job.save()
        job_map[j['id']] = mongo_job
    print(f"Migrated {len(jobs)} jobs.")

    # Migrate JobApplications
    cursor.execute("SELECT * FROM job_applications")
    apps = [dict(row) for row in cursor.fetchall()]
    for ap in apps:
        if ap['job_id'] in job_map and ap['user_id'] in user_map:
            JobApplication(
                job=job_map[ap['job_id']],
                user=user_map[ap['user_id']],
                status=ap.get('status', 'applied'),
                applied_at=datetime.fromisoformat(ap['applied_at']) if ap['applied_at'] else datetime.utcnow(),
                resume_url=ap.get('resume_url'),
                cover_letter=ap.get('cover_letter')
            ).save()
    print(f"Migrated {len(apps)} job applications.")

    # Migrate CommunityPosts
    cursor.execute("SELECT * FROM community_posts")
    posts = [dict(row) for row in cursor.fetchall()]
    for p in posts:
        if p['user_id'] in user_map:
            mongo_post = CommunityPost(
                author=user_map[p['user_id']],
                title=p.get('title'),
                content=p.get('content'),
                category=p.get('category'),
                likes=p.get('likes', 0),
                comments_count=p.get('comments_count', 0),
                created_at=datetime.fromisoformat(p['created_at']) if p['created_at'] else datetime.utcnow(),
                updated_at=datetime.fromisoformat(p['updated_at']) if p.get('updated_at') else None
            )
            mongo_post.save()
            post_map[p['id']] = mongo_post
    print(f"Migrated {len(posts)} community posts.")

    # Migrate Comments
    cursor.execute("SELECT * FROM comments")
    comments = [dict(row) for row in cursor.fetchall()]
    for c in comments:
        if c['post_id'] in post_map and c['user_id'] in user_map:
            Comment(
                post=post_map[c['post_id']],
                author=user_map[c['user_id']],
                content=c.get('content'),
                created_at=datetime.fromisoformat(c['created_at']) if c['created_at'] else datetime.utcnow()
            ).save()
    print(f"Migrated {len(comments)} comments.")

    # Migrate MentorConnections
    cursor.execute("SELECT * FROM mentor_connections")
    conns = [dict(row) for row in cursor.fetchall()]
    for cn in conns:
        if cn['mentor_id'] in user_map and cn['mentee_id'] in user_map:
            MentorConnection(
                mentor=user_map[cn['mentor_id']],
                mentee=user_map[cn['mentee_id']],
                status=cn.get('status', 'pending'),
                created_at=datetime.fromisoformat(cn['created_at']) if cn['created_at'] else datetime.utcnow(),
                last_interaction=datetime.fromisoformat(cn['last_interaction']) if cn.get('last_interaction') else None
            ).save()
    print(f"Migrated {len(conns)} mentor connections.")

    conn.close()
    print("Migration completed successfully!")

if __name__ == "__main__":
    migrate()
