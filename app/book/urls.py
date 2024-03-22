from django.urls import path, include
# from .views import listProduct, listmessages
from .views import BookListView, BookDetailedView

urlpatterns = [
    path('/', BookListView.as_view(), name="bookList"),
    path('', BookListView.as_view(), name="bookList"),
    path('/<int:pid>', BookDetailedView.as_view(), name="bookDetails"),
    path('/<int:pid>/', BookDetailedView.as_view(), name="bookDetails")
]
