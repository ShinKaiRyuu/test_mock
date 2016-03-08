import vcr

import time
from pretenders.client.http import HTTPMock
from pretenders.common.constants import FOREVER
from requests import get
import requests


class VCR(object):
    def __init__(self, record_mode='new_episodes', match_on=['uri', 'method'], serializer='json',
                 cassette_library_dir='cassettes'):
        self.vcr = self.config_vcr(record_mode, match_on, serializer,
                                   cassette_library_dir)

    def config_vcr(self, record_mode='new_episodes', match_on=['uri', 'method'], serializer='json',
                   cassette_library_dir='cassettes'):
        my_vcr = vcr.VCR(
            serializer=serializer,
            cassette_library_dir=cassette_library_dir,
            record_mode=record_mode,
            match_on=match_on,
        )
        return my_vcr

    def get_with_cassette(self, path_to_cassette, url_to_open):
        with self.vcr.use_cassette(path_to_cassette):
            resp = requests.get(url_to_open)
        return resp

    def delete_with_cassette(self, path_to_cassette, url_to_open):
        with self.vcr.use_cassette(path_to_cassette):
            resp = requests.delete(url_to_open)
        return resp

    def post_with_cassette(self, path_to_cassette, url_to_open, body):
        with self.vcr.use_cassette(path_to_cassette):
            resp = requests.post(url_to_open, body)
        return resp

    def patch_with_cassette(self, path_to_cassette, url_to_open, body):
        with self.vcr.use_cassette(path_to_cassette):
            resp = requests.patch(url_to_open, body)
        return resp


mock = HTTPMock('localhost', 8888, timeout=20, name="zingfit_api")

mock.reset()
mock.when("GET /important_data$").reply(bytes('{"account": "10000", "outstanding": "10.00"}'), status=200,
                                        times=FOREVER)
mock.when("GET /important_data2$").reply(bytes('ERROR'), status=500, times=FOREVER)
mock.when("GET /important_data3$").reply(bytes('OK'), status=200, times=FOREVER)
mock.when("POST /important_data4$", body='{"account": "10000", "outstanding": "10.00"}').reply(bytes('{"id": "10"}'),
                                                                                               status=200,
                                                                                               times=FOREVER)

start_time = time.time()
vcr_new = VCR()
# res = open_with_cassette(vcr_new, 'iana.json', 'http://www.iana.org/domains/reserved')
# assert 'Example domains' in res
print("--- %s seconds ---" % (time.time() - start_time))
start_time = time.time()
res = vcr_new.get_with_cassette('mock.json', 'http://localhost:8888/mockhttp/zingfit_api/important_data')
print("--- %s seconds ---" % (time.time() - start_time))
print(res)
start_time = time.time()
res = vcr_new.get_with_cassette('mock.json', 'http://localhost:8888/mockhttp/zingfit_api/important_data2')
print("--- %s seconds ---" % (time.time() - start_time))
print(res)
start_time = time.time()
res = vcr_new.get_with_cassette('mock.json', 'http://localhost:8888/mockhttp/zingfit_api/important_data3')
print("--- %s seconds ---" % (time.time() - start_time))
print(res)
start_time = time.time()
res = vcr_new.post_with_cassette('mock.json', 'http://localhost:8888/mockhttp/zingfit_api/important_data4',
                                 '{"account": "10000", "outstanding": "10.00"}')
print("--- %s seconds ---" % (time.time() - start_time))
print(res)
