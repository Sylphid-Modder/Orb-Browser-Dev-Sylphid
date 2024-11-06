class SettingsDialog(QDialog):
    def __init__(self, parent, memory_saver, dark_mode, language):
        super().__init__(parent)
        self.setWindowTitle("設定")
        self.language = language
        self.memory_saver = memory_saver
        self.dark_mode = dark_mode
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()

        # ダークモードのトグルボタン
        dark_mode_layout = QHBoxLayout()
        dark_mode_toggle = QLabel("ダークモード")
        self.dark_mode_toggle = QCheckBox()
        self.dark_mode_toggle.setChecked(self.dark_mode.dark_mode_enabled)
        self.dark_mode_toggle.toggled.connect(self.dark_mode.toggle_dark_mode)
        dark_mode_layout.addWidget(self.dark_mode_toggle)
        dark_mode_layout.addWidget(self.dark_mode_toggle)
        layout.addLayout(dark_mode_layout)
        self.dark_mode_toggle.setChecked(self.dark_mode.dark_mode_enabled)

        # メモリーセイバーのトグルボタン
        memory_saver_layout = QHBoxLayout()
        memory_saver_toggle = QLabel("メモリーセイバー")
        self.memory_saver_toggle = QCheckBox()
        self.memory_saver_toggle.setChecked(self.memory_saver.memory_saver_enabled)
        self.memory_saver_toggle.toggled.connect(self.memory_saver.toggle_memory_saver)
        memory_saver_layout.addWidget(memory_saver_toggle)
        memory_saver_layout.addWidget(self.memory_saver_toggle)
        layout.addLayout(memory_saver_layout)
        self.memory_saver_toggle.setChecked(self.memory_saver.memory_saver_enabled)

        language_layout = QHBoxLayout()
        language_label = QLabel("言語設定")
        self.language_toggle = QComboBox()
        self.language_toggle.addItems(["日本語", "English", "中文"])
        self.language_toggle.setCurrentText(self.language)
        self.language_toggle.currentTextChanged.connect(self.update_language)
        language_layout.addWidget(self.language_toggle)
        language_layout.addWidget(self.language_toggle)
        layout.addLayout(language_layout)

        # Orb Browserについて
        self.about_layout = QHBoxLayout()
        self.about_label = QLabel("Orb Browserについて")
        self.about_text = QLabel("Orb Browserは、Python と Qt を使って作られた軽量なブラウザです。")
        self.about_layout.addWidget(self.about_label)
        self.about_layout.addWidget(self.about_text)
        layout.addLayout(self.about_layout)

        self.setLayout(layout)

    def update_language(self, language):
        self.language = language
        if language == "日本語":
            self.about_label.setText("Orb Browserについて")
            self.about_text.setText("Orb Browserは、Python と Qt を使って作られた軽量なブラウザです")
            self.setWindowTitle("設定")
            self.dark_mode_toggle.setText("ダークモード")
            self.memory_saver_toggle.setText("メモリーセイバー")
        elif language == "English":
            self.about_label.setText("About Orb Browser")
            self.about_text.setText("Orb Browser is a lightweight and fast web browser developed using Python and QT.")
            self.setWindowTitle("Settings")
            self.dark_mode_toggle.setText("Dark Mode")
            self.memory_saver_toggle.setText("Memory Saver")
        elif language == "中文":
            self.about_label.setText("关于 Orb 浏览器")
            self.about_text.setText("Orb Browser 是一款使用 Python")
            self.setWindowTitle("设置")
            self.dark_mode_toggle.setText("暗模式")
            self.memory_saver_toggle.setText("内存保护器")