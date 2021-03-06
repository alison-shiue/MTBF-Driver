# -*- coding: iso-8859-15 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from mtbf_driver.MtbfTestCase import GaiaMtbfTestCase
from gaiatest.apps.ui_tests.app import UiTests
from mtbf_driver.mtbf_apps.ui_tests.app import MTBF_UiTests


class TestKeyboardPredictiveKey(GaiaMtbfTestCase):

    def setUp(self):
        GaiaMtbfTestCase.setUp(self)
        # enable auto-correction of keyboard
        self.data_layer.set_setting('keyboard.autocorrect', True)

    def test_keyboard_predictive_key(self):
        # TODO: Merge gaiatest new test of predictive key
        self.app_id = self.launch_by_touch("uitest")
        self.ui_tests = UiTests(self.marionette)
        self.mtbf_ui_tests = MTBF_UiTests(self.marionette)
        self.mtbf_ui_tests.back_to_main_screen()
        # go to UI/keyboard page
        keyboard_page = self.ui_tests.tap_keyboard_option()
        keyboard_page.switch_to_frame()

        # tap the field "input type=text"
        keyboard = keyboard_page.tap_text_input()

        # type first 6 letters of the expected word
        keyboard.switch_to_keyboard()
        expected_word = u'keyboard'
        keyboard.send(expected_word[:7])

        # tap the first predictive word
        keyboard.tap_first_predictive_word()
        self.apps.switch_to_displayed_app()
        keyboard_page.switch_to_frame()

        # check if the word in the input field is the same as the expected word
        typed_word = keyboard_page.text_input
        self.assertEqual(typed_word, expected_word)
