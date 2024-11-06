# System Libraries
import os
import sys
import xml.etree.ElementTree as ET
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtWebEngineWidgets import *
from PySide6.QtWebEngineCore import QWebEngineProfile
from PySide6.QtCore import QTimer

# Local Libraries
from modules.adblock import AdblockX
from modules.bookmark import BookmarkAction
from modules.darkmode import DarkMode
from modules.diag_settings import SettingsDialog
from modules.memsaver import MemorySaver

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.language = "日本語"
        self.tabs = QTabWidget()
        self.memory_saver = MemorySaver(self.tabs)
        self.dark_mode = DarkMode(self.tabs)
        self.load_settings()
        self.init_ui()

    def init_ui(self):
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.setTabsClosable(True)
        self.memory_saver = MemorySaver(self.tabs)
        self.dark_mode = DarkMode(self.tabs)
        self.add_tab_button = QPushButton("")
        self.add_tab_button.setStyleSheet("background-color: black; color: black;")
        self.add_tab_button.clicked.connect(self.add_new_tab)
        self.vertical_bar = QToolBar("Vertical Bar")
        self.vertical_bar.setOrientation(Qt.Orientation.Vertical)
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, self.vertical_bar)
        self.tabs.setCornerWidget(self.add_tab_button, Qt.TopRightCorner)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.setCentralWidget(self.tabs)
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        navtb = QToolBar("Navigation")
        self.addToolBar(navtb)
        self.load_shortcuts()
        back_btn = QAction("↩︎", self)
        back_btn.setStatusTip("Back to previous page")
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
        navtb.addAction(back_btn)
        next_btn = QAction("↪︎", self)
        next_btn.setStatusTip("Forward to next page")
        next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        navtb.addAction(next_btn)
        reload_btn = QAction("○", self)
        reload_btn.setStatusTip("Reload page")
        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
        navtb.addAction(reload_btn)
        home_btn = QAction("🏠", self)
        home_btn.setStatusTip("Go home")
        self.toolbar = QToolBar("Actions")
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolbar)
        self.star_button = QAction("⭐️", self)
        self.star_button.setStatusTip("Add shortcut to vertical bar")
        self.star_button.triggered.connect(self.add_shortcut)
        self.toolbar.addAction(self.star_button)
        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)
        navtb.addSeparator()
        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navtb.addWidget(self.urlbar)
        QWebEngineProfile.defaultProfile().downloadRequested.connect(self.on_downloadRequested)
        stop_btn = QAction("❌", self)
        stop_btn.setStatusTip("Stop loading current page")
        stop_btn.triggered.connect(lambda: self.tabs.currentWidget().stop())
        navtb.addAction(stop_btn)
        self.add_new_tab(QUrl('https://takerin-123.github.io/qqqqq.github.io/'), 'Homepage')
        self.vertical_bar = QToolBar("Vertical Bar")
        self.vertical_bar.setOrientation(Qt.Orientation.Vertical)
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, self.vertical_bar)
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.show()
        self.setWindowTitle("")
        self.setStyleSheet("background-color: black; color: white;")  # 背景色を黒に変更
        self.tabs.setStyleSheet("QTabBar::tab { background-color: white; color: black; }")
        settings_btn = QAction("⚙️", self)
        settings_btn.setStatusTip("設定")
        settings_btn.triggered.connect(self.show_settings)
        self.toolbar.addAction(settings_btn)
        self.update_language()
        ai_btn = QAction("AI", self)
        ai_btn.setStatusTip("Use Orb AI")
        ai_btn.triggered.connect(self.open_ai_tool)
        navtb.addAction(ai_btn)
    def open_ai_tool(self):
        ai_url = QUrl("https://supertakerin2-comcomgptfree.hf.space/")
        self.add_new_tab(ai_url, "AI Tool")

    def add_new_tab(self, qurl=None, label="blank"):
        if qurl is None:
            qurl = QUrl('https://takerin-123.github.io/qqqqq.github.io/')
        elif isinstance(qurl, str):
            qurl = QUrl(qurl)
        elif not isinstance(qurl, QUrl):
            raise TypeError("Variable 'qurl' must be a QUrl or a string")
        
        browser = QWebEngineView()
        browser.setUrl(qurl)
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)
        browser.urlChanged.connect(lambda qurl, browser=browser: self.update_urlbar(qurl, browser))
        browser.loadFinished.connect(lambda _, i=i, browser=browser: self.tabs.setTabText(i, browser.page().title()))
        browser.iconChanged.connect(lambda _, i=i, browser=browser: self.tabs.setTabIcon(i, browser.icon()))

    def tab_open_doubleclick(self, i):
        if i == -1:
            self.add_new_tab()

    def current_tab_changed(self, i):
        qurl = self.tabs.currentWidget().url()
        self.update_urlbar(qurl, self.tabs.currentWidget())
        self.update_title(self.tabs.currentWidget())

    def close_current_tab(self, i):
        if self.tabs.count() < 2:
            return
        self.tabs.removeTab(i)
        QWidget.deleteLater()
    
    def update_title(self, browser):
        if browser != self.tabs.currentWidget():
            return
        title = self.tabs.currentWidget().page().title()
        formatted_title = title[:7] if len(title) > 7 else title.ljust(7)
        self.setWindowTitle("%s OrbBrowser" % formatted_title)
        self.tabs.setTabText(self.tabs.currentIndex(), formatted_title)

    def navigate_home(self):
        self.tabs.currentWidget().setUrl(QUrl("https://takerin-123.github.io/qqqqq.github.io/"))

    def navigate_to_url(self):
        url = self.urlbar.text()
        if "google.com/search?q=" in url:
            self.tabs.currentWidget().setUrl(QUrl(url))
        else:
            google_search_url = "https://www.google.com/search?q=" + url
            self.tabs.currentWidget().setUrl(QUrl(google_search_url))

    def update_urlbar(self, q, browser=None):
        if browser != self.tabs.currentWidget():
            return
        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)

    def on_downloadRequested(self, download):
        home_dir = os.path.expanduser("~")
        download_dir = os.path.join(home_dir, "Downloads")
        download_filename = download.suggestedFileName()
        QWebEngineProfile.defaultProfile().setDownloadDirectory(download_dir)
        download.setDownloadFileName(download_filename)
        download.accept()
        self.show_download_progress(download)

    def show_download_progress(self, download):
        progress_bar = QProgressBar(self.status)
        self.status.addPermanentWidget(progress_bar)
        download.downloadProgress.connect(lambda bytesReceived, bytesTotal, progress_bar=progress_bar: progress_bar.setValue(int((bytesReceived / bytesTotal) * 100) if bytesTotal > 0 else 0))
        download.finished.connect(lambda progress_bar=progress_bar: progress_bar.deleteLater())

    def update_progress_bar(self, progress_bar, bytesReceived, bytesTotal):
        if bytesTotal > 0:
            progress = (bytesReceived / bytesTotal) * 100
            progress_bar.setValue(int(progress))

    def remove_progress_bar(self, progress_bar):
        self.status.removeWidget(progress_bar)
        progress_bar.deleteLater()

    def add_shortcut(self):
        current_tab = self.tabs.currentWidget()
        if isinstance(current_tab, QWebEngineView):
            url = current_tab.page().url().toString()
            title = current_tab.page().title()
            shortcut_button = QAction("", self)
            shortcut_button.setText(current_tab.page().title())
            shortcut_button.setToolTip(url)
            shortcut_button.triggered.connect(lambda: self.tabs.currentWidget().setUrl(QUrl(url)))
            self.vertical_bar.addAction(shortcut_button)
            self.tabs.currentWidget().setUrl(QUrl(url))
            self.save_shortcut_to_xml(title, url)

    def save_shortcut_to_xml(self, title, url):
        if not os.path.exists('shortcuts.xml'):
            root = ET.Element("shortcuts")
            tree = ET.ElementTree(root)
            tree.write('shortcuts.xml')
        tree = ET.parse('shortcuts.xml')
        root = tree.getroot()
        for shortcut in root.findall('shortcut'):
            if shortcut.find('url').text == url:
                print("Bookmark already exists.")
                return
        shortcut = ET.SubElement(root, 'shortcut')
        ET.SubElement(shortcut, 'title').text = title
        ET.SubElement(shortcut, 'url').text = url
        tree.write('shortcuts.xml')

    def load_shortcuts(self):
        if not os.path.exists('shortcuts.xml'):
            return
        tree = ET.parse('shortcuts.xml')
        root = tree.getroot()
        added_urls = set()
        for shortcut in root.findall('shortcut'):
            title = shortcut.find('title').text
            url = shortcut.find('url').text
            if url not in added_urls:
                self.add_website_shortcut(url, title)
                added_urls.add(url)

    def add_website_shortcut(self, url, name):
        name = name[:23] + '...' if len(name) > 23 else name
        shortcut_button = QAction(name, self)
        shortcut_button.url = url
        view = QWebEngineView()
        view.load(QUrl(url))
        view.iconChanged.connect(lambda icon, button=shortcut_button: button.setIcon(icon))
        shortcut_button.triggered.connect(lambda: self.tabs.currentWidget().setUrl(QUrl(url)))
        self.vertical_bar.addAction(shortcut_button)
        self.save_shortcut_to_xml(name, url)

    def create_database(self):
        if not os.path.exists('shortcuts.xml'):
            root = ET.Element("shortcuts")
            tree = ET.ElementTree(root)
            tree.write('shortcuts.xml')

    def show_settings(self):
        settings_dialog = SettingsDialog(self, self.memory_saver, self.dark_mode, self.language)
        settings_dialog.exec()
        self.language = settings_dialog.language
        self.save_settings()
        self.update_language()

    def save_settings(self):
        root = ET.Element("settings")
        tree = ET.ElementTree(root)
        language_element = ET.SubElement(root, "language")
        language_element.text = self.language
        memory_saver_element = ET.SubElement(root, "memory_saver")
        memory_saver_element.text = str(self.memory_saver.memory_saver_enabled)
        dark_mode_element = ET.SubElement(root, "dark_mode")
        dark_mode_element.text = str(self.dark_mode.dark_mode_enabled)
        tree.write("settings.xml")

    def load_settings(self):
        if not os.path.exists("settings.xml"):
            return
        tree = ET.parse("settings.xml")
        root = tree.getroot()
        language_element = root.find("language")
        if language_element is not None:
            self.language = language_element.text
        memory_saver_element = root.find("memory_saver")
        if memory_saver_element is not None:
            self.memory_saver.memory_saver_enabled = bool(memory_saver_element.text)
        dark_mode_element = root.find("dark_mode")
        if dark_mode_element is not None:
            self.dark_mode.dark_mode_enabled = bool(dark_mode_element.text)
        self.update_language()

    def update_language(self):
        if self.language == "日本語":
            self.setWindowTitle("Orb Browser")
        elif self.language == "English":
            self.setWindowTitle("About Orb Browser")
        elif self.language == "中文":
            self.setWindowTitle("关于 Orb Browser")

app = QApplication(sys.argv)
app.setApplicationName("OrbBrowser")
window = MainWindow()
window.create_database()
window.show()
app.exec()
