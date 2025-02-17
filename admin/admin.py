from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import BooleanProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview import RecycleView
from kivy.uix.dropdown import DropDown
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.core.text import LabelBase

from sqlqueries import QueriesSQLite
from datetime import datetime, timedelta
import csv
from pathlib import Path
import platform

# **注册支持中文的字体**
import os
# Register the custom font
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
LabelBase.register(name='SimHei', fn_regular=os.path.join(parent_dir, 'fonts', 'SimHei.ttf'))

Builder.load_file(os.path.join(parent_dir,'admin', 'admin.kv'))

class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    touch_deselect_last = BooleanProperty(True) 

class SelectableProductoLabel(RecycleDataViewBehavior, BoxLayout):
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        self.ids['_hashtag'].text = str(1+index)
        self.ids['_codigo'].text = data['codigo']
        self.ids['_articulo'].text = data['nombre'].capitalize()
        self.ids['_cantidad'].text = str(data['cantidad'])
        self.ids['_precio'].text = str("{:.2f}".format(data['precio']))
        self.set_font()  # **设置字体**
        return super(SelectableProductoLabel, self).refresh_view_attrs(rv, index, data)

    def set_font(self):
        self.ids['_hashtag'].font_name = 'SimHei'
        self.ids['_codigo'].font_name = 'SimHei'
        self.ids['_articulo'].font_name = 'SimHei'
        self.ids['_cantidad'].font_name = 'SimHei'
        self.ids['_precio'].font_name = 'SimHei'

    def on_touch_down(self, touch):
        if super(SelectableProductoLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        self.selected = is_selected
        if is_selected:
            rv.data[index]['seleccionado'] = True
        else:
            rv.data[index]['seleccionado'] = False

class SelectableClienteLabel(RecycleDataViewBehavior, BoxLayout):
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        self.ids['_hashtag'].text = str(1 + index)
        self.ids['_client'].text = data['client']
        self.ids['_name'].text = data['name'].capitalize()
        self.ids['_tel_number'].text = data['tel_number']
        self.ids['_email'].text = data['email']
        self.ids['_address'].text = data['address']
        self.ids['_city'].text = data['city']
        self.ids['_birth_date'].text = data['birth_date']
        self.ids['_observations'].text = data['observations']
        self.set_font()  # **设置字体**
        return super(SelectableClienteLabel, self).refresh_view_attrs(rv, index, data)

    def set_font(self):
        self.ids['_hashtag'].font_name = 'SimHei'
        self.ids['_client'].font_name = 'SimHei'
        self.ids['_name'].font_name = 'SimHei'
        self.ids['_tel_number'].font_name = 'SimHei'
        self.ids['_email'].font_name = 'SimHei'
        self.ids['_address'].font_name = 'SimHei'
        self.ids['_city'].font_name = 'SimHei'
        self.ids['_birth_date'].font_name = 'SimHei'
        self.ids['_observations'].font_name = 'SimHei'

    def on_touch_down(self, touch):
        if super(SelectableClienteLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        self.selected = is_selected
        if is_selected:
            rv.data[index]['seleccionado'] = True
        else:
            rv.data[index]['seleccionado'] = False

class SelectableUsuarioLabel(RecycleDataViewBehavior, BoxLayout):
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        self.ids['_hashtag'].text = str(1+index)
        self.ids['_nombre'].text = data['nombre'].title()
        self.ids['_username'].text = data['username']
        self.ids['_tipo'].text = str(data['tipo'])
        self.set_font()  # **设置字体**
        return super(SelectableUsuarioLabel, self).refresh_view_attrs(rv, index, data)

    def set_font(self):
        self.ids['_hashtag'].font_name = 'SimHei'
        self.ids['_nombre'].font_name = 'SimHei'
        self.ids['_username'].font_name = 'SimHei'
        self.ids['_tipo'].font_name = 'SimHei'

    def on_touch_down(self, touch):
        if super(SelectableUsuarioLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        self.selected = is_selected
        if is_selected:
            rv.data[index]['seleccionado'] = True
        else:
            rv.data[index]['seleccionado'] = False

class ItemVentaLabel(RecycleDataViewBehavior, BoxLayout):
    index = None

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        self.ids['_hashtag'].text = str(1+index)
        self.ids['_codigo'].text = data['codigo']
        self.ids['_articulo'].text = data['producto'].capitalize()
        self.ids['_cantidad'].text = str(data['cantidad'])
        self.ids['_precio_por_articulo'].text = str("{:.2f}".format(data['precio']))+"/件"
        self.ids['_total'].text= str("{:.2f}".format(data['total']))
        self.set_font()  # **设置字体**
        return super(ItemVentaLabel, self).refresh_view_attrs(rv, index, data)

    def set_font(self):
        self.ids['_hashtag'].font_name = 'SimHei'
        self.ids['_codigo'].font_name = 'SimHei'
        self.ids['_articulo'].font_name = 'SimHei'
        self.ids['_cantidad'].font_name = 'SimHei'
        self.ids['_precio_por_articulo'].font_name = 'SimHei'
        self.ids['_total'].font_name = 'SimHei'

class SelectableVentaLabel(RecycleDataViewBehavior, BoxLayout):
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        self.ids['_hashtag'].text = str(1+index)
        self.ids['_username'].text = data['username']
        self.ids['_client'].text = data['client']
        self.ids['_cantidad'].text = str(data['productos'])
        self.ids['_total'].text = '€ '+str("{:.2f}".format(data['total']))
        self.ids['_time'].text = str(data['fecha'].strftime("%H:%M:%S"))
        self.ids['_date'].text = str(data['fecha'].strftime("%Y-%m-%d"))
        self.set_font()  # **设置字体**
        return super(SelectableVentaLabel, self).refresh_view_attrs(rv, index, data)

    def set_font(self):
        self.ids['_hashtag'].font_name = 'SimHei'
        self.ids['_username'].font_name = 'SimHei'
        self.ids['_client'].font_name = 'SimHei'
        self.ids['_cantidad'].font_name = 'SimHei'
        self.ids['_total'].font_name = 'SimHei'
        self.ids['_time'].font_name = 'SimHei'
        self.ids['_date'].font_name = 'SimHei'

    def on_touch_down(self, touch):
        if super(SelectableVentaLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        self.selected = is_selected
        if is_selected:
            rv.data[index]['seleccionado'] = True
        else:
            rv.data[index]['seleccionado'] = False

class AdminRV(RecycleView):
    def __init__(self, **kwargs):
        super(AdminRV, self).__init__(**kwargs)
        self.data=[]

    def agregar_datos(self,datos):
        for dato in datos:
            dato['seleccionado']=False
            self.data.append(dato)
        self.refresh_from_data()

    def dato_seleccionado(self):
        indice=-1
        for i in range(len(self.data)):
            if self.data[i]['seleccionado']:
                indice=i
                break
        return indice

class ProductoPopup(Popup):
    def __init__(self, agregar_callback, **kwargs):
        super(ProductoPopup, self).__init__(**kwargs)
        self.agregar_callback=agregar_callback

    def abrir(self, agregar, producto=None):
        if agregar:
            self.ids.producto_info_1.text='添加商品'
            self.ids.producto_info_1.font_name = 'SimHei'  # **设置字体**
            self.ids.producto_codigo.disabled=False
        else:
            self.ids.producto_info_1.text='修改商品'
            self.ids.producto_info_1.font_name = 'SimHei'  # **设置字体**
            self.ids.producto_codigo.text=producto['codigo']
            self.ids.producto_codigo.disabled=True
            self.ids.producto_nombre.text=producto['nombre']
            self.ids.producto_cantidad.text=str(producto['cantidad'])
            self.ids.producto_precio.text=str(producto['precio'])
        # **设置 TextInput 的字体**
        self.ids.producto_codigo.font_name = 'SimHei'
        self.ids.producto_nombre.font_name = 'SimHei'
        self.ids.producto_cantidad.font_name = 'SimHei'
        self.ids.producto_precio.font_name = 'SimHei'
        
        self.open()

    def verificar(self, producto_codigo, producto_nombre, producto_cantidad, producto_precio):
        alert1='缺少: '
        alert2=''
        validado={}
        if not producto_codigo:
            alert1+='编号. '
            validado['codigo']=False
        else:
            try:
                numeric=int(producto_codigo)
                validado['codigo']=producto_codigo
            except:
                alert2+='代码无效. '
                validado['codigo']=False

        if not producto_nombre:
            alert1+='品名. '
            validado['nombre']=False
        else:
            validado['nombre']=producto_nombre.lower()

        if not producto_precio:
            alert1+='价格. '
            validado['precio']=False
        else:
            try:
                numeric=float(producto_precio)
                validado['precio']=producto_precio
            except:
                alert2+='价格无效. '
                validado['precio']=False

        if not producto_cantidad:
            alert1+='数量. '
            validado['cantidad']=False
        else:
            try:
                numeric=int(producto_cantidad)
                validado['cantidad']=producto_cantidad
            except:
                alert2+='数量无效. '
                validado['cantidad']=False

        valores=list(validado.values())

        if False in valores:
            self.ids.no_valid_notif.text=alert1+alert2
            self.ids.no_valid_notif.font_name = 'SimHei'  # **设置字体**
        else:
            self.ids.no_valid_notif.text='验证通过'
            self.ids.no_valid_notif.font_name = 'SimHei'  # **设置字体**
            validado['cantidad']=int(validado['cantidad'])
            validado['precio']=float(validado['precio'])
            self.agregar_callback(True, validado)
            self.dismiss()

class VistaProductos(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.cargar_productos, 1)

    def cargar_productos(self, *args):
        _productos=[]
        connection=QueriesSQLite.create_connection("pdvDB.sqlite")
        inventario_sql=QueriesSQLite.execute_read_query(connection, "SELECT * from productos")
        if inventario_sql: 
            for producto in inventario_sql:
                _productos.append({'codigo': producto[0], 'nombre': producto[1], 'precio': producto[2], 'cantidad': producto[3]})
        self.ids.rv_productos.agregar_datos(_productos)

    def agregar_producto(self, agregar=False, validado=None):
        if agregar:
            producto_tuple=tuple(validado.values())
            connection=QueriesSQLite.create_connection("pdvDB.sqlite")
            crear_producto="""
            INSERT INTO
                productos (codigo, nombre, precio, cantidad)
            VALUES
                (?,?,?,?);
            """
            QueriesSQLite.execute_query(connection, crear_producto, producto_tuple)
            self.ids.rv_productos.data.append(validado)
            self.ids.rv_productos.refresh_from_data()
        else:
            popup=ProductoPopup(self.agregar_producto)
            popup.abrir(True)

    def modificar_producto(self, modificar=False, validado=None):
        indice=self.ids.rv_productos.dato_seleccionado()
        if modificar:
            producto_tuple=(validado['nombre'], validado['precio'], validado['cantidad'], validado['codigo'])
            connection=QueriesSQLite.create_connection("pdvDB.sqlite")
            actualizar="""
            UPDATE
                productos
            SET
                nombre=?, precio=?, cantidad=?
            WHERE
                codigo=?
            """
            QueriesSQLite.execute_query(connection, actualizar, producto_tuple)
            self.ids.rv_productos.data[indice]['nombre']=validado['nombre']
            self.ids.rv_productos.data[indice]['cantidad']=validado['cantidad']
            self.ids.rv_productos.data[indice]['precio']=validado['precio']
            self.ids.rv_productos.refresh_from_data()
        else:
            if indice>=0:
                producto=self.ids.rv_productos.data[indice]
                popup=ProductoPopup(self.modificar_producto)
                popup.abrir(False, producto)

    def eliminar_producto(self):
        indice=self.ids.rv_productos.dato_seleccionado()
        if indice>=0:
            producto_tuple=(self.ids.rv_productos.data[indice]['codigo'],)
            connection=QueriesSQLite.create_connection("pdvDB.sqlite")
            borrar= """DELETE from productos WHERE codigo =? """
            QueriesSQLite.execute_query(connection, borrar, producto_tuple)
            self.ids.rv_productos.data.pop(indice)
            self.ids.rv_productos.refresh_from_data()

    def actualizar_productos(self, producto_actualizado):
        for producto_nuevo in producto_actualizado:
            for producto_viejo in self.ids.rv_productos.data:
                if producto_nuevo['codigo']==producto_viejo['codigo']:
                    producto_viejo['cantidad']=producto_nuevo['cantidad']
                    break
        self.ids.rv_productos.refresh_from_data()

class ClientePopup(Popup):
    def __init__(self, agregar_callback, **kwargs):
        super(ClientePopup, self).__init__(**kwargs)
        self.agregar_callback = agregar_callback

    def abrir(self, agregar, cliente=None):
        if agregar:
            self.ids.cliente_info_1.text = '添加客户'
            self.ids.cliente_info_1.font_name = 'SimHei'  # **设置字体**
            self.ids.cliente_id.disabled = False
        else:
            self.ids.cliente_info_1.text = '修改客户'
            self.ids.cliente_info_1.font_name = 'SimHei'  # **设置字体**
            self.ids.cliente_id.text = cliente['client']
            self.ids.cliente_id.disabled = True
            self.ids.cliente_nombre.text = cliente['name']
            self.ids.cliente_telefono.text = cliente['tel_number']
            self.ids.cliente_email.text = cliente['email']
            self.ids.cliente_direccion.text = cliente['address']
            self.ids.cliente_ciudad.text = cliente['city']
            self.ids.cliente_fecha_nacimiento.text = cliente['birth_date']
            self.ids.cliente_observaciones.text = cliente['observations']

        # **设置 TextInput 的字体**
        self.ids.cliente_id.font_name = 'SimHei'
        self.ids.cliente_nombre.font_name = 'SimHei'
        self.ids.cliente_telefono.font_name = 'SimHei'
        self.ids.cliente_email.font_name = 'SimHei'
        self.ids.cliente_direccion.font_name = 'SimHei'
        self.ids.cliente_ciudad.font_name = 'SimHei'
        self.ids.cliente_fecha_nacimiento.font_name = 'SimHei'
        self.ids.cliente_observaciones.font_name = 'SimHei'

        self.open()

    def verificar(self, cliente_id, cliente_nombre, cliente_telefono, cliente_email, cliente_direccion, cliente_ciudad,
                  cliente_fecha_nacimiento, cliente_observaciones):
        alert1 = '缺少: '
        alert2 = ''
        validado = {}
        if not cliente_id:
            alert1 += 'ID. '
            validado['client'] = False
        else:
            validado['client'] = cliente_id

        if not cliente_nombre:
            alert1 += '姓名. '
            validado['name'] = False
        else:
            validado['name'] = cliente_nombre.lower()

        if not cliente_telefono:
            alert1 += '电话. '
            validado['tel_number'] = False
        else:
            validado['tel_number'] = cliente_telefono

        if not cliente_email:
            alert1 += '邮箱. '
            validado['email'] = False
        else:
            validado['email'] = cliente_email

        if not cliente_direccion:
            alert1 += '地址. '
            validado['address'] = False
        else:
            validado['address'] = cliente_direccion

        if not cliente_ciudad:
            alert1 += '邮编. '
            validado['city'] = False
        else:
            validado['city'] = cliente_ciudad

        if not cliente_fecha_nacimiento:
            alert1 += '出生日期. '
            validado['birth_date'] = False
        else:
            validado['birth_date'] = cliente_fecha_nacimiento

        if not cliente_observaciones:
            alert1 += '备注. '
            validado['observations'] = False
        else:
            validado['observations'] = cliente_observaciones

        valores = list(validado.values())

        if False in valores:
            self.ids.no_valid_notif.text = alert1 + alert2
            self.ids.no_valid_notif.font_name = 'SimHei'  # **设置字体**
        else:
            self.ids.no_valid_notif.text = '验证通过'
            self.ids.no_valid_notif.font_name = 'SimHei'  # **设置字体**
            self.agregar_callback(True, validado)
            self.dismiss()


class VistaClientes(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.cargar_clientes, 1)

    def cargar_clientes(self, *args):
        _clientes = []
        connection = QueriesSQLite.create_connection("pdvDB.sqlite")
        clientes_sql = QueriesSQLite.execute_read_query(connection, "SELECT * from clients")
        if clientes_sql:
            for cliente in clientes_sql:
                _clientes.append({
                    'client': cliente[0],
                    'name': cliente[1],
                    'tel_number': cliente[2],
                    'email': cliente[3],
                    'address': cliente[4],
                    'city': cliente[5],
                    'birth_date': cliente[6],
                    'observations': cliente[7]
                })
        self.ids.rv_clientes.agregar_datos(_clientes)

    def agregar_cliente(self, agregar=False, validado=None):
        if agregar:
            cliente_tuple = tuple(validado.values())
            connection = QueriesSQLite.create_connection("pdvDB.sqlite")
            crear_cliente = """
            INSERT INTO
                clients (client, name, tel_number, email, address, city, birth_date, observations)
            VALUES
                (?,?,?,?,?,?,?,?);
            """
            QueriesSQLite.execute_query(connection, crear_cliente, cliente_tuple)
            self.ids.rv_clientes.data.append(validado)
            self.ids.rv_clientes.refresh_from_data()
        else:
            popup = ClientePopup(self.agregar_cliente)
            popup.abrir(True)

    def modificar_cliente(self, modificar=False, validado=None):
        indice = self.ids.rv_clientes.dato_seleccionado()
        if modificar:
            cliente_tuple = (
                validado['name'],
                validado['tel_number'],
                validado['email'],
                validado['address'],
                validado['city'],
                validado['birth_date'],
                validado['observations'],
                validado['client']
            )
            connection = QueriesSQLite.create_connection("pdvDB.sqlite")
            actualizar = """
            UPDATE
                clients
            SET
                name=?, tel_number=?, email=?, address=?, city=?, birth_date=?, observations=?
            WHERE
                client=?
            """
            QueriesSQLite.execute_query(connection, actualizar, cliente_tuple)
            self.ids.rv_clientes.data[indice]['name'] = validado['name']
            self.ids.rv_clientes.data[indice]['tel_number'] = validado['tel_number']
            self.ids.rv_clientes.data[indice]['email'] = validado['email']
            self.ids.rv_clientes.data[indice]['address'] = validado['address']
            self.ids.rv_clientes.data[indice]['city'] = validado['city']
            self.ids.rv_clientes.data[indice]['birth_date'] = validado['birth_date']
            self.ids.rv_clientes.data[indice]['observations'] = validado['observations']
            self.ids.rv_clientes.refresh_from_data()
        else:
            if indice >= 0:
                cliente = self.ids.rv_clientes.data[indice]
                popup = ClientePopup(self.modificar_cliente)
                popup.abrir(False, cliente)

    def eliminar_cliente(self):
        indice = self.ids.rv_clientes.dato_seleccionado()
        if indice >= 0:
            cliente_tuple = (self.ids.rv_clientes.data[indice]['client'],)
            connection = QueriesSQLite.create_connection("pdvDB.sqlite")
            borrar = """DELETE from clients WHERE client =? """
            QueriesSQLite.execute_query(connection, borrar, cliente_tuple)
            self.ids.rv_clientes.data.pop(indice)
            self.ids.rv_clientes.refresh_from_data()

    def actualizar_clientes(self, cliente_actualizado):
        for cliente_nuevo in cliente_actualizado:
            for cliente_viejo in self.ids.rv_clientes.data:
                if cliente_nuevo['client'] == cliente_viejo['client']:
                    cliente_viejo['tel_number'] = cliente_nuevo['tel_number']
                    cliente_viejo['email'] = cliente_nuevo['email']
                    cliente_viejo['address'] = cliente_nuevo['address']
                    cliente_viejo['city'] = cliente_nuevo['city']
                    cliente_viejo['birth_date'] = cliente_nuevo['birth_date']
                    cliente_viejo['observations'] = cliente_nuevo['observations']
                    break
        self.ids.rv_clientes.refresh_from_data()


class UsuarioPopup(Popup):
    def __init__(self, _agregar_callback, **kwargs):
        super(UsuarioPopup, self).__init__(**kwargs)
        self.agregar_usuario=_agregar_callback

    def abrir(self, agregar, usuario=None):
        if agregar:
            self.ids.usuario_info_1.text='添加用户'
            self.ids.usuario_info_1.font_name = 'SimHei'  # **设置字体**
            self.ids.usuario_username.disabled=False
        else:
            self.ids.usuario_info_1.text='编辑用户'
            self.ids.usuario_info_1.font_name = 'SimHei'  # **设置字体**
            self.ids.usuario_username.text=usuario['username']
            self.ids.usuario_username.disabled=True
            self.ids.usuario_nombre.text=usuario['nombre']
            self.ids.usuario_password.text=usuario['password']
            if usuario['tipo']=='admin':
                self.ids.admin_tipo.state='down'
            else:
                self.ids.trabajador_tipo.state='down'
        self.open()

    def verificar(self, usuario_username, usuario_nombre, usuario_password, admin_tipo, trabajador_tipo):
        alert1 = 'Falta: '
        validado = {}
        if not usuario_username:
            alert1+='Username. '
            validado['username']=False
        else:
            validado['username']=usuario_username

        if not usuario_nombre:
            alert1+='Nombre. '
            validado['nombre']=False
        else:
            validado['nombre']=usuario_nombre.lower()

        if not usuario_password:
            alert1+='Password. '
            validado['password']=False
        else:
            validado['password']=usuario_password

        if admin_tipo=='normal' and trabajador_tipo=='normal':
            alert1+='Tipo. '
            validado['tipo']=False
        else:
            if admin_tipo=='down':
                validado['tipo']='admin'
            else:
                validado['tipo']='trabajador'

        valores = list(validado.values())

        if False in valores:
            self.ids.no_valid_notif.text=alert1
            self.ids.no_valid_notif.font_name = 'SimHei'  # **设置字体**
        else:
            self.ids.no_valid_notif.text=''
            self.agregar_usuario(True,validado)
            self.dismiss()

class VistaUsuarios(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.cargar_usuarios, 1)

    def cargar_usuarios(self, *args):
        _usuarios=[]
        connection=QueriesSQLite.create_connection("pdvDB.sqlite")
        usuarios_sql=QueriesSQLite.execute_read_query(connection, "SELECT * from usuarios")
        if usuarios_sql: 
            for usuario in usuarios_sql:
                _usuarios.append({'nombre': usuario[1], 'username': usuario[0], 'password': usuario[2], 'tipo': usuario[3]})
        self.ids.rv_usuarios.agregar_datos(_usuarios)

    def agregar_usuario(self, agregar=False, validado=None):
        if agregar:
            usuario_tuple=tuple(validado.values())
            connection=QueriesSQLite.create_connection("pdvDB.sqlite")
            crear_usuario = """
            INSERT INTO
                usuarios (username, nombre, password, tipo)
            VALUES
                (?,?,?,?);
            """
            QueriesSQLite.execute_query(connection, crear_usuario, usuario_tuple)
            self.ids.rv_usuarios.data.append(validado)
            self.ids.rv_usuarios.refresh_from_data()
        else:
            popup=UsuarioPopup(self.agregar_usuario)
            popup.abrir(True)

    def modificar_usuario(self, modificar=False, validado=None):
        indice = self.ids.rv_usuarios.dato_seleccionado()
        if modificar:
            usuario_tuple=(validado['nombre'],validado['password'],validado['tipo'],validado['username'])
            connection=QueriesSQLite.create_connection("pdvDB.sqlite")
            actualizar = """
            UPDATE
              usuarios
            SET
              nombre=?, password=?, tipo = ?
            WHERE
              username = ?
            """
            QueriesSQLite.execute_query(connection, actualizar, usuario_tuple)
            self.ids.rv_usuarios.data[indice]['nombre']=validado['nombre']
            self.ids.rv_usuarios.data[indice]['tipo']=validado['tipo']
            self.ids.rv_usuarios.data[indice]['password']=validado['password']
            self.ids.rv_usuarios.refresh_from_data()
        else:
            if indice>=0:
                usuario = self.ids.rv_usuarios.data[indice]
                popup = UsuarioPopup(self.modificar_usuario)
                popup.abrir(False,usuario)

    def eliminar_usuario(self):
        indice = self.ids.rv_usuarios.dato_seleccionado()
        if indice>=0:
            usuario_tuple=(self.ids.rv_usuarios.data[indice]['username'],)
            connection=QueriesSQLite.create_connection("pdvDB.sqlite")
            borrar = """DELETE from usuarios where username = ?"""
            QueriesSQLite.execute_query(connection, borrar, usuario_tuple)
            self.ids.rv_usuarios.data.pop(indice)
            self.ids.rv_usuarios.refresh_from_data()

class InfoVentaPopup(Popup):
    connection=QueriesSQLite.create_connection("pdvDB.sqlite")
    select_item_query=" SELECT nombre FROM productos WHERE codigo = ?  "
    def __init__(self, venta, **kwargs):
        super(InfoVentaPopup, self).__init__(**kwargs)    
        self.venta=[{"codigo": producto[3], "producto": QueriesSQLite.execute_read_query(self.connection, self.select_item_query, (producto[3],))[0][0], "cantidad": producto[4], "precio": producto[2], "total": producto[4]*producto[2]} for producto in venta]

    def mostrar(self):
        self.open()
        total_items=0
        total_dinero=0.0
        for articulo in self.venta:
            total_items+=articulo['cantidad']
            total_dinero+=articulo['total']
        self.ids.total_items.text=str(total_items)
        self.ids.total_items.font_name = 'SimHei'  # **设置字体**
        self.ids.total_dinero.text="€ "+str("{:.2f}".format(total_dinero))
        self.ids.total_dinero.font_name = 'SimHei'  # **设置字体**
        self.ids.info_rv.agregar_datos(self.venta)

class VistaVentas(Screen):
    productos_actuales=[]
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def crear_csv(self):
        connection=QueriesSQLite.create_connection("pdvDB.sqlite")
        select_item_query=" SELECT nombre FROM productos WHERE codigo=? "
        if self.ids.ventas_rv.data:
            path = Path(__file__).absolute().parent
            if platform.system() == 'Windows':
                csv_nombre = path.__str__() + '\\ventas_csv\\'
            else:
                csv_nombre = path.__str__() + '/ventas_csv/'
            isExist = os.path.exists(csv_nombre)
            if not isExist:
                os.makedirs(csv_nombre)

            csv_nombre += self.ids.date_id.text+'.csv'

            productos_csv=[]
            total=0

            for venta in self.productos_actuales:
                for item in venta:
                    item_found=next((producto for producto in productos_csv if producto["codigo"] == item[3]), None)
                    total+=item[2]*item[4]
                    if item_found:
                        item_found['cantidad']+=item[4]
                        item_found['precio_total']=item_found['precio']*item_found['cantidad']
                    else:
                        nombre=QueriesSQLite.execute_read_query(connection, select_item_query, (item[3],))[0][0]
                        productos_csv.append({'nombre': nombre, 'codigo': item[3], 'cantidad': item[4], 'precio': item[2], 'precio_total': item[2]*item[4]})
            fieldnames=['nombre', 'codigo', 'cantidad', 'precio', 'precio_total']
            bottom=[{'precio_total': total}]
            with open(csv_nombre, 'w', encoding='UTF8', newline='') as f:
                writer=csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(productos_csv)
                writer.writerows(bottom)
            self.ids.notificacion.text='表格已生成'
            self.ids.notificacion.font_name = 'SimHei'  # **设置字体**
        else:
            self.ids.notificacion.text='没有需要导出的数据'
            self.ids.notificacion.font_name = 'SimHei'  # **设置字体**

    def mas_info(self):
        indice=self.ids.ventas_rv.dato_seleccionado()
        if indice>=0:
            venta=self.productos_actuales[indice]
            p=InfoVentaPopup(venta)
            p.mostrar()

    def cargar_venta(self, choice='Default'):
        connection = QueriesSQLite.create_connection("pdvDB.sqlite")
        valid_input=True
        final_sum=0
        f_inicio=datetime.strptime('1970-01-01', '%Y-%m-%d')
        f_fin=datetime.strptime('2099-12-31', '%Y-%m-%d')

        _ventas=[]
        _total_productos=[]

        select_ventas_query = " SELECT * FROM ventas WHERE fecha BETWEEN ? AND ? "
        selec_productos_query = " SELECT * FROM ventas_detalle WHERE id_venta=? "

        self.ids.ventas_rv.data=[]
        if choice=='Default':
            f_inicio=datetime.today().date()
            f_fin=f_inicio+timedelta(days=1)
            self.ids.date_id.text=str(f_inicio.strftime("%Y-%m-%d"))
            self.ids.date_id.font_name = 'SimHei'  # **设置字体**
        elif choice=='Yesterday':
            f_fin=datetime.today().date()
            f_inicio=f_fin-timedelta(days=1)
            self.ids.date_id.text=str(f_inicio.strftime("%Y-%m-%d"))
            self.ids.date_id.font_name = 'SimHei'  # **设置字体**
        elif choice=='Date':
            date=self.ids.single_date.text
            try:
                f_elegida=datetime.strptime(date,'%Y-%m-%d')
            except:
                valid_input=False
            if valid_input:
                f_inicio=f_elegida
                f_fin=f_elegida+timedelta(days=1)
                self.ids.date_id.text=f_elegida.strftime('%Y-%m-%d')
                self.ids.date_id.font_name = 'SimHei'  # **设置字体**
        else:
            if self.ids.initial_date.text:
                initial_date=self.ids.initial_date.text
                try:
                    f_inicio=datetime.strptime(initial_date, '%Y-%m-%d')
                except:
                    valid_input=False
            if self.ids.last_date.text:
                last_date=self.ids.last_date.text
                try:
                    f_fin=datetime.strptime(last_date, '%Y-%m-%d')
                except:
                    valid_input=False
            if valid_input:
                self.ids.date_id.text=f_inicio.strftime("%Y-%m-%d")+" - "+f_fin.strftime("%Y-%m-%d")
                self.ids.date_id.font_name = 'SimHei'  # **设置字体**

        if valid_input:
            inicio_fin=(f_inicio, f_fin)
            ventas_sql=QueriesSQLite.execute_read_query(connection, select_ventas_query, inicio_fin)
            if ventas_sql:
                for venta in ventas_sql:
                    final_sum+=venta[1]
                    ventas_detalle_sql=QueriesSQLite.execute_read_query(connection, selec_productos_query, (venta[0],))
                    _total_productos.append(ventas_detalle_sql)
                    count=0
                    for producto in ventas_detalle_sql:
                        count+=producto[4]
                    _ventas.append({"username": venta[3], "client": venta[4], "productos": count, "total": venta[1], "fecha": datetime.strptime(venta[2], '%Y-%m-%d %H:%M:%S.%f')})
                self.ids.ventas_rv.agregar_datos(_ventas)
                print(self.ids.ventas_rv)
                self.productos_actuales=_total_productos
        self.ids.final_sum.text='€ '+str("{:.2f}".format(final_sum))
        self.ids.final_sum.font_name = 'SimHei'  # **设置字体**
        self.ids.initial_date.text=''
        self.ids.last_date.text=''
        self.ids.single_date.text=''
        self.ids.notificacion.text='销售数据'
        self.ids.notificacion.font_name = 'SimHei'  # **设置字体**

class CustomDropDown(DropDown):
    def __init__(self, cambiar_callback, **kwargs):
        self._succ_cb = cambiar_callback
        super(CustomDropDown, self).__init__(**kwargs)

    def vista(self, vista):
        if callable(self._succ_cb):
            self._succ_cb(True, vista)

class AdminWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.vista_actual='Productos'
        self.vista_manager=self.ids.vista_manager
        self.dropdown = CustomDropDown(self.cambiar_vista)
        self.ids.cambiar_vista.bind(on_release=self.dropdown.open)

    def cambiar_vista(self, cambio=False, vista=None):
        if cambio:
            d = {'商品管理': 'Productos', '用户管理': 'Usuarios', '销售记录': 'Ventas', '客户管理': 'Clientes'}
            print(d[vista])
            self.vista_actual=d[vista]
            self.vista_manager.current=self.vista_actual
            self.dropdown.dismiss()

    def signout(self):
        self.parent.parent.current='scrn_signin'

    def venta(self):
        self.parent.parent.current='scrn_ventas'

    def actualizar_productos(self, productos):
        self.ids.vista_productos.actualizar_productos(productos)

class AdminApp(App):
    def build(self):
        return AdminWindow()

if __name__=="__main__":
    AdminApp().run()

