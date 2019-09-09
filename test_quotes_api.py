import requests
import pytest
import unittest
import json

"""
This class contains various method to test the rest api with url 'http://localhost:6543/quotes'
"""


class test_quotes_api(unittest.TestCase):

    # API URL
    url = 'http://localhost:6543/quotes'
    response = requests.get(url)

    # @unittest.skip
    def test_no_duplicate_sorted(self):
        """
        This methods checks wheter the response is sorted and it does not contains duplicate id.
        """
        self.reset_state()
        json_response = self.response.json()
        length_response = len(json_response['data'])

        i = 1
        while i < length_response:
            # assertLessEqual will check for sorting
            self.assertLessEqual(
                json_response['data'][i-1]['id'], json_response['data'][i]['id'], "Error: Quotes are not sorted.")
            i += 1

        j = 1
        while j < length_response:
            # assertLess will check for duplicated record
            self.assertLess(
                json_response['data'][j-1]['id'], json_response['data'][j]['id'], "Error: Quotes are duplicated.")
            j += 1

    def test_post_data(self):
        """
        This method test the post functionality of given api
        """
        self.reset_state()
        # Test the simple correct post request
        post_url = 'http://localhost:6543/quotes'
        payload = {"id": 4, "text": "I have a dream"}
        response_correct_post = requests.post('http://localhost:6543/quotes',
                                              data=json.dumps(payload))
        self.assertEqual(response_correct_post.status_code, 201,
                         "Error: Post functionality is not working.")
        self.assertEqual(response_correct_post.ok, True,
                         "Error: Post functionality is not working.")

        # Test the post with http code 400
        payload_error = {"id": 5}
        response_error_post = requests.post('http://localhost:6543/quotes',
                                            data=json.dumps(payload_error))
        self.assertEqual(response_error_post.status_code, 400,
                         "Error: Post functionality is creating incorrect quote.")
        self.assertEqual(response_error_post.ok, False,
                         "Error: Post functionality is creating incorrect quote.")

        # Check if the data is posted to server or not
        get_unique_url = 'http://localhost:6543/quotes/4'
        response_get_unique = requests.get(get_unique_url)
        self.assertEqual(response_get_unique.status_code, 200,
                         "Error: Post functionality is not working")
        self.assertEqual(response_get_unique.ok, True,
                         "Error: Post functionality is not working")

    # @unittest.skip
    def test_get_unique_quote(self):
        """
        This method test the quote get functionality with unique id
        """
        self.reset_state()
        get_unique_url = 'http://localhost:6543/quotes/1'
        response_get_unique = requests.get(get_unique_url)
        json_response = response_get_unique.json()
        # Test if text is same
        self.assertEqual(str(json_response['data']['text']),
                         'We have nothing to fear but fear itself!', "Error: Not able to fetch unique quote.")

        non_exsist_get_url = 'http://localhost:6543/quotes/20'
        response_get_non_exist = requests.get(non_exsist_get_url)
        # Test if it is there or not
        # self.assertEqual(response_get_non_exist.error, 'No such resource')
        self.assertEqual(response_get_non_exist.ok, False,
                         "Error Not able to fetch unique quote.")

    # unittest.skip
    def test_delete(self):
        """
        This method test the delete functionality of given api
        """
        self.reset_state()
        delete_url = 'http://localhost:6543/quotes/3'
        response_delete = requests.delete(delete_url)
        json_response_delete = response_delete.json()
        # Test if it is deleted
        self.assertEqual(response_delete.status_code, 200,
                         "Error: Delete functionality not working.")
        self.assertEqual(response_delete.ok, True,
                         "Error: Delete functionality not working")
        # Test if further deletion of the same object is not possible
        response_delete_again = requests.delete(delete_url)
        self.assertEqual(response_delete_again.status_code, 404,
                         "Error: Delete functionality not working.")
        self.assertEqual(response_delete_again.ok, False,
                         "Error: Delete functionality not working.")
        # Test that quote is no longer available once it is deleted
        response_get = requests.get(delete_url)
        self.assertEqual(response_get.status_code, 404,
                         "Error: Delete functionality not working.")
        self.assertEqual(response_get.ok, False,
                         "Error: Delete functionality not working.")

    def reset_state(self):
        """
        This methods reset the state of the server.
        """
        reset_url = 'http://localhost:6543/reset'
        payload = {}
        response_reset_post = requests.post(reset_url,
                                            data=json.dumps(payload))


if __name__ == '__main__':
    unittest.main()
