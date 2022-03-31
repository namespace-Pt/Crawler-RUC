import json
import random
import requests
from bs4 import BeautifulSoup



class VRUCCrawler():
    def __init__(
            self,
            student_id,
            password
        ):
        login_url = "https://v.ruc.edu.cn/auth/login"
        headers = self.get_headers()
        src = requests.get(login_url, headers=headers).text

        soup = BeautifulSoup(src, 'html.parser')
        csrftoken = soup.find(id='csrftoken').attrs['value']

        data = {
            "username": "ruc:" + student_id,
            "password": password,
            "redirect_uri": "https%3A%2F%2Fv.ruc.edu.cn%2Foauth2%2Fauthorize%3Fclient_id%3Daccounts.tiup.cn%26redirect_uri%3Dhttps%253A%252F%252Fv.ruc.edu.cn%252Fsso%252Fcallback%253Fschool_code%253Druc%2526theme%253Dschools%26response_type%3Dcode%26school_code%3Druc%26scope%3Dall%26state%3Du9yHOdNUROmfoNgY%26theme%3Dschools",
            "token": csrftoken,
            "twofactor_password":"",
            "twofactor_recovery":""
        }

        session = requests.Session()
        self.response = session.post(url=login_url, data=json.dumps(data), headers=headers)
        self.session = session


    def get_headers(self):
        user_agent_pool = [
            'Mozilla/5.0 (X11; CrOS i686 4319.74.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.517 Safari/537.36',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36 Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:23.0) Gecko/20131011 Firefox/23.0',
            'Mozilla/5.0 (Windows; U; Windows NT 6.0; hu-HU) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4',
        ]
        headers = {
            "User-Agent": random.choice(user_agent_pool),
            "Accept": "application/json, text/plain, */*"
        }
        return headers


    def get(self, url, headers=None, **kargs):
        if headers is None:
            headers = self.get_headers()
        return self.session.get(url, headers=headers, **kargs)


    def post(self, url, headers=None, **kargs):
        if headers is None:
            headers = self.get_headers()
        return self.session.post(url, headers=headers, **kargs)



class JWCrawler(VRUCCrawler):
    def __init__(self, student_id, password):
        super().__init__(student_id, password)
        response = super().post("https://jw.ruc.edu.cn/secService/logout?resourceCode=resourceCode&apiCode=framework.sign.controller.SignController.logout")
        redirect_uri = json.loads(response.text)["data"]
        response = super().get(redirect_uri, allow_redirects=False)
        redirect_uri = response.headers["Location"]
        response = super().get(redirect_uri)
        self.token = self.session.cookies.get_dict()["token"]


    def get_headers(self):
        user_agent_pool = [
            'Mozilla/5.0 (X11; CrOS i686 4319.74.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.517 Safari/537.36',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36 Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:23.0) Gecko/20131011 Firefox/23.0',
            'Mozilla/5.0 (Windows; U; Windows NT 6.0; hu-HU) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4',
        ]
        headers = {
            "User-Agent": random.choice(user_agent_pool),
            "Accept": "application/json, text/plain, */*"
        }
        # add TOKEN which is necessary for jw
        if hasattr(self, "token"):
            headers["TOKEN"] = self.token
        return headers


    def get_grade(self):
        headers = self.get_headers()
        headers["Content-Type"] = 'application/json'
        page = {
            "pageIndex": 1,
            "pageSize": 30,
            "orderBy": "[{\"field\":\"jczy013id\",\"sortType\":\"asc\"}]",
            "conditions": "QZDATASOFTJddJJVIJY29uZGl0aW9uR3JvdXAlMjIlM0ElNUIlN0IlMjJsaW5rJTIyJTNBJTIyYW5kJTIyJTJDJTIyY29uZGl0aW9uJTIyJTNBJTVCJTVEJTdEyTTECTTE"
        }
        data = {
            "pyfa007id": "1",
            "jczy013id": [],
            "fxjczy005id": "",
            "cjckflag": "xsdcjck",
            "page": page
        }

        response = self.post("https://jw.ruc.edu.cn/resService/jwxtpt/v1/xsd/cjgl_xsxdsq/findKccjList?resourceCode=XSMH0507&apiCode=jw.xsd.xsdInfo.controller.CjglKccjckController.findKccjList", data=json.dumps(data), headers=headers)
        return json.loads(response.text)["data"]
