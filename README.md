# Project Director

## Summary
Project Director is platform for where requests for information or RFIs or more easily tracked and created. It is split into two seperate parts the backend and the frontend. The backend uses Django, and the frontend uses Nextjs.

## Getting Start
To build and run the project you will need Docker 4.4.3 and Docker Compose 3.8. So, after cloning the repo you will also need to add these two .env files to the root of the
project directory with the values at the top filled out.

#### Environment variables for dev build: [.env.dev](https://github.com/Caleb646/Project-Director/files/7891935/default.env.dev.txt)
#### Environment variables for staging build: [.env.staging](https://github.com/Caleb646/Project-Director/files/7891962/default.env.staging.txt)

Change the names to .env.dev and .env.staging, making sure to also remove the file extension, .txt, as well.

### Development Mode
Development mode starts the backend at localhost:8000 and the frontend at localhost:3000 using the Django and Nextjs dev servers. This mode will work with both Django and Nextjs hot code reload features. To build and run the Docker container in this mode run the cmd: ./dev-build.bat.

### Staging Mode

In staging mode the backend will still be at localhost:8000, but it will be ran on a uWSGI server. The frontend will still be at localhost:3000, but running on a node server. Also, there is now a Nginx server. It sits in front of the two proxying requests to each, and it is hosted at localhost:8080.  To build and run the Docker container in this mode run the cmd: ./dev-staging.bat.
