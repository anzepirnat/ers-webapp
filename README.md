# ERS WebApp

Application used to assess the AI generated explanations of the recommendation system.

To run docker container, be in the same directory as the .env file and use:
sudo docker run --env-file .env -p 8000:8000 ersapp-v1

To run the app locally, use:
python manage.py runserver 0.0.0.0:8000

Datbase is running on AWS RDS: rds-instance-1.c1kscoawsrlb.eu-central-1.rds.amazonaws.com
