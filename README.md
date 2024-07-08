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

### Database

1. Access the database portal by navigating to localhost:8081 to check the database and track log events.

### Worker

1. Access a running Worker by navigating to [localhost:5555](http://localhost:5555).
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

After research, this link provides the best solution.
https://unix.stackexchange.com/questions/433444/cant-run-script-file-in-docker-no-such-file-or-directory