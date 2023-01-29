import random
import kivy
import pickle

kivy.require('2.1.0')  # replace with your current kivy version !

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.animation import Animation
from kivy.uix.widget import Widget
from kivy.core.window import Window


class Testing(Widget):
    pass


class Cookie(AnchorLayout):

    def __init__(self, **kwargs):
        super(Cookie, self).__init__(**kwargs)

        self.label = Label()
        self.cookie_image = Image(source='cookie.png')
        self.cookie_anim = Animation(size_hint_y=0, size_hint_x=0, t='in_back') \
                           + Animation(size_hint_y=0.5, size_hint_x=0.5, t='in_back')
        self.scroll_anim = Animation(pos=(100, 100), t='linear')
        self.label_anim = Animation(size_hint_y=2.5, size_hint_x=2.5, t='out_circ') + Animation(size_hint_y=1, size_hint_x=1, t='out_circ')

        btn = Button()
        btn.bind(on_press=self.callback)
        btn.background_color = (9, 1, 2, 0.7)

        self.cookie_image.allow_stretch = True
        self.cookie_image.size_hint_x = 0.5
        self.cookie_image.size_hint_y = 0.5

        self.label.color = (0, 0, 0, 1)
        self.label.size = self.label.texture_size
        self.label.font_name = "Brush Script"
        self.label.font_size = 70

        self.add_widget(btn)
        self.add_widget(self.cookie_image)
        self.add_widget(self.label)

    def callback(self, event):
        fortune = Fortune()
        self.label.text = fortune.generate_fortune()
        scroll = CookieScroll(anchor_x='center', anchor_y='center')
        self.add_widget(scroll, 2)
        self.cookie_anim.start(self.cookie_image)

        self.label_anim.start(self.label)

        # self.scroll_anim.start(scroll.scroll_image)


class CookieScroll(AnchorLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scroll_image = Image(source='scroll.png')

        self.scroll_image.allow_stretch = True
        self.scroll_image.size = (700, 200)
        # self.scroll_image.size_hint_y = 0.1
        self.add_widget(self.scroll_image)


class EvilCookieApp(App):

    def build(self):
        cookie = Cookie(anchor_x='center', anchor_y='top')
        return cookie


class Fortune:

    def fill_in_madlib(self, madlib, dictionary):

        keys = dictionary.keys()

        for key in keys:
            while key in madlib:
                index = madlib.index(key)  # index of first char of key
                blank_start = index - 1  # index of first '[' in blank
                index2 = index + len(key)  # index of char after last char of key

                if madlib[index2] == '_':
                    blank_end = index2 + 3
                else:
                    blank_end = index2 + 1

                blank = madlib[blank_start:blank_end]
                # madlib annotated blank from bracket to bracket

                key_values = dictionary.get(key)
                # list of words corresponding to key
                fill_in_word = random.choice(key_values)
                # random generated word to fill in blank

                while fill_in_word in madlib:
                    fill_in_word = random.choice(key_values)
                    # random generated word to fill in blank

                madlib = madlib.replace(blank, fill_in_word)

        return madlib

    def load_and_process_madlib(self, filename):

        fobj = open(filename, 'r')
        madlib = fobj.read()
        fobj.close()

        f = open('filename.pickle', 'rb')
        dictionary = pickle.load(f)
        f.close()

        filled = self.fill_in_madlib(madlib, dictionary)

        new_filename = filename.replace('.txt', '_filled.txt')

        fobj = open(new_filename, 'w')
        fobj.write(filled)
        fobj.close()

    def generate_fortune(self):

        k = random.randint(1, 15)

        filename = 'fortune' + str(k) + '.txt'

        self.load_and_process_madlib(filename)

        filled_file = 'fortune' + str(k) + '_filled.txt'

        fobj = open(filled_file, 'r')
        comment = fobj.read()
        fobj.close()

        return comment


if __name__ == '__main__':
    EvilCookieApp().run()
