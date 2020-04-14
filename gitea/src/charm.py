#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# Copyright © 2020 Tim McNamara tsm@canonical.com
# Distributed under terms of the GPL license.
"""Operator Charm main library."""
# Load modules from lib directory
import sys
sys.path.append('lib')

import subprocess
import logging

from ops.charm import CharmBase  # noqa:E402
from ops.framework import StoredState  # noqa:E402
from ops.model import (  # noqa:E402
    ActiveStatus,
    BlockedStatus,
    MaintenanceStatus
)
from ops.main import main

""" -- Example relation interface for MySQL:
from interfaces import (
    MySQLInterfaceRequires
)
"""

LOGGER = logging.getLogger("gitea_charm")

class GiteaCharm(CharmBase):
    """Class reprisenting this Operator charm."""

    state = StoredState()

    def __init__(self, *args):
        """Initialize charm and configure states and events to observe."""
        super().__init__(*args)
        #self.unit = self.framework.model.unit
        # -- standard hook observation
        self.framework.observe(self.on.install, self)
        self.framework.observe(self.on.start, self)
        self.framework.observe(self.on.config_changed, self)
        # -- example action observation
        # self.framework.observe(self.on.example_action, self)
        # -- example relation / interface observation, disabled by default
        # self.framework.observe(self.on.db_relation_changed, self)
        # self.mysql = MySQLInterfaceRequires(self, 'db')

    def on_install(self, event):
        """Handle install state.
        
        Initial case is to just 'snap install gitea'.
        Perhaps soon, have optional snap resource for side-loading.

        Uses charm config for snap-channel.
        """
        channel = self.model.config['snap-channel']
        LOGGER.info(f"installing gitea from {channel}")
        # event.log(f"installing gitea from {channel}")
        # FEATURE REQUEST
        #
        # Hopefully, soonish, we can have a command in the operator framework
        # to install a snap, and use the resource if specified.
        #   ops.snap.install("gitea", channel="latest/edge")
        # Would expect a resource for the charm called "gitea-snap", and if there is
        # on, it would install that, otherwise it will install the "gitea" snap using
        # the specified channel.
        # Perhaps, the framework could look for charm config "gitea-snap-channel", and use
        # that.
        self.unit.status = MaintenanceStatus("Installing charm software")
        res = subprocess.check_output(["snap", "install", "gitea", "--channel", channel])
        # event.log(f"snap install {res}")
        # if errcode != 0:
        #     raise RuntimeError(f"couldn't install the gitea snap from {channel} channel")
        

    def on_start(self, event):
        """Handle start state."""
        # do things on start, like install packages
        # once done, mark state as done
        # perform installation and common configuration bootstrap tasks
        self.unit.status = MaintenanceStatus("Software installed, performing configuration")
        self.state._started = True

    def on_config_changed(self, event):
        """Handle config changed hook."""

        channel = self.model.config['snap-channel']
        # event.log(f"installing gitea from {channel}")

        # res = subprocess.check_output(["snap", "refresh", "gitea", "--channel", channel])
        # event.log(f"snap install {res}")

        # if software is installed and DB related, configure software
        # if self.state._started and self.state._db_configured:
        #     # configure your software
        #     # self.example_config = self.model.config['example_config']
        #     # event.log("Install of software complete")
        #     #self.unit.status = ActiveStatus("Software installed and configured")
        #     pass
        #     #self.state._configured = True
        # elif self.state._started:
        #     # event.log("Waiting on configuration to run, and DB to be related.")
        #     #self.unit.status = BlockedStatus("Waiting for MySQL to be related")
        #     pass
        # else:
        #     # event.log("Waiting on installation to complete.")
        #     pass

    # # -- Example relation interface for MySQL, not observed by default:
    # def on_db_relation_changed(self, event):
    #     """Handle an example db relation's change event."""
    #     self.password = event.relation.data[event.unit].get("password")
    #     self.unit.status = MaintenanceStatus("Configuring database")
    #     if self.mysql.is_ready:
    #         event.log("Database relation complete")
    #     self.state._db_configured = True

    # def on_example_action(self, event):
    #     """Handle the example_action action."""
    #     event.log("Hello from the example action.")
    #     event.set_results({"success": "true"})


if __name__ == "__main__":
    main(GiteaCharm)