# Application Overview

This application utilizes two databases and one in-memory database. It includes the necessary portals and a worker.

The main functionalities of this application are to:
- Create users
- Manage tasks
- Send emails using a dedicated worker
- Save logs in a separate database

## Running the Project

To run this project, ensure Docker is installed and running. Then, use the following command:

```
docker-compose up -d
```

## Accessing Databases and Application

### PostgreSQL (pgAdmin)

1. Open pgAdmin by navigating to [localhost:5050](http://localhost:5050).
2. Login with the credentials:
   - **Username:** `admin@admin.com`
   - **Password:** `admin`
3. Create a new server connection:
   - **Hostname:** `postgres`
   - **Port:** `5432`
   - **Username:** `admin`
   - **Password:** `admin`
4. You should now see the server with two tables: `Users` and `Tasks`.

### MongoDB

1. Access MongoDB by navigating to [localhost:8081](http://localhost:8081).
   Track the log events in the MongoDB database.

### Redis

1. Access Redis by navigating to [localhost:5555](http://localhost:5555).
2. You will see a table with fields:
   - Worker
   - Status
   - Active
   - Processed
   - Failed
   - Succeeded
   - Retried
   - Load Average
3. Tasks will be present for every event (such as sending email data).

### Application Access

1. Access the application by navigating to [localhost:5000](http://localhost:5000).
2. The login page and signup page will appear.
3. Navigate to `/task` to access the tasks page where you can edit or delete tasks.

## Project Enhancement Plans

- Implement database migrations for improved schema management.
- Upgrade MongoDB integration for better database operations.
- Ensure correct email sending functionality instead of placeholder print statements.
- Enhance error handling throughout the application using try-catch blocks.


## Windows-Specific Issue and Solution

### Problem

Users running this project on Windows might encounter an error due to Windows-style line endings in shell scripts. The error looks like this:

This happens because the script file saved with Windows line endings (`CRLF`) is interpreted incorrectly in Unix-based Docker containers.

### Solution

Save the script file with Unix-style line endings (`LF`). You can use any decent text editor (Sublime Text, Notepad++, any IDE) or a command-line tool like `dos2unix`. Here’s a step-by-step solution using Notepad++:

1. Open the script file (`scripts/docker_script.sh`) in Notepad++.
2. Go to `Edit` -> `EOL Conversion` -> `Unix (LF)`.
3. Save the file.

Alternatively, you can use `dos2unix` if you have it installed:

```sh
dos2unix scripts/docker_script.sh
