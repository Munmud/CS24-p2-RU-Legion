from django.urls import path, include
# from .views import listProduct, listmessages
from .views import TrainUserListView, StationListView, TrainListView, StationDetailedView, WalletDetailedView, BuyTicketListView, RRRListView

urlpatterns = [
    path('users', TrainUserListView.as_view() ),
    path('users/', TrainUserListView.as_view()),

    path('stations', StationListView.as_view()),
    path('stations/', StationListView.as_view()),

    path('stations/<int:station_id>/trains', StationDetailedView.as_view(), name="bookDetails"),
    path('stations/<int:station_id>/trains/', StationDetailedView.as_view(), name="bookDetails"),

    path('trains', TrainListView.as_view()),
    path('trains/', TrainListView.as_view()),
    # path('/<int:pid>', BookDetailedView.as_view(), name="bookDetails"),
    # path('/<int:pid>/', BookDetailedView.as_view(), name="bookDetails")
    path('wallets/<int:wallet_id>', WalletDetailedView.as_view(), name="bookDetails"),
    path('wallets/<int:wallet_id>/', WalletDetailedView.as_view(), name="bookDetails"),

    path('tickets', BuyTicketListView.as_view()),
    path('tickets/', BuyTicketListView.as_view()),

    path('routes', RRRListView.as_view()),
    path('routes/', RRRListView.as_view()),
]