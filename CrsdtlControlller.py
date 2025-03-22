from flask import jsonify, request
from Model.Crsdtl import Crsdtl
from Model.Configure import Session
from sqlalchemy import and_

def get_student_courses_by_reg():
    try:
        # Get the registration number and semester number from the request arguments
        reg_no = request.args.get("reg_no")
        semester_no = request.args.get("semester_no")

        # Ensure the registration number is provided
        if not reg_no:
            return jsonify({"error": "Registration number (reg_no) is required"}), 400

        # Create a database session
        db = Session()

        # Query the Crsdtl table to find all courses for the student
        courses = db.query(Crsdtl).filter(
            and_(Crsdtl.REG_NO == reg_no, Crsdtl.SEMESTER_NO == semester_no)
        ).all()

        # Serialize the course data into a list of dictionaries
        course_list = []
        for course in courses:
            course_data = {
                "Course_no": course.Course_no,
                "ATTEMPT_NO": course.ATTEMPT_NO,
                "SEMESTER_NO": course.SEMESTER_NO,
                "SECTION": course.SECTION,
                "Final_score": float(course.Final_score) if course.Final_score else None,
                "Midterm_score": float(course.Midterm_score) if course.Midterm_score else None,
                "Assi_score": float(course.Assi_score) if course.Assi_score else None,
                "Prac_score": float(course.Prac_score) if course.Prac_score else None,
                "Q_points": float(course.Q_points) if course.Q_points else None,
                "Grade": course.Grade,
                "DISCIPLINE": course.DISCIPLINE,
                "SOS": course.SOS,
                "CrsSemNo": course.CrsSemNo,
            }
            course_list.append(course_data)

        # Close the session
        db.close()

        # Return the list of courses as JSON
        return jsonify({"data": course_list}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500




def get_Fail_courses_by_reg():
    try:
        # Get the registration number and semester number from the request arguments
        reg_no = request.args.get("reg_no")


        # Ensure the registration number is provided
        if not reg_no:
            return jsonify({"error": "Registration number (reg_no) is required"}), 400

        # Create a database session
        db = Session()

        # Query the Crsdtl table to find all courses for the student
        courses = db.query(Crsdtl).filter(
            and_(Crsdtl.REG_NO == reg_no, Crsdtl.Grade == 'F')
        ).all()

        # Serialize the course data into a list of dictionaries
        course_list = []
        for course in courses:
            course_data = {
                "Course_no": course.Course_no,
                "ATTEMPT_NO": course.ATTEMPT_NO,
                "SEMESTER_NO": course.SEMESTER_NO,
                "SECTION": course.SECTION,
                "Final_score": float(course.Final_score) if course.Final_score else None,
                "Midterm_score": float(course.Midterm_score) if course.Midterm_score else None,
                "Assi_score": float(course.Assi_score) if course.Assi_score else None,
                "Prac_score": float(course.Prac_score) if course.Prac_score else None,
                "Q_points": float(course.Q_points) if course.Q_points else None,
                "Grade": course.Grade,
                "DISCIPLINE": course.DISCIPLINE,
                "SOS": course.SOS,
                "CrsSemNo": course.CrsSemNo,
            }
            course_list.append(course_data)

        # Close the session
        db.close()

        # Return the list of courses as JSON
        return jsonify({"data": course_list}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

