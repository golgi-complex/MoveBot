import sqlite3 as sq
from main import bot


def sql_start():
    global base, cur
    base = sq.connect('client_requests.db')
    cur = base.cursor()
    if base:
        print('Data base connected is OK!')
    base.execute('CREATE TABLE IF NOT EXISTS requests(datetime PRIMARY KEY, client_name TEXT, client_phone TEXT, check_special TEXT, cargo TEXT, veight TEXT, kind_loading TEXT, check_pallets TEXT, pallets_count TEXT, pallets_dimension TEXT, cargo_dimensions TEXT, add_carcas TEXT, addres_loading TEXT, addres_docs TEXT, addres_unloading TEXT, date_loading TEXT, date_unloading TEXT, custom TEXT, custom_export TEXT, export_declaration TEXT, custom_import TEXT, insurance_cost TEXT, attention TEXT)')
    base.commit()


async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO requests VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', tuple(data.values()))
        base.commit()
