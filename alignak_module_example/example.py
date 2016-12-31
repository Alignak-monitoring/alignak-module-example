# -*- coding: utf-8 -*-
#
# Copyright (C) 2015-2015: Alignak contrib team, see AUTHORS.txt file for contributors
#
# This file is part of Alignak contrib projet.
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
#
"""
This module is an Alignak Broker module that collects the `monitoring_log` broks to send
them to a Python logger configured in the module configuration file
"""

import time
import logging
import inspect

from alignak.basemodule import BaseModule

logger = logging.getLogger('alignak.module')  # pylint: disable=C0103

# pylint: disable=C0103
properties = {
    # Which daemons can load this module
    'daemons': ['arbiter', 'broker', 'scheduler', 'poller', 'receiver', 'reactionner'],
    # name of the module type ; to distinguish modules each others
    'type': 'example',
    # is the module "external" (external means here a daemon module)
    'external': True,
    # Possible configuration phases where the module is involved:
    'phases': ['configuration', 'late_configuration', 'running', 'retention'],
}


def get_instance(mod_conf):
    """
    Return a module instance for the modules manager

    :param mod_conf: the module properties as defined globally in this file
    :return:
    """
    logger.info("Give an instance of %s for alias: %s", mod_conf.python_name, mod_conf.module_alias)

    return Example(mod_conf)


class Example(BaseModule):
    """
    Example module main class
    """
    def __init__(self, mod_conf):
        """
        Module initialization

        mod_conf is a dictionary that contains:
        - all the variables declared in the module configuration file
        - a 'properties' value that is the module properties as defined globally in this file

        :param mod_conf: module configuration file as a dictionary
        """
        BaseModule.__init__(self, mod_conf)

        global logger
        # Update the logger to include the module alias in the logger name
        logger = logging.getLogger('alignak.module.%s' % self.alias)

        # Dump module inner properties and received configuration in the log
        logger.debug("inner properties: %s", self.__dict__)
        logger.debug("received configuration: %s", mod_conf.__dict__)

        # Options are the variables defined in the module configuration file
        self.option_1 = getattr(mod_conf, 'option1', None)
        self.option_2 = getattr(mod_conf, 'option2', None)
        self.option_3 = getattr(mod_conf, 'option3', None)
        logger.info("configuration, %s, %s, %s", self.option_1, self.option_2, self.option_3)

    def init(self):
        """
        This function initializes the module instance. If False is returned, the modules manager
        will periodically retry an to initialize the module.
        If an exception is raised, the module will be definitely considered as dead :/

        This function must be present and return True for Alignak to consider the module as loaded
        and fully functional.

        :return: True if initialization is ok, else False
        """
        logger.info("Test - Example in %s", inspect.stack()[0][3])
        logger.info("Initialization of the example module")
        return True

    # ----------
    # Common functions
    # ----------
    def do_loop_turn(self):
        """This function is called/used when you need a module with
        a loop function (and use the parameter 'external': True)
        """
        logger.info("In loop")
        time.sleep(1)

    def hook_tick(self, daemon):
        """This function is called on each daemon 'tick'"""
        logger.info("Test - Example in %s for daemon: %s", inspect.stack()[0][3], daemon)

    # Redefined in scheduler
    # def hook_save_retention(self):
    #     """This function is called to save data - really useful?"""
    #     logger.info("Test - Example in %s", inspect.stack()[0][3])
    #
    # def hook_load_retention(self):
    #     """This function is called to restore data - really useful?"""
    #     logger.info("Test - Example in %s", inspect.stack()[0][3])

    # ----------
    # Arbiter specific functions (In execution order)
    # ----------
    def hook_read_configuration(self, daemon):
        """This function is called after conf file reading"""
        logger.info("Test - Example in %s for daemon: %s", inspect.stack()[0][3], daemon)

    def get_objects(self):
        """This function must return a list of config
        objects (hosts, services, commands, ...)

        This is usefull when your module import object from external database
        """
        logger.info("Test - Example in %s", inspect.stack()[0][3])

        r = {'hosts': []}

        h = {
            'name': 'dummy host from dummy arbiter module',
            'register': '0',
        }
        r['hosts'].append(h)

        r['hosts'].append({
            'host_name': "module_host_1",
            'address': 'localhost'
        })

        logger.info("Returning hosts objects to the Arbiter: %s", str(r))
        return r

    def hook_early_configuration(self, daemon):
        """This function is called after getting all config objects"""
        logger.info("Test - Example in %s for daemon: %s", inspect.stack()[0][3], daemon)

    def hook_late_configuration(self, daemon):
        """This function is called after configuration compilation
        This the last step of configuration reading
        """
        logger.info("Test - Example in %s for daemon: %s", inspect.stack()[0][3], daemon)

    # ----------
    # scheduler only module
    # ----------
    def update_retention_objects(self, daemon):
        """ Update retention date """
        logger.info("Test - Example in %s for daemon: %s", inspect.stack()[0][3], daemon)

    def load_retention_objects(self, daemon):
        """ Self daemon objects retention - avoid using this! """
        logger.info("Test - Example in %s for daemon: %s", inspect.stack()[0][3], daemon)

    def hook_load_retention(self, daemon):
        """This function is called by the daemon to restore the objects live state """
        logger.info("Test - Example in %s for daemon: %s", inspect.stack()[0][3], daemon)

    def hook_save_retention(self, daemon):
        """This function is called before daemon exit to save the objects live state """
        logger.info("Test - Example in %s for daemon: %s", inspect.stack()[0][3], daemon)

    def hook_get_new_actions(self, daemon):
        logger.info("Test - Example in %s for daemon: %s", inspect.stack()[0][3], daemon)

    def hook_pre_scheduler_mod_start(self, daemon):
        logger.info("Test - Example in %s for daemon: %s", inspect.stack()[0][3], daemon)

    def hook_scheduler_tick(self, daemon):
        logger.info("Test - Example in %s for daemon: %s", inspect.stack()[0][3], daemon)

    # Already defined
    # def hook_tick(self, daemon):
    #     logger.info("Test - Example in %s for daemon: %s", inspect.stack()[0][3], daemon)

    # Already defined
    # def do_loop_turn(self, daemon):
    #     logger.info("Test - Example in %s for daemon: %s", inspect.stack()[0][3], daemon)

    # ----------
    # Broker only module
    # ----------
    # Already defined
    # def hook_tick(self):
    #     logger.info("Test - Example in %s for daemon: %s", inspect.stack()[0][3], daemon)

    # Already defined
    # def do_loop_turn(self, daemon):
    #     logger.info("Test - Example in %s for daemon: %s", inspect.stack()[0][3], daemon)

    def want_brok(self, brok):
        """ This function is called to check if a module wants a specific type of brok
        Default is to return True to get all broks

        Only implement this function if it is necessary!
        """
        logger.info("Test - Example in %s, want brok type: %s", inspect.stack()[0][3], brok.type)
        return True

    # managing all broks
    def manage_brok(self, brok):
        """ This function is called as soon as a brok is received """
        logger.info("Test - Example in %s, got brok type: %s", inspect.stack()[0][3], brok.type)

    """
        Broks types:
        - monitoring_log

        - notification_raise
        - downtime_raise
        - initial_host_status, initial_service_status, initial_contact_status
        - initial_broks_done

        - update_host_status, update_service_status, initial_contact_status
        - host_check_result, service_check_result
        - host_next_schedule, service_next_scheduler
        - host_snapshot, service_snapshot
        - unknown_host_check_result, unknown_service_check_result

        - program_status
        - clean_all_my_instance_id

        - new_conf
    """
    # managing one specific type type of brok
    def manage_log_brok(self, brok):
        """Deprecated ..."""
        logger.error("Deprecated function (%s) for module example", inspect.stack()[0][3])
        pass

    def manage_monitoring_log_brok(self, brok):
        """Deprecated ..."""
        logger.error("Deprecated function (%s) for module example", inspect.stack()[0][3])
        pass

    def manage_clean_all_my_instance_id_brok(self, brok):
        """Deprecated ..."""
        logger.error("Deprecated function (%s) for module example", inspect.stack()[0][3])
        pass

    def manage_downtime_raise_brok(self, brok):
        """Deprecated ..."""
        logger.error("Deprecated function (%s) for module example", inspect.stack()[0][3])
        pass

    def manage_initial_broks_done_brok(self, brok):
        """Deprecated ..."""
        logger.error("Deprecated function (%s) for module example", inspect.stack()[0][3])
        pass

    def manage_notification_raise_brok(self, brok):
        """Deprecated ..."""
        logger.error("Deprecated function (%s) for module example", inspect.stack()[0][3])
        pass

    def manage_program_status_brok(self, brok):
        """Deprecated ..."""
        logger.error("Deprecated function (%s) for module example", inspect.stack()[0][3])
        pass

    def manage_unknown_host_check_result_brok(self, brok):
        """Deprecated ..."""
        logger.error("Deprecated function (%s) for module example", inspect.stack()[0][3])
        pass

    def manage_unknown_service_check_result_brok(self, brok):
        """Deprecated ..."""
        logger.error("Deprecated function (%s) for module example", inspect.stack()[0][3])
        pass

    def manage_initial_host_status_brok(self, brok):
        """Deprecated ..."""
        logger.error("Deprecated function (%s) for module example", inspect.stack()[0][3])
        pass

    def manage_initial_service_status_brok(self, brok):
        """Deprecated ..."""
        logger.error("Deprecated function (%s) for module example", inspect.stack()[0][3])
        pass

    def manage_host_check_result_brok(self, brok):
        """Deprecated ..."""
        logger.error("Deprecated function (%s) for module example", inspect.stack()[0][3])
        pass

    def manage_service_check_result_brok(self, brok):
        """Deprecated ..."""
        logger.error("Deprecated function (%s) for module example", inspect.stack()[0][3])
        pass

    def manage_host_next_schedule_brok(self, brok):
        """Deprecated ..."""
        logger.error("Deprecated function (%s) for module example", inspect.stack()[0][3])
        pass

    def manage_service_next_schedule_brok(self, brok):
        """Deprecated ..."""
        logger.error("Deprecated function (%s) for module example", inspect.stack()[0][3])
        pass

    def manage_host_snapshot_brok(self, brok):
        """Deprecated ..."""
        logger.error("Deprecated function (%s) for module example", inspect.stack()[0][3])
        pass

    def manage_service_snapshot_brok(self, brok):
        """Deprecated ..."""
        logger.error("Deprecated function (%s) for module example", inspect.stack()[0][3])
        pass

    def manage_update_host_status_brok(self, brok):
        """Deprecated ..."""
        logger.error("Deprecated function (%s) for module example", inspect.stack()[0][3])
        pass

    def manage_update_service_status_brok(self, brok):
        """Deprecated ..."""
        logger.error("Deprecated function (%s) for module example", inspect.stack()[0][3])
        pass

    # main is the main loop of the module if it is an external module
    def main(self):
        """
        Main loop of the process

        This module is an "external" module
        :return:
        """
        global logger
        # Update the logger to include the module alias in the logger name
        logger = logging.getLogger('alignak.module.%s' % self.alias)

        # Set the OS process title
        self.set_proctitle(self.alias)
        self.set_exit_handler()

        logger.info("starting...")

        while not self.interrupted:
            logger.debug("queue length: %s", self.to_q.qsize())
            start = time.time()

            # Get message in the queue
            try:
                l = self.to_q.get()
            except Exception as exp:
                print("Queue get failed: %s", str(exp))
                continue
            else:
                for b in l:
                    # Prepare and manage each brok in the queue message
                    b.prepare()
                    self.manage_brok(b)

            logger.debug("time to manage %s broks (%d secs)", len(l), time.time() - start)

        logger.info("stopping...")

        logger.info("stopped")
