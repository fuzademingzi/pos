from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.core.text import LabelBase

from sqlqueries import QueriesSQLite

# **注册支持中文的字体**
import os
# Register the custom font
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
LabelBase.register(name='SimHei', fn_regular=os.path.join(parent_dir, 'fonts', 'SimHei.ttf'))

Builder.load_file(os.path.join(parent_dir,'signin', 'signin.kv'))

class SigninWindow(BoxLayout):
    def __init__(self, poner_usuario_callback, **kwargs):
        super().__init__(**kwargs)
        self.poner_usuario = poner_usuario_callback

    def verificar_usuario(self, username, password):
        connection = QueriesSQLite.create_connection("pdvDB.sqlite")
        users = QueriesSQLite.execute_read_query(connection, "SELECT * from usuarios")
        if users:
            if username == '' or password == '':
                self.ids.signin_notificacion.text = '缺少用户名或密码'
                self.ids.signin_notificacion.font_name = 'SimHei'  # **设置字体**
            else:
                usuario = {}
                for user in users:
                    if user[0] == username:
                        usuario['nombre'] = user[1]
                        usuario['username'] = user[0]
                        usuario['password'] = user[2]
                        usuario['tipo'] = user[3]
                        break
                if usuario:
                    if usuario['password'] == password:
                        self.ids.username.text = ''
                        self.ids.password.text = ''
                        self.ids.signin_notificacion.text = ''
                        if usuario['tipo'] == 'trabajador':
                            self.parent.parent.current = 'scrn_ventas'
                        else:
                            self.parent.parent.current = 'scrn_admin'
                        self.poner_usuario(usuario)
                    else:
                        self.ids.signin_notificacion.text = '用户名或密码错误'
                        self.ids.signin_notificacion.font_name = 'SimHei'  # **设置字体**
                else:
                    self.ids.signin_notificacion.text = '用户名或密码错误'
                    self.ids.signin_notificacion.font_name = 'SimHei'  # **设置字体**
        else:
            usuario_tuple = ('admin', '默认用户', 'admin', 'admin')
            crear_usuario = "INSERT INTO usuarios (username, nombre, password, tipo) VALUES (?,?,?,?);"
            QueriesSQLite.execute_query(connection, crear_usuario, usuario_tuple)
            self.ids.signin_notificacion.text = '已创建默认用户 admin '
            self.ids.signin_notificacion.font_name = 'SimHei'  # **设置字体**

class SigninApp(App):
    def build(self):
        return SigninWindow()

if __name__ == "__main__":
    SigninApp().run()

