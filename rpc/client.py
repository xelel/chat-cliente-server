from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.screen import Screen
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.app import App
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
import threading
import grpc
import proto.chat_pb2 as chat
import proto.chat_pb2_grpc as rpc

address = 'localhost'
port = 11912


class NicknameScreen(Screen):
    def __init__(self, nick='', **kwargs):
        super().__init__(**kwargs)

    def show_data(self):
        texto=self.ids.nick.text
        if self.ids.nick.text is '':
            check_string = 'Please Enter a username'
            close_button = MDFlatButton(text='Close', on_release=self.close_dialog)

            self.dialog = MDDialog(title='UsernameCheck', text=check_string, size_hint=(0.7, 1), buttons=[close_button])
            self.dialog.open()
        else:
            self.manager.current='sala'
    def close_dialog(self, obj):
        self.dialog.dismiss()


class EnviarMsg(Screen):
    def __init__(self, mensagem=[], **kwargs):
        super().__init__(**kwargs)
        channel = grpc.insecure_channel(address + ':' + str(port))
        self.conn = rpc.ChatServerStub(channel)
        threading.Thread(target=self.__listen_for_messages, daemon=True).start()

    def addWidget(self, nick):
        texto = self.ids.texto.text

        if texto is not '':
            n=chat.Note()
            n.name=nick
            n.message=texto
            self.conn.SendNote(n)
            print("S[{}] {}".format(n.name, n.message))  # debugging statement

        self.ids.texto.text = ''

    def __listen_for_messages(self):
        for note in self.conn.ChatStream(chat.Empty()):  # this line will wait for new messages from the server!
            print("R[{}] {}".format(note.name, note.message))  # debugging statement
            self.ids.box.add_widget(Chat(note.name+': '+note.message))

    def _callback(self):
        self.manager.current='nickname'
class Chat(BoxLayout):
    def __init__(self, text='', **kwargs):
        super().__init__(**kwargs)
        self.ids.label.text = text


class ClientApp(MDApp):
    def build(self):
        self.title = 'Chat'
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = 'Red'


ClientApp().run()
