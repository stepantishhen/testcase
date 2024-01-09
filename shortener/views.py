import random
import string
import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Link
from .serializers import LinkSerializer


@api_view(['POST'])
def shorten_url(request):
    if request.method == 'POST':
        original_url = request.data.get('original_url')

        link = Link(original_url=original_url)
        link.short_code = generate_short_code()
        link.save()

        serializer = LinkSerializer(link)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def redirect_original(request, short_code):
    try:
        link = Link.objects.get(short_code=short_code)
        serializer = LinkSerializer(link)
        return redirect(serializer.data['original_url'])
    except Link.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


# @login_required
# def index(request):
#     user = request.user
#     user_links = Link.objects.filter(users=user)
#
#     if request.method == "POST":
#         form = Shorter(request.POST)
#         if form.is_valid():
#             link = Link.objects.create(**form.cleaned_data, short_code=generate_short_code())
#             link.users.add(user)
#             return redirect('index')
#     else:
#         form = Shorter()
#
#     context = {
#         'form': form,
#         'links': user_links
#     }
#     return render(request, 'shortener/index.html', context=context)


def generate_short_code():
    characters = string.ascii_letters + string.digits
    short_code = ''.join(random.choice(characters) for _ in range(6))
    return short_code
