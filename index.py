from auth.AuthManager import AuthManager
from data.dummy import dummy_proveedores, dummy_productos, dummy_clientes
from db.database import Database, use_in_memory
from model.cliente import ClienteAR
from model.compra import Compra, Ingreso
from model.producto import Producto
from model.proveedor import ProveedorAR
from model.referencia import Referencia
from model.venta import Venta, Egreso
from repository.UserRepository import UserRepository
from screens.HomeWindow import HomeWindow
from services.ClienteService import ClienteService
from services.ProductoService import ProductoService
from services.ProveedorServices import ProveedorService
from services.UserService import UserService

if __name__ == "__main__":
    # Arranca la base de datos

    conn = Database.get_connection()
    conn.create_tables([Compra, Venta, Ingreso, Egreso, Producto, ProveedorAR, ClienteAR, Referencia])
    proveedores_service = ProveedorService()
    cliente_service = ClienteService()

    # check if admin user exists
    # if not, create it
    user_repo = UserRepository()
    user_repo.create_table()
    user_service = UserService(user_repo)
    if not user_service.find_user('admin'):
        # create root user with username 'admin' and password 'admin'
        auth = AuthManager.get_instance()
        auth.register_user('admin', 'admin')
        user_service.update_role('admin', 'admin')

    # Popular las tablas con datos de prueba si estamos usando la base de datos en memoria
    if use_in_memory:

        auth = AuthManager.get_instance()
        auth.register_user('username1', 'username1')
        user_service = UserService(UserRepository())
        user_service.update_role('username1', 'admin')

        for proveedor in dummy_proveedores:
            proveedores_service.save(proveedor['nombre'], proveedor['telefono'], proveedor['direccion'], )

        productos_service = ProductoService()
        for producto in dummy_productos:
            productos_service.crear(
                ProductoService.CrearProductoRequest(producto['nombre'], producto['costo'],
                                                     producto['precio'], producto['existencia']))

        for cliente in dummy_clientes:
            cliente_service.save(cliente['cedula'], cliente['nombre'], cliente['telefono'], cliente['direccion'])

    app = HomeWindow()
    app.mainloop()
