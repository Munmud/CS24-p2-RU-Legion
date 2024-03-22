import os
import csv
import datetime
from django.conf import settings

CATEGORY_METADATA_CSV = os.path.join(settings.DATA_DIR, "categories_metadata.csv" )
PRODUCT_METADATA_CSV = os.path.join(settings.DATA_DIR, "products_metadata.csv" )
BOOK_METADATA_CSV = os.path.join(settings.DATA_DIR, "books_metadata.csv" )

import csv

def load_book_data():
    dataset = []
    with open(BOOK_METADATA_CSV, newline='', encoding="utf8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data = {
                'id': int(row.get("id", 0)) if row.get("id").isdigit() else None,
                'title': row.get("title", None),
                'author': row.get("author", None),
                'genre': row.get("genre", None),
                'price': float(row.get('price', 0.0)) if row.get('price').replace('.', '', 1).isdigit() else None,
            }
            dataset.append(data)
    return dataset


# def load_book_data():
#     with open(BOOK_METADATA_CSV, newline = '', encoding="utf8") as csvfile:
#         reader = csv.DictReader(csvfile)
#         dataset = []
#         for i, row in enumerate(reader):
#             id = row.get("id")
#             try: id = int(id)
#             except: id = None
            
#             title = row.get("title")
#             author = row.get("author")
#             genre = row.get("genre")
#             price = row.get('price')
#             try: price = float(price)
#             except: price = None

#             data = {
#                 'id' : id,
#                 'title' : title,
#                 'author' : author,
#                 'genre' : genre,
#                 'price' : price,
#             }
#             dataset.append(data)
#         return dataset
