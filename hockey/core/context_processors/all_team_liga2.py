# from itertools import chain

# from liga2_seasons_app.models import (
#     TeamInTable1gr, TeamInTable2gr, TransitionTournament,
#     TransitionWithoutPoints,
# )


def all_team(request):
    # all_team_liga2_1 = TeamInTable1gr.objects.values(
    #     'team_name__title',
    #     'team_name__city'
    # ).order_by('team_name__title').distinct()
    # all_team_liga2_2 = TeamInTable2gr.objects.values(
    #     'team_name__title',
    #     'team_name__city'
    # ).order_by('team_name__title').distinct()
    # all_team_liga2_3 = TransitionTournament.objects.values(
    #     'team_name__title',
    #     'team_name__city'
    # ).order_by('team_name__title').distinct()
    # all_team_liga2_4 = TransitionWithoutPoints.objects.values(
    #     'team_name__title',
    #     'team_name__city'
    # ).order_by('team_name__title').distinct()
    # all_team_liga2 = list(chain(all_team_liga2_1, all_team_liga2_2, all_team_liga2_3, all_team_liga2_4))
    # result_all_teams = [
    #     dict(s) for s in set(frozenset(d.items()) for d in all_team_liga2)
    # ]
    # result_all_teams.sort(
    #     key=lambda result_all_teams: result_all_teams['team_name__title'])
    # for key in result_all_teams:
    #     print(key['team_name__title'], ':', key['team_name__city'])
    result_all_teams = {
        'Авангард (Омск)': 'Омск',
        'Авангард (Уфа)': 'Уфа',
        'Автомобилист': 'Свердловск',
        'Автомобилист (Крг)': 'Караганда',
        'Ак Барс': 'Казань',
        'Бинокор': 'Ташкент',
        'Буран': 'Воронеж',
        'Дизелист': 'Пенза',
        'Динамо (Мин)': 'Минск',
        'Динамо (Х)': 'Харьков',
        'Енбек': 'Алма-Ата',
        'Звезда': 'Оленегорск',
        'Ижорец': 'Ленинград',
        'Ижсталь': 'Ижевск',
        'Кренгольм': 'Нарва',
        'Кристалл': 'Саратов',
        'Кристалл (Эл)': 'Электросталь',
        'Крылья Советов': 'Москва',
        'Лада': 'Тольятти',
        'Латвияс Берзс': 'Рига',
        'Локомотив': 'Москва',
        'Луч': 'Свердловск',
        'Металлург (Мг)': 'Магнитогорск',
        'Металлург (Нвк)': 'Новокузнецк',
        'Металлург (Чрп)': 'Череповец',
        'Мечел': 'Челябинск',
        'Молот': 'Пермь',
        'Прогресс-ШВСМ': 'Гродно',
        'Рубин': 'Тюмень',
        'СКА': 'Ленинград',
        'СКА (К)': 'Калинин',
        'СКА (Кб)': 'Куйбышев',
        'СКА (Нвс)': 'Новосибирск',
        'СКА (Св)': 'Свердловск',
        'СКА (Хбр)': 'Хабаровск',
        'Салават Юлаев': 'Уфа',
        'Сибирь': 'Новосибирск',
        'Сокол': 'Киев',
        'Спутник': 'Нижний Тагил',
        'Таллэкс': 'Таллин',
        'Торпедо': 'Горький',
        'Торпедо (У-К)': 'Усть-Каменогорск',
        'Торпедо (Я)': 'Ярославль',
        'Трактор': 'Челябинск',
        'Химик': 'Воскресенск',
        'ШВСМ': 'Киев',
        'Шахтер': 'Прокопьевск'
    }
    return {
        'all_team_liga2': result_all_teams
    }
