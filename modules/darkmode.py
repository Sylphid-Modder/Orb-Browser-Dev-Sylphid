from PySide6.QtCore import Qt, QObject

class DarkMode(QObject):
    def __init__(self, tabs):
        super().__init__()
        self.tabs = tabs
        self.dark_mode_enabled = False

    def toggle_dark_mode(self, enabled):
        self.dark_mode_enabled = enabled
        for i in range(self.tabs.count()):
            web_view = self.tabs.widget(i)
            if enabled:
                web_view.page().setBackgroundColor(Qt.black)
                self.apply_dark_mode_js(web_view)
            
            else:
                web_view.page().setBackgroundColor(Qt.white)
                self.remove_dark_mode_js(web_view)

    def apply_dark_mode_js(self, web_view):
        js_code = """
        document.body.style.backgroundColor = 'black';
        document.body.style.color = 'white';
        """
        web_view.page().runJavaScript(js_code)

    def remove_dark_mode_js(self, web_view):
        js_code = """
        document.body.style.backgroundColor = 'white';
        document.body.style.color = 'black';
        """
        web_view.page().runJavaScript(js_code)