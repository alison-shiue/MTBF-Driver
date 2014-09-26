# This Source Code Form is subject to the terms of the Mozilla Public
# License v.2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from mtbf_driver.MtbfTestCase import GaiaMtbfTestCase
from mtbf_driver.mtbf_apps.settings.app import MTBF_Settings
from gaiatest.apps.system.app import System


class TestAirplaneMode(GaiaMtbfTestCase):

    def setUp(self):
        GaiaMtbfTestCase.setUp(self)
        self.data_layer.disable_wifi()
        # self.data_layer.connect_to_cell_data()
        self.data_layer.connect_to_wifi()
        self.data_layer.set_setting('geolocation.enabled', 'true')

        self.settings = MTBF_Settings(self.marionette)
        self.settings.launch()

    def test_toggle_airplane_mode(self):
        self.settings.wait_for_airplane_toggle_ready()

        # Switch on Airplane mode
        self.settings.toggle_airplane_mode()

        # wait for wifi to be disabled, this takes the longest when airplane mode is switched on
        self.wait_for_condition(lambda s: 'Disabled' in self.settings.wifi_menu_item_description)

        # wait for airplane mode icon is diaplayed on status bar
        self.marionette.switch_to_default_content()
        system_app = System(self.marionette)
        system_app.wait_for_airplane_mode_icon_displayed()

        # check Wifi is disabled
        self.assertFalse(self.data_layer.is_wifi_connected(self.testvars['wifi']), "WiFi was still connected after switching on Airplane mode")

        # check that Cell Data is disabled
        # self.assertFalse(self.data_layer.get_setting('ril.data.enabled'), "Cell Data was still connected after switching on Airplane mode")

        # check GPS is disabled
        self.assertFalse(self.data_layer.get_setting('geolocation.enabled'), "GPS was still connected after switching on Airplane mode")

        # switch back to app frame
        self.apps.switch_to_displayed_app()

        # Switch off Airplane mode
        self.settings.wait_for_airplane_toggle_ready()
        self.settings.toggle_airplane_mode()

        # Wait for wifi to be connected, because this takes the longest to connect after airplane mode is switched off
        self.wait_for_condition(lambda s: 'Connected to ' + self.testvars['wifi']['ssid'] in self.settings.wifi_menu_item_description, timeout=40)

        # check Wifi is enabled
        self.assertTrue(self.data_layer.is_wifi_connected(self.testvars['wifi']), "WiFi was not connected after switching off Airplane mode")

        # check that Cell Data is enabled
        # self.assertTrue(self.data_layer.get_setting('ril.data.enabled'), "Cell data was not connected after switching off Airplane mode")

        # check GPS is enabled
        self.assertTrue(self.data_layer.get_setting('geolocation.enabled'), "GPS was not enabled after switching off Airplane mode")

    def tearDown(self):
        self.settings.back_to_main_screen()
        self.data_layer.disable_wifi()
        self.data_layer.set_setting('airplaneMode.enabled', False)
        GaiaMtbfTestCase.tearDown(self)
