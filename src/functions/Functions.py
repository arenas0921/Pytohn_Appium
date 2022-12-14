from selenium.webdriver.support.wait import WebDriverWait
from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

from functions.Configuration import Configuration
import pytest
import json
from appium import webdriver


class Functions:

    def __init__(self):
        self.json_strings = {}
        self.device = {}
        self.desired_caps = {}
        self.driver = None

    def returnDriver(self):
        driver = self.driver
        return driver

    def get_json_file(self, file, path=Configuration.devices_resources):
        json_path = path + "/" + file + '.json'
        try:
            with open(json_path, "r") as read_file:
                self.json_strings = json.loads(read_file.read())
                return self.json_strings
        except FileNotFoundError:
            pytest.skip(u"get_json_file: No se encontro el Archivo " + file)
            return False

    def get_device(self, entity):
        if self.json_strings is False:
            pytest.skip(u"Define el device para esta prueba " + entity)

        else:
            try:
                self.device = self.json_strings[entity]
                return self.device
            except KeyError:
                pytest.skip(u"get_device: No se encontro el device al cual se hace referencia: " + entity)

    def get_capabilities(self, test_device=Configuration.device):
        Functions.get_json_file(self, "Devices")
        self.desired_caps = Functions.get_device(self, test_device)
        self.desired_caps['app'] = Configuration.app
        return self.desired_caps

    def get_driver(self, capabilities, local_server=Configuration.local):
        self.driver = webdriver.Remote(local_server, capabilities)
        Functions.check_app_is_running(self)
        return self.driver

    def check_app_is_running(self):
        activity = self.driver.current_activity
        print(activity)
        assert ".MainActivity" == activity, f"La Aplicacion {Configuration.app} no esta disponible"

    def close_application(self):
        self.driver.close_app()

    def click_element(self, locator):
        try:
            Functions.implicit_wait_visible(self, locator)
            self.driver.find_element(*locator).click()
        except ValueError:
            print("Element isn't clickable")

    def setText(self, locator, text):
        try:
            Functions.implicit_wait_visible(self, locator)
            self.driver.find_element(*locator).send_keys(text)
        except ValueError:
            print("Cannot set text on element")

    def implicit_wait_visible(self, locator):
        try:
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            print("Element no visible")
