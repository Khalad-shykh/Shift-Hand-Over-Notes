import re
from flask import Flask, request, jsonify

app = Flask(__name__)

notes = []
next_id = 1

HIGH_SEVERITY_KEYWORDS = ["fall", "medication", "safeguarding"]

REQUIRED_FIELDS = ["home_id", "author", "body"]


def determine_severity(body):

    lowered = body.lower()
    for keyword in HIGH_SEVERITY_KEYWORDS:
        if re.search(rf"\b{keyword}\b", lowered):
            return "high"
    return "low"


def validate_note_payload(data):

    if not isinstance(data, dict):
        return "Request body must be a JSON object"

    for field in REQUIRED_FIELDS:
        value = data.get(field)
        if value is None or (isinstance(value, str) and value.strip() == ""):
            return f"'{field}' is required and cannot be empty"

    return None

@app.route("/", methods=["GET"])
def home():
    return "Shift Handover Notes API is running.";

@app.route("/notes", methods=["POST"])
def create_note():
    global next_id

    data = request.get_json(silent=True)

    error = validate_note_payload(data)
    if error:
        return jsonify({"error": error}), 400

    note = {
        "id": next_id,
        "home_id": data["home_id"],
        "author": data["author"],
        "body": data["body"],
        "severity": determine_severity(data["body"]),
    }
    notes.append(note)
    next_id += 1

    return jsonify(note), 201


@app.route("/notes", methods=["GET"])
def list_notes():
    home_id = request.args.get("home_id")

    if home_id is not None:
        filtered = [n for n in notes if str(n["home_id"]).strip() == home_id]
        return jsonify(filtered), 200

    return jsonify(notes), 200


@app.route("/notes/<int:note_id>", methods=["GET"])
def get_note(note_id):
    for note in notes:
        if note["id"] == note_id:
            return jsonify(note), 200

    return jsonify({"error": f"No note found with id {note_id}"}), 404


if __name__ == "__main__":
    app.run(debug=True)
