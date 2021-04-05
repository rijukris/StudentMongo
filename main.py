from flask import Flask, render_template, request
import pymongo

my_client = None
my_db = None
my_coll = None

app = Flask(__name__)


@app.route("/students")
def get_students():
    global my_coll
    result = my_coll.find()
    return render_template("students.html", data=result)


@app.route("/student/<mobile>")
def get_student_path(mobile):
    global my_coll
    result = my_coll.find_one({"mobile": mobile})
    return render_template("students.html", data=[result])


@app.route("/student")
def get_student_query():
    global my_coll
    mobile = request.args["mobile"]
    result = my_coll.find_one({"mobile": mobile})
    return render_template("students.html", data=[result])


@app.route("/students", methods=['POST'])
def create_students():
    global my_coll
    result = my_coll.insert_many(request.json)
    return f"Created {len(result.inserted_ids)} students"


@app.route("/student", methods=['POST'])
def create_student():
    global my_coll
    result = my_coll.insert_one(request.json)
    return f"Created one student"


@app.route("/students", methods=['DELETE'])
def delete_students():
    result = my_coll.delete_many({})
    return f"Deleted {result.deleted_count} students"


@app.route("/student/<mobile>", methods=['DELETE'])
def delete_student_path(mobile):
    result = my_coll.delete_one({"mobile": mobile})
    return f"Deleted {result.deleted_count} student"








def main():
    global my_client, my_db, my_coll
    my_client = pymongo.MongoClient("mongodb://localhost:27017")
    my_db = my_client["StudentDB"]
    c_list = my_db.list_collection_names()
    if "Student" not in c_list:
        my_coll = my_db.create_collection("Student")
    else:
        my_coll = my_db["Student"]

    app.run(debug=True)


if __name__ == "__main__":
    main()




