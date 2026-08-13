# Day 6 - Raw HTTP server, no framework. See LESSON.md for the full
# step-by-step build. This file is the complete, working solution.
#
# Run: python3 server.py
# Then in another terminal:
#   curl http://localhost:8000/health
#   curl http://localhost:8000/students
#   curl -X POST http://localhost:8000/students -H "Content-Type: application/json" -d '{"name":"Bruno","score":77}'
#   curl http://localhost:8000/students/1
#   curl http://localhost:8000/system-info

import json
import platform
from http.server import BaseHTTPRequestHandler, HTTPServer

from data import load_students, save_students


class Handler(BaseHTTPRequestHandler):
    def _send_json(self, status_code, data):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/health":
            self._send_json(200, {"status": "ok"})

        elif self.path == "/students":
            students = load_students()
            self._send_json(200, {"students": students})

        elif self.path.startswith("/students/"):
            try:
                student_id = int(self.path.split("/")[-1])
            except ValueError:
                self._send_json(400, {"error": "Student id must be a number"})
                return
            students = load_students()
            match = next((s for s in students if s["id"] == student_id), None)
            if match:
                self._send_json(200, match)
            else:
                self._send_json(404, {"error": "Student not found"})

        elif self.path == "/system-info":
            info = {
                "system": platform.system(),
                "python_version": platform.python_version(),
                "machine": platform.machine(),
            }
            self._send_json(200, info)

        else:
            self._send_json(404, {"error": "Not found"})

    def do_POST(self):
        if self.path == "/students":
            content_length = int(self.headers["Content-Length"])
            body = self.rfile.read(content_length)
            new_student = json.loads(body)

            students = load_students()
            new_student["id"] = len(students) + 1
            students.append(new_student)
            save_students(students)

            self._send_json(201, new_student)
        else:
            self._send_json(404, {"error": "Not found"})


if __name__ == "__main__":
    server = HTTPServer(("localhost", 8000), Handler)
    print("Server running at http://localhost:8000")
    server.serve_forever()
