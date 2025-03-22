# import re
# from flask import Flask, jsonify, request
# import pyodbc
# from flask_cors import CORS
# import jwt  # Ensure you have the correct import for PyJWT
# import datetime
#
# app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
#
# SECRET_KEY = "1a2a3a"  # Replace this with a secure key
#
# ########################################### STudent SignUp/Login ##########################################
#
# @app.route('/login', methods=['POST'])
# def login():
#     try:
#         # Parse incoming JSON data
#         data = request.get_json()
#         reg_no = data.get('reg_no')
#         password = data.get('password')
#         print(f"Received request body: {data}")
#         # Input validation: Check if reg_no or password is empty
#         if not reg_no or not password:
#             return jsonify({"message": "Registration number and password are required.", "status": "failure"}), 400
#         # SQL query to check user credentials (Fetch only required columns)
#         query = "SELECT Reg_No, Password FROM STMTR WHERE REG_NO = ? AND Password = ?"
#         params = (reg_no, password)
#         try:
#             # Fetch user data from the database
#             user = get_sql_data(query, params)
#             if not user:
#                 return jsonify({"message": "Invalid registration number or password.", "status": "failure"}), 401
#         except Exception as e:
#             return jsonify({"message": "Database error occurred.", "status": "failure"}), 500
#         # Validate if the user exists
#         if user:  # User exists
#             payload = {
#                 "reg_no": reg_no,
#                 "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1)
#             }
#             # token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
#             token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")  # Returns a string in PyJWT v2.x
#
#             token = token.decode('utf-8')  # Ensure the token is a string
#             return jsonify({"message": "Login successful", "token": token, "status": "success"}), 200
#         else:  # No user found (invalid credentials)
#             return jsonify({"message": "Invalid registration number or password.", "status": "failure"}), 401
#     except Exception as e:
#         # Catch any unexpected error
#         print(f"Unexpected error: {e}")
#         return jsonify({"message": "An unexpected error occurred.", "status": "failure"}), 500
#
#
# @app.route('/signup', methods=['POST'])
# def signup():
#     try:
#         data = request.get_json()
#         print("Received data:", data)
#         reg_no = data.get("reg_no")
#         first_name = data.get("first_name")
#         password = data.get("password")
#         # Validate required fields
#         if not reg_no or not password or not first_name:
#             return jsonify({"message": "All fields are required.", "status": "failure"}), 400
#         # Validate Reg_No format
#         if not re.match(r'^\d{4}-ARID-\d{4}$', reg_no):
#             return jsonify({"message": "Invalid registration number format.", "status": "failure"}), 400
#         # Validate Password format
#         if not re.match(r'^\d{8}$', password):
#             return jsonify({"message": "Password must be 8 digits.", "status": "failure"}), 400
#         query_check = "SELECT COUNT(*) AS user_count FROM STMTR WHERE Reg_No = ?"
#         result = get_sql_data(query_check, (reg_no,))
#         if result and result[0]["user_count"] > 0:
#             return jsonify({"message": "User already exists.", "status": "failure"}), 409
#         # Insert new user into the database
#         query_insert = """
#         INSERT INTO STMTR (Reg_No, St_firstname, Password)
#         VALUES (?, ?, ?)
#         """
#         insertion_result = get_sql_data(query_insert, (reg_no, first_name, password), fetch_data=False)
#
#         if "error" in insertion_result:
#             return jsonify({"message": "Failed to register user.", "status": "failure"}), 500
#         return jsonify({"message": "User registered successfully.", "status": "success"}), 201
#     except Exception as e:
#         print(f"Error: {e}")
#         return jsonify({"message": "An error occurred.", "status": "failure"}), 500
#
#
# @app.route("/allCourcesDetails/<aridno>")
# def allCourcesDetails(aridno):
#     q = "SELECT * FROM Crsdtl WHERE REG_NO = ?"
#     data = get_sql_data(q, params=(aridno,), fetch_data=True)
#     if data:
#         return jsonify(data)
#     else:
#         return jsonify({"message": "No data found for the given AridNo"}), 404
#
#
# ########################################### ADMIN SIDE ##########################################
#
# # 1. Data Load API
# @app.route('/get_rules', methods=['GET'])
# def get_rules():
#     try:
#         query = "SELECT Key_Name, Type, Value FROM KnowledgeBase"
#         result = get_sql_data(query)
#
#         if "error" in result:
#             return jsonify({"message": result["error"], "status": "failure"}), 500
#
#         return jsonify({"data": result, "message": "Rules fetched successfully.", "status": "success"}), 200
#     except Exception as e:
#         print(f"Error: {e}")
#         return jsonify({"message": "An unexpected error occurred.", "status": "failure"}), 500
#
# # 2. Add Rule API
# @app.route('/add_rule', methods=['POST'])
# def add_rule():
#     try:
#         data = request.get_json()
#         key_name = data.get('Key_Name')
#         type_ = data.get('Type')
#         value = data.get('Value')
#
#         if not key_name or not type_ or not value:
#             return jsonify({"message": "All fields are required.", "status": "failure"}), 400
#
#         # Check if Key_Name already exists
#         check_query = "SELECT COUNT(*) AS count FROM KnowledgeBase WHERE Key_Name = ?"
#         result = get_sql_data(check_query, (key_name))
#
#         if result[0]['count'] > 0:
#             return jsonify({"message": "Key_Name already exists.", "status": "failure"}), 409
#
#         # Insert new rule
#         insert_query = "INSERT INTO KnowledgeBase (Key_Name, Type, Value) VALUES (?, ?, ?)"
#         result = get_sql_data(insert_query, (key_name, type_, value), fetch_data=False)
#
#         if "error" in result:
#             return jsonify({"message": result["error"], "status": "failure"}), 500
#
#         return jsonify({"message": "Rule added successfully.", "status": "success"}), 201
#     except Exception as e:
#         print(f"Error: {e}")
#         return jsonify({"message": "An unexpected error occurred.", "status": "failure"}), 500
#
# # 3. Update Rule API
# @app.route('/update_rule', methods=['PUT'])
# def update_rule():
#     try:
#         data = request.get_json()
#         key_name = data.get('Key_Name')
#         type_ = data.get('Type')
#         value = data.get('Value')
#
#         if not key_name or not type_ or not value:
#             return jsonify({"message": "All fields are required.", "status": "failure"}), 400
#
#         # Check if Key_Name exists
#         check_query = "SELECT COUNT(*) AS count FROM KnowledgeBase WHERE Key_Name = ?"
#         result = get_sql_data(check_query, (key_name,))
#
#         if result[0]['count'] == 0:
#             return jsonify({"message": "Key_Name does not exist.", "status": "failure"}), 404
#
#         # Update rule
#         update_query = "UPDATE KnowledgeBase SET Type = ?, Value = ? WHERE Key_Name = ?"
#         result = get_sql_data(update_query, (type_, value, key_name), fetch_data=False)
#
#         if "error" in result:
#             return jsonify({"message": result["error"], "status": "failure"}), 500
#
#         return jsonify({"message": "Rule updated successfully.", "status": "success"}), 200
#     except Exception as e:
#         print(f"Error: {e}")
#         return jsonify({"message": "An unexpected error occurred.", "status": "failure"}), 500
#
# # 4. Disable Rule API
# @app.route('/disable_rule', methods=['PATCH'])
# def disable_rule():
#     try:
#         data = request.get_json()
#         key_name = data.get('Key_Name')
#
#         if not key_name:
#             return jsonify({"message": "Key_Name is required.", "status": "failure"}), 400
#
#         # Check if Key_Name exists
#         check_query = "SELECT COUNT(*) AS count FROM KnowledgeBase WHERE Key_Name = ?"
#         result = get_sql_data(check_query, (key_name))
#
#         if result[0]['count'] == 0:
#             return jsonify({"message": "Key_Name does not exist.", "status": "failure"}), 404
#
#         # Disable rule (set Type to Disabled)
#         disable_query = "UPDATE KnowledgeBase SET Type = 'Disabled' WHERE Key_Name = ?"
#         result = get_sql_data(disable_query, (key_name,), fetch_data=False)
#
#         if "error" in result:
#             return jsonify({"message": result["error"], "status": "failure"}), 500
#
#         return jsonify({"message": "Rule disabled successfully.", "status": "success"}), 200
#     except Exception as e:
#         print(f"Error: {e}")
#         return jsonify({"message": "An unexpected error occurred.", "status": "failure"}), 500
#
#
# ########################################### Database Connection ##########################################
#
# server = 'DESKTOP-8TUN3M3\\SQLEXPRESS'
# database = 'biitCourseAdvisorChatbot'
# connection_string = f"DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes"
#
# def get_sql_data(query, params=None, fetch_data=True):
#     try:
#         connection = pyodbc.connect(connection_string)
#         cursor = connection.cursor()
#         # Check if params is None, and execute accordingly
#         if params is None:
#             cursor.execute(query)
#         else:
#             cursor.execute(query, params)
#
#         # For SELECT queries, fetch data
#         if fetch_data:
#             columns = [column[0] for column in cursor.description]
#             data = [dict(zip(columns, row)) for row in cursor.fetchall()]
#             return data
#         else:
#             # For INSERT/UPDATE/DELETE, commit the transaction
#             connection.commit()
#             return {"message": "Query executed successfully"}
#     except pyodbc.DatabaseError as db_error:
#         print(f"Database error: {db_error}")
#         return {"error": "Database query failed"}
#     except Exception as e:
#         print(f"General error: {e}")
#         return {"error": "An unexpected error occurred"}
#     finally:
#         print(f"Executing query: {query} with params: {params}")
#         connection.close()
#
#
#
# if __name__ == '__main__':
#     app.run('0.0.0.0',debug=True)
