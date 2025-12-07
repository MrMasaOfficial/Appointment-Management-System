from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QApplication, QMessageBox
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtCore import Qt, QTimer, QDateTime
from datetime import datetime, timedelta
from database import Database
import config
import sys

class NotificationManager:
    def __init__(self, db: Database):
        self.db = db
        self.sent_notifications = set()

    def send_notification(self, client_name: str, message: str, notification_id: int):
        try:
            self.show_popup_notification(client_name, message)
            self.db.mark_notification_sent(notification_id)
            self.sent_notifications.add(notification_id)
        except Exception as e:
            print(f"خطأ في إرسال التنبيه: {str(e)}")

    def show_popup_notification(self, title: str, message: str):
        app = QApplication.instance()
        if app:
            msg_box = QMessageBox()
            msg_box.setWindowTitle("تذكير موعد")
            msg_box.setText(f"{title}\n\n{message}")
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setStyleSheet(f"""
                QMessageBox {{
                    background-color: {config.COLORS['background']};
                }}
                QMessageBox QLabel {{
                    color: {config.COLORS['text']};
                }}
                QPushButton {{
                    background-color: {config.COLORS['primary']};
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 4px;
                    min-width: 80px;
                }}
                QPushButton:hover {{
                    background-color: #1e5f8f;
                }}
            """)
            msg_box.exec_()

    def get_pending_notifications(self):
        return self.db.get_pending_notifications()

    def check_upcoming_appointments(self) -> list:
        now = datetime.now()
        upcoming_time = now + timedelta(minutes=config.NOTIFICATION_ADVANCE_MINUTES)
        
        all_appointments = self.db.get_all_appointments()
        upcoming = []
        
        for apt in all_appointments:
            apt_datetime = datetime.strptime(
                f"{apt['appointment_date']} {apt['appointment_time']}", 
                f"{config.DATE_FORMAT} {config.TIME_FORMAT}"
            )
            
            if now < apt_datetime <= upcoming_time and apt['status'] == 'scheduled':
                upcoming.append(apt)
        
        return upcoming

    def create_tray_icon(self) -> QSystemTrayIcon:
        tray_icon = QSystemTrayIcon()
        
        tray_menu = QMenu()
        
        open_action = tray_menu.addAction("فتح التطبيق")
        tray_menu.addSeparator()
        exit_action = tray_menu.addAction("خروج")
        
        tray_icon.setContextMenu(tray_menu)
        
        return tray_icon, open_action, exit_action

class AppointmentReminder:
    def __init__(self, db: Database):
        self.db = db
        self.notification_manager = NotificationManager(db)
        self.reminders_sent = {}

    def check_and_send_reminders(self):
        try:
            pending = self.db.get_pending_notifications()
            
            now = datetime.now()
            notification_datetime = now.strftime(f"{config.DATE_FORMAT} %H:%M")
            
            for notification in pending:
                notification_time_str = notification['notification_time'][:16]
                
                try:
                    notification_dt = datetime.strptime(
                        notification_time_str, 
                        f"{config.DATE_FORMAT} {config.TIME_FORMAT}"
                    )
                    
                    current_dt = datetime.strptime(
                        notification_datetime,
                        f"{config.DATE_FORMAT} {config.TIME_FORMAT}"
                    )
                    
                    if current_dt >= notification_dt and notification['id'] not in self.reminders_sent:
                        self.notification_manager.send_notification(
                            notification['name'],
                            notification['message'],
                            notification['id']
                        )
                        self.reminders_sent[notification['id']] = True
                except Exception as e:
                    print(f"خطأ في معالجة التنبيه: {str(e)}")
        except Exception as e:
            print(f"خطأ في فحص التنبيهات: {str(e)}")

    def schedule_reminders(self):
        self.check_and_send_reminders()

    def get_upcoming_appointments(self):
        return self.notification_manager.check_upcoming_appointments()
