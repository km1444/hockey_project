from rating.models import Season


def all_seasons(request):
    all_seasons = Season.objects.all().order_by('name')
    return {
        'all_seasons': all_seasons
    }
