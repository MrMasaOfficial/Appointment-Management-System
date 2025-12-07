from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QCalendarWidget, 
                             QTableWidget, QTableWidgetItem, QPushButton, QLabel, QComboBox)
from PyQt5.QtCore import Qt, QDate, QLocale
from PyQt5.QtGui import QFont, QColor, QBrush
import config
from database import Database

class CalendarWidget(QWidget):
    def __init__(self, db: Database):
        super().__init__()
        self.db = db
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()

        left_layout = QVBoxLayout()

        calendar_label = QLabel("التقويم:")
        calendar_label.setFont(config.FONTS['heading'])
        left_layout.addWidget(calendar_label)

        self.calendar = QCalendarWidget()
        self.calendar.setLocale(QLocale(QLocale.Arabic, QLocale.SaudiArabia))
        self.calendar.clicked.connect(self.on_date_selected)
        left_layout.addWidget(self.calendar)

        view_layout = QHBoxLayout()
        view_layout.addWidget(QLabel("العرض:"))
        self.view_combo = QComboBox()
        self.view_combo.addItems(["يومي", "أسبوعي"])
        self.view_combo.currentIndexChanged.connect(self.refresh_calendar)
        view_layout.addWidget(self.view_combo)
        view_layout.addStretch()
        left_layout.addLayout(view_layout)

        layout.addLayout(left_layout, 1)

        right_layout = QVBoxLayout()

        appointments_label = QLabel("المواعيد:")
        appointments_label.setFont(config.FONTS['heading'])
        right_layout.addWidget(appointments_label)

        self.appointments_table = QTableWidget()
        self.appointments_table.setColumnCount(5)
        self.appointments_table.setHorizontalHeaderLabels([
            "الوقت", "العميل", "الخدمة", "الحالة", "ملاحظات"
        ])
        self.appointments_table.horizontalHeader().setStretchLastSection(True)
        right_layout.addWidget(self.appointments_table)

        btn_refresh = QPushButton("تحديث")
        btn_refresh.clicked.connect(self.refresh_calendar)
        right_layout.addWidget(btn_refresh)

        layout.addLayout(right_layout, 2)

        self.setLayout(layout)
        self.setStyleSheet(self.get_stylesheet())

        self.on_date_selected(self.calendar.selectedDate())

    def on_date_selected(self, date: QDate):
        self.selected_date = date.toString(config.DATE_FORMAT)
        self.refresh_appointments()

    def refresh_appointments(self):
        view_type = self.view_combo.currentText()

        if view_type == "يومي":
            appointments = self.db.get_appointments_by_date(self.selected_date)
        else:
            from datetime import datetime, timedelta
            
            selected = datetime.strptime(self.selected_date, config.DATE_FORMAT)
            start = selected - timedelta(days=selected.weekday())
            end = start + timedelta(days=6)
            
            start_str = start.strftime(config.DATE_FORMAT)
            end_str = end.strftime(config.DATE_FORMAT)
            
            all_appointments = self.db.get_all_appointments()
            appointments = [apt for apt in all_appointments 
                          if start_str <= apt['appointment_date'] <= end_str]

        self.appointments_table.setRowCount(len(appointments))

        for row, apt in enumerate(appointments):
            time_item = QTableWidgetItem(apt.get('appointment_time', ''))
            name_item = QTableWidgetItem(apt.get('name', ''))
            service_item = QTableWidgetItem(apt.get('service', ''))
            
            status = apt.get('status', 'scheduled')
            status_ar = config.APPOINTMENT_STATUS_AR.get(status, status)
            status_item = QTableWidgetItem(status_ar)
            
            notes_item = QTableWidgetItem(apt.get('notes', ''))

            if status == "completed":
                color = QColor(180, 220, 180)
            elif status == "cancelled":
                color = QColor(255, 200, 200)
            else:
                color = QColor(255, 255, 255)

            for item in [time_item, name_item, service_item, status_item, notes_item]:
                item.setBackground(QBrush(color))

            self.appointments_table.setItem(row, 0, time_item)
            self.appointments_table.setItem(row, 1, name_item)
            self.appointments_table.setItem(row, 2, service_item)
            self.appointments_table.setItem(row, 3, status_item)
            self.appointments_table.setItem(row, 4, notes_item)

    def refresh_calendar(self):
        self.refresh_appointments()

    def get_stylesheet(self) -> str:
        return f"""
        QCalendarWidget {{
            background-color: white;
            border: 1px solid #ddd;
        }}
        
        QCalendarWidget QWidget {{
            background-color: white;
        }}
        
        QCalendarWidget QAbstractItemView {{
            background-color: white;
            selection-background-color: {config.COLORS['primary']};
            border: 1px solid #ddd;
        }}
        
        QTableWidget {{
            background-color: white;
            border: 1px solid #ddd;
            gridline-color: #f0f0f0;
        }}
        
        QHeaderView::section {{
            background-color: {config.COLORS['primary']};
            color: white;
            padding: 5px;
            border: none;
        }}
        
        QPushButton {{
            background-color: {config.COLORS['primary']};
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
        }}
        
        QPushButton:hover {{
            background-color: #1e5f8f;
        }}
        
        QComboBox {{
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 5px;
            background-color: white;
        }}
        
        QLabel {{
            color: {config.COLORS['text']};
        }}
        """
