# from rest_framework import serializers
#
#
# class Allocations(serializers.Serializer):
#     grant_name = serializers.CharField()
#     start = serializers.DateTimeField()
#     end = serializers.DateTimeField()
#     provider = serializers.CharField()
#     resource = serializers.CharField()
#     resources = serializers.ListField(child=serializers.CharField())
#     site = serializers.CharField()
#
#
# class GrantSerializer(serializers.Serializer):
#     name = serializers.CharField()
#     start = serializers.DateTimeField()
#     end = serializers.DateTimeField()
#     state = serializers.CharField()
#     allocations = None
#     team = serializers.CharField()
#     team_members = serializers.ListField(child=serializers.CharField())
#
#     def create(self, validated_data):
#         return Grant.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get("name", instance.name)
    #     instance.start = validated_data.get("start", instance.start)
    #     instance.end = validated_data.get("end", instance.end)
    #     instance.state = validated_data.get("state", instance.state)
    #     instance.allocations = validated_data.get("allocations", instance.allocations)
    #     instance.team = validated_data.get("team", instance.team)
    #     instance.team_members = validated_data.get("team_members", instance.team_members)
    #     return instance
