from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from .models import db, User

bp = Blueprint('auth', __name__)


@bp.route('/register', methods=['POST'])
def register():
    """
    Регистрация нового пользователя.
    """
    data = request.get_json()

    new_user = User(
        username=data['username'],
        password=data['password'],
        role=data['role']
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


@bp.route('/login', methods=['POST'])
def login():
    """
    Вход пользователя в систему.
    """
    data = request.get_json()

    user = User.query.filter_by(username=data['username']).first()

    if user and user.password == data['password']:
        access_token = create_access_token(
            identity={'username': user.username, 'role': user.role}
        )
        return jsonify(access_token=access_token)

    return jsonify({"message": "Invalid credentials"}), 401
