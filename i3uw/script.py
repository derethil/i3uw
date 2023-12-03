#!/usr/bin/env python

from datetime import datetime, timedelta
from time import sleep
import logging
from i3ipc import Connection, Event

from i3uw.config import config

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)-7s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


class Handler:
    """
    Handle i3ipc events
    """

    def __init__(self, i3: Connection, handled: list[str]):
        """
        Initialize the handler for i3uw.

        Parameters:
        - i3: i3ipc connection
        - handled: list of i3 workspaces to handle
        """

        self.i3 = i3
        self.handled = handled
        self.last_event_at = datetime.now()

        logging.info("Handling workspaces: %s", self.handled)

    def msg(self, command: str):
        """
        Wrapper around i3.command to log the message and response

        Parameters:
        - command: i3ipc command to send
        """
        logging.info("Sending message: %s", command)
        response = self.i3.command(command)
        ipc_data = list(map(lambda x: x.ipc_data, response))
        logging.debug("Message Response: %s", ipc_data)

    def on_single_window_event(self):
        """
        Handle a single window in a workspace
        """
        sleep(0.05)
        focused = self.i3.get_tree().find_focused()
        logging.info("Handling single floating window with name: %s", focused.name)
        self.msg(
            f"floating enable; resize set {config.size.width} px {config.size.height} px; move position {config.position.x} {config.position.y}"
        )

    def on_multiple_window_event(self, event):
        """
        Handle multiple windows in a workspace

        Parameters:
        - event: i3ipc event
        """

        leaves = self.i3.get_tree().find_focused().workspace().leaves()

        logging.debug("Handling multiple windows: %s", [leaf.name for leaf in leaves])

        for window in leaves:
            logging.info("Unfloating window with name: %s", window.name)
            self.msg(f"[con_id={window.id}] floating disable")

        logging.debug("Focus window with name: %s", event.container.name)

        self.msg(f"[con_id={event.container.id}] focus")

        if event.change == "new":
            self.msg("move right")

        self.last_event_at = datetime.now()

    def handle_event(self, event):
        """
        Handle an event

        Parameters:
        - event: i3ipc event
        """

        logging.debug("Handling event: %s", event.change)
        time_since_last = datetime.now() - self.last_event_at
        logging.debug("Time since last handle: %s", time_since_last.microseconds / 1000)

        if time_since_last < timedelta(milliseconds=333):
            logging.debug("Too soon to handle, ignoring")
            return

        curr = self.i3.get_tree().find_focused().workspace()

        if curr.name not in self.handled:
            logging.debug("Workspace %s not in %s - ignoring", curr.name, self.handled)
            return

        logging.debug("Workspace %s in %s - handling", curr.name, self.handled)

        logging.debug("Workspace leaves: %s", curr.leaves())

        match len(curr.leaves()):
            case 1:
                self.on_single_window_event()
            case 2:
                self.on_multiple_window_event(event)

    def __call__(self, i3, event):
        """
        On i3ipc event, handle it

        Parameters:
        - i3: i3ipc connection
        - e: i3ipc event
        """
        self.i3 = i3
        self.handle_event(event)


def start():
    """Start the i3ipc connection and event loop"""
    i3 = Connection()
    handler = Handler(i3, config.handled_workspaces)

    i3.on(Event.WINDOW_NEW, handler)
    i3.on(Event.WINDOW_CLOSE, handler)

    # I will implement this eventually, but not necessary for a single ultra-wide monitor (my use case)
    # i3.on(Event.WINDOW_MOVE, handler)

    i3.main()
