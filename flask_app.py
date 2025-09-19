from app import create_app
from app.models import db

app = create_app('ProductionConfig')

with app.app_context():
    #db.drop_all()   # Uncomment only if you want to wipe all tables
    db.create_all()    # Creates tables only if they don't exist

#if __name__ == '__main__':
   # app.run()
   