from django.test import TestCase
from ...models import Location, Action


class TestAction(TestCase):
    def setUp(self):
        self.location = Location.objects.create(name='town')
        self.location.save()
        self.action = Action.objects.create(name='quest', location=self.location)
        self.action.save()
        
    def test_action_string_representation(self):
        str_repr = "Action " + self.action.name
        self.assertEqual(str(self.action), str_repr)

