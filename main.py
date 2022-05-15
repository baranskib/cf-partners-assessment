"""
Main module for the hello world HTTP server app.
"""
import datetime
from logging import debug, error
from sqlite3 import Error
from flask import Flask, jsonify, request, make_response
from database import DB

app = Flask(__name__)
db = DB()


@app.route('/hello/<username>', methods=['PUT'])
def put(username):
    """
    Saves/updates the given user’s name and date of birth in the database.
    :param username: username taken from the URL
    :return: A status code dependent on the result of the operation.
    """
    debug('Receiving a PUT request')
    try:
        # check if the username contains only alphabetic characters
        if username.isalpha():

            # read the request as json
            req = request.get_json()
            # check if dateOfBirth is one of the keys in the json dictionary
            if "dateOfBirth" not in req.keys():
                return make_response(jsonify({"error": "The request payload must contain 'dateOfBirth'"}), 400)

            # convert the dateOfBirth string into a datetime object
            try:
                date_of_birth_object = datetime.datetime.strptime(req['dateOfBirth'], '%Y-%m-%d')
                date_of_birth = date_of_birth_object.date()
            except ValueError as exception:
                error(exception)
                return make_response((jsonify({"error": "'dateOfBirth' needs to be in YYYY-MM-DD format"})), 400)

            # check if the date of birth is before today's date
            if datetime.date.today() <= date_of_birth:
                return make_response((jsonify({"error": "'dateOfBirth' needs to be a date before today's date"})), 400)

            connection = DB.connection.cursor()

            # insert or replace a user's date of birth
            query = """INSERT OR REPLACE INTO users (username, date_of_birth) VALUES ('%s', '%s') """ % (
                username, date_of_birth.strftime('%Y-%m-%d'))

            try:
                connection.execute(query)
                DB.connection.commit()
            except Error as exception:
                error(exception)
                return make_response((jsonify({"error": "Error while trying to upsert into the database"})), 501)

            return make_response((jsonify('')), 204)

        else:
            return make_response(jsonify({"error": "Username needs to be made with alphabetic characters only"}), 400)

    except Exception as exception:
        error(exception)
        return make_response(jsonify({"error": "An error occurred"}), 400)


@app.route('/hello/<username>', methods=['GET'])
def get(username):
    """
    Returns hello birthday message for the given user.
    :param username: username taken from the URL
    :return: A status code dependent on the result of the operation.
    """
    debug('Receiving a GET request')

    try:
        # setup the db connection the the query
        connection = DB.connection.cursor()

        query = """SELECT date_of_birth FROM users WHERE username = '%s'""" % username

        # create a cursor to execute the query
        cursor = connection.execute(query)

        # fetch one row
        row = cursor.fetchone()

        # check if the row is not empty
        if row is None:
            return make_response(jsonify({"error": "Username not found"}), 404)

        # get today's date
        today_date = datetime.date.today()
        # read the date of birth from the db response
        date_of_birth = datetime.datetime.strptime(row[0], '%Y-%m-%d').date()
        # calculate the next birthday date
        next_birthday = datetime.datetime(today_date.year, date_of_birth.month, date_of_birth.day).date()
        # calculate the days to birthday
        days_to_birthday = (next_birthday - today_date).days

        # if statements to determine the correct response
        if days_to_birthday > 0:
            return make_response(
                jsonify(message="Hello, {}! Your birthday is in {} day(s)".format(username, str(days_to_birthday))),
                200)
        if days_to_birthday == 0:
            return jsonify(message="Hello, {}! Happy birthday!".format(username))
        # in case the birthday has passed - take the next years date and subtract today's date from it
        else:
            next_birthday_updated = datetime.datetime(today_date.year + 1, date_of_birth.month,
                                                      date_of_birth.day).date()
            days_to_birthday_updated = (next_birthday_updated - today_date).days
            return make_response(
                jsonify(
                    message="Hello, {}! Your birthday is in {} day(s)".format(username, str(days_to_birthday_updated))),
                200)

    except Exception as exception:
        error(exception)
        return make_response(jsonify({"error": "An error occurred"}), 400)


if __name__ == '__main__':
    app.run(debug=False)
