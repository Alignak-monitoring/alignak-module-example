#!/usr/bin/python

# -*- coding: utf-8 -*-

# Copyright (C) 2015:
# Thibault Cohen, titilambert@gmail.com
#
# This file is part of Alignak
#
# Alignak is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Alignak is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Alignak. If not, see <http://www.gnu.org/licenses/>.

"""
This module job is to get configuration data from Surveil
"""

import time

from alignak.basemodule import BaseModule
from alignak.log import logger

properties = {
    # Which daemon can load this module
    'daemons': ['arbiter', 'broker', 'scheduler', 'poller', 'receiver', 'reactionner'],
    # name of the module type ; to distinguish between them:
    'type': 'example',
     # is the module "external" (external means here a daemon module)
    'external': True,
    # Possible configuration phases where the module is involved:
    'phases': ['configuration', 'late_configuration', 'running', 'retention'],
}


def get_instance(mod_conf):
    logger.info("[example] Example module %s", 
                mod_conf.get_name())
    instance = Example(mod_conf)
    return instance


class Example(BaseModule):
    def __init__(self, modconf):
        BaseModule.__init__(self, modconf)
        self.option_1 = getattr(modconf, 'option_1', None)
        self.option_2 = getattr(modconf, 'option_2', None)
        self.option_3 = getattr(modconf, 'option_3', None)

    def init(self):
        logger.info("[Dummy Arbiter] Initialization of the dummy arbiter module")
        pass

    # Common functions
    def do_loop_turn(self):
        """This function is called/used when you need a module with
        a loop function (and use the parameter 'external': True)
        """
        logger.info("[mod-example] In loop")
        time.sleep(1)

    def hook_tick(self):
        """This function is called on each daemon 'tick'"""
        logger.info("[mod-example] In hook tick")

    # Arbiter specific functions
    ## In execution order
    def hook_load_retention(self):
        """This function is called after retention loading"""
        logger.info("[mod-example] In hook load retention")

    def hook_read_configuration(self):
        """This function is called after conf file reading"""
        logger.info("[mod-example] In hook read config")

    def get_objects(self):
        """This function must return a list of config
        objects (hosts, services, commands, ...)

        This is usefull when your module import object from external database
        """
        logger.info("[mod-example] Ask me for objects to return")
        return []

    def hook_early_configuration(self):
        """This function is called after getting all config objects"""
        logger.info("[mod-example] In hook early config")

    def hook_late_configuration(self, conf):
        """This function is called after configuration compilation
        This the last step of configuration reading
        """
        logger.info("[mod-example] In hook late config")


    # scheduler
    def update_retention_objects(self):
        pass
    def load_retention_objects(self):
        pass
    def hook_save_retention(self):
        logger.info("[Dummy Arbiter] Raise a external command as example")
    def hook_load_retention(self):
        logger.info("[Dummy Arbiter] Raise a external command as example")
    def hook_get_new_actions(self):
        logger.info("[Dummy Arbiter] Raise a external command as example")
    def hook_pre_scheduler_mod_start(self):
        logger.info("[Dummy Arbiter] Raise a external command as example")
    def hook_scheduler_tick(self):
        logger.info("[Dummy Arbiter] Raise a external command as example")
    def hook_tick(self):
        logger.info("[Dummy Arbiter] Dummy in hook late config")
    def do_loop_turn(self):
        logger.info("[Dummy Arbiter] Raise a external command as example")
        time.sleep(0.1)       


    # Broker

    def load_retention(self):
        logger.info("[Dummy Arbiter] Dummy in hook late config")
    def hook_tick(self):
        logger.info("[Dummy Arbiter] Dummy in hook late config")
    def main(self):
        pass
    def hook_pre_scheduler_mod_start(self):
        logger.info("[Dummy Arbiter] Raise a external command as example")
    def do_loop_turn(self):
        logger.info("[Dummy Arbiter] Raise a external command as example")
        time.sleep(0.1)

    ## managing all broks
    def manage_brok(self, brok):
        pass

    ## managing one type of brok
    def manage_clean_all_my_instance_id_brok(self, brok):
        pass
    def manage_downtime_raise_brok(self, brok):
        pass

    def manage_initial_broks_done_brok(self, brok):
        pass

    def manage_log_brok(self, brok):
        pass
    def manage_notification_raise_brok(self, brok):
        pass

    def manage_program_status_brok(self, brok):
        pass



    def  manage_unknown_host_check_result_brok(self, broker):
        pass
    def  manage_unknown_service_check_result_brok(self, broker):
        pass

    brok_types = ["arbiter", "brok", "broker", "businessimpactmodulation",
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

