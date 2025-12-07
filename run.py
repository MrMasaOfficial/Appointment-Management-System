#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

try:
    from PyQt5.QtWidgets import QApplication, QMessageBox
    from PyQt5.QtCore import Qt
except ImportError:
    print("خطأ: يجب تثبيت PyQt5 أولاً")
    print("قم بتشغيل: pip install -r requirements.txt")
    sys.exit(1)

from app import main

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"خطأ في التطبيق: {str(e)}")
        sys.exit(1)
