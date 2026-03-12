from utils.gemini_assessment import GeminiAssessment
import os
from dotenv import load_dotenv
import json

load_dotenv(override=True)

def verify_ai():
    print("Verifying AI Integration...")
    
    if not os.getenv('GEMINI_API_KEY'):
        print("ERROR: GEMINI_API_KEY not found!")
        return

    assessor = GeminiAssessment()
    
    # 1. Verify Assess Skills
    print("\n1. Testing Assess Skills...")
    user_data = {
        'previous_role': 'Teacher',
        'desired_role': 'Data Analyst',
        'career_break_years': 3,
        'skills': 'Basic Excel, Teaching',
        'location': 'Remote'
    }
    result = assessor.assess_skills(user_data)
    print(f"Result Type: {type(result)}")
    if 'skill_gaps' in result:
        print("✅ Assess Skills: Success (Found skill_gaps)")
    else:
        print(f"❌ Assess Skills: Failed. Output: {result.keys()}")

    # 2. Verify Learning Path
    print("\n2. Testing Learning Path...")
    path = assessor.generate_learning_path(['Python', 'SQL'], 'Beginner')
    if 'daily_schedule' in path: 
        print("✅ Learning Path: Success")
    else:
        print(f"❌ Learning Path: Failed. Output: {path.keys()}")

    # 3. Verify Quiz
    print("\n3. Testing Quiz Generation...")
    quiz = assessor.generate_quiz('Python Basics')
    if 'questions' in quiz and len(quiz['questions']) > 0:
        print(f"✅ Quiz Gen: Success ({len(quiz['questions'])} questions)")
    else:
        print(f"❌ Quiz Gen: Failed. Output: {quiz.keys() if isinstance(quiz, dict) else quiz}")

if __name__ == "__main__":
    verify_ai()
