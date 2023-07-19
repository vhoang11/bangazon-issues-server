"""View module for handling requests about categories"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from bangazonissuesserverapi.models import User
from datetime import datetime

class UserView(ViewSet):
    """Rare Users view"""
    
    def list(self, request):
        """Handle GET requests to get all users
        Returns:
            Response -- JSON serialized list of users
        """
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)
      
    def retrieve(self, request, pk):
      try:
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)
      except User.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
          
    def update(self, request, pk):
        user = User.objects.get(pk=pk)
        user.first_name = request.data["first_name"]
        user.last_name = request.data["last_name"]
        user.bio = request.data["bio"]
        user.profile_image_url=request.data["profile_image_url"]
        user.created_on = request.data["created_on"]
        user.email=request.data["email"]
        
        user.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
      
class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for categories
    """
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'bio', 'profile_image_url', 'created_on', 'email', 'uid')
        depth = 1
