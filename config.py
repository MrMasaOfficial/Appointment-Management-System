from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt

APP_NAME = "نظام حجز المواعيد"
APP_VERSION = "1.0.0"
DB_NAME = "appointments.db"

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

SERVICES = [
    "استشارة",
    "علاج",
    "تنظيف",
    "تقويم",
    "خدمة أخرى"
]

APPOINTMENT_STATUS = [
    "scheduled",
    "completed",
    "cancelled"
]

APPOINTMENT_STATUS_AR = {
    "scheduled": "مجدول",
    "completed": "مكتمل",
    "cancelled": "ملغى"
}

COLORS = {
    'primary': '#2E86AB',
    'secondary': '#A23B72',
    'success': '#06A77D',
    'warning': '#F18F01',
    'danger': '#C73E1D',
    'background': '#F5F5F5',
    'text': '#333333'
}

FONTS = {
    'title': QFont('Arial', 16, QFont.Bold),
    'heading': QFont('Arial', 14, QFont.Bold),
    'normal': QFont('Arial', 11),
    'small': QFont('Arial', 9)
}

TIME_FORMAT = "HH:mm"
DATE_FORMAT = "yyyy-MM-dd"
DATETIME_FORMAT = "yyyy-MM-dd HH:mm"

NOTIFICATION_ADVANCE_MINUTES = 60
NOTIFICATION_CHECK_INTERVAL = 60000
