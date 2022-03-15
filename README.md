# Assignment 4
## REST API connected to database

<br>

### Objective
Learn how to connect a RESTful API to persistent storage. Use an ORM library like SQLAlchemy to simplify database retrieval. Develop error handling code to handle unexpted user input.
<br>

### Instructions
Create a REST API using Python Flask and connect it to a PostgreSQL database. The API will keep track of simple notes from its users.
- Store data on two separate tables -- user and note
- Notes from a user are not accessible to other users
- Return appropriate HTTP status code and message whether it was successful or not
- Authenicate with a token

<br>

### API calls to complete

<br>

| Method | URL | Action |
| ------ | --- | ------ |
| POST | /user/ | Add a new user |
| DELETE | /user/{id}/ | Delete user with specified {id} |
| GET | /login | Login username and password in payload and return a token |
| GET | /user/{id}/note/ | Retrieve all notes for a particular user |
| GET | /user/{id}/note/:id | Retrieve the note for the matching note :id |
| GET | /user/{id}/note/:title | Retrieve the note with the specified :title |
| PUT | /user/{id}/note/:id | Update note with the specified :id |
| PUT | /user/{id}/note/:title | Update note with the specified :title |
| POST | /user/{id}/note | Add a new note |
| DELETE | /user/{id}/note/:id | Delete note with specified :id |