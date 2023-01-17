from datetime import timedelta
from kivymd.app import MDApp
from kivy.properties import NumericProperty, StringProperty
from kivy.clock import Clock
from kivymd.uix.list import TwoLineIconListItem, IconLeftWidget

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton


class Content(MDBoxLayout):
    pass


class MainApp(MDApp):
    count = 1
    watch_started = False
    stopwatch_time = StringProperty()
    milliseconds = NumericProperty()
    seconds = NumericProperty()
    minutes = NumericProperty()
    last_lap_time = {
        'minutes': 0,
        'seconds': 0,
        'milliseconds': 0
    }

    dialog = None

    def build(self):
        self.theme_cls.theme_style = "Dark"

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

        # disable reset and lap buttons
        self.root.ids['reset_btn'].disabled = True
        self.root.ids['record_lap_btn'].disabled = True

        # Reset lap time
        self.last_lap_time['minutes'] = 0
        self.last_lap_time['seconds'] = 0
        self.last_lap_time['milliseconds'] = 0

    def time_lap(self):
        lap_time = f"Count {self.count}: " + self.stopwatch_time
        list_item = TwoLineIconListItem(
            IconLeftWidget(
                icon="av-timer"
            ),
            text=lap_time,
            secondary_text=self.calculate_time_difference(),
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            secondary_theme_text_color="Custom",
            secondary_text_color=(1, 1, 1, 1)
        )

        self.root.ids['count_list'].add_widget(list_item, index=-1)

        self.count += 1

    def calculate_time_difference(self):
        """Calculate the time difference between the laps records
        """
        lap_time = timedelta(
            minutes=self.minutes,
            seconds=self.seconds,
            milliseconds=self.milliseconds
        ) - timedelta(
            minutes=self.last_lap_time['minutes'], seconds=self.last_lap_time['seconds'], milliseconds=self.last_lap_time['milliseconds'])

        lap_time = str(lap_time)[2:-3]

        lap_time = lap_time.split(':')

        lap_time = [i.split('.') for i in lap_time]

        minutes = int(lap_time[0][0])
        seconds = int(lap_time[1][0])
        milliseconds = int(lap_time[1][1])

        self.last_lap_time['minutes'] = self.minutes
        self.last_lap_time['seconds'] = self.seconds
        self.last_lap_time['milliseconds'] = self.milliseconds

        return f"{minutes}:{seconds}:{milliseconds}"

    def on_start(self):
        self.stopwatch_time = "00:00:00"

    def show_add_timer_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Add Timer",
                type="custom",
                content_cls=Content(),
            )
        self.dialog.open()

    def add_timer(self):
        pass


MainApp().run()
