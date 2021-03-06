# Kivy imports
import random

from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty

from ui.screens.default_screen import DefaultScreen

Builder.load_file(r'ui\screens\listening_training_screen.kv')


class ListeningScreen(DefaultScreen):
    prompt = StringProperty("")
    user_text_field = ObjectProperty(None)
    decode_output_label = ObjectProperty(None)
    tapping_prompt_label = ObjectProperty(None)
    play_button = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(title='Listening Training', **kwargs)
        self.util = App.get_running_app().util

    def on_enter(self):
        Clock.schedule_once(self.init_listening_screen, 0)
        self.sound_list = []
        self.cur_sound_index = 0
        self.cur_sound = None

    def init_listening_screen(self, dt):
        self.tapping_prompt_label = self.ids.tapping_prompt_label
        self.user_text_field.children[2].children[2].disabled = False
        self.user_text_field.children[2].children[2].bind(on_press=lambda x: self.clear_input())
        self.training_prompt_dict = self.util.training_prompt_dict
        self.decode_output_label.text = "^-- click on the left button to clear" \
                                        " and the right button for new prompt --^\n" \
                                        "v---click here to replay audio and here" \
                                        " to play new audio --v"
        self.play_new_prompt()

    def check_answer(self, *args):
        user_input = self.user_text_field.text.lower()

        if self.prompt == user_input:
            self.decode_output_label.text = f"You got it right!"
            if self.util.training_difficulty == 'Easy':
                mnemonic_help = f" Remember {user_input} with mnemonic: {self.util.mnemonic_dict[user_input]}"
                self.decode_output_label.text += mnemonic_help
        else:
            self.decode_output_label.text = "nope you got it wrong!"

    def play_prompt(self):
        self.util.morse_helper.text_to_morse_sound(self.prompt)

    def play_new_prompt(self):
        self.clear_input()
        if self.util.training_difficulty == 'Easy':
            training_level = 'letter'
        elif self.util.training_difficulty == 'Medium':
            training_level = 'word'
        else:
            training_level = 'sentence'
        self.prompt = random.choice(self.util.training_prompt_dict[training_level])
        self.tapping_prompt_label.text = f"Please translate the morse code " \
                                         f"({training_level}) being played"

        self.play_prompt()

    def clear_input(self):
        self.user_text_field.text = ''
        self.decode_output_label.text = ""

    def return_menu(self):
        self.manager.current = 'training'

    def return_home(self):
        self.manager.current = 'home'
