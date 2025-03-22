# # class studentController:
# #     @staticmethod
# #     def get_student_by_id():
# #
#
# @app.route('/signup', methods=['POST'])
# def signup():
#     data = request.json
#     username = data.get('username')
#     email = data.get('email')
#     reg_no = data.get('reg_no')
#     password = data.get('password')
#
#     # Check if user already exists
#     if fetch_user_by_email(email):
#         return jsonify({"message": "Email already registered"}), 400
#
#     if fetch_user_by_reg_no(reg_no):
#         return jsonify({"message": "Registration number already registered"}), 400
#
#     # Hash the password
#     hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
#
#     # Insert user into the database
#     query = "INSERT INTO Users (username, email, reg_no, password) VALUES (?, ?, ?, ?)"
#     db.execute(query, (username, email, reg_no, hashed_password))
#     conn.commit()
#
#     return jsonify({"message": "User registered successfully"}), 201
#
#
