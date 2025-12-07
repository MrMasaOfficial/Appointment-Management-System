#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from database import Database
from datetime import datetime, timedelta

def populate_sample_data():
    db = Database("appointments.db")
    
    clients_data = [
        ("أحمد محمد", "0501234567", "ahmed@example.com"),
        ("فاطمة علي", "0502345678", "fatima@example.com"),
        ("محمود حسن", "0503456789", "mahmoud@example.com"),
        ("سارة خالد", "0504567890", "sarah@example.com"),
        ("علي عبدالله", "0505678901", "ali@example.com"),
    ]
    
    print("إضافة العملاء...")
    client_ids = []
    for name, phone, email in clients_data:
        try:
            client_id = db.add_client(name, phone, email)
            client_ids.append(client_id)
            print(f"✓ تم إضافة {name}")
        except Exception as e:
            print(f"✗ خطأ في إضافة {name}: {str(e)}")
    
    print("\nإضافة المواعيد...")
    today = datetime.now().date()
    
    appointments_data = [
        (client_ids[0] if client_ids else 1, (today + timedelta(days=1)).isoformat(), "09:00", "استشارة", "موعد أول"),
        (client_ids[1] if client_ids else 2, (today + timedelta(days=1)).isoformat(), "10:00", "علاج", ""),
        (client_ids[2] if client_ids else 3, (today + timedelta(days=2)).isoformat(), "14:00", "تنظيف", ""),
        (client_ids[3] if client_ids else 4, (today + timedelta(days=3)).isoformat(), "11:30", "تقويم", ""),
        (client_ids[4] if client_ids else 5, (today + timedelta(days=5)).isoformat(), "15:00", "استشارة", "متابعة"),
    ]
    
    for client_id, date, time, service, notes in appointments_data:
        try:
            appointment_id = db.add_appointment(client_id, date, time, service, notes)
            client = db.get_client_by_id(client_id)
            print(f"✓ تم إضافة موعد لـ {client['name']} في {date} {time}")
        except Exception as e:
            print(f"✗ خطأ في إضافة موعد: {str(e)}")
    
    print("\n✓ تم ملء قاعدة البيانات بنجاح!")

if __name__ == "__main__":
    populate_sample_data()
