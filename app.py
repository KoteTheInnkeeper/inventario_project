from databases.database_management import InvDatabase

INVENTORY_DATABASE = './databases/inventory.db'

inv_database = InvDatabase(INVENTORY_DATABASE)

print(inv_database.update('cerveza quilmes 1l', 0, 0, 0))
