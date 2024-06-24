from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from app.config import Config
from app import routes  # Импортируем модуль routes

# Инициализация расширений без создания экземпляра Flask приложения
db = SQLAlchemy()
jwt = JWTManager()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Инициализация расширений с привязкой к приложению
    db.init_app(app)
    jwt.init_app(app)

    # Регистрация маршрутов
    app.register_blueprint(routes.bp)

    return app
