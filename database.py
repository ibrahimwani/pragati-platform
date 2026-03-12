from mongoengine import connect

# We'll keep a dummy object if needed, but usually we just use the documents
class Database:
    def init_app(self, app):
        self.app = app
        connect(host=app.config['MONGODB_SETTINGS']['host'])

db = Database()

def init_db():
    """MongoDB initialization (collections created on first insert)"""
    pass