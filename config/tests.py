from django.test import TestCase
from utils.args_utils import kwargs_id_creator
# Create your tests here.


class RouteTest(TestCase):
    def test_route(self):
        d = kwargs_id_creator(company="bienfait", user=2)
        print("oura test here", d)
