## HexOcean_recruitment
 API made using the Django Rest Framework that allows given users to add images and obtain links to these images. Task completed as part of recruitment to HexOcean.
 
## Environment set up - with docker image
1. Put in one Docker image `HexOcean_web.tar`, `Dockerfile` and `docker-compose.yml`
2. Enable the console at the file location and run the `docker load -i HexOcean_web.tar` command.
3. After executing the command, execute the `docker-compose up` command.
4. Access your web browser to `localhost:8000`. If everything went well you will see the API with DRF.

## Environment set up - without docker image
1. To set up the environment, you must have Docker installed.
2. While in the project folder, enter `docker-compose up` in the console
3. The next step is to check the project started successfully and enter the browser to the address `localhost:8000`
4. If you can see the Django screen, everything has worked out.
5. Now type `docker ps` in the console. Two processes should be displayed.
6. The next step is to enter the command `docker exec -it [CONTAINER ID]` bash.
7. After entering the server process, enter the command `python manage.py migrate` and then `python manage.py createsuperuser`.
8. After creating the user, you can go to the browser.

## API
Available addresses:
- `localhost:8000/admin/` - administration panel. Available after logging in to the superuser account.
- `localhost:8000` - displays links to images of the currently logged in user
- `localhost:8000/[image id]?t=[time until expiration]`- address for generating an expiring link by users whose tier allows it.

# User creating
First, create tiers in the Administration Panel and specify the possibilities for each:
Available options:
- link to the original image
- the ability to generate expiring links to the original image
- sizes of thumbnails

Then in the users tab you can create users and assign them appropriate tiers. After this operation, the created users, after logging into the API at `localhost:8000`, can add images and browse available links.

# Expiring links
Expiring links give you the opportunity to preview the image without logging in. The duration of the access ranges from 300 to 3000 seconds.

# TIERS - bulit-in
- BASIC - users get:
    - link to a thumbnail that's 200px in height

- PREMIUM - users get:
    - a link to a thumbnail that's 200px in height
    - link to a thumbnail that's 400px in height
    - link to the originally uploaded image

- ENTERPRISE - users get:
    - a link to a thumbnail that's 200px in height
    - link to a thumbnail that's 400px in height
    - link to the originally uploaded image
    - ability to fetch an expiring link to the image (the link expires after a given number of seconds (the user can specify any number between 300 and 30000))

## DEV 
Entering to virtual envoriment:
cmd: .\.venv\Scripts\activate
Docker:
1. Strting project's containers `docker-compose up`
2. Listing avaible containers `docker ps`
3. To enter containter `docker exec -it {id} bash`
 

## ACCESS to administrator panel:
# Superuser - only this one has access to admin panel
user: `root`
password: `admin123#`

## Bulit-in users(lo)
# Basic user - login only via django panel
username/password: `user_b`
password: `admin123#`

# Premium user
username/password: `user_p`
password: `admin123#`

# Enterprise user
username/password: `user_e`
password: `admin123#`
=======
# HexOcean_recruitment
 API made using the Django Rest Framework that allows given users to add images and obtain links to these images. Task completed as part of recruitment to HexOcean.
>>>>>>> parent of 9df6059 (Docker images + README edit)
