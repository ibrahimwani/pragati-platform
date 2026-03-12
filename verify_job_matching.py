from utils.job_matching import get_job_match_score, get_recommended_jobs
from models import User, Job
from app import app
from database import db

def verify_job_matching():
    with app.app_context():
        print("Testing Job Matching...")
        
        # Mock User
        user = User(
            first_name="Test",
            last_name="User",
            desired_role="Python Developer",
            skills="Python, Flask, SQL"
        )
        
        # Mock Jobs
        job1 = Job(title="Python Engineer", skills_required="Python, Django", is_active=True)
        job2 = Job(title="Frontend dev", skills_required="React, CSS", is_active=True)
        job3 = Job(title="Junior Python Developer", skills_required="Python, Flask", is_active=True)
        
        score1 = get_job_match_score(user, job1)
        score2 = get_job_match_score(user, job2)
        score3 = get_job_match_score(user, job3)
        
        print(f"Match Score (Python Engineer): {score1}")
        print(f"Match Score (Frontend dev): {score2}")
        print(f"Match Score (Junior Python Developer): {score3}")
        
        if score3 > score1 > score2:
             print("✅ Matching Ranking: Correct")
        else:
             print("❌ Matching Ranking: Unexpected")

if __name__ == "__main__":
    verify_job_matching()
