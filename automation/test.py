"""
**Created on 2018-03-15 17:12:08**

**@author: Wai**

TEST module for automated testing exercise

"""
import collections
import data
import unittest
import logging
import datetime
import time
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


class EbayNavigationTestCase(unittest.TestCase):
    """**Ebay Navigation test case class**
    
    :param test_name: The name of the current test
    :param test_data: Dictionary data that contains all the xpaths
    :param sequence_no: The number of current test case
    :param args: The parameters/arguments passed in by the user

    """

    def __init__(self, test_name, test_data, sequence_no, args):
        """*Initialise the Test Case Class*
        """
        super(EbayNavigationTestCase, self).__init__()
        self.test_name = test_name
        self.test_data = test_data
        self.seq = sequence_no
        self.args = args

    def setUp(self):
        """*The Set up method of the test case object*

        """
        logging.debug(str(datetime.datetime.now()) + " Start testing " + self.id())


    def runTest(self, success=True, error_message=""):
        """*The core navigation test logic*

        """
        driver = None
        try:
            # Creating the webdriver
            driver = self.initialise_driver()
            driver.maximize_window()
            driver.get(data.START_URL)
            # Start executing the test
            success, error_message = self.execute_test(driver, self.test_data)
        except Exception as e:
            # Take screenshot and quit the web driver when the test have failed unexpected
            logging.debug(str(datetime.datetime.now()) + " Unhandled exception *** FAILED ***")
            logging.debug(str(datetime.datetime.now()) + " " + str(e))
            driver.save_screenshot("Fail_" + self.id() + ".png")
            driver.quit()
            self.assertTrue(False, " Test Failed due to unhandled exception : " + str(e))

        driver.quit()
        # Check if the test have passed or not, if not then display an appropriate error message
        self.assertTrue(success, error_message)

    def execute_test(self, driver, current_test_data):
        """Perform a sequence of GUI navigation & checking 

        :param driver: Webdriver instance
        :param current_test_data: Test data for the current test case (mainly xpaths)
        :returns: **success -** Boolean which indicates if the status of current test
        :returns: **error_message -** Error message which explains the reason of the test case failed (*message will be empty if the test case passed*)
        """
        success = True
        error_message = ""
        for action in current_test_data:
            # Perform a series of GUI navigation
            if list(action)[0] == "steps" and success:
                driver, success, error_message = self.process_buttons(driver, action["steps"])
            # Check if the expected element exists on the screen
            elif list(action)[0] == "check" and success:
                driver, success, error_message = self.check_element_on_gui(driver, action["check"])
        return success, error_message

    def initialise_driver(self):
        """*Create a web driver instance*

        :returns: **driver -** A new web driver instance
        """
        logging.debug(str(datetime.datetime.now()) + " Creating Driver ...")
        driver = None
        try:
            if self.args.driver == "chrome":
                logging.debug(str(datetime.datetime.now()) + " Using Chrome Web driver")
                driver = webdriver.Chrome()
            elif self.args.driver == "phantomJS":
                logging.debug(str(datetime.datetime.now()) + " Using PhantomJS driver")
                driver = webdriver.phantomJS()
            else:
                logging.debug(str(datetime.datetime.now()) + " Using Firefox Web driver")
                driver = webdriver.Firefox()
        except WebDriverException as e:
            logging.debug(str(datetime.datetime.now()) + " WebDriverException")
            logging.debug(str(datetime.datetime.now()) + str(e))
            self.assertTrue(False, " Failed to initialise the web driver")
        return driver

    def process_buttons(self, driver, button_data,success=True, error_message=""):
        """*Perform a sequence of buttons/links clicking*

        :param driver: Web driver instance
        :param button_data: A list data structure which contains the xpath of the buttons/links
        :returns: **driver -** Current web driver instance
        :returns: **success -** Boolean which indicates if the status of current test
        :returns: **error_message -** Error message which explains the reason of the test case failed (*message will be empty if the test case passed*)
        """
        logging.debug(str(datetime.datetime.now()) + " --------Performing GUI Navigation-------")
        medium_timeout = 30
        driver.set_page_load_timeout(medium_timeout)
        # Click multiple buttons
        for steps in button_data:
            try:
                # Wait for element to show up
                WebDriverWait(driver, medium_timeout).until(EC.presence_of_element_located((By.XPATH, steps)))
                WebDriverWait(driver, medium_timeout).until(EC.visibility_of_element_located((By.XPATH, steps)))
            except TimeoutException:
                # Take a screenshot if the element cannot be found
                logging.debug(str(datetime.datetime.now()) + " TimeoutException: Unable to locate " + steps)
                driver.save_screenshot("Failed_" + self.id() + ".png")
                return driver, False, " TimeoutException: Unable to locate " + steps
            logging.debug(str(datetime.datetime.now()) + " Clicking on " + steps)
            try:
                driver.find_element_by_xpath(steps).click()
            except TimeoutException:
                logging.debug(str(datetime.datetime.now()) + " TimeoutException: The page still loading after " + str(medium_timeout) + " seconds ")
                driver.save_screenshot("Failed_" + self.id() + ".png")
                error_message = "Exception occurred, element cannot be found/clicked, please check the screenshot(Failed_" + self.id() + ".png) or log for more information"
                return driver, False, error_message
            except Exception as ex:
                logging.debug("!+!+!+!+!+!+!+!FATAL ERROR!+!+!+!+!+!+!+!")
                logging.debug(str(e))
                return driver, False, str(e)

        return driver, success, error_message


    def check_element_on_gui(self, driver, action):
        """Check if the expected element present on the screen

        :param driver: Web webdriver instance
        :param action: Test data associated with the checking process
        :returns: **driver -** Current web driver instance
        :returns: **success -** Boolean to indicates if the expected element present
        :returns: **error_message -** Error message which explains the reason of the test case failed (*message will be empty if the test case passed*)
        """
        logging.debug(str(datetime.datetime.now()) + " --------Performing GUI Element Checking-------")
        check = error_message = ""
        success = True
        try:
            for check in action.keys():
                logging.debug(str(datetime.datetime.now()) + " Looking for %s element on the screen" % check)
                WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, action[check])))
                driver.find_element_by_xpath(action[check])
            logging.debug(str(datetime.datetime.now()) + " --------GUI Checking have been completed successfully-------")
        except (NoSuchElementException, TimeoutException):
            driver.save_screenshot("Fail_" + self.id() + ".png")
            success = False
            error_message = "Checking failed, unable to locate %s element with xpath: %s" % (check, action[check])
            logging.debug(str(datetime.datetime.now()) + " " + error_message)
        return driver, success, error_message


    def id(self):
        """*The identifier of the test case object*

        :returns: A string that contains the sequence number of the test case and the name of the current test case
        """
        return str(self.seq).zfill(3) + "_Test_" + str(self.test_name)

    def tearDown(self):
        """*Do some clean up if required*
        """
        logging.debug(str(datetime.datetime.now()) + " All done")


class EbayNavigationTestSuite(unittest.TestSuite):
    """**Test suite class**

    :param unittest.TestSuite: A unittest TestSuite object
    """

    def suite(args):
        """Creating multiple test cases and adding those test cases to the suite

        :param args: The parameters/arguments passed in by the user
        :returns: A test suite which contain all the test cases
        """
        test_suite = unittest.TestSuite()
        sequence = 0
        data_set = data.EBAY_DATA
        for test_case in collections.OrderedDict(sorted(data_set.items())).keys():
            ebay_gui_data = data_set[test_case]
            logging.debug(str(datetime.datetime.now()) + " Ebay navigation test suite adding " + test_case)
            test_suite.addTest(EbayNavigationTestCase(test_case, ebay_gui_data, sequence, args))
            sequence += 1
        return test_suite
