# !/usr/bin/python3
# -*- coding: utf-8 -*-

# Импорт системных библиотек
import os

filename = 'eda'
os.system(f'jupyter nbconvert --to webpdf --allow-chromium-download {filename}.ipynb')