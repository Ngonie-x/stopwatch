from kivymd.app import MDApp
from kivy.properties import NumericProperty, StringProperty
from kivy.clock import Clock
from kivymd.uix.list import TwoLineIconListItem, IconLeftWidget


class MainApp(MDApp):
    count = 1
    watch_started = False
    stopwatch_time = StringProperty()
    milliseconds = NumericProperty()
    seconds = NumericProperty()
    minutes = NumericProperty()

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"

    def get_string_time(self, dt):
        self.increment_milliseconds()

        milliseconds = str(self.milliseconds)
        seconds = str(self.seconds)
        minutes = str(self.minutes)

        if len(milliseconds) < 2:
            milliseconds = '0' + milliseconds

        if len(seconds) < 2:
            seconds = '0' + seconds

        if len(minutes) < 2:
            minutes = '0' + minutes

        self.stopwatch_time = minutes + ":" + seconds + ":" + milliseconds

    def start_or_stop_stopwatch(self):
        if self.watch_started:
            self.watch_started = False
            self.root.ids['record_lap_btn'].disabled = True
            self.root.ids['play_pause_btn'].icon = 'play'
            self.root.ids['reset_btn'].disabled = False
            Clock.unschedule(self.get_string_time)
        else:
            self.watch_started = True
            self.root.ids['play_pause_btn'].icon = 'pause'
            self.root.ids['record_lap_btn'].disabled = False
            Clock.schedule_interval(self.get_string_time, 0.01)

    def increment_milliseconds(self):
        self.milliseconds += 1

        if self.milliseconds == 100:
            self.increment_seconds()
            self.milliseconds = 0

    def increment_seconds(self):
        self.seconds += 1

        if self.seconds == 60:
            self.increment_minutes()
            self.seconds = 0

    def increment_minutes(self):
        self.minutes += 1

    def reset_stopwatch(self):
        if self.watch_started:
            Clock.unschedule(self.get_string_time)
        self.stopwatch_time = "00:00:00"
        self.milliseconds = 0
        self.seconds = 0
        self.minutes = 0

        self.root.ids['reset_btn'].disabled = True
        self.root.ids['record_lap_btn'].disabled = True

    def time_lap(self):
        lap_time = f"Count {self.count}: " + self.stopwatch_time
        list_item = TwoLineIconListItem(
            IconLeftWidget(
                icon="av-timer"
            ),
            text=lap_time,
            secondary_text="00:04:43",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            secondary_theme_text_color="Custom",
            secondary_text_color=(1, 1, 1, 1)
        )

        self.root.ids['count_list'].add_widget(list_item, index=-1)

        self.count += 1

    def on_start(self):
        self.stopwatch_time = "00:00:00"


MainApp().run()
