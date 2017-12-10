from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout

import glob

LABEL_LIST = []
IMAGE_COUNT = 0
BASE_FILE_PATH = '../data/*.jpg'

PATH = glob.iglob(BASE_FILE_PATH)

class HelloApp(App):
    def build(self):
    	return ShowImageLayout()

class ShowImageLayout(BoxLayout):
	def __init__(self, **kwargs):
		super(ShowImageLayout, self).__init__(**kwargs)
		self.source = next(PATH)

		good_btn = GoodBtn()
		notgood_btn = NotGoodBtn()
		sexy_btn = SexyBtn()
		notclear_btn = NotClearBtn()

		good_btn.bind(on_release=self.set_source)
		notgood_btn.bind(on_release=self.set_source)
		sexy_btn.bind(on_release=self.set_source)
		notclear_btn.bind(on_release=self.set_source)

		self.add_widget(good_btn)
		self.add_widget(notgood_btn)
		self.add_widget(sexy_btn)
		self.add_widget(notclear_btn)

	def set_source(self, obj):
		global PATH
		self.source = next(PATH)

class GoodBtn(Button):
	def onclick(self):
		global LABEL_LIST
		global IMAGE_COUNT

		LABEL_LIST.append(0)
		IMAGE_COUNT += 1

class NotGoodBtn(Button):
	def onclick(self):
		global LABEL_LIST
		global IMAGE_COUNT

		LABEL_LIST.append(1)
		IMAGE_COUNT += 1

class SexyBtn(Button):
	def onclick(self):
		global LABEL_LIST
		global IMAGE_COUNT

		LABEL_LIST.append(2)
		IMAGE_COUNT += 1

class NotClearBtn(Button):
	def onclick(self):
		global LABEL_LIST
		global IMAGE_COUNT

		LABEL_LIST.append(-1)
		IMAGE_COUNT += 1

if __name__ == '__main__':
	HelloApp().run()