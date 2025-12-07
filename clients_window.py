from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
                             QLineEdit, QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import config
from database import Database

class ClientsWindow(QDialog):
    def __init__(self, db: Database, parent=None):
        super().__init__(parent)
        self.db = db
        self.init_ui()
        self.refresh_table()

    def init_ui(self):
        self.setWindowTitle("إدارة العملاء")
        self.setGeometry(150, 150, 900, 600)
        self.setStyleSheet(self.get_stylesheet())
        
        main_layout = QVBoxLayout()

        input_layout = self.create_input_section()
        main_layout.addLayout(input_layout)

        buttons_layout = self.create_buttons_section()
        main_layout.addLayout(buttons_layout)

        table_layout = QVBoxLayout()
        table_layout.addWidget(QLabel("قائمة العملاء:"))
        table_layout.setSpacing(10)
        
        self.clients_table = QTableWidget()
        self.clients_table.setColumnCount(5)
        self.clients_table.setHorizontalHeaderLabels([
            "رقم العميل", "الاسم", "رقم الهاتف", "البريد الإلكتروني", "تاريخ التسجيل"
        ])
        self.clients_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.clients_table.itemSelectionChanged.connect(self.on_client_selected)
        
        table_layout.addWidget(self.clients_table)
        main_layout.addLayout(table_layout)

        self.setLayout(main_layout)

    def create_input_section(self) -> QHBoxLayout:
        layout = QHBoxLayout()
        
        layout.addWidget(QLabel("الاسم:"))
        self.name_input = QLineEdit()
        layout.addWidget(self.name_input)
        
        layout.addWidget(QLabel("رقم الهاتف:"))
        self.phone_input = QLineEdit()
        layout.addWidget(self.phone_input)
        
        layout.addWidget(QLabel("البريد الإلكتروني:"))
        self.email_input = QLineEdit()
        layout.addWidget(self.email_input)
        
        return layout

    def create_buttons_section(self) -> QHBoxLayout:
        layout = QHBoxLayout()
        
        btn_add = QPushButton("+ إضافة عميل")
        btn_add.clicked.connect(self.add_client)
        layout.addWidget(btn_add)
        
        btn_update = QPushButton("تحديث")
        btn_update.clicked.connect(self.update_client)
        layout.addWidget(btn_update)
        
        btn_delete = QPushButton("حذف")
        btn_delete.clicked.connect(self.delete_client)
        layout.addWidget(btn_delete)
        
        btn_clear = QPushButton("مسح الحقول")
        btn_clear.clicked.connect(self.clear_inputs)
        layout.addWidget(btn_clear)
        
        layout.addStretch()
        
        return layout

    def add_client(self):
        name = self.name_input.text().strip()
        phone = self.phone_input.text().strip()
        email = self.email_input.text().strip()

        if not name or not phone:
            QMessageBox.warning(self, "خطأ", "يجب إدخال الاسم ورقم الهاتف")
            return

        try:
            self.db.add_client(name, phone, email)
            QMessageBox.information(self, "نجاح", f"تم إضافة العميل {name} بنجاح")
            self.clear_inputs()
            self.refresh_table()
            
            if self.parent():
                self.parent().refresh_all_data()
        except Exception as e:
            QMessageBox.critical(self, "خطأ", str(e))

    def update_client(self):
        if not self.selected_client_id:
            QMessageBox.warning(self, "خطأ", "يجب اختيار عميل أولاً")
            return

        name = self.name_input.text().strip()
        phone = self.phone_input.text().strip()
        email = self.email_input.text().strip()

        if not name or not phone:
            QMessageBox.warning(self, "خطأ", "يجب إدخال الاسم ورقم الهاتف")
            return

        try:
            self.db.update_client(self.selected_client_id, name, phone, email)
            QMessageBox.information(self, "نجاح", "تم تحديث بيانات العميل بنجاح")
            self.clear_inputs()
            self.refresh_table()
        except Exception as e:
            QMessageBox.critical(self, "خطأ", str(e))

    def delete_client(self):
        if not self.selected_client_id:
            QMessageBox.warning(self, "خطأ", "يجب اختيار عميل أولاً")
            return

        reply = QMessageBox.question(self, "تأكيد", 
                                     "هل أنت متأكد من حذف هذا العميل؟\nسيتم حذف جميع مواعيده أيضاً",
                                     QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.db.delete_client(self.selected_client_id)
            QMessageBox.information(self, "نجاح", "تم حذف العميل بنجاح")
            self.clear_inputs()
            self.refresh_table()

    def refresh_table(self):
        clients = self.db.get_all_clients()
        self.clients_table.setRowCount(len(clients))

        for row, client in enumerate(clients):
            self.clients_table.setItem(row, 0, QTableWidgetItem(str(client['id'])))
            self.clients_table.setItem(row, 1, QTableWidgetItem(client['name']))
            self.clients_table.setItem(row, 2, QTableWidgetItem(client['phone']))
            self.clients_table.setItem(row, 3, QTableWidgetItem(client.get('email', '')))
            self.clients_table.setItem(row, 4, QTableWidgetItem(client.get('created_at', '')[:10]))

    def on_client_selected(self):
        selected_rows = self.clients_table.selectionModel().selectedRows()
        if selected_rows:
            row = selected_rows[0].row()
            client_id = int(self.clients_table.item(row, 0).text())
            client = self.db.get_client_by_id(client_id)
            
            if client:
                self.selected_client_id = client_id
                self.name_input.setText(client['name'])
                self.phone_input.setText(client['phone'])
                self.email_input.setText(client.get('email', ''))

    def clear_inputs(self):
        self.name_input.clear()
        self.phone_input.clear()
        self.email_input.clear()
        self.selected_client_id = None
        self.clients_table.clearSelection()

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
        
        QLineEdit {{
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 5px;
        }}
        
        QLineEdit:focus {{
            border: 2px solid {config.COLORS['primary']};
        }}
        """
