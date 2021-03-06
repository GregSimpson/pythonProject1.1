from unittest import TestCase
from app import create_app

import logging
logger = logging.getLogger("RealplaySync")

class TestWelcome(TestCase):
    def setUp(self):
        self.app = create_app().test_client()

    def test_welcome(self):
        """
        Tests the route screen message
        """
        rv = self.app.get('/api/')
        ##logger.info(" running api test_welcome ")
        #print(rv.get_json())

        # If we recalculate the hash on the block we should get the same result as we have stored
        self.assertEqual({"message": 'Hello Welcome Model !'}, rv.get_json())


    def test_auth0_sync(self):
        """
        Tests the route screen message
        """
        #print (" running test_auth0_sync ")
        ##logger.info(" running test_auth0_sync ")
        rv = self.app.get('/api/auth0_sync/')
        #print("\n\t\tgjs >>> " )
        #print ( rv.get_json() )

        # If we recalculate the hash on the block we should get the same result as we have stored
        ####self.assertEqual({"auth0_sync": 'auth0_sync Model!'}, rv.get_json())

    def test_async_example(self):
        """
        Tests the route screen message
        """
        #print (" running test_async_example ")
        ##logger.info(" running test_async_example ")
        rv = self.app.get('/api/async_example/')
        #print("\n\t\tgjs >>> " )
        #print ( rv.get_json() )

        # If we recalculate the hash on the block we should get the same result as we have stored
        self.assertEqual({"async_example": 'async_example'}, rv.get_json())

    def test_auth0_async(self):
        """
        Tests the route screen message
        """
        #print (" running test_auth0_async ")
        ##logger.info(" running test_auth0_async ")
        rv = self.app.get('/api/auth0_async/')
        #print("\n\t\tTODAY gjs >>> " )
        #print ( rv.get_json() )

        # If we recalculate the hash on the block we should get the same result as we have stored
        self.assertEqual({"auth0_async": 'auth0_async'}, rv.get_json())




'''
    def logtest(self):
        """
        Tests the route screen message
        """
        #print (" running test_async_example ")
        logger.info(" running log_test ")
        rv = self.app.get('/api/logtest/')
        #print("\n\t\tgjs >>> " )
        #print ( rv.get_json() )

        # If we recalculate the hash on the block we should get the same result as we have stored
        ##self.assertEqual({"async_example": 'async_example'}, rv.get_json())
'''



