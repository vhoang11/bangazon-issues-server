"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers, status
from bangazonissuesserverapi.models import Product, User, Category


class ProductView(ViewSet):
    """Product view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single product
        Returns:
            Response -- JSON serialized game type
        """
        try:
            post = Product.objects.get(pk=pk)
            serializer = ProductSerializer(post)
            return Response(serializer.data)
        except Product.DoesNotExist:
          return Response({'message': 'Product does not exist'}, status=status.HTTP_404_NOT_FOUND)


    def list(self, request):
        """Handle GET requests to get all products

        Returns:
            Response -- JSON serialized list of products
        """
        post = Product.objects.all()
        serializer = ProductSerializer(post, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def create(self, request):
       
        SellerId = User.objects.get(uid=request.data["seller_id"])
        CatId = Category.objects.get(pk=request.data["category_id"])

        product = Product.objects.create(
						seller_id = SellerId,
						category_id=CatId,
            title=request.data["title"],
            created_on=request.data["created_on"],
            image_url=request.data["image_url"],
            description=request.data["description"],
            price=request.data["price"],
        )
        serializer = ProductSerializer(product)
        return Response(serializer.data)  
    
    def update(self, request, pk):

        product = Product.objects.get(pk=pk)
        product.seller_id = User.objects.get(uid=request.data["seller_id"])
        product.category_id= Category.objects.get(pk=request.data["category_id"])
        product.title = request.data["title"]
        product.created_on = request.data["created_on"]
        product.image_url=request.data["image_url"]
        product.description=request.data["description"]
        product.price=request.data["price"]
        
        product.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)   
    
    def destroy(self, request, pk):
        product = Product.objects.get(pk=pk)
        product.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    
class ProductSerializer(serializers.ModelSerializer):
    """JSON serializer for events
    """
    class Meta:
        model = Product
        fields = ('id', 'seller_id', 'category_id', 'title', 'created_on', 'image_url', 'description','price')
        depth = 1
