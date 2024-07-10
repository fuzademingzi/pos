from sqlqueries import QueriesSQLite

conn = QueriesSQLite.create_connection("pdvDB.sqlite")

#list of tables
tables = ["productos", "usuarios", "ventas", "detalle_ventas"]

#list all users
users = QueriesSQLite.execute_read_query(conn, "SELECT * from usuarios")
print("Usuarios:")
for user in users:
    print(user)

#get all products
products = QueriesSQLite.execute_read_query(conn, "SELECT * from productos")
print("\nProductos:")
for product in products:
    print(product)

#get all sales
sales = QueriesSQLite.execute_read_query(conn, "SELECT * from ventas")
print("\nVentas:")
for sale in sales:
    print(sale)

#get all sales details
sales_details = QueriesSQLite.execute_read_query(conn, "SELECT * from detalle_ventas")
print("\nDetalle de ventas:")
for sale_detail in sales_details:
    print(sale_detail)

#delete all sales
QueriesSQLite.execute_query(conn, "DELETE FROM ventas", None)
QueriesSQLite.execute_query(conn, "DELETE FROM detalle_ventas", None)
