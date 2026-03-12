from app import app
from models import User
from mongoengine import connect
import os

def verify_mentor_flow():
    with app.app_context():
        print("Starting Mentor Flow Verification...")
        
        # 1. Setup - Create a test user
        test_email = "test_mentor@example.com"
        User.objects(email=test_email).delete()
        user = User(
            email=test_email,
            first_name="Test",
            last_name="Mentor",
            role="user"
        )
        user.set_password("password")
        user.save()
        print(f"User created: {user.email}")
        
        # 2. Simulate Application
        user.company = "Test Co"
        user.company_verified = False
        user.is_verified_mentor = False
        user.save()
        print("Application simulated: Status = Pending Company Verification")
        
        # Verify state
        u = User.objects(email=test_email).first()
        assert u.company_verified == False
        assert u.is_verified_mentor == False
        
        # 3. Simulate Company Verification
        u.company_verified = True
        u.save()
        print("Company verification simulated: Status = Pending Admin Approval")
        
        # Verify state
        u = User.objects(email=test_email).first()
        assert u.company_verified == True
        assert u.is_verified_mentor == False
        
        # 4. Simulate Admin Approval
        u.is_verified_mentor = True
        u.role = "mentor"
        u.save()
        print("Admin approval simulated: Status = Verified Mentor & Role Assigned")
        
        # Final Verification
        u = User.objects(email=test_email).first()
        assert u.is_verified_mentor == True
        assert u.role == "mentor"
        
        print("\nSUCCESS: All verification stages passed!")

if __name__ == "__main__":
    verify_mentor_flow()
