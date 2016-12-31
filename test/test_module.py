#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2015-2016: Alignak team, see AUTHORS.txt file for contributors
#
# This file is part of Alignak.
#
# Alignak is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Alignak is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Alignak.  If not, see <http://www.gnu.org/licenses/>.
#
"""
Test the module
"""

import re
import time

import requests

from alignak_test import AlignakTest, time_hacker
from alignak.modulesmanager import ModulesManager
from alignak.objects.module import Module
from alignak.basemodule import BaseModule

import alignak_module_example


class TestModules(AlignakTest):
    """
    This class contains the tests for the module
    """

    def test_module_loading(self):
        """
        Alignak module loading

        :return:
        """
        self.print_header()
        self.setup_with_file('./cfg/cfg_default.cfg')
        self.assertTrue(self.conf_is_correct)
        self.show_configuration_logs()

        # No arbiter modules created
        modules = [m.module_alias for m in self.arbiter.myself.modules]
        self.assertListEqual(modules, ['example'])

        # The only existing broker module is logs declared in the configuration
        modules = [m.module_alias for m in self.brokers['broker-master'].modules]
        self.assertListEqual(modules, ['example'])

        # No poller module
        modules = [m.module_alias for m in self.pollers['poller-master'].modules]
        self.assertListEqual(modules, ['example'])

        # No receiver module
        modules = [m.module_alias for m in self.receivers['receiver-master'].modules]
        self.assertListEqual(modules, ['example'])

        # No reactionner module
        modules = [m.module_alias for m in self.reactionners['reactionner-master'].modules]
        self.assertListEqual(modules, ['example'])

        # No scheduler modules
        modules = [m.module_alias for m in self.schedulers['scheduler-master'].modules]
        self.assertListEqual(modules, ['example'])

    def test_module_manager(self):
        """
        Test if the module manager manages correctly all the modules
        :return:
        """
        self.print_header()
        self.setup_with_file('cfg/cfg_default.cfg')
        self.assertTrue(self.conf_is_correct)

        time_hacker.set_real_time()

        # Create an Alignak module
        mod = Module({
            'module_alias': 'example',
            'module_types': 'example',
            'python_name': 'alignak_module_example',
        })

        # Create the modules manager for a daemon type
        self.modulemanager = ModulesManager('receiver', None)

        # Load and initialize the modules:
        #  - load python module
        #  - get module properties and instances
        self.modulemanager.load_and_init([mod])

        # Loading module logs
        self.assert_any_log_match(re.escape(
            "Importing Python module 'alignak_module_example' for example..."
        ))
        self.assert_any_log_match(re.escape(
            "Module properties: {'daemons': "
            "['arbiter', 'broker', 'scheduler', 'poller', 'receiver', 'reactionner'], "
            "'phases': ['configuration', 'late_configuration', 'running', 'retention'], "
            "'type': 'example', 'external': True}"
        ))
        self.assert_any_log_match(re.escape(
            "Imported 'alignak_module_example' for example"
        ))
        self.assert_any_log_match(re.escape(
            "Loaded Python module 'alignak_module_example' (example)"
        ))
        self.assert_any_log_match(re.escape(
            "Give an instance of alignak_module_example for alias: example"
        ))

        my_module = self.modulemanager.instances[0]

        # Get list of not external modules
        self.assertListEqual([], self.modulemanager.get_internal_instances())
        for phase in ['configuration', 'late_configuration', 'running', 'retention']:
            self.assertListEqual([], self.modulemanager.get_internal_instances(phase))

        # Get list of external modules
        self.assertListEqual([my_module], self.modulemanager.get_external_instances())
        for phase in ['configuration', 'late_configuration', 'retention']:
            self.assertListEqual([my_module], self.modulemanager.get_external_instances(phase))
        for phase in ['running']:
            self.assertListEqual([my_module], self.modulemanager.get_external_instances(phase))

        # Clear logs
        self.clear_logs()

        # Start external modules
        self.modulemanager.start_external_instances()

        # Starting external module logs
        self.assert_log_match("Trying to initialize module: example", 0)
        self.assert_log_match(re.escape("Test - Example in init"), 1)
        self.assert_log_match("Initialization of the example module", 2)
        self.assert_log_match("Starting external module example", 3)
        self.assert_log_match("Starting external process for module example", 4)
        self.assert_log_match("example is now started", 5)

        # Check alive
        self.assertIsNotNone(my_module.process)
        self.assertTrue(my_module.process.is_alive())

        # Clear logs
        self.clear_logs()

        # Kill the external module (normal stop is .stop_process)
        my_module.kill()
        time.sleep(0.1)
        self.assert_log_match("Killing external module", 0)
        self.assert_log_match("External module killed", 1)

        # Should be dead (not normally stopped...) but we still know a process for this module!
        self.assertIsNotNone(my_module.process)

        # Nothing special ...
        self.modulemanager.check_alive_instances()
        self.assert_log_match("The external module example died unexpectedly!", 2)
        self.assert_log_match("Setting the module example to restart", 3)

        # Try to restart the dead modules
        self.modulemanager.try_to_restart_deads()
        self.assert_log_match("Trying to initialize module: example", 4)

        # In fact it's too early, so it won't do it
        # The module instance is still dead
        self.assertFalse(my_module.process.is_alive())

        # So we lie, on the restart tries ...
        my_module.last_init_try = -5
        self.modulemanager.check_alive_instances()
        self.modulemanager.try_to_restart_deads()
        self.assert_log_match("Trying to initialize module: example", 5)
        self.assert_log_match(re.escape("Test - Example in init"), 6)
        self.assert_log_match("Initialization of the example module", 7)

        # The module instance is now alive again
        self.assertTrue(my_module.process.is_alive())
        self.assert_log_match("I'm stopping module 'example'", 8)
        self.assert_log_match("Starting external process for module example", 9)
        self.assert_log_match("example is now started", 10)

        # There is nothing else to restart in the module manager
        self.assertEqual([], self.modulemanager.to_restart)

        # Clear logs
        self.clear_logs()

        # Now we look for time restart so we kill it again
        my_module.kill()
        time.sleep(0.2)
        self.assertFalse(my_module.process.is_alive())
        self.assert_log_match("Killing external module", 0)
        self.assert_log_match("External module killed", 1)

        # Should be too early
        self.modulemanager.check_alive_instances()
        self.assert_log_match("The external module example died unexpectedly!", 2)
        self.assert_log_match("Setting the module example to restart", 3)

        self.modulemanager.try_to_restart_deads()
        self.assert_log_match("Trying to initialize module: example", 4)

        # In fact it's too early, so it won't do it
        # The module instance is still dead
        self.assertFalse(my_module.process.is_alive())

        # So we lie, on the restart tries ...
        my_module.last_init_try = -5
        self.modulemanager.check_alive_instances()
        self.modulemanager.try_to_restart_deads()
        self.assert_log_match("Trying to initialize module: example", 5)
        self.assert_log_match(re.escape("Test - Example in init"), 6)
        self.assert_log_match("Initialization of the example module", 7)

        # The module instance is now alive again
        self.assertTrue(my_module.process.is_alive())
        self.assert_log_match("I'm stopping module 'example'", 8)
        self.assert_log_match("Starting external process for module example", 9)
        self.assert_log_match("example is now started", 10)

        # And we clear all now
        self.modulemanager.stop_all()
        # Stopping module logs

        self.assert_log_match("Request external process to stop for example", 11)
        self.assert_log_match(re.escape("I'm stopping module 'example' (pid="), 12)
        self.assert_log_match(
            re.escape("'example' is still alive after normal kill, I help it to die"), 13
        )
        self.assert_log_match("Killing external module ", 14)
        self.assert_log_match("External module killed", 15)
        self.assert_log_match("External process stopped.", 16)

    def test_module_start_default(self):
        """
        Test the module initialization function, no parameters, using default
        :return:
        """
        self.print_header()
        # Obliged to call to get a self.logger...
        self.setup_with_file('cfg/cfg_default.cfg')
        self.assertTrue(self.conf_is_correct)

        # -----
        # Default initialization
        # -----
        # Clear logs
        self.clear_logs()

        # Create an Alignak module
        mod = Module({
            'module_alias': 'example',
            'module_types': 'example',
            'python_name': 'alignak_module_example'
        })

        instance = alignak_module_example.get_instance(mod)
        self.assertIsInstance(instance, BaseModule)

        self.assert_log_match(
            re.escape("Give an instance of alignak_module_example for "
                      "alias: example"), 0)

    def test_module_start_parameters(self):
        """
        Test the module initialization function, no parameters, provide parameters
        :return:
        """
        self.print_header()
        # Obliged to call to get a self.logger...
        self.setup_with_file('cfg/cfg_default.cfg')
        self.assertTrue(self.conf_is_correct)

        # -----
        # Provide parameters
        # -----
        # Clear logs
        self.clear_logs()

        # Create an Alignak module
        mod = Module({
            'module_alias': 'example',
            'module_types': 'example',
            'python_name': 'alignak_module_example',
            'option1': 'foo',
            'option2': 'bar',
            'option3': 'foobar'
        })

        instance = alignak_module_example.get_instance(mod)
        self.assertIsInstance(instance, BaseModule)

        self.assert_log_match(
            re.escape("Give an instance of alignak_module_example for "
                      "alias: example"), 0)
        self.assert_log_match(
            re.escape("configuration, foo, bar, foobar"), 1)

    def test_module_zzz_run(self):
        """
        Test the module while running
        :return:
        """
        self.print_header()
        # Obliged to call to get a self.logger...
        self.setup_with_file('cfg/cfg_default.cfg')
        self.assertTrue(self.conf_is_correct)

        # -----
        # Provide parameters - logger configuration file (exists)
        # -----
        # Clear logs
        self.clear_logs()

        """
        To be done !
        """
