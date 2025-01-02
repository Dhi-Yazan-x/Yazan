import rarfile  # تأكد من تثبيت مكتبة rarfile
from kivy.core.clipboard import Clipboard
from kivymd.app import MDApp
from kivymd.uix.navigationdrawer import MDNavigationLayout, MDNavigationDrawer
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.list import OneLineIconListItem, IconLeftWidget, MDList
from kivymd.uix.slider import MDSlider
from kivymd.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.colorpicker import ColorPicker
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.filechooser import FileChooserListView, FileChooserIconView
from kivy.uix.textinput import TextInput
from kivy.properties import NumericProperty, ListProperty
from kivy.graphics import Color, Rectangle
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
import webbrowser
import requests
import os,shutil, zipfile,tarfile,patoolib
Window.size = (300, 600)

dhi_yazan = """
<CustomMDNavigationDrawer@MDNavigationDrawer>:
    canvas.before:
        Color:
            rgba: 0.95, 0.95, 0.95, 1
        Rectangle:
            pos: self.pos
            size: self.size

Screen:
    MDNavigationLayout:
        ScreenManager:
            Screen:
                BoxLayout:
                    orientation: 'vertical'
                    MDTopAppBar:
                        title: 'YAZAN[ME APP]'
                        md_bg_color: 0.1, 0.5, 0.8, 1
                        left_action_items: [['menu', lambda x: nav_drawer.set_state('open')]]
                    TextInput:
                        id: search_input
                        hint_text: 'Search for files...'
                        on_text: app.filter_files(self.text)
                    FileChooserListView:
                        id: file_chooser
                        on_selection: app.load_file(self.selection)
        CustomMDNavigationDrawer:
            id: nav_drawer
            size_hint_x: 0.8
            BoxLayout:
                orientation: 'vertical'
                Image:
                    source: 'main.jpg'
                MDLabel:
                    id: name_label
                    text: 'DhiYazan AL_Kadani'
                    font_style: 'Subtitle1'
                    size_hint_y: None
                    height: self.texture_size[1]
                    theme_text_color: "Secondary"
                MDLabel:
                    id: contact_label
                    text: 'Call me : +967776991059'
                    font_style: 'Caption'
                    size_hint_y: None
                    height: self.texture_size[1]
                ScrollView:
                    MDList:
                        OneLineIconListItem:
                            text: 'Call me'
                            on_press: app.call_me()
                            IconLeftWidget:
                                icon: 'phone'
                        OneLineIconListItem:
                            text: 'UserInfo'
                            on_press: app.show_files()
                            IconLeftWidget:
                                icon: 'account'
                        OneLineIconListItem:
                            text: 'Upload'
                            on_press: app.upload_file()
                            IconLeftWidget:
                                icon: 'upload'
                        OneLineIconListItem:
                            text: 'Download'
                            on_press: app.download_file()
                            IconLeftWidget:
                                icon: 'download'
                        OneLineIconListItem:
                            text: 'Remote Control'
                            on_press: app.remote_control()
                            IconLeftWidget:
                                icon: 'remote'
                        OneLineIconListItem:
                            text: 'Extract Files'
                            on_press: app.show_destination_chooser()
                            IconLeftWidget:
                                icon: 'text'
                        OneLineIconListItem:
                            text: 'Text Editor'
                            on_press: app.open_text_editor()
                            IconLeftWidget:
                                icon: 'text'
                        OneLineIconListItem:
                            text: 'Terminal Emulator'
                            on_press: app.open_terminal_emulator()
                            IconLeftWidget:
                                icon: 'terminal'
                        OneLineIconListItem:
                            text: 'Activity Record'
                            on_press: app.record_activity()
                            IconLeftWidget:
                                icon: 'record'
                        OneLineIconListItem:
                            text: 'Settings'
                            on_press: app.show_settings()
                            IconLeftWidget:
                                icon: 'cog'
                        OneLineIconListItem:
                            text: 'Exit'
                            on_press: app.logout()
                            IconLeftWidget:
                                icon: 'logout'
"""

class DhiYazan(MDApp):
    theme_color = ListProperty([0, 0, 0, 1])
    font_size = NumericProperty(14)
    destination_directory = ""

    def build(self):
        self.root = Builder.load_string(dhi_yazan)
        return self.root

    def call_me(self):
        webbrowser.open('tel:+967776991059')

    def download_file(self):
        url = "https://example.com/your_file.txt"  # استبدل هذا بالرابط الفعلي
        try:
            response = requests.get(url)
            with open("downloaded_file.txt", "wb") as f:
                f.write(response.content)
            popup = Popup(title='Successful', content=Label(text='The file was successfully downloaded!'), size_hint=(0.6, 0.3))
            popup.open()
        except Exception as e:
            popup = Popup(title='Erorr', content=Label(text=f'Failure to download the file successfully: {e}'), size_hint=(0.6, 0.3))
            popup.open()

    def logout(self):
        self.stop()

    def show_files(self):
        self.root.ids.file_chooser.path = os.path.expanduser('~')

    def filter_files(self, search_text):
        search_dirs = [
            os.path.join(os.path.expanduser('~'), 'Documents'),
            os.path.join(os.path.expanduser('~'), 'Downloads'),
            os.path.join(os.path.expanduser('~'), 'Desktop'),
        ]
        
        filtered_files = []
        
        for directory in search_dirs:
            if os.path.exists(directory):
                all_files = os.listdir(directory)
                for file in all_files:
                    file_path = os.path.join(directory, file)
                    if file.endswith(('.txt', '.zip', '.rar', '.tar', '.gz', '.7z', '.bz2', '.xz')):  # إضافة الامتدادات
                        filtered_files.append(file_path)

        file_chooser = self.root.ids.file_chooser
        file_chooser.filters = []
        file_chooser._update_files(filtered_files)

    def load_file(self, selection):
        if selection:
            selected_file = selection[0]
            content = self.read_file(selected_file)
            if content:
                self.show_edit_popup(selected_file, content)

    def read_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Erorr reading the file {file_path}: {e}")
            return None

    def edit_file(self, file_path, new_content):
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            popup = Popup(title='Successful', content=Label(text='The file has been modified!'), size_hint=(0.6, 0.3))
            popup.open()
        except Exception as e:
            popup = Popup(title='Erorr', content=Label(text=f'We could not edit the file: {e}'), size_hint=(0.6, 0.3))
            popup.open()

    def show_edit_popup(self, file_path, content):
        edit_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        self.text_input = TextInput(text=content, multiline=True, size_hint_y=None, height=300)
        edit_layout.add_widget(self.text_input)

        button_layout = BoxLayout(size_hint_y=None, height=50)
        
        save_button = Button(text='Save')
        save_button.bind(on_release=lambda x: self.edit_file(file_path, self.text_input.text))
        button_layout.add_widget(save_button)

        copy_button = Button(text='Copy')
        copy_button.bind(on_release=lambda x: self.copy_text())
        button_layout.add_widget(copy_button)

        cut_button = Button(text='Cut')
        cut_button.bind(on_release=lambda x: self.cut_text())
        button_layout.add_widget(cut_button)

        paste_button = Button(text='Paste')
        paste_button.bind(on_release=lambda x: self.paste_text())
        button_layout.add_widget(paste_button)

        edit_layout.add_widget(button_layout)

        popup = Popup(title='Edit the file', content=edit_layout, size_hint=(0.8, 0.8))
        popup.open()

    def copy_text(self):
        Clipboard.copy(self.text_input.text)

    def cut_text(self):
        Clipboard.copy(self.text_input.text)
        self.text_input.text = ''

    def paste_text(self):
        self.text_input.text += Clipboard.paste()

    def show_settings(self):
        settings_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        settings_title = Label(text='App settings', halign='center', size_hint_y=None, height=40)
        settings_layout.add_widget(settings_title)

        color_picker_label = Label(text="Choose the color:", size_hint_y=None, height=30)
        settings_layout.add_widget(color_picker_label)

        text_color_picker = ColorPicker()
        text_color_picker.bind(color=self.on_text_color_change)
        settings_layout.add_widget(text_color_picker)

        background_color_label = Label(text="Choose the background color:", size_hint_y=None, height=30)
        settings_layout.add_widget(background_color_label)

        background_color_picker = ColorPicker()
        background_color_picker.bind(color=self.on_background_color_change)
        settings_layout.add_widget(background_color_picker)

        font_size_label = Label(text="Font size:", size_hint_y=None, height=30)
        settings_layout.add_widget(font_size_label)

        font_size_slider = MDSlider(min=10, max=40, value=self.font_size)
        font_size_slider.bind(value=self.on_font_size_change)
        settings_layout.add_widget(font_size_slider)

        popup = Popup(title='Settings', content=settings_layout, size_hint=(0.8, 0.6))
        popup.open()

    def on_text_color_change(self, instance, value):
        self.theme_color = value
        self.update_labels()

    def on_background_color_change(self, instance, value):
        self.root.canvas.before.clear()
        with self.root.canvas.before:
            Color(*value)
            Rectangle(pos=self.root.pos, size=self.root.size)

    def on_font_size_change(self, instance, value):
        self.font_size = value
        self.update_labels()

    def update_labels(self):
        self.root.ids.name_label.color = self.theme_color
        self.root.ids.contact_label.color = self.theme_color
        self.root.ids.name_label.font_size = self.font_size
        self.root.ids.contact_label.font_size = self.font_size

    def remote_control(self):
        popup = Popup(title='Remote Control', content=Label(text='Under Development!'), size_hint=(0.6, 0.3))
        popup.open()

    def show_destination_chooser(self):
        # عرض نافذة اختيار المجلد
        chooser = FileChooserIconView()
        chooser.path = os.path.expanduser('~')  # بدء في المجلد الرئيسي
        chooser.bind(on_submit=self.set_destination_directory)  # ربط حدث عند تحديد مجلد
        popup = Popup(title='Choose the interface folder', content=chooser, size_hint=(0.8, 0.8))
        popup.open()

    def set_destination_directory(self, chooser, selection, touch):
        if selection:
            self.destination_directory = selection[0]  # تعيين المجلد المحدد
            self.extract_files()  # استدعاء وظيفة استخراج الملفات

    def extract_files(self):
        # تحديد المسار الحالي لمجلد التنزيلات
        source_directory = os.path.join(os.path.expanduser('~'), 'Downloads')  # مجلد التنزيلات

        # أنواع الملفات المضغوطة التي نريد دعمها
        file_extensions = ['.apk', '.zip', '.rar', '.tar', '.gz', '.7z', '.bz2', '.xz']
        
        try:
            # التأكد من وجود مجلد الوجهة
            if not self.destination_directory:
                popup = Popup(title='Eroor', content=Label(text='Please choose the front folder first!'), size_hint=(0.6, 0.3))
                popup.open()
                return
            
            # استعراض الملفات في مجلد التنزيلات
            files_to_extract = [f for f in os.listdir(source_directory) if any(f.endswith(ext) for ext in file_extensions)]
            if files_to_extract:
                for file in files_to_extract:
                    source_path = os.path.join(source_directory, file)
                    destination_path = os.path.join(self.destination_directory, file)
                    shutil.copy2(source_path, destination_path)  # نسخ الملف
                    self.extract_file(destination_path)  # فك ضغط الملف بعد النسخ
                popup = Popup(title='Successful', content=Label(text='The file was Successfully extracted!'), size_hint=(0.6, 0.3))
            else:
                popup = Popup(title='Erorr', content=Label(text='There are no files available in the downloads folder!'), size_hint=(0.6, 0.3))
            popup.open()
        except Exception as e:
            popup = Popup(title='Erorr', content=Label(text=f'File extraction failed: {e}'), size_hint=(0.6, 0.3))
            popup.open()

    def extract_file(self, file_path):
        """فك ضغط الملفات بناءً على نوع الملف."""
        if file_path.endswith('.zip'):
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                files = zip_ref.namelist()
                progress_popup = self.show_progress_popup(len(files))
                for i, file in enumerate(files):
                    zip_ref.extract(file, self.destination_directory)
                    progress_popup.value = (i + 1) / len(files) * 100
                progress_popup.dismiss()
        elif file_path.endswith('.tar'):
            with tarfile.open(file_path, 'r') as tar_ref:
                files = tar_ref.getnames()
                progress_popup = self.show_progress_popup(len(files))
                for i, file in enumerate(files):
                    tar_ref.extract(file, self.destination_directory)
                    progress_popup.value = (i + 1) / len(files) * 100
                progress_popup.dismiss()
        elif file_path.endswith('.gz'):
            with tarfile.open(file_path, 'r:gz') as tar_ref:
                files = tar_ref.getnames()
                progress_popup = self.show_progress_popup(len(files))
                for i, file in enumerate(files):
                    tar_ref.extract(file, self.destination_directory)
                    progress_popup.value = (i + 1) / len(files) * 100
                progress_popup.dismiss()
        elif file_path.endswith('.bz2'):
            with tarfile.open(file_path, 'r:bz2') as tar_ref:
                files = tar_ref.getnames()
                progress_popup = self.show_progress_popup(len(files))
                for i, file in enumerate(files):
                    tar_ref.extract(file, self.destination_directory)
                    progress_popup.value = (i + 1) / len(files) * 100
                progress_popup.dismiss()
        elif file_path.endswith('.rar'):
            with rarfile.RarFile(file_path) as rar_ref:
                files = rar_ref.namelist()
                progress_popup = self.show_progress_popup(len(files))
                for i, file in enumerate(files):
                    rar_ref.extract(file, self.destination_directory)
                    progress_popup.value = (i + 1) / len(files) * 100
                progress_popup.dismiss()
        elif file_path.endswith('.7z'):
            import patoolib  # تأكد من تثبيت مكتبة patool
            patoolib.extract_archive(file_path, outdir=self.destination_directory)
            popup = Popup(title='Successful', content=Label(text='The 7z file was Successfully unloaded!'), size_hint=(0.6, 0.3))
            popup.open()
        elif file_path.endswith('.xz'):
            import lzma
            with lzma.open(file_path) as xz_ref:
                with open(os.path.join(self.destination_directory, os.path.basename(file_path[:-3])), 'wb') as out_file:
                    out_file.write(xz_ref.read())
            popup = Popup(title='Successful', content=Label(text='The xz file was Successfully unloaded!'), size_hint=(0.6, 0.3))
            popup.open()
        
        # إظهار رسالة نجاح
        popup = Popup(title='Successful', content=Label(text=f'{file_path}was compressed Successfully !'), size_hint=(0.6, 0.3))
        popup.open()

    def show_progress_popup(self, total_files):
        """إظهار نافذة شريط التقدم."""
        progress_layout = BoxLayout(orientation='vertical', padding=10)
        progress_label = Label(text='Unzip the file...', size_hint_y=None, height=40)
        progress_bar = ProgressBar(max=100, size_hint_y=None, height=30)
        
        progress_layout.add_widget(progress_label)
        progress_layout.add_widget(progress_bar)

        popup = Popup(title=' Progress', content=progress_layout, size_hint=(0.8, 0.2))
        popup.open()

        return progress_bar

    def open_text_editor(self):
        popup = Popup(title='Text Editor', content=Label(text='Under Development!'), size_hint=(0.6, 0.3))
        popup.open()

    def open_terminal_emulator(self):
        popup = Popup(title='Terminal Emulator', content=Label(text='Under Development!'), size_hint=(0.6, 0.3))
        popup.open()

    def record_activity(self):
        popup = Popup(title='Activity Record', content=Label(text='Under Development!'), size_hint=(0.6, 0.3))
        popup.open()

if __name__ == '__main__':
    DhiYazan().run()
