# SPDX-License-Identifier: GPL-3.0-only
# Orion System
#
# Copyright (C) 2026 0x4248
# Copyright (C) 2026 4248 Systems
#
# Orion is free software; you may redistribute it and/or modify it
# under the terms of the GNU General Public License version 3 only,
# as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

import os
from fastapi import Request
from core.registry import registry
from core.commands import Command
from core import page
import sqlite3
from core.auth import users as auth_users
from core.console import logger
DB_PATH = "data/orion.db"

db = sqlite3.connect(DB_PATH)
cursor = db.cursor()

# if tables dont exist make DEMO and ACCOUNTS tables for testing
cursor.execute("""
CREATE TABLE IF NOT EXISTS DEMO (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    value TEXT NOT NULL
);
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS ACCOUNTS (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);
""")
db.commit()

cursor.execute("INSERT INTO DEMO (name, value) VALUES ('example1', 'value1')")
cursor.execute("INSERT INTO DEMO (name, value) VALUES ('example2', 'value2')")
cursor.execute("INSERT INTO ACCOUNTS (username, password) VALUES ('admin', 'admin')")
cursor.execute("INSERT INTO ACCOUNTS (username, password) VALUES ('user', 'password')")
db.commit()

def auth_check(request: Request):
    logger.info(m="Checking auth for SQLDB command", caller="SQLDB_Command")
    user = request.cookies.get('user', 'None')
    if not user:
        return False
    elif 'admin' not in auth_users[user]["roles"] and 'db' not in auth_users[user]["roles"]:
        return False
    return True

def sql_print_table(request: Request, *args):
    if not auth_check(request):
        return page.message(request, "SQL ERROR", error="Unauthorized: Admin/DB role required.")
    if len(args) == 0 or args[0] == "*":
        logger.info(m="Selecting all tables", caller="SQLDB_Command")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        args = [row[0] for row in cursor.fetchall()]
        logger.info(m=f"Found tables: {args}", caller="SQLDB_Command")
    output = "<span class='grey-text'>F4 to exit table view.</span><br><br>"
    for arg in args:
        logger.info(m=f"Printing table: {arg}", caller="SQLDB_Command")
        table_name = arg
        
        try:
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            columns = [description[0] for description in cursor.description]
            
            output += f"<h2>{table_name}</h2><table style='width:100%; border-collapse: collapse;' border='1'><tr>"
            for col in columns:
                output += f"<th style='text-align:left'>{col}</th>"
            output += "</tr>"
            for row in rows:
                output += "<tr>"
                for cell in row:
                    output += f"<td>{cell}</td>"
                output += "</tr>"
            output += "</table><br>"
        except sqlite3.Error as e:
            output = f"Error accessing table '{table_name}': {e}"
            return page.message(request, "SQL ERROR", output)
    if output:
        return page.static(request, "SQL TABLES", output)
    else:
        return page.message(request, "SQL TABLES", error="No tables found in search.")
    
registry.register(Command(
    name="db.table.print",
    handler=sql_print_table,
    summary="Print a database table",
    mode="cli",
))

def sql_exec(request: Request, *args):
    if not auth_check(request):
        return page.message(request, "SQL ERROR", error="Unauthorized: Admin/DB role required.")
    query = " ".join(args)
    response = ""
    try:
        cursor.execute(query)
        response = cursor.fetchall()
        db.commit()
        return page.message(request, "SQL EXECUTED", f"Successfully executed SQL command: {query}<br>Response: {response}")
    except sqlite3.Error as e:
        return page.message(request, "SQL ERROR", error=f"Error executing SQL command: {e}")
    
registry.register(Command(
    name="db.sql",
    handler=sql_exec,
    summary="Execute an SQL command",
    mode="cli",
    parse_mode="raw",
))

# E.G db.sql SELECT * FROM DEMO
