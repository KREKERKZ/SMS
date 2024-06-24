from app import db
from werkzeug.security import generate_password_hash, check_password_hash


# Модель пользователя
class User(db.Model):
    """
    Модель пользователя для хранения информации о пользователях.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), nullable=False)

    def set_password(self, password):
        """
        Установка пароля пользователя с хешированием.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Проверка пароля пользователя.
        """
        return check_password_hash(self.password_hash, password)
