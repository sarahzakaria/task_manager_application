from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from api import create_app
from api.models import db

app = create_app()

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command("db", MigrateCommand)

@manager.command
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@manager.command
def runserver():
    app.run(debug=True, host="0.0.0.0", port=5000)

if __name__ == "__main__":
    manager.run()