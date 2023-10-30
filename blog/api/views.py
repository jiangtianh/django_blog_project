from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, ChangePasswordSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from app_blog.models import Category, Post


# Create your views here.
class ResgistrationView(APIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User created successfully'}, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    

class ObtainToken(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        if not 'username' in request.data or not 'password' in request.data:
            return Response({'message': 'username and password required'}, status = status.HTTP_400_BAD_REQUEST)
        username = request.data['username']
        password = request.data['password']
        user = authenticate(username = username, password = password)
        if user:
            try:
                token = Token.objects.get(user = user)
            except Token.DoesNotExist:
                token = None
            if token:
                    token.delete()  
            token = Token.objects.create(user = user)
            return Response({'token': token.key}, status = status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid credentials'}, status = status.HTTP_401_UNAUTHORIZED)
        
class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status = status.HTTP_200_OK)
    def patch(self, request):
        serializer = UserSerializer(request.user, data = request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response({'message': 'Invalid data'}, status = status.HTTP_400_BAD_REQUEST)
    
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        serializer = ChangePasswordSerializer(data = request.data)
        if serializer.is_valid():
            if not user.check_password(serializer.data.get('old_password')):
                return Response({'old_password': 'Wrong password'}, status = status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.data.get('new_password'))
            user.save()
            return Response({'message': 'Password changed successfully'}, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    

class CategoryEndpointView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        categories = Category.objects.all()
        res = []
        for category in categories:
            res.append({'id': category.id, 'name': category.name})
        return Response(res, status = status.HTTP_200_OK)
    def post(self, request):
        user = request.user
        if user.is_superuser:
            try:
                new_category = Category(name = request.data['name'])
            except KeyError:
                return Response({'message': 'name field is required'}, status = status.HTTP_400_BAD_REQUEST)
            
            try:
                new_category.save()
            except Exception:
                return Response({'message': 'Category already exists'}, status = status.HTTP_400_BAD_REQUEST)
            
            return Response({'message': 'Category created successfully'}, status = status.HTTP_201_CREATED)
        else:
            return Response({'message': 'You are not authorized to perform this action'}, status = status.HTTP_403_UNAUTHORIZED)
        
    def delete(self, request):
        user = request.user
        if user.is_superuser:
            try:
                name = request.data['name']
            except KeyError:
                return Response({'message': 'name field is required'}, status = status.HTTP_400_BAD_REQUEST)
            try:
                category = Category.objects.get(name=name)
            except Category.DoesNotExist:
                return Response({'message': 'Category does not exist'}, status = status.HTTP_400_BAD_REQUEST)
            category.delete()
            return Response({'message': 'Category deleted successfully'}, status = status.HTTP_200_OK)
        

class PostListEndpointView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        posts = Post.objects.all()
        res = []
        for post in posts:
            res.append({'id': post.id, 
                        'title': post.title, 
                        'author': post.author.first_name + ' ' + post.author.last_name, 
                        'category': post.category.name,
                        'likes': post.likes.count(),
                        'body': post.body,
                        })
        return Response(res, status = status.HTTP_200_OK)
    def post(self, request):
        user = request.user
        if user.is_superuser:
            try:
                title = request.data['title']
                title_tag = request.data['title_tag']
                author = User.objects.get(id = request.data['author'])
                category = Category.objects.get(id = request.data['category'])
                body = request.data['body']
            except KeyError:
                return Response({'message': 'title, title_tag, author, category and body fields are required'}, status = status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({'message': 'Author does not exist'}, status = status.HTTP_400_BAD_REQUEST)
            except Category.DoesNotExist:
                return Response({'message': 'Category does not exist'}, status = status.HTTP_400_BAD_REQUEST)
            
            try:
                new_post = Post(title = title, title_tag = title_tag, author = author, category = category, body = body)
            except Exception:
                return Response({'message': 'Post already exists'}, status = status.HTTP_400_BAD_REQUEST)
            
            new_post.save()
            return Response({'message': 'Post created successfully'}, status = status.HTTP_201_CREATED)
        else:
            return Response({'message': 'You are not authorized to perform this action'}, status = status.HTTP_403_UNAUTHORIZED)
        

class PostDetailEndpointView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        try:
            post = Post.objects.get(id = pk)
        except Post.DoesNotExist:
            return Response({'message': 'Post does not exist'}, status = status.HTTP_400_BAD_REQUEST)
        res = {'id': post.id, 
                        'title': post.title, 
                        'author': post.author.first_name + ' ' + post.author.last_name, 
                        'category': post.category.name,
                        'likes': post.likes.count(),
                        'body': post.body,
                        }
        return Response(res, status = status.HTTP_200_OK)
    def delete(self, request, pk):
        user = request.user 
        try:
            post = Post.objects.get(id = pk)
        except Post.DoesNotExist:
            return Response({'message': 'Post does not exist'}, status = status.HTTP_400_BAD_REQUEST)
        if user.is_superuser or user == post.author:
            post.delete()
            return Response({'message': 'Post deleted successfully'}, status = status.HTTP_200_OK)
        else:
            return Response({'message': 'You are not authorized to perform this action'}, status = status.HTTP_403_UNAUTHORIZED)