from flask_script import Manager

from helpers.initialize_db_content import initialize_demo_db_content
from papernest import app, db

manager = Manager(app)


@manager.command
def init_db_demo():
    initialize_demo_db_content(db)


if __name__ == "__main__":
    manager.run()
