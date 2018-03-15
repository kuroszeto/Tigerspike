"""
**Created on 2018-03-15 17:12:08**

***@author: Wai***

RUN module for automated testing exercise
"""

import unittest
import logging
import datetime
import argparse
from test import EbayNavigationTestSuite


def main():
    """*Running the test suite(s)*

    """
    start_time = datetime.datetime.now()
    args = get_cli_parameter()
    selenium_logger = logging.getLogger('selenium.webdriver.remote.remote_connection')
    # Only display possible problems
    selenium_logger.setLevel(logging.WARNING)
    logging.basicConfig(filename='EbayNavigationTest.log', filemode='w', level=logging.DEBUG)
    logging.debug(str(datetime.datetime.now()) + " Running Ebay Navigation Test Cases ")
    logging.debug(str(datetime.datetime.now()) + " ************* Starting **************")
    # Create Test Suite
    suite = unittest.TestSuite()
    logging.debug(str(datetime.datetime.now()) + ' Created TestSuite')
    ebay_navigation_test_suite = EbayNavigationTestSuite.suite(args)
    suite.addTests(ebay_navigation_test_suite)
    unittest.TextTestRunner().run(suite)
    logging.debug(str(datetime.datetime.now()) + " ************* Test Completed **************")

def get_cli_parameter():
    """*Get all the parameters entered by the user*

    :returns: **args -** The values of all the parameters
    """
    parser = argparse.ArgumentParser(__file__, description="Test Input")
    parser.add_argument("--driver", "-d", help="Desired webdriver", type=str, default="firefox")

    return parser.parse_args()

if __name__ == '__main__':
    main()
