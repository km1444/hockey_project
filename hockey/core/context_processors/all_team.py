from rating.models import Team


def all_team(request):
    all_team = Team.objects.all().order_by('title')
    return {
        'all_team': all_team
    }
