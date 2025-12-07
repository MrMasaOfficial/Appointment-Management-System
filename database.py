import sqlite3
import os
from datetime import datetime
from typing import List, Tuple, Optional, Dict, Any

class Database:
    def __init__(self, db_name: str = "appointments.db"):
        self.db_path = db_name
        self.init_database()

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_database(self):
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL UNIQUE,
                email TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id INTEGER NOT NULL,
                appointment_date TEXT NOT NULL,
                appointment_time TEXT NOT NULL,
                service TEXT,
                notes TEXT,
                status TEXT DEFAULT 'scheduled',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE CASCADE
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                appointment_id INTEGER NOT NULL,
                notification_time TEXT NOT NULL,
                message TEXT,
                is_sent INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (appointment_id) REFERENCES appointments(id) ON DELETE CASCADE
            )
        ''')

        conn.commit()
        conn.close()

    def add_client(self, name: str, phone: str, email: str = "") -> int:
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO clients (name, phone, email)
                VALUES (?, ?, ?)
            ''', (name, phone, email))
            conn.commit()
            client_id = cursor.lastrowid
            return client_id
        except sqlite3.IntegrityError as e:
            raise Exception(f"خطأ: رقم الهاتف موجود بالفعل")
        finally:
            conn.close()

    def get_all_clients(self) -> List[Dict[str, Any]]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM clients ORDER BY name')
        clients = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return clients

    def get_client_by_id(self, client_id: int) -> Optional[Dict[str, Any]]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM clients WHERE id = ?', (client_id,))
        client = cursor.fetchone()
        conn.close()
        return dict(client) if client else None

    def update_client(self, client_id: int, name: str, phone: str, email: str = ""):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                UPDATE clients 
                SET name = ?, phone = ?, email = ?
                WHERE id = ?
            ''', (name, phone, email, client_id))
            conn.commit()
        except sqlite3.IntegrityError:
            raise Exception(f"خطأ: رقم الهاتف موجود بالفعل")
        finally:
            conn.close()

    def delete_client(self, client_id: int):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM clients WHERE id = ?', (client_id,))
        conn.commit()
        conn.close()

    def add_appointment(self, client_id: int, appointment_date: str, 
                       appointment_time: str, service: str = "", notes: str = "") -> int:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO appointments (client_id, appointment_date, appointment_time, service, notes)
            VALUES (?, ?, ?, ?, ?)
        ''', (client_id, appointment_date, appointment_time, service, notes))
        conn.commit()
        appointment_id = cursor.lastrowid
        
        self.add_notification(appointment_id, appointment_date, appointment_time)
        
        conn.close()
        return appointment_id

    def get_appointments_by_date(self, date: str) -> List[Dict[str, Any]]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT a.*, c.name, c.phone, c.email 
            FROM appointments a
            JOIN clients c ON a.client_id = c.id
            WHERE a.appointment_date = ?
            ORDER BY a.appointment_time
        ''', (date,))
        appointments = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return appointments

    def get_appointments_by_client(self, client_id: int) -> List[Dict[str, Any]]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT a.*, c.name, c.phone 
            FROM appointments a
            JOIN clients c ON a.client_id = c.id
            WHERE a.client_id = ?
            ORDER BY a.appointment_date, a.appointment_time DESC
        ''', (client_id,))
        appointments = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return appointments

    def get_all_appointments(self) -> List[Dict[str, Any]]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT a.*, c.name, c.phone, c.email 
            FROM appointments a
            JOIN clients c ON a.client_id = c.id
            ORDER BY a.appointment_date DESC, a.appointment_time DESC
        ''')
        appointments = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return appointments

    def update_appointment(self, appointment_id: int, appointment_date: str, 
                         appointment_time: str, service: str = "", 
                         notes: str = "", status: str = "scheduled"):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE appointments 
            SET appointment_date = ?, appointment_time = ?, service = ?, notes = ?, status = ?
            WHERE id = ?
        ''', (appointment_date, appointment_time, service, notes, status, appointment_id))
        conn.commit()
        conn.close()

    def delete_appointment(self, appointment_id: int):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM appointments WHERE id = ?', (appointment_id,))
        conn.commit()
        conn.close()

    def add_notification(self, appointment_id: int, appointment_date: str, appointment_time: str):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        appointment = self.get_appointment_by_id(appointment_id)
        if appointment:
            client = self.get_client_by_id(appointment['client_id'])
            message = f"تذكير: لديك موعد في {appointment_time} مع {client['name']}"
            
            cursor.execute('''
                INSERT INTO notifications (appointment_id, notification_time, message)
                VALUES (?, ?, ?)
            ''', (appointment_id, appointment_date + " " + appointment_time, message))
            conn.commit()
        
        conn.close()

    def get_appointment_by_id(self, appointment_id: int) -> Optional[Dict[str, Any]]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT a.*, c.name, c.phone, c.email 
            FROM appointments a
            JOIN clients c ON a.client_id = c.id
            WHERE a.id = ?
        ''', (appointment_id,))
        appointment = cursor.fetchone()
        conn.close()
        return dict(appointment) if appointment else None

    def get_pending_notifications(self) -> List[Dict[str, Any]]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT n.*, a.appointment_date, a.appointment_time, c.name, c.phone, c.email
            FROM notifications n
            JOIN appointments a ON n.appointment_id = a.id
            JOIN clients c ON a.client_id = c.id
            WHERE n.is_sent = 0 AND n.notification_time <= ?
            ORDER BY n.notification_time
        ''', (datetime.now().strftime('%Y-%m-%d %H:%M'),))
        notifications = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return notifications

    def mark_notification_sent(self, notification_id: int):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE notifications 
            SET is_sent = 1
            WHERE id = ?
        ''', (notification_id,))
        conn.commit()
        conn.close()

    def get_statistics(self) -> Dict[str, int]:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) as count FROM clients')
        total_clients = cursor.fetchone()['count']
        
        cursor.execute('SELECT COUNT(*) as count FROM appointments')
        total_appointments = cursor.fetchone()['count']
        
        cursor.execute('''
            SELECT COUNT(*) as count FROM appointments 
            WHERE status = "scheduled"
        ''')
        scheduled_count = cursor.fetchone()['count']
        
        cursor.execute('''
            SELECT COUNT(*) as count FROM appointments 
            WHERE status = "completed"
        ''')
        completed_count = cursor.fetchone()['count']
        
        conn.close()
        
        return {
            'total_clients': total_clients,
            'total_appointments': total_appointments,
            'scheduled': scheduled_count,
            'completed': completed_count
        }
