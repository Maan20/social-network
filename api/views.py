from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import SignupSerializer, FriendRequestSerializer, LoginSerializer, UserSerializer,PendingFriendRequestSerializer
from accounts.models import FriendRequest,User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .pagination import CustomLimitOffsetPagination
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from accounts.constants import *

class SignupView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, email=email, password=password)

            if user is not None:
                refresh = RefreshToken.for_user(user)
                data= UserSerializer(user).data
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    "details":data
                })
            else:
                return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserSearchAPIView(APIView):
    pagination_class = CustomLimitOffsetPagination

    def get(self, request, *args, **kwargs):
        query = request.query_params.get('query', '')
        if not query:
            return Response({"message": "query keyword is required."}, status=status.HTTP_400_BAD_REQUEST)

        
        users = User.objects.filter(email__iexact=query).exclude(id=request.user.id)
        if not users: # if email search is not returning any instance then we will check on the basis of name
            users = User.objects.filter(full_name__icontains=query).exclude(id=request.user.id)

        paginator = CustomLimitOffsetPagination()
        paginated_queryset = paginator.paginate_queryset(users, request, view=self)
        if paginated_queryset is not None:
            serializer = UserSerializer(paginated_queryset, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class FriendRequestAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        to_user_id = request.data.get('to_user_id')
        to_user = User.objects.get(id=to_user_id)

        # Limit sending friend requests
        one_minute_ago = timezone.now() - timedelta(minutes=1)
        recent_requests = FriendRequest.objects.filter(from_user=request.user, created_at__gte=one_minute_ago).count()
        if recent_requests >= 3:
            return Response({"detail": "You cannot send more than 3 friend requests within a minute."}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        # Check if a friend request already exists
        if FriendRequest.objects.filter(from_user=request.user, to_user=to_user).exists():
            return Response({"detail": "Friend request already sent."}, status=status.HTTP_400_BAD_REQUEST)

        FriendRequest.objects.create(from_user=request.user, to_user=to_user)
        return Response({"detail": "Friend request sent."}, status=status.HTTP_201_CREATED)

    def put(self, request,):
        friend_request_id = request.data.get("friend_request_id")
        try:
            friend_request = FriendRequest.objects.get(id=friend_request_id, to_user=request.user, status=PENDING)
        except FriendRequest.DoesNotExist:
            return Response({"detail": "Friend request not found."}, status=status.HTTP_404_NOT_FOUND)

        request_status = request.data.get('status')
        print(request_status)
        if request_status not in [ACCEPTED, REJECTED,str(ACCEPTED),str(REJECTED)]: # we will only accepting 1 or 2 from front as action of status 1 for accept and 2 for rejet
            return Response({"detail": "Invalid status."}, status=status.HTTP_400_BAD_REQUEST)

        friend_request.status = request_status
        friend_request.save()
        return Response({"detail": f"Friend request {friend_request.get_status_display()}."}, status=status.HTTP_200_OK)

class FriendsListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        friends = User.objects.filter(
            Q(from_user__to_user=request.user, from_user__status=ACCEPTED) |
            Q(to_user__from_user=request.user, to_user__status=ACCEPTED)
        ).distinct()
        paginator = CustomLimitOffsetPagination()
        paginated_queryset = paginator.paginate_queryset(friends, request, view=self)
        if paginated_queryset is not None:
            serializer = UserSerializer(paginated_queryset, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = UserSerializer(friends, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PendingFriendRequestsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        pending_requests = FriendRequest.objects.filter(to_user=request.user, status=PENDING)
        paginator = CustomLimitOffsetPagination()
        paginated_queryset = paginator.paginate_queryset(pending_requests, request, view=self)
        if paginated_queryset is not None:
            serializer = PendingFriendRequestSerializer(paginated_queryset, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = PendingFriendRequestSerializer(pending_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
