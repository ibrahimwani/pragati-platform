from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, current_user
from database import db, init_db
from models import User
import os
from dotenv import load_dotenv

# Blueprint imports
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.jobs import jobs_bp
from routes.mentorship import mentorship_bp
from routes.admin import admin_bp
from routes.community import community_bp

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
app.config['MONGODB_SETTINGS'] = {
    'host': os.getenv('MONGODB_URI', 'mongodb://localhost:27017/pragati')
}

# Initialize database
db.init_app(app)

# Initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'


@login_manager.user_loader
def load_user(user_id):
    try:
        from bson.objectid import ObjectId
        if not ObjectId.is_valid(user_id):
            return None
        return User.objects(id=user_id).first()
    except Exception:
        return None


# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(jobs_bp)
app.register_blueprint(mentorship_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(community_bp)


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.home"))
    return render_template("index.html")


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template("500.html"), 500


if __name__ == "__main__":
     with app.app_context():
        init_db()

        # Create default admin user AFTER tables exist
        if not User.objects(email="admin@pragati.com").first():
            admin = User(
                email="admin@pragati.com",
                first_name="Admin",
                last_name="User",
                role="admin"
            )
            admin.set_password("admin123")
            admin.save()

        app.run(debug=True, port=5000)




    temp = last; 
              if(last->next == last) 
                     last = NULL; 
              else 
              { 
                      while(temp->next!=last) 
                                prev = temp
                              temp = temp->next; 

                      prev->next = last->next;  
              }      
              printf(“\nLast Node with info %d is deleted”,temp->info); 
              free(temp);  

return(prev)
}
