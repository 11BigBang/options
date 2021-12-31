"""Module that initially creates the database and tables.

This module must run before anything else to create the database locally and also create
any tables listed below.
"""
import sqlite3

conn = sqlite3.connect('options.db')

c = conn.cursor()

# Creating tables in SQLite are a bit different since it is made as simple as possible.
# The only data types available are NULL, INTEGER, REAL, TEXT, BLOB
c.execute("""CREATE TABLE gme (
            date integer,
            symbol text,
            type text,
            strike real,
            last real,
            bid real,
            b_size integer,
            ask real,
            a_size integer,
            volume integer,
            OI integer,
            IV real,
            delta real,
            theta real,
            gamma real,
            vega real,
            rho real
            )""")

conn.commit()

conn.close()