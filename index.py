from auth.AuthManager import AuthManager
from data.dummy import dummy_proveedores, dummy_productos, dummy_clientes
from db.database import Database, use_in_memory
from model.compra import Compra, Ingreso
from model.producto import Producto
from model.venta import Venta, Egreso
from screens.HomeWindow import HomeWindow
from services.ClienteService import ClienteService
from services.ProductoService import ProductoService
from services.ProveedorServices import ProveedorService

if __name__ == "__main__":
    # Arranca la base de datos

    # Popular las tablas con datos de prueba si estamos usando la base de datos en memoria
    if use_in_memory:
        conn = Database.get_connection()
        conn.create_tables([Compra, Venta, Ingreso, Egreso, Producto])
        proveedores_service = ProveedorService()
        cliente_service = ClienteService()

        auth = AuthManager.get_instance()
        auth.register_user('username1', 'username1')

        for proveedor in dummy_proveedores:
            proveedores_service.save(proveedor['nombre'], proveedor['telefono'], proveedor['direccion'], )

        productos_service = ProductoService()
        for producto in dummy_productos:
            productos_service.crear(
                ProductoService.CrearProductoRequest(producto['nombre'], producto['proveedor'], producto['costo'],
                                                     producto['precio'], producto['existencia']))

        for cliente in dummy_clientes:
            cliente_service.save(cliente['cedula'], cliente['nombre'], cliente['telefono'], cliente['direccion'])

    app = HomeWindow()
    app.mainloop()
