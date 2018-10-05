import unittest
import sys
sys.path.append('..')
from api import app, TODOS


class TestIntegrations(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_get(self):
        response = self.app.get()
        if TODOS == {}:
            self.assertEqual(response.data, '"No Todos yet"\n')
        else:
            self.assertEqual(response.data, TODOS)

    def test_get_single(self, todo_id=1):
        response = self.app.get('/<string:todo_id>')
        if TODOS == {}:
            self.assertEqual(response.data, '"No Todo exists with that ID"\n')
        else:
            self.assertEqual(response.data, {todo_id: TODOS[todo_id]})


