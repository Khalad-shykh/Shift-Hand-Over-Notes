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

There are 2 tests, as required by the brief:

1. `test_add_note` — creating a valid note returns `201` with
   the correct fields, and confirms the severity keyword matching works
   (the body mentions "safeguarding," so it should come back `"high"`).
2. `test_add_note_failed` — a note missing `home_id`
   is rejected with `400`, and the error message names the missing field.

## Design choices

* **One file, using functions instead of classes.** The assignment is small, so using multiple files or classes would add unnecessary complexity.
* **Validation is in a separate function** (`validate_note_payload`). This keeps the route simple and makes the validation easier to test and understand.
* **Severity is handled by a separate function** (`determine_severity`). This keeps all the severity keywords in one place, so they can be easily changed later.
* I treated a body with only spaces as empty because a note like `"   "` is not useful.
* **Severity matching checks whole words.** For example, `"fall"` will be detected, but `"waterfall"` or `"footfall"` will not. This avoids incorrect high-severity results.
* **`home_id` is compared as a string** because query parameters are received as strings, while the JSON body could contain either a number or a string.

## What I found difficult / worth flagging

* The brief doesn't clearly define the format of `home_id`, so I allowed it to be either a number or a string.
* I had to decide how to handle an empty body. I treated both an empty string and whitespace-only text as empty.
* I also had to decide how to match severity keywords. At first, I used simple substring matching, but `"waterfall"` incorrectly matched `"fall"`. I changed this to whole-word matching using regex.

## What I'd do with more time

* Add more edge-case tests for invalid data types, invalid JSON, `home_id` filtering, and the 404 case.
* Add **data type validation** for fields such as `home_id`, `body`, and other request values to make sure the API receives the expected types.
* Add **text validation for the `body`** to make sure it contains meaningful text instead of only special characters like `...`, `,,,`, or `!!!`.
* Add pagination or sorting to `GET /notes` if the number of notes becomes large.
* Move the severity keywords and validation rules into a configuration file so they can be changed more easily.
* Add a `PATCH /notes/<id>` endpoint to allow notes to be updated.


## AI tooling note

I used Claude to create the initial Flask routes and pytest test file.

Claude initially used simple substring matching for severity. This caused `"waterfall"` to incorrectly trigger high severity because it contains `"fall"`. I asked for this to be changed to whole-word matching using regex.

I also rewrote the README myself to make sure it reflects the decisions I actually made and can explain them clearly.
