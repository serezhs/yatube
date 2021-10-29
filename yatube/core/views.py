from http import HTTPStatus

from django.shortcuts import render


def page_not_found(request, exception):
    status = HTTPStatus.NOT_FOUND
    path = request.path
    return render(request, 'core/404.html', {'path': path}, status=status)


def csrf_failure(request, reason=''):
    return render(request, 'core/403csrf.html')


def server_error(request):
    status = HTTPStatus.INTERNAL_SERVER_ERROR
    return render(request, 'core/500.html', status=status)
