from app import app
from models import User, CommunityPost, Job, Course

with app.app_context():
    mentors_count = User.query.filter(User.company.isnot(None)).count()
    posts_count = CommunityPost.query.count()
    courses_count = Course.query.count()

    print(f"Mentors (Applied): {mentors_count}")
    print(f"Community Posts: {posts_count}")
    print(f"Courses: {courses_count}")
