from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Client:
    id: int
    name: str
    phone: str
    email: str = ""
    created_at: Optional[str] = None

    @staticmethod
    def from_dict(data: dict) -> 'Client':
        return Client(
            id=data['id'],
            name=data['name'],
            phone=data['phone'],
            email=data.get('email', ''),
            created_at=data.get('created_at')
        )

@dataclass
class Appointment:
    id: int
    client_id: int
    appointment_date: str
    appointment_time: str
    service: str = ""
    notes: str = ""
    status: str = "scheduled"
    client_name: str = ""
    client_phone: str = ""
    created_at: Optional[str] = None

    @staticmethod
    def from_dict(data: dict) -> 'Appointment':
        return Appointment(
            id=data['id'],
            client_id=data['client_id'],
            appointment_date=data['appointment_date'],
            appointment_time=data['appointment_time'],
            service=data.get('service', ''),
            notes=data.get('notes', ''),
            status=data.get('status', 'scheduled'),
            client_name=data.get('name', ''),
            client_phone=data.get('phone', ''),
            created_at=data.get('created_at')
        )

@dataclass
class Notification:
    id: int
    appointment_id: int
    notification_time: str
    message: str = ""
    is_sent: bool = False
    client_name: str = ""
    client_phone: str = ""
    client_email: str = ""

    @staticmethod
    def from_dict(data: dict) -> 'Notification':
        return Notification(
            id=data['id'],
            appointment_id=data['appointment_id'],
            notification_time=data['notification_time'],
            message=data.get('message', ''),
            is_sent=bool(data.get('is_sent', 0)),
            client_name=data.get('name', ''),
            client_phone=data.get('phone', ''),
            client_email=data.get('email', '')
        )

class AppointmentManager:
    def __init__(self, database):
        self.db = database

    def validate_appointment(self, client_id: int, date: str, time: str) -> tuple[bool, str]:
        if not client_id:
            return False, "يجب اختيار عميل"
        
        if not date:
            return False, "يجب اختيار تاريخ"
        
        if not time:
            return False, "يجب اختيار وقت"
        
        existing = self.db.get_appointments_by_date(date)
        for apt in existing:
            if apt['appointment_time'] == time:
                return False, "هذا الوقت محجوز بالفعل"
        
        return True, "OK"

    def get_available_times(self, date: str, interval_minutes: int = 30) -> list:
        from datetime import datetime, timedelta
        
        business_hours = [
            (9, 0),
            (17, 0)
        ]
        
        existing = self.db.get_appointments_by_date(date)
        existing_times = {apt['appointment_time'] for apt in existing}
        
        available = []
        current = datetime.strptime(f"{business_hours[0][0]:02d}:{business_hours[0][1]:02d}", "%H:%M")
        end = datetime.strptime(f"{business_hours[1][0]:02d}:{business_hours[1][1]:02d}", "%H:%M")
        
        while current < end:
            time_str = current.strftime("%H:%M")
            if time_str not in existing_times:
                available.append(time_str)
            current += timedelta(minutes=interval_minutes)
        
        return available

    def get_appointments_by_date_range(self, start_date: str, end_date: str) -> list:
        all_appointments = self.db.get_all_appointments()
        filtered = []
        
        for apt in all_appointments:
            if start_date <= apt['appointment_date'] <= end_date:
                filtered.append(apt)
        
        return sorted(filtered, key=lambda x: x['appointment_date'])
