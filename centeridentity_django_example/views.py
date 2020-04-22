import json
from uuid import uuid4
from django.http import HttpResponse
from django.shortcuts import render
from centeridentity.api import CenterIdentity
from rest_framework.views import APIView


ci = CenterIdentity('YOUR_CENTER_IDENTITY_API_KEY', 'YOUR_CENTER_IDENTITY_USERNAME')


def home(request):
    if not request.session.get('uuid'):
        request.session['uuid'] = str(uuid4())
    return render(
        request,
        'index.html',
        dict(session_id=request.session['uuid'])
    )


class CreateCustomerViewSet(APIView):
    def post(self, request, format=None):
        body_json = request.data
        result = ci.add_user(body_json)
        return HttpResponse(json.dumps(result))


class SignInViewSet(APIView):
    def post(self, request, format=None):
        body_json = request.data
        user = ci.authenticate(
            request.session['uuid'],
            body_json
        )
        request.session['user'] = user.to_dict
        return HttpResponse(json.dumps(request.session['user']))