import os
import requests


class IAMClient:
    def __init__(self):
        self.base_url = "https://iet-ws.ucdavis.edu/api/iam"
        self.base_params = {"v": "1.0", "key": os.environ["IAM_KEY"]}

    def get_email_by_student_id(self, sid):
        url = f"{self.base_url}/people/search"
        result = self.__get(url, {"studentId": sid})
        return result["campusEmail"] if result else ""

    def get_user_by_login(self, login):
        url = f"{self.base_url}/people/prikerbacct/search"
        iam_id = self.__get(url, {"userId": login})["iamId"]

        person = self.get_person_by_iam_id(iam_id)
        department = self.get_department_by_iam_id(iam_id)

        user = {
            "first_name": person["dFirstName"],
            "last_name": person["dLastName"],
            "email": person["campusEmail"],
            "department": department["deptDisplayName"],
        }

        return user

    def get_person_by_iam_id(self, iam_id):
        url = f"{self.base_url}/people/{iam_id}"
        return self.__get(url)

    def get_department_by_iam_id(self, iam_id):
        url = f"{self.base_url}/associations/odr/{iam_id}"
        return self.__get(url)

    def __get(self, url, params=None):
        if params is None:
            params = {}

        try:
            merged_params = {**self.base_params, **params}
            response = requests.get(url, merged_params)
            response.raise_for_status()
            return response.json()["responseData"]["results"][0]
        except IndexError:
            return None
        except requests.exceptions.HTTPError as errh:
            print(f"HTTP Error: {errh}")
        except requests.exceptions.ConnectionError as errc:
            print(f"Error Connecting: {errc}")
        except requests.exceptions.Timeout as errt:
            print(f"Timeout Error: {errt}")
        except requests.exceptions.RequestException as err:
            print(f"Other Error: {err}")
