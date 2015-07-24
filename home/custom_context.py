from home.models import RealmStatusAPI


#realm status api
def add_realm_status(request):
    realm_status = RealmStatusAPI.objects.all()
    group_name = 'not_officer'
    if request.user.groups.filter(name='Officer'):
        group_name = 'Officer'

    args = {}
    args['realm_status'] = realm_status
    args['group'] = group_name
    return args