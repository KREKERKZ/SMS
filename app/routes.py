from flask import jsonify, request
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    get_jwt_identity
)
from app import app, db
from app.models import User


# Регистрация пользователя
@app.route('/register', methods=['POST'])
def register():
    """
    Регистрация нового пользователя.
    """
    username = request.json.get('username')
    password = request.json.get('password')
    role = request.json.get('role')

    if not (
        username and
        password and
        role in ['parent', 'student', 'teacher', 'administration']
    ):
        # Действия, если условие не выполнено
        return jsonify({'message': 'Invalid registration data'}), 400
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'message': 'Username already exists'}), 400

    new_user = User(username=username, role=role)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201


# Аутентификация пользователя
@app.route('/login', methods=['POST'])
def login():
    """
    Вход пользователя в систему.
    """
    username = request.json.get('username')
    password = request.json.get('password')

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401


# Пример защищенного маршрута для получения данных
@app.route('/data', methods=['GET'])
@jwt_required()
def get_data():
    """
    Пример защищенного маршрута для получения данных.
    """
    current_user = get_jwt_identity()
    return (
        jsonify(message=f'Hello, {current_user}! This data is protected.'),
        200
        )


# Пример маршрута для обновления оценок (для учителя)
@app.route('/update_grades', methods=['POST'])
@jwt_required()
def update_grades():
    """
    Пример маршрута для обновления оценок (для учителя).
    """
    current_user = get_jwt_identity()
    role = User.query.filter_by(username=current_user).first().role

    if role != 'teacher':
        return jsonify({'message': 'Unauthorized'}), 403

    # Логика обновления оценок здесь

    return jsonify({'message': 'Grades updated successfully'}), 200
