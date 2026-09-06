# Shift Handover Notes API

A small Flask API for recording care-home shift handover notes and flagging
the ones that need attention.

## What it does

- `POST /notes` — create a note. Requires `home_id`, `author`, `body` (all
  non-empty). Returns the created note with a `201`.
- `GET /notes` — list all notes.
- `GET /notes?home_id=<id>` — list notes for a single home.
- `GET /notes/<id>` — fetch one note, or `404` if it doesn't exist.
- Every note is automatically tagged `severity: "high"` if its body mentions
  **fall**, **medication**, or **safeguarding** (case-insensitive).
  Otherwise it's `"low"`.

Notes are kept in a plain Python list in memory — there's no database, so
everything resets when the app restarts. That's intentional, per the brief.

## How to run it

### macOS / Linux

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

### Windows (Command Prompt)

```cmd
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
python app.py
```

> **Note:** Run `pip install -r requirements.txt` once after creating and activating the virtual environment. This installs Flask and the other required dependencies. You do not need to run it again every time you start the application, unless the dependencies change or you create a new virtual environment.

Once running, the API is available at `http://127.0.0.1:5000`.

## Trying it out

### In Postman

1. Create a new request, set the method to `POST`.
2. URL: `http://127.0.0.1:5000/notes`
3. Go to the **Body** tab → select **raw** → choose **JSON** from the
   dropdown on the right.
4. Paste in a note, for example:
   ```json
   {
     "home_id": "home-1",
     "author": "Mark Henry",
     "body": "Resident is on his medication."
   }
   ```
5. Hit **Send**. You should get a `201` response with the created note,
   including its `id` and `severity`.
6. To test the validation, remove `body` from the JSON and send again —
   you should get a `400` with a message naming the missing field.
7. For the `GET` endpoints, create a new request with method `GET` and the
   URL `http://127.0.0.1:5000/notes` (no json body needed).
   URL `http://127.0.0.1:5000/notes/1` (no json body needed).
   URL `http://127.0.0.1:5000/notes?home_id=home-1` (no json body needed).

### With curl (Secondary Option to Try it out)

```cmd
curl -X POST http://127.0.0.1:5000/notes ^
  -H "Content-Type: application/json" ^
  -d "{\"home_id\": \"home-1\", \"author\": \"Mark Henry\", \"body\": \"Resident is on his medication.\"}"

curl http://127.0.0.1:5000/notes

curl http://127.0.0.1:5000/notes/1

curl http://127.0.0.1:5000/notes?home_id=home-1
```

## How to run the tests

```cmd
pytest test_app.py -v
```
