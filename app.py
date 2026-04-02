from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os

app = Flask(__name__)
CORS(app)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
app.config['PROPAGATE_EXCEPTIONS'] = True

db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)


# JWT error handlers
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({'error': 'Token has expired'}), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({'error': 'Invalid token', 'message': str(error)}), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({'error': 'Authorization token is missing', 'message': str(error)}), 401


# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    tasks = db.relationship('Task', backref='user', lazy=True, cascade='all, delete-orphan')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    priority = db.Column(db.String(20), default='medium')
    status = db.Column(db.String(20), default='pending')
    due_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# Marshmallow Schemas for validation (simplified)
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'email', 'created_at')


class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description', 'priority', 'status', 'due_date', 'user_id', 'created_at', 'updated_at')


user_schema = UserSchema()
users_schema = UserSchema(many=True)
task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)


# Helper function to serialize tasks
def serialize_task(task):
    return {
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'priority': task.priority,
        'status': task.status,
        'due_date': task.due_date.isoformat() if task.due_date else None,
        'user_id': task.user_id,
        'created_at': task.created_at.isoformat() if task.created_at else None,
        'updated_at': task.updated_at.isoformat() if task.updated_at else None
    }


def serialize_user(user):
    return {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'created_at': user.created_at.isoformat() if user.created_at else None
    }


# Create tables
with app.app_context():
    db.create_all()


# Routes
@app.route('/')
def home():
    return jsonify({'message': 'Task Management API', 'version': '1.0', 'status': 'running'})


@app.route('/app')
def serve_app():
    return '''
    <!DOCTYPE REDIRECT>
    <html>
    <head>
        <meta http-equiv="refresh" content="0; url=/static/index.html">
    </head>
    <body>
        <p>Redirecting to app...</p>
        <p>If not redirected, <a href="/static/index.html">click here</a></p>
    </body>
    </html>
    '''


@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({'message': 'API is working!', 'timestamp': datetime.utcnow().isoformat()})


# Authentication Routes
@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        print(f"Registration attempt - Received data: {data}")  # Debug

        if not data or not data.get('username') or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Missing required fields'}), 400

        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already exists'}), 400

        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already exists'}), 400

        hashed_password = generate_password_hash(data['password'])
        print(f"Creating user with hashed password length: {len(hashed_password)}")

        new_user = User(username=data['username'], email=data['email'], password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        print(f"User created successfully: {new_user.username}")

        return jsonify({'message': 'User registered successfully', 'user': serialize_user(new_user)}), 201
    except Exception as e:
        db.session.rollback()
        print(f"Registration error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        print(f"Login attempt - Received data: {data}")  # Debug

        if not data or not data.get('username') or not data.get('password'):
            print("Missing credentials")
            return jsonify({'error': 'Missing credentials'}), 400

        user = User.query.filter_by(username=data['username']).first()
        print(f"User found: {user is not None}")  # Debug

        if not user:
            print(f"No user found with username: {data['username']}")
            return jsonify({'error': 'Invalid credentials'}), 401

        password_match = check_password_hash(user.password, data['password'])
        print(f"Password match: {password_match}")  # Debug

        if not password_match:
            print("Password does not match")
            return jsonify({'error': 'Invalid credentials'}), 401

        # IMPORTANT: Convert user.id to string for JWT
        access_token = create_access_token(identity=str(user.id))
        print(f"Token created successfully for user: {user.username} (ID: {user.id})")

        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'user': serialize_user(user)
        }), 200
    except Exception as e:
        print(f"Login error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


# Task Routes
@app.route('/api/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    try:
        # Convert back to int when retrieving
        current_user_id = int(get_jwt_identity())
        status = request.args.get('status')
        priority = request.args.get('priority')

        query = Task.query.filter_by(user_id=current_user_id)

        if status:
            query = query.filter_by(status=status)
        if priority:
            query = query.filter_by(priority=priority)

        tasks = query.order_by(Task.created_at.desc()).all()
        return jsonify([serialize_task(task) for task in tasks]), 200
    except Exception as e:
        print(f"Error getting tasks: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/tasks/<int:id>', methods=['GET'])
@jwt_required()
def get_task(id):
    try:
        current_user_id = int(get_jwt_identity())
        task = Task.query.filter_by(id=id, user_id=current_user_id).first()

        if not task:
            return jsonify({'error': 'Task not found'}), 404

        return jsonify(serialize_task(task)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/tasks', methods=['POST'])
@jwt_required()
def create_task():
    try:
        current_user_id = int(get_jwt_identity())
        data = request.get_json()

        print(f"Received data: {data}")  # Debug print

        if not data or not data.get('title'):
            return jsonify({'error': 'Title is required'}), 400

        due_date = None
        if data.get('due_date'):
            try:
                # Handle various date formats
                date_str = data['due_date']
                if 'T' in date_str:
                    # Remove timezone info if present
                    date_str = date_str.replace('Z', '').split('+')[0].split('.')[0]
                    due_date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')
                else:
                    due_date = datetime.strptime(date_str, '%Y-%m-%d')
            except Exception as date_error:
                print(f"Date parsing error: {date_error}")
                pass  # If date parsing fails, just set to None

        new_task = Task(
            title=data['title'],
            description=data.get('description', ''),
            priority=data.get('priority', 'medium'),
            status=data.get('status', 'pending'),
            due_date=due_date,
            user_id=current_user_id
        )

        db.session.add(new_task)
        db.session.commit()

        result = serialize_task(new_task)
        print(f"Task created successfully: {result}")

        return jsonify({'message': 'Task created successfully', 'task': result}), 201
    except Exception as e:
        db.session.rollback()
        error_msg = str(e)
        print(f"Error creating task: {error_msg}")  # This will show in terminal
        import traceback
        traceback.print_exc()  # Print full stack trace
        return jsonify({'error': error_msg}), 500


@app.route('/api/tasks/<int:id>', methods=['PUT'])
@jwt_required()
def update_task(id):
    try:
        current_user_id = int(get_jwt_identity())
        task = Task.query.filter_by(id=id, user_id=current_user_id).first()

        if not task:
            return jsonify({'error': 'Task not found'}), 404

        data = request.get_json()

        if data.get('title'):
            task.title = data['title']
        if 'description' in data:
            task.description = data['description']
        if data.get('priority'):
            task.priority = data['priority']
        if data.get('status'):
            task.status = data['status']
        if 'due_date' in data:
            if data['due_date']:
                try:
                    date_str = data['due_date']
                    if 'T' in date_str:
                        date_str = date_str.replace('Z', '').split('+')[0].split('.')[0]
                        task.due_date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')
                    else:
                        task.due_date = datetime.strptime(date_str, '%Y-%m-%d')
                except:
                    pass
            else:
                task.due_date = None

        db.session.commit()

        return jsonify({'message': 'Task updated successfully', 'task': serialize_task(task)}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error updating task: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/tasks/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_task(id):
    try:
        current_user_id = int(get_jwt_identity())
        task = Task.query.filter_by(id=id, user_id=current_user_id).first()

        if not task:
            return jsonify({'error': 'Task not found'}), 404

        db.session.delete(task)
        db.session.commit()

        return jsonify({'message': 'Task deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/tasks/stats', methods=['GET'])
@jwt_required()
def get_stats():
    try:
        current_user_id = int(get_jwt_identity())

        total = Task.query.filter_by(user_id=current_user_id).count()
        pending = Task.query.filter_by(user_id=current_user_id, status='pending').count()
        in_progress = Task.query.filter_by(user_id=current_user_id, status='in_progress').count()
        completed = Task.query.filter_by(user_id=current_user_id, status='completed').count()

        return jsonify({
            'total': total,
            'pending': pending,
            'in_progress': in_progress,
            'completed': completed
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)