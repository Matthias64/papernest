from app import create_app, db
from app.db_models.operator import Operator
from app.db_models.position import Position

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Operator': Operator, 'Position': Position}


if __name__ == '__main__':
    app.run(debug=True)
