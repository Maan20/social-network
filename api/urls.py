from django.urls import path
from .views import (
    SignupView, LoginAPIView, UserSearchAPIView, FriendRequestAPIView,
    FriendsListAPIView,PendingFriendRequestsAPIView
    )

urlpatterns = [
    path('signup', SignupView.as_view(), name='signup'),
    path('login', LoginAPIView.as_view(), name='login'),
    path('search-user', UserSearchAPIView.as_view(), name='search_user'),

    path('friend-request', FriendRequestAPIView.as_view(), name='friend_request'),

    path('friends', FriendsListAPIView.as_view(), name='friends-list'),
    path('pending-requests', PendingFriendRequestsAPIView.as_view(), name='pending-requests'),

]
