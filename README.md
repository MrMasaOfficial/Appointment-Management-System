# Appointment Management System

A comprehensive desktop application for managing appointments and scheduling, built with Python, PyQt5, and SQLite3. Perfect for clinics, salons, service centers, and any business that needs to manage client appointments efficiently.

## 📋 Table of Contents

- [Features](#features)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Guide](#usage-guide)
- [Project Structure](#project-structure)
- [Database Schema](#database-schema)
- [Configuration](#configuration)
- [Features in Detail](#features-in-detail)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

### Core Functionality
- **Client Management**: Add, edit, and delete client information with contact details
- **Appointment Booking**: Schedule appointments with date, time, service, and notes
- **Calendar View**: Interactive calendar with daily and weekly appointment views
- **Dashboard**: Real-time statistics showing total clients, appointments, and their status
- **Automatic Notifications**: Timed reminders for upcoming appointments
- **Search & Filter**: Easily find appointments and clients by various criteria

### Advanced Features
- **Status Management**: Track appointment status (scheduled, completed, cancelled)
- **Service Categories**: Pre-defined service types or custom services
- **Appointment Duration**: Set custom duration for each appointment
- **Available Time Slots**: View and manage available time slots
- **Database Integration**: SQLite3 database for persistent data storage
- **Arabic/English Support**: Full RTL support for Arabic interface
- **Professional UI**: Modern, intuitive graphical user interface
- **Data Export**: Comprehensive appointment history and statistics

## 🖥️ System Requirements

### Minimum Requirements
- **Python**: 3.7 or higher
- **RAM**: 512 MB
- **Storage**: 100 MB available space
- **OS**: Windows, macOS, or Linux

### Recommended Requirements
- **Python**: 3.9 or higher
- **RAM**: 2 GB
- **Storage**: 500 MB available space
- **Display**: 1366x768 or higher resolution

## 📦 Installation

### 1. Clone or Download the Project

```bash
git clone https://github.com/yourusername/appointment-system.git
cd appointment_system
```

Or download the ZIP file and extract it.

### 2. Create Virtual Environment (Optional but Recommended)

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Required Packages:**
- PyQt5==5.15.7
- PyQt5-sip==12.11.0

## 🚀 Quick Start

### Running the Application

**Method 1: Using app.py**
```bash
python app.py
```

**Method 2: Using run.py**
```bash
python run.py
```

### Load Sample Data (First Time Setup)

To populate the database with sample data:

```bash
python sample_data.py
```

This will add:
- 5 sample clients with contact information
- 5 sample appointments for demonstration

## 📖 Usage Guide

### Main Dashboard

1. **Launch the application**: Run `python app.py`
2. **View Statistics**: Dashboard tab shows real-time statistics
3. **Manage Clients**: Click "Manage Clients" button
4. **Book Appointment**: Click "New Appointment" button
5. **View Calendar**: Switch to Calendar tab for visual appointment view

### Managing Clients

#### Add a New Client
1. Click "Manage Clients" button
2. Fill in client details:
   - **Name**: Client's full name (required)
   - **Phone**: Contact number (required, must be unique)
   - **Email**: Email address (optional)
3. Click "Add Client" button
4. Confirm the success message

#### Edit Client Information
1. Select a client from the list by clicking on a row
2. Edit the fields in the input area
3. Click "Update" button
4. Confirm the success message

#### Delete a Client
1. Select a client from the list
2. Click "Delete" button
3. Confirm the deletion in the dialog
4. Client and all their appointments will be permanently removed

### Booking Appointments

#### Create New Appointment
1. Click "New Appointment" button
2. Select client from dropdown:
   - Existing clients will be listed
   - Or click "Add New Client" for quick client creation
3. Set appointment details:
   - **Date**: Select from calendar popup
   - **Time**: Choose time (30-minute intervals available)
   - **Service**: Select from predefined services or leave blank
   - **Duration**: Set appointment duration in minutes (15-480 minutes)
   - **Notes**: Add any special notes or instructions
4. Click "Save Appointment"
5. View available times by clicking "Available Times" button

#### Edit Appointment
1. Go to Appointments tab
2. Double-click on an appointment to edit
3. Modify the details
4. Click "Save Appointment"

#### View Available Times
1. Select a date using the date picker
2. Click "Available Times" button
3. A dialog will show all available time slots for that day

### Calendar & Schedule View

#### Daily View
1. Click "Calendar" tab
2. Select a date from the calendar
3. Right panel shows all appointments for that day
4. Appointments are color-coded by status:
   - White: Scheduled appointments
   - Green: Completed appointments
   - Red: Cancelled appointments

#### Weekly View
1. Click "Calendar" tab
2. Change view to "Weekly" in the dropdown
3. Select any date in the week
4. All appointments for that week will be displayed

### Dashboard & Statistics

The dashboard displays:
- **Total Clients**: Overall number of registered clients
- **Total Appointments**: All appointments in the system
- **Scheduled**: Active appointments awaiting completion
- **Completed**: Finished appointments
- **Recent Appointments**: Latest 5 appointments in the system

## 📁 Project Structure

```
appointment_system/
├── app.py                      # Main application entry point
├── run.py                      # Alternative run script
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── appointments.db             # SQLite database (created on first run)
│
├── Core Modules
├── database.py                 # Database operations and queries
├── config.py                   # Configuration and constants
├── models.py                   # Data models and business logic
│
├── GUI Components
├── main_window.py              # Main application window and dashboard
├── clients_window.py           # Client management interface
├── appointments_window.py      # Appointment booking interface
├── calendar_widget.py          # Calendar and schedule view
│
├── Utilities
├── notifications.py            # Notification system
├── sample_data.py              # Sample data generator
│
└── __pycache__/               # Python cache (auto-generated)
```

## 🗄️ Database Schema

### Clients Table
```sql
CREATE TABLE clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT NOT NULL UNIQUE,
    email TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### Appointments Table
```sql
CREATE TABLE appointments (
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
```

### Notifications Table
```sql
CREATE TABLE notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    appointment_id INTEGER NOT NULL,
    notification_time TEXT NOT NULL,
    message TEXT,
    is_sent INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (appointment_id) REFERENCES appointments(id) ON DELETE CASCADE
)
```

## ⚙️ Configuration

### config.py Settings

**Application**
```python
APP_NAME = "نظام حجز المواعيد"  # Application name
APP_VERSION = "1.0.0"            # Version number
DB_NAME = "appointments.db"      # Database filename
```

**UI Dimensions**
```python
WINDOW_WIDTH = 1200              # Main window width
WINDOW_HEIGHT = 800              # Main window height
```

**Services**
```python
SERVICES = [
    "استشارة",      # Consultation
    "علاج",         # Treatment
    "تنظيف",        # Cleaning
    "تقويم",        # Alignment
    "خدمة أخرى"    # Other service
]
```

**Status Types**
```python
APPOINTMENT_STATUS = [
    "scheduled",    # Scheduled
    "completed",    # Completed
    "cancelled"     # Cancelled
]
```

**Notification Settings**
```python
NOTIFICATION_ADVANCE_MINUTES = 60        # Reminder time before appointment
NOTIFICATION_CHECK_INTERVAL = 60000      # Check interval (milliseconds)
```

### Customizing Colors

Edit the `COLORS` dictionary in `config.py`:

```python
COLORS = {
    'primary': '#2E86AB',        # Primary color
    'secondary': '#A23B72',      # Secondary color
    'success': '#06A77D',        # Success color
    'warning': '#F18F01',        # Warning color
    'danger': '#C73E1D',         # Danger color
    'background': '#F5F5F5',     # Background color
    'text': '#333333'            # Text color
}
```

## 🎯 Features in Detail

### Client Management System

**Full CRUD Operations**
- Create new client records with validation
- Read and display all client information
- Update existing client details
- Delete clients (cascade deletes associated appointments)

**Data Validation**
- Phone number uniqueness verification
- Required field validation
- Email format validation (optional)

### Appointment Booking

**Smart Scheduling**
- Automatic conflict detection
- Available time slot calculation
- 30-minute interval scheduling
- Business hours support (9 AM - 5 PM)

**Flexible Appointments**
- Custom service selection
- Customizable duration (15-480 minutes)
- Additional notes and instructions
- Status tracking

### Calendar System

**Interactive Calendar**
- Click-based date selection
- Color-coded appointment status
- Day/week view switching
- Real-time appointment display

**Schedule Management**
- Visual appointment overview
- Time-sorted appointment lists
- Status-based color coding
- Easy navigation between dates

### Notification System

**Automatic Reminders**
- 60-minute advance notifications
- Popup alert messages
- Automatic database marking
- Recurring check every minute

**Notification Features**
- Client-specific messages
- Appointment details inclusion
- Customizable timing
- Multiple notification support

### Dashboard Analytics

**Real-Time Statistics**
- Total client count
- Total appointment count
- Scheduled appointment tracking
- Completed appointment count
- Recent appointment list (latest 5)

## 🔧 Troubleshooting

### Common Issues

#### Issue: "ModuleNotFoundError: No module named 'PyQt5'"

**Solution:**
```bash
pip install PyQt5==5.15.7 PyQt5-sip==12.11.0
```

#### Issue: "UnicodeEncodeError" when running sample_data.py

**Solution:**
The script uses UTF-8 encoding. If you encounter encoding issues:
```bash
chcp 65001  # On Windows Command Prompt
python sample_data.py
```

#### Issue: Database locked error

**Solution:**
1. Close the application
2. Delete `appointments.db`
3. Run the application again (fresh database will be created)

#### Issue: Application window not displaying correctly

**Solution:**
1. Ensure your screen resolution is at least 1366x768
2. Check if PyQt5 is properly installed
3. Try running: `python -m PyQt5.examples.browser`

#### Issue: Arabic text showing as boxes or incorrect characters

**Solution:**
1. Ensure Windows Arabic language support is installed
2. Update PyQt5: `pip install --upgrade PyQt5`
3. Check font availability on your system

### Performance Issues

**If the application is slow:**
- Close other applications consuming system resources
- Ensure you have at least 2GB RAM available
- Rebuild the database: Delete `appointments.db` and restart

**Large Database Management:**
- For databases with 10,000+ appointments, consider archiving old data
- Implement database optimization: `VACUUM` command in SQLite

## 📝 File Descriptions

### Core Application Files

**database.py**
- Database initialization and schema creation
- CRUD operations for all entities
- Query methods for filtering and searching
- Connection management
- Statistics calculation

**config.py**
- Application constants and settings
- Color scheme definitions
- Font configurations
- Service types
- Notification settings

**models.py**
- Data classes: Client, Appointment, Notification
- Business logic: AppointmentManager
- Validation methods
- Data transformation utilities

### GUI Components

**main_window.py**
- Main application window
- Dashboard with statistics
- Tabbed interface management
- Appointment list and calendar integration
- Event handling and refresh logic

**clients_window.py**
- Client management dialog
- Client CRUD interface
- Search and filter functionality
- Data validation
- Input forms

**appointments_window.py**
- Appointment booking dialog
- Client selection
- Date/time picking
- Service selection
- Duration configuration
- Quick client addition

**calendar_widget.py**
- Interactive calendar widget
- Daily/weekly view toggle
- Appointment display
- Color-coded status
- Date-based filtering

### Utility Files

**notifications.py**
- Notification manager class
- Popup notification handling
- Tray icon creation
- Reminder checking logic
- Appointment reminders

**sample_data.py**
- Sample data generator
- Database population script
- Test data creation
- Encoding-safe printing

## 🚀 Performance Optimization

### Tips for Better Performance

1. **Regular Maintenance**
   - Archive old appointments monthly
   - Run database optimization periodically
   - Clear notification history

2. **Database Optimization**
   ```python
   import sqlite3
   conn = sqlite3.connect('appointments.db')
   conn.execute('VACUUM')
   conn.close()
   ```

3. **Caching**
   - Application caches client list in memory
   - Appointments loaded on-demand
   - Calendar data optimized for weekly views

## 🔒 Security Considerations

### Data Safety
- SQLite database uses transaction-based operations
- Foreign key constraints prevent data inconsistency
- Input validation prevents SQL injection
- Phone number uniqueness prevents duplicate entries

### Privacy
- No external data transmission
- All data stored locally in SQLite database
- No cloud sync or online features
- User data remains on the machine

### Best Practices
- Regular database backups recommended
- Store database file in secure location
- Use strong computer passwords
- Keep Python and PyQt5 updated

## 📚 Additional Resources

### PyQt5 Documentation
- [PyQt5 Official Documentation](https://doc.qt.io/qt-5/)
- [PyQt5 API Reference](https://www.riverbankcomputing.com/static/Docs/PyQt5/)

### SQLite Documentation
- [SQLite Official Site](https://www.sqlite.org/)
- [SQLite Python Integration](https://docs.python.org/3/library/sqlite3.html)

### Python Resources
- [Python Official Documentation](https://docs.python.org/3/)
- [Python Style Guide (PEP 8)](https://www.python.org/dev/peps/pep-0008/)
