# yourapp/management/commands/load_initial_data.py
from django.core.management.base import BaseCommand
from book.models import Book
import random
from core.utils import load_book_data

class Command(BaseCommand):
    help = 'Load initial data into the database'

    def handle(self, *args, **options):

        for i, book in enumerate(load_book_data()):
            book = Book.objects.create(
                title=book['title'],
                author=book['author'],
                genre=book['genre'],
                price=book['price'], 
                id =book['id']  )
        self.stdout.write(self.style.SUCCESS('Successfully loaded initial data'))
        # self.stdout.write(self.style.SUCCESS(load_category_data()))



