import json

from rest_framework.permissions import IsAuthenticated, AllowAny

from post.models import *
from django.shortcuts import render, HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, api_view
from rest_framework import status
from post.api.serializers import *
from rest_framework.authtoken.models import Token
from .serializers import RegisterSerializer
from rest_framework import generics
from django.contrib.auth import authenticate


def home(request):
    return Response({'status': 'success'}, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def post_all(request):
    posts = Post.objects.all().values()
    serializer = PostSerializer(data=posts, many=True)
    return Response(serializer.initial_data, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def post_create(request):
    current_user = request.user
    req_body = request.body
    js = json.loads(req_body)
    post = Post(title=js['title'], description=js['description'], uploader=current_user)
    if 'image' in request.data.keys():
        post.image = request.data['image']
    post.time = datetime.now()
    post.save()
    serializer = PostSerializer(post)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['DELETE', ])
@permission_classes((IsAuthenticated,))
def post_delete(request, id):
    if id is None:
        return Response({'status': 'No ID sent'}, status=status.HTTP_400_BAD_REQUEST)
    count = Post.objects.filter(pk=id).count()
    if count == 0:
        return Response({'status': f'Post with ID: {id} not found'}, status=status.HTTP_400_BAD_REQUEST)
    post = Post.objects.get(pk=id)
    post.delete()
    return Response({'status': f'Successfully deleted the post'}, status=status.HTTP_200_OK)


@api_view(['PUT', ])
@permission_classes((IsAuthenticated,))
def post_update(request, id):
    if id is None:
        return Response({'status': 'No ID sent'}, status=status.HTTP_400_BAD_REQUEST)
    count = Post.objects.filter(pk=id).count()
    if count == 0:
        return Response({'status': f'Post with ID: {id} not found'}, status=status.HTTP_400_BAD_REQUEST)
    post = Post.objects.get(pk=id)
    req_body = request.body
    js = json.loads(req_body)
    if js['title'] is not None:
        post.title = js['title']
    if js['description'] is not None:
        post.description = js['description']
    if 'image' in request.data.keys():
        post.image = request.data['image']
    post.time = datetime.now()
    post.save()
    serializer = PostSerializer(post)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def post_get(request, id):
    if id is None:
        return Response({'status': 'No ID sent'}, status=status.HTTP_400_BAD_REQUEST)
    count = Post.objects.filter(pk=id).count()
    if count == 0:
        return Response({'status': f'Post with ID: {id} not found'}, status=status.HTTP_400_BAD_REQUEST)
    post = Post.objects.get(pk=id)
    serializer = PostSerializer(post)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def register(request):
    serializer = UserSerializer(data=request.data)
    print(serializer.initial_data)
    user = dict(serializer.initial_data)
    first_name = user.get('first_name')
    last_name = user.get('last_name')
    username = user.get('username')
    email = user.get('email')
    password = user.get('password')
    try:
        if first_name is None or len(first_name) == 0:
            return Response({'status': 'No first_name sent of Bad first_name sent'}, status=status.HTTP_400_BAD_REQUEST)
        if last_name is None or len(last_name) == 0:
            return Response({'status': 'No last_name sent of Bad last_name sent'}, status=status.HTTP_400_BAD_REQUEST)
        if username is None or len(username) == 0:
            return Response({'status': 'No username sent of Bad username sent'}, status=status.HTTP_400_BAD_REQUEST)
        if email is None or len(email) == 0:
            return Response({'status': 'No email sent of Bad email sent'}, status=status.HTTP_400_BAD_REQUEST)
        if password is None or len(password) == 0:
            return Response({'status': 'No password sent of Bad password sent'}, status=status.HTTP_400_BAD_REQUEST)

        new_user = User(first_name=user['first_name'], last_name=user['last_name'], email=user['email'],
                        password=user['password'], username=user['username'], )
        new_user.save()
        token, _ = Token.objects.get_or_create(user=new_user)
        user['token'] = token.key

    except Exception as e:
        return Response({'status': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    js = json.dumps(user, indent=None)
    return Response(json.loads(js), status=status.HTTP_201_CREATED)


@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'status': 'Provide both username and password'},
                        status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'status': 'Invalid Credentials'},
                        status=status.HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    data = dict()
    data['first_name'] = user.first_name
    data['last_name'] = user.last_name
    data['user_name'] = user.username
    data['email'] = user.email
    data['token'] = token.key
    data['password'] = password
    js = json.dumps(data, indent=None)
    return Response(json.loads(js),
                    status=status.HTTP_200_OK)
