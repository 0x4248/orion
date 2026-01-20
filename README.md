<h1 align="center">Orion</h1>
<p align="center">
    <img src="src/static/mascot_hd.png" width="250px" style="w">
</p>

Orion is a command driven extendable system interface built on top of FastAPI. It exposes a unified execution model where the same command can be invoked via a terminal like CLI over HTTP, a form based UI, and many more to come.

## Design Overview

Orion is structured around a command registry.

Each command is a small, self-contained unit with:
- a name
- a handler function
- an execution mode (CLI, UI, or both)
- optional form metadata

Commands are registered once and dispatched uniformly, regardless of entry point.

This avoids duplicating logic between:
- HTML forms
- CLI parsing
- internal routing


This design is hevily inspired by discord bots and the way they handle commands with both having a text based and a form based interface.

### Example Command

```python
# Ping pong

from fastapi import Request # Standard for FastAPI request handling
from core.registry import registry # Import the global command registry
from core.commands import Command # Import the Command class to define new commands
from core import page # Import page rendering utilities


def ping(request: Request, name: str = ""):
    if name == "":
        return page.message(request, "PONG", "PONG!")
    else:
        return page.message(request, "PONG", f"PONG, {name}!")

registry.register(Command(
    name="ping",
    handler=ping,
    summary="Ping pong command", 
    mode="both", # Tell orion we can have this command in both CLI and UI
    form_fields=[ # Let him know what fields to show in the form or we will just get a blank screen
        {"name": "name", "type": "text"}
    ]
))
```

Because nothing but the command it self was implemented, this means orion has total control over how to expose this command via different interfaces.

<p align="center"style="font-family: Times;font-size:26px"><i>Write once - run everywhere.</i></p>

## Features

Orion by default feels like a full blown system with:
- Manuals
- SQL DB management
- Heartbeats
- Login system

*But you can make it a blank system by removing all the files in the `commands` folder and start from scratch.*

## TODO

- [ ] HTTP**S**
- [ ] SUDB (Secure User DataBase)
- [ ] OrionReg (Enviroment variables and config)
- [ ] Menu System
- [ ] /
- [ ] Matenince system
- [ ] OrionWarden (OrionUMS, Security and watchdog)
    - [ ] OrionUMS (User Management System)
    - [ ] Security system (password policies, etc)
    - [ ] Watchdog (Monitor system health and restart if needed)
- [ ] Plugin system
- [ ] Theming system
- [ ] API Documentation (OrionDoc)
- [ ] Tests
- [ ] Proper SDK or development kit

### TODO COMMANDS
- [ ] Mail
- [ ] Snippets
- [ ] Todo
- [ ] Notice board