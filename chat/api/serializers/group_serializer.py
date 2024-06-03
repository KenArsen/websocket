from rest_framework import serializers
from chat.models import Group


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name', 'creator', 'info', 'members')
        ref_name = 'Group'

    def update(self, instance, validated_data):
        members_data = validated_data.pop('members', [])
        instance = super().update(instance, validated_data)
        instance.members.set(members_data)
        return instance
