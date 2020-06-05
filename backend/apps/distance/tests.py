from unittest.mock import patch, Mock

from django.test import SimpleTestCase, TestCase, RequestFactory, Client

from .utils import read_query_params


class UtilsTest(SimpleTestCase):
    def test_read_empty_params(self):
        request = RequestFactory().get('/distance/')
        self.assertEqual(len(read_query_params(request, 'a', 'b')), 0)

    def test_read_wrong_params(self):
        request = RequestFactory().get('/distance/?a=1&b=2')
        result = read_query_params(request, 'c', 'b')
        self.assertEqual(result, ['2'])

    def test_read_less_params(self):
        request = RequestFactory().get('/distance/?a=1')
        result = read_query_params(request, 'a', 'b')
        self.assertEqual(result, ['1'])

    def test_read_params(self):
        request = RequestFactory().get('/distance/?a=1&b=2')
        result = read_query_params(request, 'a', 'b')
        self.assertEqual(result, ['1', '2'])


class DistanceCalculationTest(SimpleTestCase):
    def setUp(self):
        self.client = Client()

    def test_no_params_request(self):
        responce = self.client.get('/distance/').json()
        self.assertEqual('error', responce['status'])

    def test_not_all_required_params_request(self):
        responce = self.client.get('/distance/?lng2=5').json()
        self.assertEqual('error', responce['status'])

    def test_wrong_value_params_request(self):
        responce = self.client.get('/distance/?lat1=1&lng1=1&lat2=1&lng2=char').json()
        self.assertEqual('error', responce['status'])

    @patch('apps.distance.views.geodesic')
    def test_valid_params_request(self, geo_mock):
        geo_mock.return_value = Mock(miles=1, kilometers=2)
        responce = self.client.get('/distance/?lat1=1&lng1=1&lat2=2&lng2=2').json()
        self.assertEqual('ok', responce['status'])
        self.assertEqual(1, responce['data']['ml'])
        self.assertEqual(2, responce['data']['km'])


class SaveDistanceTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_invalid_schema(self):
        responce = self.client.post('/distance/', content_type='application/json', data = {'random': 'value'})

        self.assertEqual(responce.status_code, 400)


    def test_valid_schema(self):
        responce = self.client.post('/distance/', content_type='application/json',
                                    data = {'start': 'kyiv', 'end': 'horenychi', 'kilometers': 1, 'miles': 2})

        self.assertEqual(responce.status_code, 201)
