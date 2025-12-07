from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QTableWidget, QTableWidgetItem, 
                             QTabWidget, QStatusBar, QMessageBox)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QFont, QColor
from datetime import datetime
import config
from database import Database
from clients_window import ClientsWindow
from appointments_window import AppointmentsWindow
from calendar_widget import CalendarWidget
from notifications import NotificationManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = Database(config.DB_NAME)
        self.notification_manager = NotificationManager(self.db)
        self.init_ui()
        self.setup_notifications_timer()

    def init_ui(self):
        self.setWindowTitle(config.APP_NAME)
        self.setGeometry(100, 100, config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        self.setStyleSheet(self.get_stylesheet())

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()

        header_layout = self.create_header()
        main_layout.addLayout(header_layout)

        tabs = QTabWidget()
        
        dashboard_tab = self.create_dashboard_tab()
        appointments_tab = self.create_appointments_tab()
        calendar_tab = self.create_calendar_tab()

        tabs.addTab(dashboard_tab, "لوحة التحكم")
        tabs.addTab(appointments_tab, "المواعيد")
        tabs.addTab(calendar_tab, "التقويم")

        main_layout.addWidget(tabs)

        central_widget.setLayout(main_layout)

        self.statusBar().showMessage("جاهز")
        
        self.clients_window = None
        self.appointments_window = None

    def create_header(self) -> QHBoxLayout:
        header = QHBoxLayout()
        
        title = QLabel(config.APP_NAME)
        title.setFont(config.FONTS['title'])
        header.addWidget(title)

        header.addStretch()

        btn_clients = QPushButton("إدارة العملاء")
        btn_clients.clicked.connect(self.open_clients_window)
        header.addWidget(btn_clients)

        btn_new_appointment = QPushButton("موعد جديد")
        btn_new_appointment.clicked.connect(self.open_appointments_window)
        header.addWidget(btn_new_appointment)

        return header

    def create_dashboard_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout()

        stats_layout = QHBoxLayout()

        stats = self.db.get_statistics()

        self.stat_clients = self.create_stat_box(f"إجمالي العملاء", str(stats['total_clients']))
        self.stat_appointments = self.create_stat_box(f"إجمالي المواعيد", str(stats['total_appointments']))
        self.stat_scheduled = self.create_stat_box(f"مواعيد مجدولة", str(stats['scheduled']))
        self.stat_completed = self.create_stat_box(f"مواعيد مكتملة", str(stats['completed']))

        stats_layout.addWidget(self.stat_clients)
        stats_layout.addWidget(self.stat_appointments)
        stats_layout.addWidget(self.stat_scheduled)
        stats_layout.addWidget(self.stat_completed)

        layout.addLayout(stats_layout)

        layout.addWidget(QLabel("آخر المواعيد:"))
        layout.setSpacing(10)

        self.appointments_table = QTableWidget()
        self.appointments_table.setColumnCount(6)
        self.appointments_table.setHorizontalHeaderLabels([
            "العميل", "التاريخ", "الوقت", "الخدمة", "الحالة", "ملاحظات"
        ])
        self.appointments_table.horizontalHeader().setStretchLastSection(True)

        self.update_dashboard_appointments()

        layout.addWidget(self.appointments_table)

        widget.setLayout(layout)
        return widget

    def create_appointments_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout()

        btn_layout = QHBoxLayout()
        btn_new = QPushButton("+ موعد جديد")
        btn_new.clicked.connect(self.open_appointments_window)
        btn_refresh = QPushButton("تحديث")
        btn_refresh.clicked.connect(self.update_dashboard_appointments)
        
        btn_layout.addWidget(btn_new)
        btn_layout.addWidget(btn_refresh)
        btn_layout.addStretch()

        layout.addLayout(btn_layout)

        self.all_appointments_table = QTableWidget()
        self.all_appointments_table.setColumnCount(7)
        self.all_appointments_table.setHorizontalHeaderLabels([
            "رقم", "العميل", "التاريخ", "الوقت", "الخدمة", "الحالة", "ملاحظات"
        ])
        self.all_appointments_table.horizontalHeader().setStretchLastSection(True)
        self.all_appointments_table.itemDoubleClicked.connect(self.on_appointment_double_click)

        self.update_all_appointments()

        layout.addWidget(self.all_appointments_table)

        widget.setLayout(layout)
        return widget

    def create_calendar_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout()

        self.calendar_widget = CalendarWidget(self.db)
        layout.addWidget(self.calendar_widget)

        widget.setLayout(layout)
        return widget

    def create_stat_box(self, label: str, value: str) -> QWidget:
        box = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)

        label_widget = QLabel(label)
        label_widget.setFont(config.FONTS['small'])
        label_widget.setStyleSheet("color: #666;")

        value_widget = QLabel(value)
        value_widget.setFont(config.FONTS['heading'])
        value_widget.setStyleSheet(f"color: {config.COLORS['primary']}; font-weight: bold;")

        layout.addWidget(label_widget)
        layout.addWidget(value_widget)
        layout.addStretch()

        box.setLayout(layout)
        box.setStyleSheet(f"border: 1px solid #ddd; border-radius: 5px; background-color: #f9f9f9;")

        return box

    def update_dashboard_appointments(self):
        appointments = self.db.get_all_appointments()[-5:]
        
        self.appointments_table.setRowCount(len(appointments))
        
        for row, apt in enumerate(appointments):
            self.appointments_table.setItem(row, 0, QTableWidgetItem(apt.get('name', '')))
            self.appointments_table.setItem(row, 1, QTableWidgetItem(apt.get('appointment_date', '')))
            self.appointments_table.setItem(row, 2, QTableWidgetItem(apt.get('appointment_time', '')))
            self.appointments_table.setItem(row, 3, QTableWidgetItem(apt.get('service', '')))
            
            status = apt.get('status', 'scheduled')
            status_ar = config.APPOINTMENT_STATUS_AR.get(status, status)
            self.appointments_table.setItem(row, 4, QTableWidgetItem(status_ar))
            
            self.appointments_table.setItem(row, 5, QTableWidgetItem(apt.get('notes', '')))

        stats = self.db.get_statistics()
        self.stat_clients.layout().itemAt(1).widget().setText(str(stats['total_clients']))
        self.stat_appointments.layout().itemAt(1).widget().setText(str(stats['total_appointments']))
        self.stat_scheduled.layout().itemAt(1).widget().setText(str(stats['scheduled']))
        self.stat_completed.layout().itemAt(1).widget().setText(str(stats['completed']))

    def update_all_appointments(self):
        appointments = self.db.get_all_appointments()
        
        self.all_appointments_table.setRowCount(len(appointments))
        
        for row, apt in enumerate(appointments):
            self.all_appointments_table.setItem(row, 0, QTableWidgetItem(str(apt.get('id', ''))))
            self.all_appointments_table.setItem(row, 1, QTableWidgetItem(apt.get('name', '')))
            self.all_appointments_table.setItem(row, 2, QTableWidgetItem(apt.get('appointment_date', '')))
            self.all_appointments_table.setItem(row, 3, QTableWidgetItem(apt.get('appointment_time', '')))
            self.all_appointments_table.setItem(row, 4, QTableWidgetItem(apt.get('service', '')))
            
            status = apt.get('status', 'scheduled')
            status_ar = config.APPOINTMENT_STATUS_AR.get(status, status)
            self.all_appointments_table.setItem(row, 5, QTableWidgetItem(status_ar))
            
            self.all_appointments_table.setItem(row, 6, QTableWidgetItem(apt.get('notes', '')))

    def on_appointment_double_click(self, item):
        row = item.row()
        appointment_id = int(self.all_appointments_table.item(row, 0).text())
        
        appointment = self.db.get_appointment_by_id(appointment_id)
        if appointment:
            self.open_appointments_window(appointment_id)

    def open_clients_window(self):
        if self.clients_window is None or not self.clients_window.isVisible():
            self.clients_window = ClientsWindow(self.db, self)
        self.clients_window.show()

    def open_appointments_window(self, appointment_id=None):
        if self.appointments_window is None or not self.appointments_window.isVisible():
            self.appointments_window = AppointmentsWindow(self.db, self)
        
        if appointment_id:
            self.appointments_window.load_appointment(appointment_id)
        
        self.appointments_window.show()

    def setup_notifications_timer(self):
        self.notification_timer = QTimer()
        self.notification_timer.timeout.connect(self.check_notifications)
        self.notification_timer.start(config.NOTIFICATION_CHECK_INTERVAL)

    def check_notifications(self):
        pending = self.db.get_pending_notifications()
        
        for notification in pending:
            self.notification_manager.send_notification(
                notification['client_name'],
                notification['message'],
                notification['id']
            )

    def refresh_all_data(self):
        self.update_dashboard_appointments()
        self.update_all_appointments()
        self.calendar_widget.refresh_calendar()
        self.statusBar().showMessage("تم التحديث بنجاح")

    def get_stylesheet(self) -> str:
        return f"""
        QMainWindow {{
            background-color: {config.COLORS['background']};
        }}
        
        QTabWidget::pane {{
            border: 1px solid #ddd;
        }}
        
        QTabBar::tab {{
            background-color: #e0e0e0;
            color: {config.COLORS['text']};
            padding: 8px 20px;
            margin-right: 2px;
            border: 1px solid #ccc;
            border-radius: 4px 4px 0 0;
        }}
        
        QTabBar::tab:selected {{
            background-color: {config.COLORS['primary']};
            color: white;
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
        
        QPushButton:pressed {{
            background-color: #164570;
        }}
        
        QTableWidget {{
            background-color: white;
            border: 1px solid #ddd;
            gridline-color: #f0f0f0;
        }}
        
        QTableWidget::item {{
            padding: 5px;
        }}
        
        QHeaderView::section {{
            background-color: {config.COLORS['primary']};
            color: white;
            padding: 5px;
            border: none;
        }}
        
        QLabel {{
            color: {config.COLORS['text']};
        }}
        
        QLineEdit, QTextEdit, QComboBox, QDateEdit, QTimeEdit {{
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 5px;
            background-color: white;
        }}
        
        QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QDateEdit:focus, QTimeEdit:focus {{
            border: 2px solid {config.COLORS['primary']};
        }}
        """
