from rest_framework.permissions import IsAuthenticated

from post.models import *
from django.shortcuts import render, HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, api_view
from rest_framework import status
from post.api.serializers import *


def home(request):
    return Response({'status': 'success'}, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def post_all(request):
    posts = Post.objects.all().values()
    serializer = PostSerializer(data=posts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def post_create(request):
    return None


@api_view(['DELETE', ])
@permission_classes((IsAuthenticated,))
def post_delete(request):
    id = request.query_params.get('id', None)
    if id is None:
        return Response({'status': 'No ID sent'}, status=status.HTTP_400_BAD_REQUEST)
    post = Post.objects.get(pk=id)
    if post is None:
        return Response({'status': f'Post with ID: {id} not found'}, status=status.HTTP_400_BAD_REQUEST)
    post.delete()
    return Response({'status': f'Successfully deleted the post'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', ])
@permission_classes((IsAuthenticated,))
def post_update(request):
    id = request.query_params.get('id', None)
    print(request.query_params)
    if id is None:
        return Response({'status': 'No ID sent'}, status=status.HTTP_400_BAD_REQUEST)
    post = Post.objects.get(pk=id)
    if post is None:
        return Response({'status': f'Post with ID: {id} not found'}, status=status.HTTP_400_BAD_REQUEST)
    post.delete()
    return Response({'status': f'Successfully deleted the post'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def post_get(request):
    id = request.query_params.get('id', None)
    if id is None:
        return Response({'status': 'No ID sent'}, status=status.HTTP_400_BAD_REQUEST)
    post = Post.objects.get(pk=id)
    if post is None:
        return Response({'status': f'Post with ID: {id} not found'}, status=status.HTTP_400_BAD_REQUEST)
    serializer = PostSerializer(data=post)
    return Response(serializer.data, status=status.HTTP_200_OK)
