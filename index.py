from db.database import Database
from model.compra import Compra, Ingreso
from model.producto import Producto
from model.venta import Venta, Egreso
from screens.HomeWindow import HomeWindow

if __name__ == "__main__":
    # Arranca la base de datos

    conn = Database.get_connection()
    conn.create_tables([Compra, Venta, Ingreso, Egreso, Producto])
    app = HomeWindow()
    app.mainloop()
