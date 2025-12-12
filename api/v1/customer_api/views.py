from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from customer.models import Customer,Agent
from .serializers import CustomerSerializer,AgentProfileSerializer,CustomerListSerializer,AgentListSerializer
from django.core.paginator import Paginator
from users.models import CustomUser, UserRoles
from api.v1.users_api.serializers import UserSerializer

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def customer_detail(request, id):
    """Retrieve details of a specific active customer."""
    customer = get_object_or_404(Customer, id=id, is_deleted=False)
    serializer = CustomerSerializer(customer)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def customer_update(request, id):
    """Update an existing customer and its associated CustomUser."""
    customer = get_object_or_404(Customer, id=id)
    serializer = CustomerSerializer(customer, data=request.data, partial=True, context={"request": request})
    if serializer.is_valid():
        serializer.save(updated_by=request.user) 
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def customer_list(request):
    """Retrieve only active customers (users who are not deleted)."""
    customers = Customer.objects.filter(user__is_deleted=False)
    serializer = CustomerListSerializer(customers, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def customer_detail(request, id):
    """Retrieve details of a specific customer (if the user is not deleted)."""
    customer = get_object_or_404(Customer, id=id, user__is_deleted=False)
    serializer = CustomerSerializer(customer)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def customer_delete(request, id):
    """Soft delete a customer by setting user.is_deleted=True."""
    customer = get_object_or_404(Customer, id=id, user__is_deleted=False)
    customer.user.is_deleted = True
    customer.user.save()
    return Response({"message": "Customer soft deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def customer_restore(request, id):
    """Restore a soft-deleted customer by setting user.is_deleted=False."""
    customer = get_object_or_404(Customer, id=id, user__is_deleted=True)
    customer.user.is_deleted = False
    customer.user.save()
    return Response({"message": "Customer restored successfully"}, status=status.HTTP_200_OK)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_agent(request, id):
    print("request.data",request.data)
    agent = get_object_or_404(Agent, id=id)
    serializer = AgentProfileSerializer(agent, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_agent(request, id):
    agent = get_object_or_404(Agent, id=id)
    agent.delete()
    return Response({"message": "Agent deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def agent_restore(request):
    agent = Agent.objects.filter(is_deleted=True)
    agent.restore()
    return Response({"message": "Agent restored successfully"}, status=status.HTTP_200_OK)
   


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_agents(request):
    agent = Agent.objects.all()
    paginator = Paginator(agent, 20)  
    page = request.GET.get("page", 1)
    agent_page = paginator.page(page)

    serializer = AgentListSerializer(agent_page, many=True)
    return Response({
        "count": paginator.count,
        "total_pages": paginator.num_pages,
        "current_page": int(page),
        "results": serializer.data
    }, status=status.HTTP_200_OK)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def agent_detail(request, id):
    agent = get_object_or_404(Agent, id=id)
    serializer = AgentProfileSerializer(agent)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def agent_create(request):
    """API to create a new Agent with a linked user"""
    serializer = AgentProfileSerializer(data=request.data, context={"request": request})

    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message": "Agent created successfully", "data": serializer.data},
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def customer_create(request):
    """API to create a new customer with a linked user"""
    serializer = CustomerSerializer(data=request.data, context={"request": request})

    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message": "Customer created successfully", "data": serializer.data},
            status=status.HTTP_201_CREATED
        )
    # Return detailed error messages
    return Response(
        {"errors": serializer.errors, "message": "Validation failed"},
        status=status.HTTP_400_BAD_REQUEST
    )

