# Task 1
from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
ma = Marshmallow(app)

class MemberSchema(ma.Schema):
    id = fields.Integer(required=True)
    name = fields.String(required=True)
    age = fields.Integer(required=True)

    class Meta:
        fields = ("id", "name", "age")

class WorkoutSchema(ma.Schema):
    session_id = fields.Integer(required=True)
    member_id = fields.Integer(required=True)
    session_date = fields.Date()
    duration = fields.Integer()
    calories_burned = fields.Integer()

    class Meta:
        fields = ("session_id","member_id", "session_date", "duration", "calories_burned")

member_schema = MemberSchema()
members_schema = MemberSchema(many=True)
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

@app.route('/')
def home():
    return 'Welcome'

# Task 2: crud operations for members

@app.route('/members', methods=['POST'])
def add_member():
    # Logic to add a member
    try:
        member_data = member_schema.load(request.json)
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        new_member = (member_data['id'], member_data['name'], member_data['age'])
        query = "INSERT INTO members (id, name, age) VALUES (%s, %s, %s)"
        cursor.execute(query, new_member)
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "New member added successfully"}), 201
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


@app.route('/members/<int:id>', methods=['GET'])
def get_member(id):
    print(id)
    try:
    # Logic to retrieve a member
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM members WHERE id = %s"
        cursor.execute(query, (id,))
        member = cursor.fetchall()[0]
        print(member)
        cursor.close()
        conn.close()
        return member_schema.jsonify(member)
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/members/<int:id>', methods=['PUT'])
def update_member(id):
    try:
        member_data = member_schema.load(request.json)
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        updated_member = (member_data['name'], member_data['age'], member_data['id'])
        query = "UPDATE members SET name = %s, age = %s WHERE id = %s"
        cursor.execute(query, updated_member)
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Member updated successfully"}), 201
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route("/members/<int:id>", methods=["DELETE"])
def delete_member(id):
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()
        member_to_remove = (id,)
        cursor.execute("SELECT * FROM members where id = %s", member_to_remove)
        member = cursor.fetchone()
        if not member:
            return jsonify({"error": "Member not found"}), 404
        
        query = "DELETE FROM members WHERE id = %s"
        cursor.execute(query, member_to_remove)
        conn.commit()

        return jsonify({"message": "Member removed successfully"}), 200
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
#Task 3

#Schedule/add workouts
@app.route('/workouts', methods=['POST'])
def add_workout():
    # Logic to add a member
    try:
        workout_data = workout_schema.load(request.json)
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        new_workout = (workout_data['session_id'], workout_data['member_id'], workout_data['session_date'], workout_data['duration'], workout_data['calories_burned'])
        query = "INSERT INTO workoutsessionsdetailed (session_id, member_id, session_date, duration, calories_burned) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, new_workout)
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "New workout added successfully"}), 201
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# View/get workout
@app.route('/workouts/<int:session_id>', methods=['GET'])
def get_workout(session_id):
    print(session_id)
    try:
    # Logic to retrieve a member
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM workoutsessionsdetailed WHERE session_id = %s"
        cursor.execute(query, (session_id,))
        workout = cursor.fetchall()[0]
        cursor.close()
        conn.close()
        return workout_schema.jsonify(workout)
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

#Update workout info
@app.route('/workouts/<int:session_id>', methods=['PUT'])
def update_workout(session_id):
    try:
        workout_data = workout_schema.load(request.json)
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        updated_workout = (workout_data['member_id'], workout_data['session_date'], workout_data['duration'], workout_data['calories_burned'], workout_data['session_id'])
        query = "UPDATE workoutsessionsdetailed SET member_id = %s, session_date = %s, duration = %s, calories_burned = %s WHERE session_id = %s"
        cursor.execute(query, updated_workout)
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Workout updated successfully"}), 201
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

#Retrieve all workout sessions for a specific member
@app.route('/member-workouts/<int:member_id>', methods=['GET'])
def get_member_workouts(member_id):
    print(member_id)
    try:
    # Logic to retrieve a member
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM workoutsessionsdetailed WHERE member_id = %s"
        cursor.execute(query, (member_id,))
        workouts = cursor.fetchall()
        cursor.close()
        conn.close()
        return workouts_schema.jsonify(workouts)
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# Get db connection - helper function
def get_db_connection():
    # Database connection parameters:
    db_name = "fitness_center_db"
    user = "root"
    password = "0711"
    host = "localhost"
    try:
        conn = mysql.connector.connect(
        database=db_name,
        user=user,
        password=password,
        host=host)
        print("Successfully connected to MySQL database")
        return conn
    except mysql.connector.Error as db_err:
        print(f"Database error: {db_err}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    app.run(debug=True ,port=5000,use_reloader=False)
