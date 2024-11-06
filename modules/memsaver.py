class MemorySaver(QObject):
    def __init__(self, tabs):
        super().__init__()
        self.tabs = tabs
        self.tabs.currentChanged.connect(self.save_memory)
        self.memory_saver_enabled = False
        self.last_access_times = {}
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_inactive_tabs)
        self.timer.start(60000)  # 1分ごとにチェック


    def save_memory(self, index):
        if self.memory_saver_enabled:
            current_time = QDateTime.currentDateTime()
            for i in range(self.tabs.count()):
                if i != index:
                    if i not in self.last_access_times:
                        self.last_access_times[i] = current_time
                    self.tabs.widget(i).setVisible(False)
                else:
                    self.last_access_times[i] = current_time
                    self.tabs.widget(i).setVisible(True)
        else:
            for i in range(self.tabs.count()):
                self.tabs.widget(i).setVisible(True)

    def toggle_memory_saver(self, enabled):
        self.memory_saver_enabled = enabled
        self.save_memory(self.tabs.currentIndex())

    def check_inactive_tabs(self):
        if not self.memory_saver_enabled:
            return

        current_time = QDateTime.currentDateTime()
        for i in range(self.tabs.count()):
            if i != self.tabs.currentIndex():
                last_access_time = self.last_access_times.get(i, current_time)
                if last_access_time.secsTo(current_time) > 600:  # 10分以上経過
                    self.tabs.widget(i).setVisible(False)
                else:
                    self.tabs.widget(i).setVisible(True)