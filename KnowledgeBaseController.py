from flask import jsonify, request
from Model.Configure import Session
from Model.KnowledgeBaseValue import KnowledgeBaseValue

def get_all_knowledgebase():
    """Fetch all records from the KnowledgeBase table."""
    try:
        db = Session()  # Initialize the database session
        knowledgebase_records = db.query(KnowledgeBaseValue).all()  # Query all records

        # Serialize data into a list of dictionaries
        knowledgebase_list = [
            {
                "key_name": kb.Key_Name,
                "value": kb.Value,
                "Type":kb.Type
            }
            for kb in knowledgebase_records
        ]

        db.close()
        return jsonify({"data": knowledgebase_list}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def add_knowledgebase():
    """Add a new record to the KnowledgeBase table."""
    try:
        knowledgebase_data = request.get_json()
        if not knowledgebase_data:
            return jsonify({"error": "Invalid or missing JSON payload"}), 400

        # Ensure required fields exist
        key_name = knowledgebase_data.get("key_name")
        type_value = knowledgebase_data.get("type")
        value = knowledgebase_data.get("value")
        status = knowledgebase_data.get("status", 0)

        if key_name is None or type_value is None or value is None:
            return jsonify({"error": "Missing required fields"}), 400

        # Ensure Type is correctly formatted
        type_value = int(type_value)

        # Create a new KnowledgeBase object
        new_knowledgebase = KnowledgeBaseValue(
            Key_Name=key_name,
            Type=type_value,
            Value=value,
            Status=int(status),
        )

        db = Session()
        db.add(new_knowledgebase)
        db.commit()
        db.close()

        return jsonify({"message": "KnowledgeBase record added successfully!"}), 201

    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500

def update_knowledgebase():
    """Update a record in the KnowledgeBase table based on Key_Name."""
    try:
        knowledgebase_data = request.get_json()

        # Ensure Key_Name is provided
        key_name = knowledgebase_data.get("key")
        if not key_name:
            return jsonify({"error": "key_name is required"}), 400

        db = Session()
        # Query the existing record
        knowledgebase = db.query(KnowledgeBaseValue).filter_by(
            Key_Name=key_name
        ).first()

        if not knowledgebase:
            return jsonify({"error": "KnowledgeBase record not found"}), 404

        # Update fields based on the provided data
        if "key" in knowledgebase_data:
            knowledgebase.Key_Name = knowledgebase_data["key"]
        if "value" in knowledgebase_data:
            knowledgebase.Value = knowledgebase_data["value"]

        db.commit()
        db.close()

        return jsonify({"message": "KnowledgeBase record updated successfully!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def disable_knowledgebase_rule():
    try:
        key_name = request.args.get("key_name")
        if not key_name:
            return jsonify({"error": "Key_Name is required"}), 400

        db = Session()
        knowledgebase = db.query(KnowledgeBaseValue).filter_by(Key_Name=key_name).first()

        if not knowledgebase:
            return jsonify({"error": "KnowledgeBase record not found"}), 404

        knowledgebase.Status = 1  # Disable rule
        db.commit()  # Commit transaction
        db.close()

        return jsonify({"message": f"KnowledgeBase rule '{key_name}' disabled successfully!"}), 200

    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500


def enable_knowledgebase_rule():
    try:
        key_name = request.args.get("key_name")
        if not key_name:
            return jsonify({"error": "Key_Name is required"}), 400

        db = Session()
        knowledgebase = db.query(KnowledgeBaseValue).filter_by(Key_Name=key_name).first()

        if not knowledgebase:
            return jsonify({"error": "KnowledgeBase record not found"}), 404

        knowledgebase.Status = 0  # Enable rule
        db.commit()  # Commit transaction
        db.close()

        return jsonify({"message": f"KnowledgeBase rule '{key_name}' enabled successfully!"}), 200

    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500

