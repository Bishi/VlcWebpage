from django.shortcuts import render


def handler404(request):
    response = render('404.html', {})
    response.status_code = 404

    return response


def handler403(request):
    response = render('403.html', {},)
    response.status_code = 403

    return response
