from flask import Flask, request, jsonify
from Model.Configure import Session   # Ensure the imported Session is in lowercase
from Model.STMTR import STMTR


app = Flask(__name__)



def login():
    try:
        data = request.get_json()
        reg_no = data.get("reg_no")
        password = data.get("password")

        if not reg_no or not password:
            return jsonify({"error": "Registration number (reg_no) and password are required"}), 400

        db = Session()  # Use db_session to avoid conflict with sqlalchemy.orm Session
        try:
            student = db.query(STMTR).filter(STMTR.Reg_No == reg_no , STMTR.Password==password).first()

            if student and student.Password==password:
                student_data = {
                    "Reg_No": student.Reg_No,
                    "St_firstname": student.St_firstname,
                    "St_lastname": student.St_lastname
                }
                return jsonify({"message": "Login successful", "data": student_data}), 200
            else:
                 return jsonify({"error": "Invalid registration number or password"}), 401
        except Exception as e:
            return jsonify({"error": str(e)}), 500

        db.close();
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def signup():
    try:
        data = request.get_json()
        reg_no = data.get("reg_no")
        st_firstname = data.get("st_firstname")
        st_lastname = data.get("st_lastname")
        password = data.get("password")

        if not reg_no or not st_firstname or not st_lastname or not password:
            return jsonify({"error": "All fields (reg_no, st_firstname, st_lastname, password) are required"}), 400

        db = Session()  # Use db_session to avoid conflict with sqlalchemy.orm Session
        try:
            existing_student = db.query(STMTR).filter(STMTR.Reg_No == reg_no).first()

            if existing_student:
                return jsonify({"error": "Student with this registration number already exists"}), 400


            new_student = STMTR(
                Reg_No=reg_no,
                St_firstname=st_firstname,
                St_lastname=st_lastname,
                Password=password
            )

            db.add(new_student)
            db.commit()
            return jsonify({"message": "Signup successful", "data": {
                "Reg_No": reg_no,
                "St_firstname": st_firstname,
                "St_lastname": st_lastname
            }}), 201

        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            db.close()  # Always close the session

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
