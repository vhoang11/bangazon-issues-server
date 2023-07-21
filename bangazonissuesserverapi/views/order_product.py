"""View module for handling requests about orders"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers, status
from bangazonissuesserverapi.models import OrderProduct, User, Category, Order, Product


class OrderProductView(ViewSet):
    """Order products view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single order products
        Returns:
            Response -- JSON serialized order products
        """
        try:
            order_product = OrderProduct.objects.get(pk=pk)
            serializer = OrderProductSerializer(order_product)
            return Response(serializer.data)
        except OrderProduct.DoesNotExist:
          	return Response({'message': 'order product does not exist'}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all order products

        Returns:
            Response -- JSON serialized list of order products
        """
        order_product = OrderProduct.objects.all()
        serializer = OrderProductSerializer(order_product, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def create(self, request):
       
        ProductId = Product.objects.get(uid=request.data["product_id"])
        OrderId = Order.objects.get(uid=request.data["order_id"])

        order_product = OrderProduct.objects.create(
						product_id = ProductId,
      			order_id = OrderId,
						quantity=request.data["quantity"],
            quantity_total=request.data["quantity_total"],
        )
        serializer = OrderProductSerializer(order_product)
        return Response(serializer.data)  
    
    def update(self, request, pk):

        order_product = OrderProduct.objects.get(pk=pk)
        order_product.product_id = Product.objects.get(uid=request.data["product_id"])
        order_product.order_id= Order.objects.get(pk=request.data["order_id"])
        order_product.quantity = request.data["quantity"]
        order_product.quantity_total=request.data["quantity_total"]
        
        order_product.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)   
    
    def destroy(self, request, pk):
        order_product = OrderProduct.objects.get(pk=pk)
        order_product.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    
class OrderProductSerializer(serializers.ModelSerializer):
    """JSON serializer for events
    """
    class Meta:
        model = OrderProduct
        fields = ('product_id', 'order_id', 'quantity', 'quantity_total')
        depth = 1
