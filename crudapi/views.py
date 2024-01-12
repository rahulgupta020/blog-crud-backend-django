from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.decorators import permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from .models import BlogPost
from .serializers import UserSerializer, BlogPostSerializer

class UserRegistrationView(APIView):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'message': 'User registered successfully'})
        return JsonResponse(serializer.errors, status=400)

class UserLoginView(APIView):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return JsonResponse({'token': str(refresh.access_token)})
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)

class BlogListView(APIView):
    @csrf_exempt
    @permission_classes([permissions.IsAuthenticated])
    def get(self, request, *args, **kwargs):
        blogs = BlogPost.objects.all()
        serializer = BlogPostSerializer(blogs, many=True)
        return JsonResponse(serializer.data, safe=False)

    @csrf_exempt
    @permission_classes([permissions.IsAuthenticated])
    def post(self, request, *args, **kwargs):
        serializer = BlogPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

class BlogDetailView(APIView):
    @csrf_exempt
    @permission_classes([permissions.IsAuthenticated])
    def get(self, request, pk, *args, **kwargs):
        blog = BlogPost.objects.get(pk=pk)
        serializer = BlogPostSerializer(blog)
        return JsonResponse(serializer.data)

    @csrf_exempt
    @permission_classes([permissions.IsAuthenticated])
    def put(self, request, pk, *args, **kwargs):
        blog = BlogPost.objects.get(pk=pk)
        serializer = BlogPostSerializer(blog, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    @csrf_exempt
    @permission_classes([permissions.IsAuthenticated])
    def delete(self, request, pk, *args, **kwargs):
        blog = BlogPost.objects.get(pk=pk)
        blog.delete()
        return JsonResponse({'message': 'Blog post deleted successfully'}, status=204)
