import numpy as np

from util.sound_engine import SoundEngine


class MorseEngine:
    def __init__(self):
        self.__letter_to_morse = {'a': '.-', 'b': '-...', 'c': '-.-.', 'd': '-..', 'e': '.', 'f': '..-.', 'g': '--.',
                                  'h': '....', 'i': '..', 'j': '.---', 'k': '-.-', 'l': '.-..', 'm': '--', 'n': '-.',
                                  'o': '---', 'p': '.--.', 'q': '--.-', 'r': '.-.', 's': '...', 't': '-', 'u': '..-',
                                  'v': '...-', 'w': '.--', 'x': '-..-', 'y': '-.--', 'z': '--..',
                                  '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
                                  '6': '-....', '7': '--...', '8': '---..', '9': '----.', ' ': '/'}
        self.__morse_to_letter = {morse: letter for letter, morse in self.__letter_to_morse.items()}
        self.speaker = SoundEngine()
        self.rate = 16000
        self.morse_time_unit = .08
        self.beep_pitch = 200
        self.morse_signal_templates = self.gen_morse_signal_template(self.beep_pitch, self.morse_time_unit)

    def gen_morse_signal_template(self, frequency, morse_time_unit):
        morse_time_sample = int(self.rate * morse_time_unit)
        short_short_pause = np.zeros(morse_time_sample * 1)
        short_pause = np.zeros(morse_time_sample * 2)
        long_pause = np.zeros(morse_time_sample * 6)

        dot_sig = np.sin(frequency * 2 * np.pi * np.arange(morse_time_sample) / self.rate)
        dot_sig[:100] = dot_sig[:100] * np.linspace(0, 1, 100)
        dot_sig[-100:] = dot_sig[-100:] * np.linspace(1, 0, 100)
        dot_sig = np.concatenate([dot_sig, short_short_pause]).astype(np.float32).tostring()

        dash_sig = np.sin(frequency * 2 * np.pi * np.arange(morse_time_sample * 3) / self.rate)
        dash_sig[:100] = dash_sig[:100] * np.linspace(0, 1, 100)
        dash_sig[-100:] = dash_sig[-100:] * np.linspace(1, 0, 100)
        dash_sig = dash_sig.astype(np.float32).tostring()
        dash_sig = np.concatenate([dash_sig, short_short_pause]).astype(np.float32).tostring()
        return {'dot': dot_sig, 'dash': dash_sig, 'spause': short_pause, 'lpause': long_pause}

    def morse_to_text(self, morse_code):
        text = ''
        morse_words = [word.strip() for word in morse_code.split('/') if word.strip() != '']
        for morse_word in morse_words:
            for morse_letter in morse_word.split(' '):
                if morse_letter in self.__morse_to_letter:
                    text += self.__morse_to_letter[morse_letter]
                else:
                    text += '?'
            text += ' '
        return text.strip().strip('/')

    def text_to_morse(self, text):
        morse_code = ''
        text = text.lower()
        for letter in text:
            if letter in self.__letter_to_morse:
                morse_code += self.__letter_to_morse[letter] + ' '
            else:
                morse_code += '?'
        return morse_code

    def text_to_morse_sound(self, text):
        self.morse_to_sound(self.text_to_morse(text))

    def morse_to_sound(self, morse_code):
        signal_list = []
        for code in morse_code:
            if code == '.':
                signal_list.append(self.morse_signal_templates['dot'])
            elif code == '-':
                signal_list.append(self.morse_signal_templates['dash'])
            elif code == ' ':
                signal_list.append(self.morse_signal_templates['spause'])
            elif code == '/':
                signal_list.append(self.morse_signal_templates['lpause'])
        self.speaker.play_audio_as_thread(signal_list)
