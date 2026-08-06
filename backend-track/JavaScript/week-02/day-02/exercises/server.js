// Raw HTTP server — today's big assignment, built one small step at a time.
// GET /health is SOLVED — worked together in the session, see LESSON.md.
// Everything else is your TODO. Do the steps IN ORDER — each one builds on the last.
// Full instructions (with hints) for every step are in LESSON.md, section "Your Turn".
//
// Built with Node's built-in `http` module — no Express. The point is to feel what
// Express saves you: manual routing, manual headers, manual JSON, manual persistence.
//
// Run: npm run dev   (nodemon, auto-restarts on save — you write this script, Step 6)
//   or: npm start    (plain node, no auto-restart)

const http = require("http");
// TODO Step 3: const fs = require("fs");
// TODO Step 3: const path = require("path");
// TODO Step 5: const os = require("os");

const PORT = 3000;
const startedAt = Date.now();

// Seed data — what the server uses the very first time it runs, before Step 3 wires
// up real persistence. After Step 3, this array only matters if data/students.json
// doesn't exist yet.
let students = [
  { id: 1, name: "Ada", score: 91 },
  { id: 2, name: "Kofi", score: 68 },
  { id: 3, name: "Zara", score: 84 },
];

function sendJson(res, statusCode, data) {
  res.writeHead(statusCode, { "Content-Type": "application/json" });
  res.end(JSON.stringify(data));
}

const server = http.createServer((req, res) => {
  // ----- SOLVED: GET /health -----
  if (req.method === "GET" && req.url === "/health") {
    const uptimeSeconds = Math.floor((Date.now() - startedAt) / 1000);
    sendJson(res, 200, { status: "ok", uptime: uptimeSeconds });
    return;
  }

  // ----- TODO Step 1: GET /students — list everyone -----
  // Respond 200 with { students }. Same shape as /health above: check
  // req.method + req.url, then sendJson(res, 200, { students }), then return.

  // ----- TODO Step 2: GET /students/:id — one student -----
  // The URL looks like "/students/2" — there's no built-in route param here like
  // Express has, so split the string yourself:
  //   const parts = req.url.split("/");   // ["", "students", "2"]
  // Only treat this as a match when req.method is GET, parts[1] === "students",
  // and parts.length === 3 (so it doesn't also match plain "/students" above).
  // Look up Number(parts[2]) in `students`. Found -> 200 with that student.
  // Not found -> 404 with { error: "Student not found" }.

  // ----- TODO Step 3: persist `students` to disk -----
  // This step's code goes at the TOP of the file, not inside the request handler:
  //   1. require("fs") and require("path") (uncomment the lines near the top).
  //   2. const dataDir = path.join(__dirname, "data");
  //      const dataFile = path.join(dataDir, "students.json");
  //   3. If dataFile exists (fs.existsSync), replace the seed `students` array with
  //      JSON.parse(fs.readFileSync(dataFile, "utf-8")).
  //   4. If it doesn't exist yet: fs.mkdirSync(dataDir, { recursive: true }), then
  //      fs.writeFileSync(dataFile, JSON.stringify(students, null, 2)).
  // Then write a tiny helper, saveStudents(), that re-runs the writeFileSync line —
  // call it from Step 4 every time `students` changes, so changes survive a restart.

  // ----- TODO Step 4: POST /students — add a new student -----
  // There's no express.json() here, so the request body arrives in pieces over time.
  // Collect it yourself, then parse and respond only once it's fully arrived:
  //   let body = "";
  //   req.on("data", (chunk) => { body += chunk; });
  //   req.on("end", () => {
  //     const newStudent = JSON.parse(body);       // expects { name, score }
  //     newStudent.id = students.length + 1;
  //     students.push(newStudent);
  //     saveStudents();                             // from Step 3
  //     sendJson(res, 201, newStudent);
  //   });
  //   return;   // stop here — the response above happens later, inside "end"
  // Careful: sendJson must be called INSIDE the "end" callback, not after it — the
  // body hasn't arrived yet by the time the outer function reaches that line.

  // ----- TODO Step 5: GET /system-info — about this machine -----
  // Respond 200 with { platform, cpuCount, totalMemoryMB }, using os.platform(),
  // os.cpus().length, and Math.round(os.totalmem() / 1024 / 1024).

  sendJson(res, 404, { error: "Not found" });
});

server.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});
