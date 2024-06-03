from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from chat.models import Group
from rest_framework.permissions import IsAuthenticated
from chat.api.serializers import GroupSerializer


class UserGroupListAPI(generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        groups = Group.objects.filter(members=user)
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data)


class GroupCreateAPI(generics.CreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class AddUserToGroupAPI(generics.GenericAPIView):
    def post(self, request, group_id):
        try:
            group = Group.objects.get(pk=group_id)
            user_id = request.data.get('user_id')
            group.members.add(user_id)
            group.save()
            serializer = GroupSerializer(group)
            return Response(serializer.data)
        except Group.DoesNotExist:
            return Response({"error": "Group does not exist."}, status=status.HTTP_404_NOT_FOUND)


class RemoveUserFromGroupAPI(generics.GenericAPIView):
    def post(self, request, group_id):
        try:
            group = Group.objects.get(pk=group_id)
            user_id = request.data.get('user_id')
            group.members.remove(user_id)
            group.save()
            serializer = GroupSerializer(group)
            return Response(serializer.data)
        except Group.DoesNotExist:
            return Response({"error": "Group does not exist."}, status=status.HTTP_404_NOT_FOUND)
