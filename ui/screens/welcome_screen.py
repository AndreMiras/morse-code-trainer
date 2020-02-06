from kivy.properties import ObjectProperty, ListProperty
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.uix.anchorlayout import AnchorLayout
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.app import App
# Project imports
from ui.widgets.nav_drawer import MyNavigationLayout


Builder.load_string("""
#:import MDCard kivymd.uix.card
#:import MDToolbar kivymd.uix.toolbar
#:import MDRectangleFlatIconButton kivymd.uix.button
#:import MDLabel kivymd.uix.label
#:import WelcomButton ui.widgets.welcome_button

<WelcomeButton>
    elevation_normal: 10
    md_bg_color: app.theme_cls.primary_color
    md_border_color: app.theme_cls.primary_color

<WelcomeScreen>
    canvas.before:
        Rectangle:
            pos: self.pos
            size: self.size
            source: 'ui/img/morse_code_bg.jpg'
            tex_coords: root.tex_coords

    FloatLayout:
        size_hint: .65, .65
        pos_hint: {'center_x': 0.5, 'center_y': .5}
        canvas.before:
            Color:
                rgba:  app.theme_cls.accent_color
            RoundedRectangle:
                size: self.size
                pos: self.pos
                radius: [dp(10)]

        BoxLayout:
            size_hint: .8, .8
            orientation: 'vertical'
            pos_hint: {'center_x': 0.5, 'center_y': .5}

            Image:
                source: 'ui/img/welcome_morse_code.png'
                size_hint_y: .3
                allow_stretch: True

            Widget:
                size_hint_y: .1

            GridLayout:
                spacing: dp(20)
                cols: 2

                WelcomeButton:
                    text: 'Decode'
                    size_hint_x: 1
                    icon: 'database-export'
                    on_press:
                        root.manager.current = 'decode'

                WelcomeButton:
                    text: 'Encode'
                    icon: 'database-import'
                    size_hint_x: 1
                    on_press:
                        root.manager.current = 'encode'

                WelcomeButton:
                    text: 'Train'
                    icon: 'dumbbell'
                    size_hint_x: 1
                    on_press:
                        root.manager.current = 'training'

                WelcomeButton:
                    text: 'Calibrate'
                    icon: 'cogs'
                    size_hint_x: 1
                    on_press:
                        root.manager.current = 'calibration'

                WelcomeButton:
                    text: 'Sign In'
                    icon: 'login-variant'
                    size_hint_x: 1
                    on_press:
                        root.manager.current = 'sign_in'

                WelcomeButton:
                    text: 'Message'
                    icon: 'message'
                    size_hint_x: 1
                    on_press:
                        root.manager.current = 'message'
                        if app.util.auth_token == '': \
                        root.manager.current = 'sign_in'

""")


class WelcomeScreen(Screen):
    texture = ObjectProperty(None)
    tex_coords = ListProperty([0, 0, 1, 0, 1, 1, 0, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.texture_init, 0)
        Clock.schedule_interval(self.scroll_texture, 1 / 60.)

    def texture_init(self, *args):
        self.canvas.before.children[-1].texture.wrap = 'repeat'

    def scroll_texture(self, dt):
        for i in range(0, 8, 2):
            self.tex_coords[i] += dt / 3.
