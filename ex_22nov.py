from flask import Flask, jsonify, request
import psycopg2

connection = psycopg2.connect(
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432",  # database
    database="flask_intro",
)

cur = connection.cursor()

# instantiating a class (Flask)
app = Flask(__name__)

# List (empty)
REMINDERS = []

# Decorator
@app.route("/")
def index():
    # Fetch all the reminders from the database
    cur.execute("SELECT * FROM reminders")
    # store in a variable
    reminder_data = cur.fetchall()  # 50% correct
    reminder_data = [
        {"title": item[0], "description": item[1]} for item in reminder_data
    ]  # list comprehension
    # JSON ->
    return jsonify({"reminders": reminder_data})


# @app.route("/")
# def index():
#     # Fetch all the reminders from the database
#     # cur.execute("SELECT * FROM employees;")
#     cur.execute("SELECT * FROM reminders;")
#     # store in a variable
#     reminder_data = cur.fetchall()

# columns = ['title', 'description']
# empty_list = []


# for l in reminder_data:
#     ex_dict = {}

#     for index, value in enumerate(columns):
#         ex_dict[columns[index]] = l[index]

#     empty_list.append(ex_dict)

# # JSON ->
# # return "Hello World"
# return jsonify({"reminders": empty_list})

# we want to store "reminders"
#
# GET
# POST
# DELETE
# PATCH
# PUT
# how do we save the reminders?

# Decorator -- URL path call add-reminder
@app.route("/hinzufuegen-reminder", methods=["POST"])
def add_reminder():
    try:
        title = request.json["title"]
    except KeyError:
        title = None

    # handle the exception (error handling)
    try:
        description = request.json["description"]
    except KeyError:
        description = None
    # Null
    print(f"INSERT INTO reminders (title, description) VALUES({title}, {description});")
    cur.execute(
        f"INSERT INTO reminders (title, description) VALUES('{title}', '{description}');"
    )
    connection.commit()
    print(title, description)
    # change the return value from empty list to have REMINDERS instead
    return jsonify({"reminders": REMINDERS})


@app.route("/reminders/<int:id>")
def reminder(id):
    cur.execute(f"SELECT title, description FROM reminders WHERE id = {id};")
    reminder_data = cur.fetchone()
    try:
        reminder_dict = {
            "id": id,
            "title": reminder_data[0],
            "description": reminder_data[1],
        }
        return jsonify(reminder_dict)
    except:
        return jsonify({"message": "Sorry something bad happened"}), 500

# DELETE 
@app.route("/reminders/<int:id>", methods=['DELETE'])
def delete_reminder(id):
    cur.execute(f"DELETE FROM reminders WHERE id={id};")
    # commit the changes
    connection.commit()
    return jsonify({"message": "Successfully deleted!"})

# 1000 x connections    
# Garbage collection (memory management)
@app.route("/reminders/<int:id>/update", methods=['PUT'])
def update_reminder(id):
    cur.execute(f"""
        UPDATE reminders
        SET title='{request.json.get('title')}', 
        description='{request.json.get('description')}'
        WHERE id={id}
    """)
    connection.commit()
    # Exercise: Return the updated information as a dictionary
    return jsonify({})

# Core HTTP verbs a developer must know
# - GET
# - POST
# - DELETE
# - PUT (Update)
# - PATCH

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5050)  # port for flask