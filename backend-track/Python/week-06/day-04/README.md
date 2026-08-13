# Day 24 — File Uploads & Emails

## Objective
Handle two things almost every real API needs: accepting a file from a client, and
sending an email from the server.

## Concepts
`UploadFile`/`File()`; validating file type and size; saving uploads to disk (or a
cloud store); sending email with `fastapi-mail`; using a free testing inbox
(Mailtrap) so you never accidentally email a real person while developing.

## Watch before the session
- FastAPI official docs — "Request Files" page
- "Send Emails with FastAPI" — Tech With Tim or similar
- Mailtrap docs — "Getting Started" quickstart

## Task of the day
Add `POST /students/{id}/photo` to upload and store a profile photo (validating type
and size), and send a welcome email via Mailtrap when a new user registers. Full
step-by-step instructions are in `LESSON.md`.

---
*Done? Submit your daily report in the `daily-reports` repo before midnight.*
