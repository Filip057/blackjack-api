from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from django.http import HttpRequest


# Create your views here.
@api_view(['GET'])
def test_header(request):
    header = request.headers.get('test')

    if header is None:
        return Response(data='failure')

    return Response(data={"succes": header})