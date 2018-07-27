#!/usr/bin/env python3
# coding: utf-8
""" Define the view for the datepicker widget when we click on install button"""
#
# (c) 2018 Siveo, http://www.siveo.net
#
# This file is part of Pulse 2, http://www.siveo.net
#
# Pulse 2 is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Pulse 2 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Pulse 2; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.

from PyQt5.QtWidgets import QWidget, QMessageBox, QGridLayout, QPushButton, QLabel, QCalendarWidget, QComboBox
from PyQt5.QtCore import QDate, QDateTime, QTime, QTimeZone, Qt
from datetime import datetime


class DatePickerWidget(QWidget):
    """The class DatePickerWidget give a view of calendar elements"""

    def __init__(self, ref=None, button=None):
        """Initialize the widget
        Params;
            ref QWidget object which is calling this one
        """
        super().__init__()
        self.ref = ref
        self.ref_button = button
        self.date_selected = None
        self.date_today = None
        self.hour_current = None
        self.hour_selected = None
        self.datetime_selected = None
        self.timestamp_selected = None
        self.label_ask = None
        self.label_hour = None
        self.button_now = None
        self.button_later = None
        self.button_cancel = None
        self.combo_hours = None
        self.combo_minutes = None
        self.calendar = None
        self.layout = None
        self.messagebox_confirm = None
        self.returned_message = None
        self.init_ui()

    def init_ui(self):
        """Set the UI Elements for each attributes"""

        #
        # UI
        #
        self.ref_button.setEnabled(False)
        self.setWindowFlags(
            Qt.CustomizeWindowHint |
            Qt.WindowTitleHint |
            Qt.WindowStaysOnTopHint
        )

        #
        # Labels
        #
        if self.ref is None:
            self.label_ask = QLabel("When do you want to install this package ? ")
        else:
            package_name = self.ref.name.text()[0].upper() + self.ref.name.text()[1:]
            self.label_ask = QLabel("When do you want to install the <span style=\" "
                                    "font-size:10pt; font-weight:800; color:#000000;\" >%s</span> package ?"
                                    % package_name)
        self.label_hour = QLabel("Select the installation hour :")
        sep_widget = QLabel("")

        #
        # Buttons
        #
        self.button_now = QPushButton("Now")
        self.button_later = QPushButton("Later")
        self.button_cancel = QPushButton("Cancel")

        #
        # Calendar
        #
        self.calendar = QCalendarWidget()
        # Define minimum and maximum dates to launch the installation
        self.calendar.setMinimumDate(QDate.currentDate())
        self.calendar.setMaximumDate(QDate.currentDate().addDays(2))
        self.calendar.resize(250, 200)

        #
        # Combobox
        #
        self.combo_hours = QComboBox()
        self.combo_minutes = QComboBox()

        #
        # Dates  and hour
        #
        self.date_today = QDate.currentDate()
        self.get_date()
        self.hour_current = datetime.now()
        self.hour_selected = self.hour_current = [self.hour_current.hour, self.hour_current.minute]
        self.get_hour("hour")
        self.get_hour("minute")

        #
        # Layout
        #
        self.layout = QGridLayout()
        self.layout.addWidget(self.label_ask, 0, 0, 1, 4)
        self.layout.addWidget(self.calendar, 1, 0, 1, 4)
        self.layout.addWidget(self.label_hour, 2, 0, 1, 4)
        self.layout.addWidget(self.combo_hours, 3, 0)
        self.layout.addWidget(QLabel("h"), 3, 1)
        self.layout.addWidget(self.combo_minutes, 3, 2)
        self.layout.addWidget(QLabel("min"), 3, 3)

        self.layout.addWidget(sep_widget, 4, 0, 1, 4)
        self.layout.addWidget(self.button_now, 6, 0)
        self.layout.addWidget(self.button_later, 6, 1)
        self.layout.addWidget(sep_widget, 6, 2)
        self.layout.addWidget(self.button_cancel, 6, 3)

        self.setLayout(self.layout)

        #
        # Events
        #
        self.calendar.selectionChanged.connect(self.get_date)
        self.button_cancel.clicked.connect(self.close)
        self.button_later.clicked.connect(self.later)
        self.combo_hours.currentIndexChanged.connect(lambda: self.get_hour('hour'))
        self.combo_minutes.currentIndexChanged.connect(lambda: self.get_hour('minute'))

    #
    # Events actions
    #
    def show(self):
        """Bind the QWidget.show method for this one"""
        super().show()

    def get_date(self):
        """Method called when the date is updated"""

        self.date_selected = self.calendar.selectedDate()

        # Refresh the selection of the hour if today is selected
        if self.date_selected == self.date_today:
            self.hour_current = datetime.now()
            self.hour_selected = self.hour_current = [self.hour_current.hour, self.hour_current.minute]

            hours_list = generate_list(self.hour_current[0], 24)
            minutes_list = generate_list(self.hour_current[1], 60)
        else:
            hours_list = generate_list(0, 24)
            minutes_list = generate_list(0, 60)

        self.combo_hours.clear()
        self.combo_minutes.clear()

        self.combo_hours.addItems(hours_list)
        self.combo_minutes.addItems(minutes_list)

    def get_hour(self, type="hour"):
        """set the selected hour into hour_selected
        Param:
            type: string indicate if it is the hour or the minute combobox which has changed the string can have this
                values:
                    type = "hour" | "minute"
        """

        if type == "hour":
            self.hour_selected[0] = self.combo_hours.currentText()
        elif type == "minute":
            self.hour_selected[1] = self.combo_minutes.currentText()

        # Generate the final datetime into utc format
        self.datetime_selected = QDateTime(self.date_selected,
                                           QTime(int(self.hour_selected[0]),int(self.hour_selected[1])),
                                           Qt.LocalTime).toUTC()
        self.timestamp_selected = self.datetime_selected.toTime_t()

    def get_timestamp(self):
        """Getter for the timestamp selected
        Returns:
            int representing the timestamp
        """
        return self.timestamp_selected

    def get_utc_datetime(self):
        """Getter for the the selected date
        Returns:
            QDateTime formated in utc
        """
        print("Call get_utc_datetime")
        return self.datetime_selected

    def later(self):
        """Method called when the Later button is called"""
        print("Call later")
        self.close()

    def close(self):
        """Method called when the Cancel button is called"""
        super().close()
        if self.ref_button is not None:
            self.ref_button.setEnabled(True)

        print(self.get_timestamp())
        print(self.get_utc_datetime())


def generate_list(min, max):
    """Generate a list of int stringified in the range of min to max
    Params:
        min int minimum included
        max int maximum excluded
    Returns:
        list of string
    """
    min = int(min)
    max = int(max)

    tmp = []
    _tmp = []

    if min > max:
        min, max = max, min

    tmp = list(range(min,max))

    for element in tmp:
        _tmp.append(str(element))

    return _tmp
