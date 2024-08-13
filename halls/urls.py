from django.urls import path
from .views import (
    HallCreateView, HallListView, HallUpdateView, 
    ServiceListView, UserHallsView, 
    ManagerHomeView, ReviewCreateView, ReplayCreateView,BookingCreateView
)
#
urlpatterns = [
    path('halls/', HallListView.as_view(), name='hall-list'),
    path('create/', HallCreateView.as_view(), name='hall-create'),
    path('<int:pk>/update/', HallUpdateView.as_view(), name='hall-update'),
    path('services/', ServiceListView.as_view(), name='service-list'),
    path('bookings/create/', BookingCreateView.as_view(), name='booking-create'),
    path('userhalls/', UserHallsView.as_view(), name='user-halls'),
    path('managerhome/', ManagerHomeView.as_view(), name='manager-home'),
    path('reviews/create/', ReviewCreateView.as_view(), name='review-create'),
    path('replay/create/', ReplayCreateView.as_view(), name='replay-create'),
]



