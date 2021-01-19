# Twitter Pipeline

## About

This project contains a full stack, deployable Twitter pipeline for the real-time collection of tweets based on a key word or words. The application is built using Python and deployed on Amazon Web Services.

## Using This Repo

In order to use this repository, please follow the steps outlined below:

1. Fork the Repo to your personal GitHub account.
2. Clone this repository to your local machine `git clone https://github.com/mattsunner/tweet-pipeline.git`.
3. Install all needed dependencies contained in the requirements.txt file using `pip install -r requirements.txt`.
4. Create a config.cfg file. Add in the following format:

   [twitter] \
   consumer_key = XXXXXXXXXXXXX \
   consumer_secret = XXXXXXXXXXXXXX \
   access_token = XXXXXXXXXXXXXXXX \
   access_token_secret = XXXXXXXXXX

5. Create a .env file. Using the format below, fill out the applicable fields for your MySQL database connection.

   HOST=XXXXXXX \
   USER=XXXXXXX \
   PASSWORD=XXXXXXXX \
   DB=XXXXXXX

6. Create a MySQL Schema for the database. Update the name of the schema throughout the pipeline.py file.

7. Update the `track=["python]` in the main() function of pipeline.py to reflect the term or terms that should be streamed.

## Tech Stack Used

- Pipeline functionality: Python
- Server-Side Hosting: AWS
- Data Storage: AWS RDS - MySQL

## Contact

If you have any questions about using this repo, feel free to reach me at matt@mattsunner.com.
