import unittest
from peewee import *

from app import TimelinePost

MODELS = [TimelinePost]

test_db = SqliteDatabase(':memory:')

class TestTimelinePost(unittest.TestCase):
    def setUp(self):
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
        test_db.connect()
        test_db.create_tables(MODELS)

    def tearDown(self):
        test_db.drop_tables(MODELS)
        test_db.close()

    def test_create_post(self):
        first_post = TimelinePost.create( name="John Does", email="john@example.com", content="Hello World!" )
        assert first_post.id == 1

        second_post = TimelinePost.create( name="Jane Does", email="jame@example.com", content="Hello World!" )
        assert second_post.id == 2

        assert TimelinePost.get( TimelinePost.id == 1 ) == first_post
        assert TimelinePost.get( TimelinePost.id == 2 ) == second_post
