# i3uw

A simple utility for managing windows in the i3 window manager when using ultra-wide monitors.

## Features

- Floating and resizing windows to e.g. 2/3 of the screen when they are the only window in a workspace.
- Unfloating windows when they are no longer the only window in a workspace.

## Known Issues

- Multiple monitors have an issue where it is annoying to focus with keybinds between the floating single window and the other monitor. I will implement this eventually but it is not required for my use case (I use a single monitor).

### Dependencies

- [i3ipc-python](https://github.com/altdesktop/i3ipc-python)
- [i3](https://i3wm.org/)
