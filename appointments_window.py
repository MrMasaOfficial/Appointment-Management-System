from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
                             QLineEdit, QComboBox, QDateEdit, QTimeEdit, QTextEdit, 
                             QMessageBox, QSpinBox)
from PyQt5.QtCore import Qt, QDate, QTime
from PyQt5.QtGui import QFont
import config
from database import Database
from models import AppointmentManager

class AppointmentsWindow(QDialog):
    def __init__(self, db: Database, parent=None):
        super().__init__(parent)
        self.db = db
        self.appointment_manager = AppointmentManager(db)
        self.current_appointment_id = None
        self.init_ui()
        self.load_clients()

    def init_ui(self):
        self.setWindowTitle("حجز موعد جديد")
        self.setGeometry(150, 150, 600, 700)
        self.setStyleSheet(self.get_stylesheet())

        main_layout = QVBoxLayout()

        title = QLabel("حجز موعد جديد")
        title.setFont(config.FONTS['heading'])
        main_layout.addWidget(title)

        main_layout.addWidget(QLabel("اختر العميل:"))
        self.client_combo = QComboBox()
        self.client_combo.currentIndexChanged.connect(self.on_client_changed)
        main_layout.addWidget(self.client_combo)

        btn_add_client = QPushButton("+ إضافة عميل جديد")
        btn_add_client.clicked.connect(self.open_quick_add_client)
        main_layout.addWidget(btn_add_client)

        main_layout.addWidget(QLabel("التاريخ:"))
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        self.date_edit.dateChanged.connect(self.on_date_changed)
        main_layout.addWidget(self.date_edit)

        main_layout.addWidget(QLabel("الوقت:"))
        time_layout = QHBoxLayout()
        
        self.time_edit = QTimeEdit()
        self.time_edit.setTime(QTime(9, 0))
        time_layout.addWidget(self.time_edit)
        
        btn_available_times = QPushButton("أوقات متاحة")
        btn_available_times.clicked.connect(self.show_available_times)
        time_layout.addWidget(btn_available_times)
        
        main_layout.addLayout(time_layout)

        main_layout.addWidget(QLabel("الخدمة:"))
        self.service_combo = QComboBox()
        self.service_combo.addItems([""] + config.SERVICES)
        main_layout.addWidget(self.service_combo)

        main_layout.addWidget(QLabel("مدة الموعد (بالدقائق):"))
        self.duration_spin = QSpinBox()
        self.duration_spin.setMinimum(15)
        self.duration_spin.setMaximum(480)
        self.duration_spin.setValue(30)
        self.duration_spin.setSuffix(" دقيقة")
        main_layout.addWidget(self.duration_spin)

        main_layout.addWidget(QLabel("ملاحظات:"))
        self.notes_edit = QTextEdit()
        self.notes_edit.setMaximumHeight(100)
        main_layout.addWidget(self.notes_edit)

        buttons_layout = QHBoxLayout()
        
        btn_save = QPushButton("حفظ الموعد")
        btn_save.clicked.connect(self.save_appointment)
        buttons_layout.addWidget(btn_save)
        
        btn_cancel = QPushButton("إلغاء")
        btn_cancel.clicked.connect(self.close)
        buttons_layout.addWidget(btn_cancel)
        
        main_layout.addLayout(buttons_layout)
        main_layout.addStretch()

        self.setLayout(main_layout)

    def load_clients(self):
        self.client_combo.clear()
        clients = self.db.get_all_clients()
        
        self.clients_dict = {}
        for client in clients:
            self.client_combo.addItem(f"{client['name']} ({client['phone']})", client['id'])
            self.clients_dict[client['id']] = client

    def on_client_changed(self):
        pass

    def on_date_changed(self):
        pass

    def show_available_times(self):
        date_str = self.date_edit.date().toString(config.DATE_FORMAT)
        available_times = self.appointment_manager.get_available_times(date_str)
        
        if available_times:
            times_str = "\n".join(available_times)
            QMessageBox.information(self, "الأوقات المتاحة", 
                                   f"الأوقات المتاحة في {date_str}:\n\n{times_str}")
        else:
            QMessageBox.warning(self, "لا توجد أوقات", 
                               f"لا توجد أوقات متاحة في {date_str}")

    def save_appointment(self):
        client_id = self.client_combo.currentData()
        
        if not client_id:
            QMessageBox.warning(self, "خطأ", "يجب اختيار عميل")
            return

        appointment_date = self.date_edit.date().toString(config.DATE_FORMAT)
        appointment_time = self.time_edit.time().toString(config.TIME_FORMAT)
        service = self.service_combo.currentText()
        notes = self.notes_edit.toPlainText()

        is_valid, message = self.appointment_manager.validate_appointment(
            client_id, appointment_date, appointment_time
        )

        if not is_valid:
            QMessageBox.warning(self, "خطأ", message)
            return

        try:
            if self.current_appointment_id:
                self.db.update_appointment(
                    self.current_appointment_id, 
                    appointment_date, 
                    appointment_time, 
                    service, 
                    notes
                )
                QMessageBox.information(self, "نجاح", "تم تحديث الموعد بنجاح")
            else:
                self.db.add_appointment(
                    client_id, 
                    appointment_date, 
                    appointment_time, 
                    service, 
                    notes
                )
                QMessageBox.information(self, "نجاح", "تم حجز الموعد بنجاح")
            
            self.close()
            
            if self.parent():
                self.parent().refresh_all_data()
        except Exception as e:
            QMessageBox.critical(self, "خطأ", str(e))

    def open_quick_add_client(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("إضافة عميل سريعة")
        dialog.setGeometry(200, 200, 400, 250)

        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("الاسم:"))
        name_input = QLineEdit()
        layout.addWidget(name_input)
        
        layout.addWidget(QLabel("رقم الهاتف:"))
        phone_input = QLineEdit()
        layout.addWidget(phone_input)
        
        layout.addWidget(QLabel("البريد الإلكتروني:"))
        email_input = QLineEdit()
        layout.addWidget(email_input)
        
        buttons_layout = QHBoxLayout()
        
        def add_quick_client():
            name = name_input.text().strip()
            phone = phone_input.text().strip()
            email = email_input.text().strip()
            
            if not name or not phone:
                QMessageBox.warning(dialog, "خطأ", "يجب إدخال الاسم ورقم الهاتف")
                return
            
            try:
                self.db.add_client(name, phone, email)
                self.load_clients()
                dialog.close()
                QMessageBox.information(self, "نجاح", "تم إضافة العميل بنجاح")
            except Exception as e:
                QMessageBox.critical(self, "خطأ", str(e))
        
        btn_add = QPushButton("إضافة")
        btn_add.clicked.connect(add_quick_client)
        buttons_layout.addWidget(btn_add)
        
        btn_cancel = QPushButton("إلغاء")
        btn_cancel.clicked.connect(dialog.close)
        buttons_layout.addWidget(btn_cancel)
        
        layout.addLayout(buttons_layout)
        dialog.setLayout(layout)
        dialog.exec_()

    def load_appointment(self, appointment_id: int):
        appointment = self.db.get_appointment_by_id(appointment_id)
        
        if appointment:
            self.current_appointment_id = appointment_id
            self.setWindowTitle("تعديل الموعد")
            
            client_index = self.client_combo.findData(appointment['client_id'])
            if client_index >= 0:
                self.client_combo.setCurrentIndex(client_index)
            
            self.date_edit.setDate(self.date_edit.date().fromString(
                appointment['appointment_date'], config.DATE_FORMAT
            ))
            
            self.time_edit.setTime(self.time_edit.time().fromString(
                appointment['appointment_time'], config.TIME_FORMAT
            ))
            
            service_index = self.service_combo.findText(appointment.get('service', ''))
            if service_index >= 0:
                self.service_combo.setCurrentIndex(service_index)
            
            self.notes_edit.setPlainText(appointment.get('notes', ''))

    def get_stylesheet(self) -> str:
        return f"""
        QDialog {{
            background-color: {config.COLORS['background']};
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
        
        QLineEdit, QTextEdit, QComboBox, QDateEdit, QTimeEdit, QSpinBox {{
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 5px;
            background-color: white;
        }}
        
        QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QDateEdit:focus, QTimeEdit:focus, QSpinBox:focus {{
            border: 2px solid {config.COLORS['primary']};
        }}
        
        QLabel {{
            color: {config.COLORS['text']};
            font-weight: bold;
        }}
        """
