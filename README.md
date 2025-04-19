Testing instructions:

Clone this repository to your own machine and go to its root folder. Create an .env file in the folder and set its contents as follows:


DATABASE_URL=<tietokannan-paikallinen-osoite>
SECRET_KEY=<salainen-avain>

Next, activate the virtual environment and install the application dependencies with the commands:

$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r ./requirements.txt

Also define the database schema with the command

$ psql < schema.sql

Initialize the database, add users with the command

$ python3 initialize_db.py

Now you can launch the application with the command

$ flask run

