import os
from flask import Flask, render_template, request, redirect, url_for
from db.dbhelper import init_db, getall, getbyid, insert, update, delete

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, "static", "uploads")
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)


init_db()

@app.route("/")
def index():
    edit_id = request.args.get("edit")
    student_data = getbyid("Students", edit_id) if edit_id else None
    students = getall("Students")
    return render_template("index.html", studentlist=students, student_data=student_data)

@app.route("/save_student", methods=["POST"])
def save_student():
    idno = request.form.get("idno")
    lastname = request.form.get("lastname")
    firstname = request.form.get("firstname")
    course = request.form.get("course")
    level = request.form.get("level")

    
    photo_file = request.files.get("photo")
    filename = None

    if photo_file and photo_file.filename:
        
        safe_name = f"{idno}_{os.path.basename(photo_file.filename)}"
        save_path = os.path.join(app.config["UPLOAD_FOLDER"], safe_name)
        photo_file.save(save_path)
        filename = safe_name

    existing = getbyid("Students", idno)
    if existing:
       
        if not filename:
            filename = existing.get("photo")
        update("Students", idno, lastname, firstname, course, level, filename)
    else:
        insert("Students", idno, lastname, firstname, course, level, filename)

    return redirect(url_for("index"))

@app.route("/delete_student/<idno>")
def delete_student(idno):
    delete("Students", idno)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
