from django.shortcuts import render

# Create your views here.

# HTTP Error 400
def bad_request(request):
    response = render(
        request,
        'Errors/400.html',
    )

    response.status_code = 400

    return response

# HTTP Error 403
def permission_denied(request):
    response = render(
        request,
        'Errors/403.html',
    )
    
    response.status_code = 403

    return response

# HTTP Error 404
def page_not_found(request):
    response = render(
        request,
        'Errors/404.html',
    )
    
    response.status_code = 404

    return response

# HTTP Error 500
def server_error(request):
    response = render(
        request,
        'Errors/500.html',
    )
    
    response.status_code = 500

    return response