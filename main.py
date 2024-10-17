from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:789456@localhost:5432/AdvancedAnalytics'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    city = db.Column(db.String(120), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/api/data', methods=['GET'])
def get_data():
    users = User.query.all()
    return jsonify([{'id': user.id, 'name': user.name, 'age': user.age, 'city': user.city} for user in users])


@app.route('/api/add', methods=['POST'])
def add_data():
    users = request.get_json()
    print("Received Data:", users)

    if not users or not isinstance(users, list):
        return jsonify({'error': 'Invalid data provided, must be a list of users'}), 400
    added_users = []
    for new_user in users:
        if 'name' not in new_user or 'age' not in new_user or 'city' not in new_user:
            return jsonify({'error': 'Invalid data provided for one of the users'}), 400

        user = User(name=new_user['name'], age=new_user['age'], city=new_user['city'])
        db.session.add(user)
        db.session.flush()
        added_users.append({'id': user.id, 'name': user.name, 'age': user.age, 'city': user.city})

    db.session.commit()
    return jsonify({'message': 'Users added!', 'data': added_users}), 201


@app.route('/api/update/<int:user_id>', methods=['PUT'])
def update_data(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404

    update_info = request.get_json()
    if not update_info:
        return jsonify({'error': 'Invalid data provided'}), 400

    user.name = update_info.get('name', user.name)
    user.age = update_info.get('age', user.age)
    user.city = update_info.get('city', user.city)
    db.session.commit()
    return jsonify({'message': 'User updated!', 'data': {'id': user.id, 'name': user.name, 'age': user.age, 'city': user.city}})

@app.route('/api/delete/<int:user_id>', methods=['DELETE'])
def delete_data(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted!'})

if __name__ == '__main__':
    app.run(debug=True)
