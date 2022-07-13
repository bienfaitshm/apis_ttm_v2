from django.test import TestCase

from ..services import reservations_services as rs


class ReservationTests(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_create_pnr(self):
        print("Test pnr")
        pnr = rs.create_pnr()
