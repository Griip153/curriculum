# Persistence helpers - load/save the students list to a JSON file on disk.
# See LESSON.md Step 5.

import json
import os

FILE_PATH = "students.json"


def load_students():
    if not os.path.exists(FILE_PATH):
        return []
    with open(FILE_PATH, "r") as f:
        return json.load(f)


def save_students(students):
    with open(FILE_PATH, "w") as f:
        json.dump(students, f, indent=2)
