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

import os
import json
import time
import logging

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
        logger = logging.getLogger('alignak.module.%s' % self.alias)

        logger.debug("inner properties: %s", self.__dict__)
        logger.debug("received configuration: %s", mod_conf.__dict__)

        # Options are the variables defined in the module configuration file
        self.option_1 = getattr(mod_conf, 'option_1', None)
        self.option_2 = getattr(mod_conf, 'option_2', None)
        self.option_3 = getattr(mod_conf, 'option_3', None)

    def init(self):
        logger.info("Initialization of the dummy arbiter module")
        pass

    # Common functions
    def do_loop_turn(self):
        """This function is called/used when you need a module with
        a loop function (and use the parameter 'external': True)
        """
        logger.info("In loop")
        time.sleep(1)

    def hook_tick(self):
        """This function is called on each daemon 'tick'"""
        logger.info("In hook tick")

    # Arbiter specific functions
    ## In execution order
    def hook_load_retention(self):
        """This function is called after retention loading"""
        logger.info("In hook load retention")

    def hook_read_configuration(self):
        """This function is called after conf file reading"""
        logger.info("In hook read config")

    def get_objects(self):
        """This function must return a list of config
        objects (hosts, services, commands, ...)

        This is usefull when your module import object from external database
        """
        logger.info("Ask me for objects to return")
        return []

    def hook_early_configuration(self):
        """This function is called after getting all config objects"""
        logger.info("In hook early config")

    def hook_late_configuration(self, conf):
        """This function is called after configuration compilation
        This the last step of configuration reading
        """
        logger.info("In hook late config")


    # scheduler only module
    def update_retention_objects(self):
        pass
    def load_retention_objects(self):
        pass
    def hook_save_retention(self, scheduler):
        logger.info("Dummy in save retention")
    def hook_load_retention(self, scheduler):
        logger.info("Dummy in load retention")
    def hook_get_new_actions(self, scheduler):
        logger.info("Dummy in get new actions")
    def hook_pre_scheduler_mod_start(self, scheduler):
        logger.info("Dummy in hook pre-scheduler")
    def hook_scheduler_tick(self, scheduler):
        logger.info("Dummy in hook scheduler tick")
    def hook_tick(self, scheduler):
        logger.info("Dummy in hook tick")
    def do_loop_turn(self, scheduler):
        logger.info("Dummy in loop turn")
        time.sleep(0.1)


    # Broker only module
    def load_retention(self):
        logger.info("Dummy in load retention")
    def hook_tick(self):
        logger.info("Dummy in hook tick")
    def main(self):
        pass
    def hook_pre_scheduler_mod_start(self):
        logger.info("Dummy in hook pre-scheduler")
    def do_loop_turn(self):
        logger.info("Dummy in loop turn")
        time.sleep(0.1)

    ## managing all broks
    def manage_brok(self, brok):
        pass

    brok_types = [
        "arbiter", "brok", "broker", "businessimpactmodulation",
        "check", "checkmodulation", "CommandCall", "contact",
        "contactgroup", "escalation", "eventhandler",
        "externalcommand", "host", "hostdependency",
        "hostescalation", "hostextinfo", "hostgroup",
        "macromodulation", "macroresolver", "message", "module",
        "notification", "notificationway", "command", "config",
        "servicedependency", "pack", "poller", "reactionner",
        "realm", "receiver", "resultmodulation", "scheduler",
        "service", "serviceescalation", "serviceextinfo",
        "servicegroup", "timeperiod", "trigger",
    ]

    ## managing one type of brok
    def manage_clean_all_my_instance_id_brok(self, brok):
        pass
    def manage_downtime_raise_brok(self, brok):
        pass
    def manage_initial_broks_done_brok(self, brok):
        pass
    def manage_notification_raise_brok(self, brok):
        pass
    def manage_program_status_brok(self, brok):
        pass
    def  manage_unknown_host_check_result_brok(self, broker):
        pass
    def  manage_unknown_service_check_result_brok(self, broker):
        pass

    def manage_initial_host_status_brok(self, brok):
        pass
    def manage_initial_service_status_brok(self, brok):
        pass

    def manage_host_check_result_brok(self, brok):
        pass
    def manage_service_check_result_brok(self, brok):
        pass

    def manage_host_next_schedule_brok(self, brok):
        pass
    def manage_service_next_schedule_brok(self, brok):
        pass

    def manage_host_snapshot_brok(self, brok):
        pass
    def manage_service_snapshot_brok(self, brok):
        pass

    def manage_update_host_status_brok(self, brok):
        pass
    def manage_update_service_status_brok(self, brok):
        pass

    # main is the main loop of the module if it is an external module
    def main(self):
        """
        Main loop of the process

        This module is an "external" module
        :return:
        """
        # Set the OS process title
        self.set_proctitle(self.alias)
        self.set_exit_handler()

        logger.info("starting...")

        while not self.interrupted:
            logger.debug("queue length: %s", self.to_q.qsize())
            start = time.time()

            # Get message in the queue
            l = self.to_q.get()
            for b in l:
                # Prepare and manage each brok in the queue message
                b.prepare()
                self.manage_brok(b)

            logger.debug("time to manage %s broks (%d secs)", len(l), time.time() - start)

        logger.info("stopping...")

        logger.info("stopped")
