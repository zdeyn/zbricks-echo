# from zbricks import zBrick
from zbricks.bricks import zFlaskBrick
# from zbricks.bricks import zSQLAlchemyBrick
# from zbricks import flask_host
# from zbricks import flask_brick
# from zbricks import sqlalchemy_brick


def create_app():
    app = zFlaskBrick()
    # flask_host = app.attach(flask_brick) # requires nothing, installs itself so app is now also an instance of Flask
    # app.attach(sqlalchemy_brick) # requires flask_brick
    return app
