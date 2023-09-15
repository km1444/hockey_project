from rating.models import Player, Statistic, Team, TeamForTable
from rest_framework import serializers


class PlayerSerializer(serializers.ModelSerializer):
    game = serializers.IntegerField()
    point = serializers.IntegerField()
    name__name = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Statistic
        fields = ('name__name', 'game', 'point')


class PlayerMostGoalsSerializer(serializers.ModelSerializer):
    game = serializers.IntegerField()
    goal = serializers.IntegerField()
    name__name = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Statistic
        fields = ('name__name', 'game', 'goal')


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Team


class StatisticSerializer(serializers.ModelSerializer):
    name = serializers.StringRelatedField(read_only=True)
    season = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Statistic
        fields = (
            'id', 'name', 'season', 'game', 'goal', 'assist', 'point')


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
