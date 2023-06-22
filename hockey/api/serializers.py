from rating.models import Player, Statistic, Team, TeamForTable
from rest_framework import serializers


class PlayerSerializer(serializers.ModelSerializer):
    # name = serializers.StringRelatedField(many=True, read_only=True)
    total_game = serializers.IntegerField()
    total_point = serializers.IntegerField()

    class Meta:
        model = Player
        fields = ('id', 'name', 'total_game', 'total_point')


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Team


class StatisticSerializer(serializers.ModelSerializer):
    name = serializers.StringRelatedField(read_only=True)
    season = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Statistic
        fields = ('id', 'name', 'season', 'game', 'goal', 'assist', 'point')


class PlayerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'name', 'season')


class TeamForTableSerializer(serializers.ModelSerializer):
    season = serializers.StringRelatedField(read_only=True)
    name = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = TeamForTable
        fields = '__all__'
