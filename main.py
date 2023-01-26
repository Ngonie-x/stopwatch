from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import TwoLineIconListItem, IconLeftWidget
from kivy.clock import Clock
from kivy.properties import NumericProperty, StringProperty
from kivymd.app import MDApp
from datetime import timedelta
import kivy
kivy.require('2.1.0')


class Content(MDBoxLayout):
    def removes_marks_all_chips(self, selected_instance_chip):
        for instance_chip in self.ids.chip_box.children:
            if instance_chip != selected_instance_chip:
                instance_chip.active = False

    def reset_timer_dialog(self):
        self.ids['d_timer_hour'].text = "00"
        self.ids['d_timer_minute'].text = "00"
        self.ids['d_timer_second'].text = "00"

        self.ids['timer_name'].text = ""

        chip_box = self.ids['chip_box']

        for child in chip_box.children:
            if child.active == True:
                child.active = False


class TimerContent(MDBoxLayout):
    """"""


class MainApp(MDApp):

    # Stop watch
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

    # timer

    timer_started = False

    timer_chips = {
        'Timer': 'timer-sand',
        'Meeting': 'presentation',
        'Sleep': 'moon-waning-crescent',
        'Exercise': 'dumbbell',
        'Mindfulness': 'bullseye-arrow',
        'Work': 'briefcase',
    }

    timer_time = StringProperty()

    timer_seconds = NumericProperty()

    timer_minutes = NumericProperty()

    timer_hours = NumericProperty()

    timer_dialog = None

    dialog = None

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Gray"
        self.theme_cls.primary_hue = "200"

    # STOP WATCH

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
            Clock.schedule_interval(self.get_string_time, 0.1)

    def increment_milliseconds(self):
        self.milliseconds += 10

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
        self.timer_time = "00:00:00"

    # TIMER

    def add_timer(self, title, hours, minutes, seconds, chip_box):
        timer_list = self.root.ids['timer_list']

        for child in chip_box.children:
            if child.active == True:
                icon = self.timer_chips[child.text]

        list_item = TwoLineIconListItem(
            IconLeftWidget(
                icon=icon
            ),
            text=title,
            secondary_text=f"{hours}:{minutes}:{seconds}",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            secondary_theme_text_color="Custom",
            secondary_text_color=(1, 1, 1, 1),
            on_release=lambda x: self.set_timer(hours, minutes, seconds),
        )

        timer_list.add_widget(
            list_item
        )

        self.dialog.dismiss()

    def close_dialog(self):
        self.dialog.dismiss()

    def set_timer(self, hours, minutes, seconds):
        """Set the timer when the list item is clicked

        Args:
            list_item (widget): list item widget
        """

        self.root.ids['timer_hour'].text = hours
        self.root.ids['timer_minute'].text = minutes
        self.root.ids['timer_second'].text = seconds

    def start_timer(self):
        self.timer_hours = int(self.root.ids['timer_hour'].text)
        self.timer_minutes = int(self.root.ids['timer_minute'].text)
        self.timer_seconds = int(self.root.ids['timer_second'].text)

        seconds = self.timer_seconds
        minutes = self.timer_minutes
        hours = self.timer_hours

        self.root.current = 'timer_screen'

        if len(str(seconds)) < 2:
            seconds = '0' + str(seconds)

        if len(str(minutes)) < 2:
            minutes = '0' + str(minutes)

        if len(str(hours)) < 2:
            hours = '0' + str(hours)

        self.timer_time = f"{hours}:{minutes}:{seconds}"

        self.start_or_stop_timer()

    def back_to_main_screen(self):
        self.root.current = 'main_screen'

    def decrement_seconds(self):

        # Stop the timer in the case that time is up
        if self.timer_seconds == 0 and self.timer_minutes == 0 and self.timer_hours == 0:
            self.start_or_stop_timer()

        elif self.timer_seconds == 0 and self.timer_minutes >= 1:
            self.decrement_minutes()
            self.timer_seconds = 60
            self.timer_seconds -= 1

        elif self.timer_seconds > 0:
            self.timer_seconds -= 1

    def decrement_minutes(self):

        if self.timer_minutes == 0 and self.timer_hours != 0:
            self.decrement_hours()
            self.timer_minutes = 60

        if self.timer_minutes != 0:
            self.timer_minutes -= 1

    def decrement_hours(self):
        if self.timer_hours != 0:
            self.timer_hours -= 1

    def show_add_timer_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Add Timer",
                type="custom",
                content_cls=Content(),
            )
        self.dialog.open()

    def start_or_stop_timer(self):

        if self.timer_started:
            self.timer_started = False
            self.root.ids['timer_pause_btn'].icon = 'play'
            self.root.ids['timer_reset_btn'].disabled = False
            Clock.unschedule(self.get_string_time_timer)
        else:
            self.timer_started = True
            self.root.ids['timer_pause_btn'].icon = 'pause'
            self.root.ids['timer_reset_btn'].disabled = True
            Clock.schedule_interval(self.get_string_time_timer, 1)

    def get_string_time_timer(self, dt):
        self.decrement_seconds()

        seconds = str(int(self.timer_seconds))
        minutes = str(int(self.timer_minutes))
        hours = str(int(self.timer_hours))

        if len(seconds) < 2:
            seconds = '0' + seconds

        if len(minutes) < 2:
            minutes = '0' + minutes

        if len(hours) < 2:
            hours = '0' + hours

        self.timer_time = hours + ":" + minutes + ":" + seconds

    def reset_timer(self):

        hours = self.root.ids['timer_hour'].text
        minutes = self.root.ids['timer_minute'].text
        seconds = self.root.ids['timer_second'].text

        self.timer_hours = hours
        self.timer_minutes = minutes
        self.timer_seconds = seconds

        if len(seconds) < 2:
            seconds = '0' + seconds

        if len(minutes) < 2:
            minutes = '0' + minutes

        if len(hours) < 2:
            hours = '0' + hours

        self.timer_time = hours + ":" + minutes + ":" + seconds


if __name__ == '__main__':
    app = MainApp()
    app.run()
