from django.test import Client, TestCase
from django.urls import reverse
from rating.models import Player, Position, Season, Statistic, Team
from rating.secondary import prev_next_season, top_goal


class ViewTests(TestCase):
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

    def test_pages_uses_correct_template(self):
        """view-классы используют ожидаемые HTML-шаблоны"""
        templates_pages_names = {
            reverse('rating:index'): 'posts/index.html',
            reverse(
                'rating:team_players_in_season',
                kwargs={'team': 'ЦСКА', 'season': '1969-70'}
            ): 'posts/team_players_in_season.html',
            reverse(
                'rating:leaders_career',
                kwargs={'team': 'ЦСКА'}
            ): 'posts/leaders_career.html',
            reverse(
                'rating:season_leaders',
                kwargs={'team': 'ЦСКА'}
            ): 'posts/season_leaders.html',
            reverse(
                'rating:player_detail',
                kwargs={'id': 1}
            ): 'posts/profile.html',
            reverse(
                'rating:statistic',
                kwargs={'stat_rule': 'goal_career'}
            ): 'posts/index.html',
            # reverse('rating:statistic'): 'posts/index.html',
            # reverse('rating:statistic'): 'posts/index.html',
            reverse(
                'rating:best_of_season',
                kwargs={'season': '1969-70', 'stat_rule': 'goal'}
            ): 'posts/best_of_season.html',
            reverse(
                'rating:all_time_all_player_one_team',
                kwargs={'team': 'ЦСКА'}
            ): 'posts/all_time_all_player_one_team.html',
            reverse(
                'rating:create_table',
                kwargs={'season': '1969-70'}
            ): 'table/teams_table.html',
            reverse(
                'rating:history_team',
                kwargs={'team': 'ЦСКА'}
            ): 'posts/history_team.html'
        }
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.guest_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_context(self):
        """Шаблон  index сформирован с правильным контекстом."""
        response = self.guest_client.get(
            reverse('rating:index')
        )
        first_object = response.context['page_obj'][0]
        self.assertEqual(first_object['name__name'], 'Mikhail')

    def test_team_players_in_season_context(self):
        """Шаблон team_players_in_season сформирован
        с правильным контекстом."""
        response = self.guest_client.get(
            reverse(
                'rating:team_players_in_season',
                kwargs={'team': 'ЦСКА', 'season': '1969-70'}
            ))
        page_obj = response.context['page_obj'][0]
        self.assertEqual(page_obj.name.name, 'Mikhail')
        self.assertEqual(response.context['previous_season'], '1968-69')
        self.assertEqual(response.context['next_season'], '1970-71')

    def test_leaders_career_context(self):
        """Шаблон leaders_career сформирован с правильным контекстом."""
        response = self.guest_client.get(
            reverse(
                'rating:leaders_career',
                kwargs={'team': 'ЦСКА'}
            ))
        top_10_game = response.context['top_10_game'][0]
        top_10_goal = response.context['top_10_goal'][0]
        top_10_assist = response.context['top_10_assist'][0]
        top_10_penalty = response.context['top_10_penalty'][0]
        self.assertEqual(
            top_10_game['name__name'], 'Mikhail')
        self.assertEqual(
            top_10_goal['name__name'], 'Mikhail')
        self.assertEqual(
            top_10_assist['name__name'], 'Mikhail')
        self.assertEqual(
            top_10_penalty['name__name'], 'Mikhail')

    def test_secondary_prev_next_season(self):
        val = '1969-70'
        expect = ('1970-71', '1968-69')
        assert prev_next_season(val) == expect, (
            f'Функция {prev_next_season.__name__} неверные значения'
        )

    # def test_secondary_prev_next_season(self):
    #     val = '1969-70'
    #     expect = ('1970-71', '1968-69')
    #     assert prev_next_season(val) == expect, (
    #         f'Функция {prev_next_season.__name__} неверные значения'
    #     )

    def test_top_goal(self):
        val = 'ЦСКА'
        expect = {'name__id': 1, 'name__name': 'Mikhail', 'goal': 0}
        assert top_goal(val) == expect, (
            f'Функция {top_goal.__name__} неверные значения'
        )
