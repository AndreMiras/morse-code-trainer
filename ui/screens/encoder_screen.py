# TODO remove after debug
import random

from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.screenmanager import Screen
# kivymd imports
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextFieldRound

# Project imports
from ui.widgets.audio_indicator import AudioIndicator
from ui.widgets.nav_drawer import MyNavigationLayout

# Speech to text imports
try:
    import speech_recognition as sr
    SR_AVAILABLE = True
except ModuleNotFoundError:
    print('WARNING SPEECH_RECOGNITION NOT FOUND')
    SR_AVAILABLE = False


class EncoderScreen(Screen):
    def __init__(self, **kwargs):
        super(EncoderScreen, self).__init__(name=kwargs.get('name'))
        self.util = kwargs.get('util')
        self.ui_layout()

    def ui_layout(self):
        play_button_anchor = AnchorLayout(anchor_x='center', anchor_y='bottom',
                                          padding=[dp(25), dp(25), dp(25), dp(25)])

        # disable play button for now
        play_button = MDFloatingActionButton(icon='play', size=[dp(56), dp(56)])
        play_button.disabled = True
        play_button.opacity = 0
        # [76/255, 175/255, 80/255, 1]
        # play_button.md_bg_color = App.get_running_app().theme_cls.primary_color
        # play_button.text_color = [1, 1, 1, 1]
        # play_button.bind(on_press=lambda x: self.play_audio())
        # play_button_anchor.add_widget(play_button)

        self.encode_input = MDTextFieldRound(pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                             size_hint=(0.85, 0.5))
        self.encode_input.icon_right = 'send'

        self.encode_input.children[2].children[0].bind(
            on_press=lambda x: self.play_prompt())
        self.encode_input.icon_left = 'close-circle'
        self.encode_input.children[2].children[2].disabled = False
        self.encode_input.children[2].children[2].bind(on_press=lambda x: self.clear_input())

        encode_card = MDCard(padding=dp(24), spacing=dp(24),
                             orientation='vertical', size_hint_x=0.85,
                             size_hint_y=0.7, pos_hint={'top': 0.85, 'center_x': 0.5})
        encode_label = MDLabel(text='Encode Morse Code Audio',
                               font_style='Body1', halign='center', size_hint=(1, 0.5))
        encode_label.theme_text_color = 'Custom'
        encode_label.text_color = [1, 1, 1, 1]

        self.encode_output_label = MDLabel(text='Enter text to convert to morse code',
                                           halign='center', size_hint=(1, 0.5))
        self.encode_output_label.theme_text_color = 'Custom'
        self.encode_output_label.text_color = [1, 1, 1, 1]

        self.audio_indicator = AudioIndicator()
        self.audio_indicator.size_hint = (1, 2)
        Clock.schedule_interval(self.update_audio_indicator, 0.1)

        encode_card.add_widget(encode_label)
        encode_card.add_widget(self.audio_indicator)
        encode_card.add_widget(self.encode_output_label)
        encode_card.add_widget(self.encode_input)
        encode_card.md_bg_color = App.get_running_app().theme_cls.accent_color
        encode_card.elevation = 15

        self.add_widget(encode_card)
        self.add_widget(play_button_anchor)

        # Nav Bar
        self.nav_bar = MyNavigationLayout()
        self.nav_bar_anchor = AnchorLayout(anchor_x='center', anchor_y='top')
        self.nav_bar_anchor.add_widget(self.nav_bar)
        self.add_widget(self.nav_bar_anchor)

        self.cur_sound_index = 0
        self.sound_list = []
        self.cur_sound = None

    def clear_input(self):
        self.encode_input.text = ''
        self.encode_output_label.text = ''
        self.clear_sound()

    def update_audio_indicator(self, dt):
        if hasattr(self.audio_indicator, 'stack_width'):
            level_array = []
            for columns in range(self.audio_indicator.stack_width):
                level_array.append(random.randrange(0, self.audio_indicator.stack_height))
            self.audio_indicator.set_levels(level_array)

    def display_text_as_morse(self):
        prompt_as_morse = self.util.morse_helper.text_to_morse(self.prompt)
        self.encode_output_label.text = f'{self.prompt} as morse: {prompt_as_morse}'

    def play_prompt(self):
        self.prompt = self.encode_input.text
        self.clear_input()
        if self.cur_sound:
            self.cur_sound_index = 999999
            self.cur_sound.stop()
        print(f"playing morse for: {self.prompt}")
        self.display_text_as_morse()
        Clock.schedule_once(self.init_morse_sounds, 0)

    def clear_sound(self):
        if self.cur_sound:
            self.cur_sound.stop()
        self.cur_sound_index = 0
        self.sound_list = []
        self.cur_sound = None

    def init_morse_sounds(self, dt):
        self.clear_sound()

        for letter in self.prompt:
            if letter == ' ':
                self.sound_list.append('long_pause')
            else:
                self.sound_list.append(letter)
                self.sound_list.append('short_pause')

        if len(self.sound_list) > self.cur_sound_index:
            letter_to_play = self.sound_list[self.cur_sound_index]
            self.cur_sound = self.util.morse_helper.get_letter_as_morse_sound(letter_to_play)
            self.cur_sound.bind(on_stop=self.play_next_sound)
            self.cur_sound.play()

    def play_next_sound(self, dt):
        self.cur_sound_index += 1
        if len(self.sound_list) > self.cur_sound_index:
            letter_to_play = self.sound_list[self.cur_sound_index]
            self.cur_sound = self.util.morse_helper.get_letter_as_morse_sound(letter_to_play)
            self.cur_sound.bind(on_stop=self.play_next_sound)
            self.cur_sound.play()

    def speech_to_text(self):
        if SR_AVAILABLE:
            recognizedSpeech = ""

            # obtain audio from the microphone
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("Say something!")
                audio = r.listen(source)

            # # recognize speech using Google Cloud Speech
            # GOOGLE_CLOUD_SPEECH_CREDENTIALS = None
            # try:
            #     recognizedSpeech = r.recognize_google_cloud(audio,
            #                         credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS)
            #     print("Google Cloud:", recognizedSpeech)
            # except sr.UnknownValueError:
            #     print("Google Cloud Speech could not understand audio")
            # except sr.RequestError as e:
            #     print("Could not request results from Google Cloud Speech service; {0}".format(e))
            # except:
            #     print("Google Cloud: Another Exception occurred. Trying with Sphinx.")

            # If google cloud fails, try with Sphinx
            if recognizedSpeech == "":
                try:
                    recognizedSpeech = r.recognize_sphinx(audio)
                    print("Sphinx:", recognizedSpeech)
                except sr.UnknownValueError:
                    print("Sphinx could not understand audio")
                except sr.RequestError as e:
                    print("Sphinx error; {0}".format(e))

            self.encode_input.text = recognizedSpeech
        else:
            self.encode_input.text = ""

    def return_home(self):
        self.manager.current = 'welcome'
