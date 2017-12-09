from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty

class Image(Widget):
	def __init__():
		pass

class ShowImage(App):
	def build(self):
		parent = Image()

		btn_good = Button(text='good')
		btn_notgood = Button(text='not good',pos=(parent.width,0))
		btn_sexy = Button(text='sexy',pos=(2*parent.width,0))
		btn_notclear = Button(text='not clear',pos=(3*parent.width,0))

		btn_good.bind(on_release=self.set_good)
		btn_notgood.bind(on_release=self.set_notgood)
		btn_sexy.bind(on_release=self.set_sexy)
		btn_notclear.bind(on_release=self.set_notclear)

		parent.add_widget(self.painter)
		parent.add_widget(btn_good)
		parent.add_widget(btn_notgood)
		parent.add_widget(btn_sexy)
		parent.add_widget(btn_notclear)
		return parent

	def set_good(self, obj):
		pass

	def set_notgood(self, obj):
		pass

	def set_sexy(self, obj):
		pass

	def set_notclear(self, obj):
		pas