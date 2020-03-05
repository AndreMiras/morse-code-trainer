# Kivy imports
import random

from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty

from ui.screens.default_screen import DefaultScreen

Builder.load_file(r'ui\screens\tapping_speed_test_screen.kv')


class TappingSpeedTestScreen(DefaultScreen):
    decode_morse_text = StringProperty('')
    decode_text = StringProperty('')
    prompt_display = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(title='Tapping Training', **kwargs)
        self.util = App.get_running_app().util
        self.morse_button_text = "Start Speed Test"
        self.prompt_text = ""
        self.prompt_display = ""
        self.cur_state = None
        self.reset_test()

    def update_displays(self, morse_code):
        self.decode_morse_text = self.decode_morse_text + ''.join(morse_code)
        self.decode_text = self.util.morse_helper.morse_to_text(self.decode_morse_text)

    def update_prompt(self):
        num_correct = self.calc_correct_position()
        self.prompt_display = f"[color = 3333ff]{self.prompt_text[:num_correct]}[/color]{self.prompt_text[num_correct:]}"

    def reset_test(self):
        self.decode_morse_text = ''
        self.decode_text = ''
        self.prompt_text = ''
        self.prompt_display = ""
        self.cur_state = 'stopped'

    def start_test(self):
        Clock.schedule_once(self.display_score_popup, 2)
        self.generate_prompt_text()

    def on_enter(self, *args):
        self.reset_test()

    def on_leave(self):
        super().on_leave()

    def tapped(self, morse_char):
        if self.cur_state == 'stopped':
            self.start_test()
            self.cur_state = "started"
        else:
            self.update_displays([morse_char])

    def calc_correct_position(self):
        num_correct = 0
        for decoded_char in self.decode_text:
            if self.prompt_text[num_correct] == decoded_char:
                num_correct += 1
        return num_correct

    def display_score_popup(self, _):
        num_correct = self.calc_correct_position()
        num_mistake = len(self.decode_text) - num_correct
        score_popup = Popup(title='test')
        score_popup.open()

    def generate_prompt_text(self):
        self.prompt_text = ' '.join(random.sample(self.util.training_prompt_dict['word'], 10))
        self.prompt_display = self.prompt_text

    def return_home(self):
        self.manager.current = 'home'

