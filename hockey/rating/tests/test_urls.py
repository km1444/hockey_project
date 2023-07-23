# from http import HTTPStatus

from django.test import Client, TestCase
from rating.models import Player, Position, Season, Statistic, Team

# from rating.models import Statistic


class URLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.player = Player.objects.create(
            id=1,
            name='Mikhail',
            year_of_birth=20
        )
        cls.team = Team.objects.create(
            id=1,
            title='ЦСКА'
        )
        cls.season = Season.objects.create(
            id=1,
            name='1969-70'
        )
        cls.position = Position.objects.create(
            id=1,
            name='Защитник'
        )
        cls.statistic = Statistic.objects.create(
            name=cls.player,
            age=20,
            team=cls.team,
            season=cls.season,
            position=cls.position,
            game=1,
            goal=0,
            assist=0,
            point=0,
            penalty=0,
        )

    def setUp(self):
        self.guest_client = Client()

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            '/': 'posts/index.html',
            '/team/ЦСКА/1969-70/': 'posts/team_players_in_season.html',
            '/leaders/ЦСКА/': 'posts/leaders_career.html',
            '/season_leaders/ЦСКА/': 'posts/season_leaders.html',
            '/player/1/': 'posts/profile.html',
            '/players/goals_career/': 'posts/index.html',
            '/players/goals_season/': 'posts/index.html',
            '/players/assist_career/': 'posts/index.html',
            '/year/1969-70/point/': 'posts/best_of_season.html',
            '/team/ЦСКА/': 'posts/all_time_all_player_one_team.html',
            '/table/1969-70/': 'table/teams_table.html',
            '/history/ЦСКА/': 'posts/history_team.html',
            '/search/?q=1': 'search/search_result.html',
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertTemplateUsed(response, template)
