# flock-tagg

Build for an Internal Hackathon on the FlockOS platform

The app is basically a tagging feature where any type of communication on Flock can be tagged with meta info.

For example a shared log file can have a LOG tag, making it easy to find.

These tags are attached to the message throughout it's lifecycle. Tags can even be carry forwarded and/or edited when forwarding the messages.

The feature make's information more manageable on Flock and easily searchable. 
This is the external server app which hold's the meta data info for messages.


### Setup Instructions
* pip install -r requirements.txt
* Create database and add details in local_settings.py folder.
* Configure redis and celery
* Run:  python manage.py makemigrations
* Run: python manage.py migrate
* Run celery server: celery -A webapp worker -l info
* Run redis server
* Run server: python manage.py runserver

### Tech Stack:
* Django==1.8
* psycopg2==2.5.4
* djangorestframework==3.3.2
* PostgreSQL
* Angular JS - 1.4.7
* Restangular
* Redis 2.8
* Celery 3.1

	##### UI Stack: 
    * Angular Material - 1.1.0-RC4
    * Materialize
    * CSS3
    * HTML5
