from rest_framework.response import Response
from socialDistribution.models import Author, ConnectedNode, FriendRequest
from socialDistribution.pagination import Pagination
from socialDistribution.serializers import AuthorSerializer, ConnectedNodeSerializer, FriendRequestSerializer
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from drf_spectacular.utils import extend_schema


class FriendRequestDetailViewSet(generics.GenericAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    @extend_schema(
        tags=['Befriend'],
    )
    def get(self, request, author_pk, foreign_author_pk, format=None):
        """_summary_

        Args:
            request (_type_): _description_
            author_pk (_type_): _description_
            foreign_author_pk (_type_): _description_
            format (_type_, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        friend_requests = FriendRequest.objects.filter(to_author=author_pk)
        page = self.paginate_queryset(friend_requests)
        return self.get_paginated_response(FriendRequestSerializer(page, many=True).data)

    @extend_schema(
        tags=['Befriend'],
        description='Send a friend request from FOREIGN_AUTHOR_ID'
    )
    def put(self, request, author_pk, foreign_author_pk, format=None):
        """_summary_

        Args:
            request (_type_): _description_
            author_pk (_type_): _description_
            foreign_author_pk (_type_): _description_
            format (_type_, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        author = Author.objects.get(pk=author_pk)
        foreign_author = Author.objects.get(pk=foreign_author_pk)
        # create follow object
        follow = FriendRequest.objects.filter(from_author=foreign_author, to_author=author)
        if follow:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        follow = FriendRequest.objects.create(from_author=foreign_author, to_author=author)
        return Response(FriendRequestSerializer(follow).data, status=status.HTTP_201_CREATED)

    @extend_schema(
        tags=['Befriend'],
        description='Accept a friend request from FOREIGN_AUTHOR_ID'
    )
    def post(self, request, author_pk, foreign_author_pk, format=None):
        """_summary_

        Args:
            request (_type_): _description_
            author_pk (_type_): _description_
            foreign_author_pk (_type_): _description_
            format (_type_, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        author = Author.objects.get(pk=author_pk)
        foreign_author = Author.objects.get(pk=foreign_author_pk)
        # create follow object
        friendRequest = FriendRequest.objects.filter(from_author=foreign_author, to_author=author)
        if not friendRequest:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        friendRequest.status = "Accepted"
        return Response(status=status.HTTP_200_OK)

class FriendRequestListViewSet(generics.ListAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = Pagination
    
    @extend_schema(
        tags=['Befriend'],
    )
    def get(self, request, author_pk, format=None):
        """_summary_

        Args:
            request (_type_): _description_
            author_pk (_type_): _description_
            format (_type_, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        friend_requests = FriendRequest.objects.filter(to_author=author_pk)
        friends = Author.objects.filter(pk__in=friend_requests.values('from_author'))
        page = self.paginate_queryset(friends)
        return self.get_paginated_response(AuthorSerializer(page, many=True).data)


class ConnectedNodeViewSet(generics.ListCreateAPIView):
    queryset = ConnectedNode.objects.all()
    serializer_class = ConnectedNodeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = Pagination