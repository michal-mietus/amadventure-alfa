from django.test import TestCase
from ...models.location import Location


class TestLocation(TestCase):
    def setUp(self):
        self.location = Location.objects.create(name='town')
        self.location.save()

    def test_location_string_representation(self):
        str_repr = "Location " + self.location.name
        self.assertEqual(str(self.location), str_repr)
