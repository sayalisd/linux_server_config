IP Address:SSH port - 13.232.88.71:2200

URL - http://13.232.88.71/

S/ws installed are: modules of python(flask, sqlalchemy, oauth2client, requests, jsonpickle, flask_sqlalchemy,python-psycopg2), postgresql, apache, mod_wsgi
heroku

This project is about hosting web application on Linux server. For this, I have used Amazon Lighsail services to create ubuntu linux server. I have created lightsail instance. I updated firewall settings to access ssh on 2200 port, as well http port 80. ufw settings are updated accordingly. Also postgresql is installed and database,catalog, is created to access database services with web. Web services are used by installing apache. WSGI application is used to communicate between web server and web application.
