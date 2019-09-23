from django.http import HttpResponse
from django.template import loader

from .models import User


def index(request):
    user_list = User.objects.order_by('birth_date')[::-1]
    template = loader.get_template('index.html')
    context = {
        'user_list': user_list,
    }
    return HttpResponse(template.render(context, request))


def detail(request, user_id):
    return HttpResponse("You're looking at User %s." % user_id)
