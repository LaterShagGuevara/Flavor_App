from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from django.conf import settings
import jwt
import firebase_admin
from firebase_admin import auth as firebase_auth
from .models import CustomUser, UserProfile

class AuthenticationService:
    @staticmethod
    def generate_jwt_token(user):
        payload = {
            'user_id': str(user.id),
            'username': user.username,
            'email': user.email,
            'is_premium': user.is_premium_user
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

    @staticmethod
    def verify_firebase_token(id_token):
        try:
            decoded_token = firebase_auth.verify_id_token(id_token)
            return decoded_token
        except Exception as e:
            return None

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    dietary_preferences = request.data.get('dietary_preferences', {})
    allergies = request.data.get('allergies', [])

    if not username or not email or not password:
        return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = CustomUser.objects.create_user(
            username=username, 
            email=email, 
            password=password
        )
        
        # Create user profile
        UserProfile.objects.create(
            user=user,
            dietary_preferences=dietary_preferences,
            allergies=allergies
        )
        
        token = AuthenticationService.generate_jwt_token(user)
        return Response({
            'user_id': str(user.id),
            'username': user.username,
            'token': token
        }, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = authenticate(username=email, password=password)
    if user:
        token = AuthenticationService.generate_jwt_token(user)
        return Response({
            'user_id': str(user.id),
            'username': user.username,
            'token': token,
            'is_premium': user.is_premium_user
        })
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([AllowAny])
def social_login(request):
    provider = request.data.get('provider')  # 'google' or 'facebook'
    id_token = request.data.get('id_token')
    
    decoded_token = AuthenticationService.verify_firebase_token(id_token)
    if not decoded_token:
        return Response({'error': 'Invalid Firebase token'}, status=status.HTTP_401_UNAUTHORIZED)

    email = decoded_token.get('email')
    uid = decoded_token.get('uid')

    try:
        # Check if user exists
        if provider == 'google':
            user, created = CustomUser.objects.get_or_create(
                google_id=uid,
                defaults={
                    'username': email.split('@')[0], 
                    'email': email, 
                    'is_active': True
                }
            )
        elif provider == 'facebook':
            user, created = CustomUser.objects.get_or_create(
                facebook_id=uid,
                defaults={
                    'username': email.split('@')[0], 
                    'email': email, 
                    'is_active': True
                }
            )
        
        token = AuthenticationService.generate_jwt_token(user)
        return Response({
            'user_id': str(user.id),
            'username': user.username,
            'token': token,
            'created': created
        })
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    
    return Response({
        'username': user.username,
        'email': user.email,
        'total_flavor_points': user.total_flavor_points,
        'badges': user.badges,
        'dietary_preferences': user_profile.dietary_preferences,
        'allergies': user_profile.allergies,
        'cooking_skill_level': user_profile.cooking_skill_level,
        'is_premium': user.is_premium_user
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_user_profile(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    
    # Update user fields
    user.profile_picture = request.data.get('profile_picture', user.profile_picture)
    user.bio = request.data.get('bio', user.bio)
    user.save()
    
    # Update user profile fields
    user_profile.dietary_preferences = request.data.get('dietary_preferences', user_profile.dietary_preferences)
    user_profile.allergies = request.data.get('allergies', user_profile.allergies)
    user_profile.cooking_skill_level = request.data.get('cooking_skill_level', user_profile.cooking_skill_level)
    user_profile.save()
    
    return Response({
        'message': 'Profile updated successfully'
    })
