from rating.models import Season


def all_seasons(request):
    # all_seasons = [
    #     ['1946-47', '1947-48', '1948-49'],
    #     ['1949-50', '1950-51', '1951-52'],
    #     ['1952-53', '1953-54', '1954-55']
    # ]
    all_seasons = Season.objects.all().order_by('name')
    return {
        'all_seasons': all_seasons
    }
