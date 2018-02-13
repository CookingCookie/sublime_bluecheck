import sublime
import sublime_plugin


class GetIdCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		sublime.Window.show_input_panel(sublime.active_window(), "TU-ID", "", self.get_id, None, None)
	def get_id(self, user_input):		
		tu_id_file = open('/tmp/sublime_tu_id.txt', 'w+')
		tu_id_file.write(user_input)
		tu_id_file.close()