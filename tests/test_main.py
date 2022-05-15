import unittest
import main
import json
import datetime


class TestCases(unittest.TestCase):

    def setUp(self) -> None:
        main.app.testing = True
        self.app = main.app.test_client()
        self.api = "/hello/"
        self.format = "%Y-%m-%d"

    def test_1_put(self):
        data = {"dateOfBirth": "1996-08-20"}
        headers = {'content-type': 'application/json'}
        response = self.app.put(self.api + 'user', data=json.dumps(data), headers=headers)
        print("PUT - Add to database with 1996-05-05 - 204")
        self.assertEqual(204, response.status_code)

    def test_2_put(self):
        data = {"dateOfBirth": "2023-05-05"}
        headers = {'content-type': 'application/json'}
        response = self.app.put(self.api + 'user', data=json.dumps(data), headers=headers)
        print("PUT - Add to database with 2023-05-05 - 400")
        self.assertEqual(400, response.status_code)

    def test_3_get(self):
        today_date = datetime.date.today()
        date_of_birth = datetime.datetime.strptime('1996-08-20', self.format).date()
        next_birthday = datetime.datetime(today_date.year, date_of_birth.month, date_of_birth.day).date()
        days_to_birthday = (next_birthday - today_date).days
        response_message = {"message": "Hello, {}! Your birthday is in {} day(s)".format("user", str(days_to_birthday))}
        print("GET - 200")
        response = self.app.get(self.api + 'user')
        self.assertEqual(200, response.status_code)
        self.assertEqual(response_message, json.loads(response.get_data()))


if __name__ == '__main__':
    unittest.main()
