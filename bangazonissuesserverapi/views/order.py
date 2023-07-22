"""View module for handling requests about orders"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers, status
from bangazonissuesserverapi.models import Order, User, Category


class OrderView(ViewSet):
    """Order view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single order
        Returns:
            Response -- JSON serialized order
        """
        try:
            order = Order.objects.get(pk=pk)
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        except Order.DoesNotExist:
          	return Response({'message': 'order does not exist'}, status=status.HTTP_404_NOT_FOUND)
       
    def list(self, request):
        """Handle GET requests to get all orders

        Returns:
            Response -- JSON serialized list of orders
        """
        order = Order.objects.all()
        serializer = OrderSerializer(order, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def create(self, request):
       
        CustomerId = User.objects.get(pk=request.data["customer_id"])

        order = Order.objects.create(
            customer_id = CustomerId,
            first_name=request.data["first_name"],
            last_name=request.data["last_name"],
            address=request.data["address"],
            payment_type=request.data["payment_type"],
            is_open=request.data["is_open"],
            created_on=request.data["created_on"],
            order_total=request.data["order_total"],
        )
        serializer = OrderSerializer(order)
        return Response(serializer.data)  
    
    def update(self, request, pk):

        order = Order.objects.get(pk=pk)
        order.customer_id = User.objects.get(pk=request.data["customer_id"])
        order.first_name= request.data["first_name"]
        order.last_name = request.data["last_name"]
        order.address = request.data["address"]
        order.payment_type = request.data["payment_type"]
        order.is_open = request.data["is_open"]
        order.created_on=request.data["created_on"]
        order.order_total=request.data["order_total"]
        
        order.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)   
    
    def destroy(self, request, pk):
        order = Order.objects.get(pk=pk)
        order.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    
class OrderSerializer(serializers.ModelSerializer):
    """JSON serializer for events
    """
    class Meta:
        model = Order
        fields = ('id', 'customer_id', 'first_name', 'last_name', 'address', 'payment_type', 'is_open', 'created_on','order_total')
        depth = 1
