from home.models import RealmStatusAPI


#realm status api
def add_realm_status(request):
    realm_status = RealmStatusAPI.objects.all()
    return {'realm_status': realm_status}