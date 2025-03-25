from rest_framework import viewsets
from .serializers import SchemeSerializer,CashCollectionSerializer,CashCollectionEntrySerializer,CustomerSchemePaymentSerializer
from rest_framework.response import Response
from rest_framework import status
from collectionplans.models import CashCollection, Scheme
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import permission_classes
from customer.models import Customer
from collectionplans.models import CashCollectionEntry


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def scheme_list(request):
    """Retrieve all schemes."""
    schemes = Scheme.objects.all()
    serializer = SchemeSerializer(schemes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def scheme_create(request):
    """Create a new scheme."""
    serializer = SchemeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def scheme_update(request, id):
    """Update an existing scheme."""
    try:
        scheme = Scheme.objects.get(id=id)
    except Scheme.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = SchemeSerializer(scheme, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  


@api_view(['POST'])
@permission_classes([AllowAny])
def enroll_customer_in_scheme(request):
    """Enrolls a customer in a selected scheme (Creates CashCollection)."""
   
    if not request.data.get("customer") or not request.data.get("scheme"):
        return Response({"error": "Customer and Scheme are required"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        customer = Customer.objects.get(id=request.data["customer"])
    except Customer.DoesNotExist:
        return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
    try:
        scheme = Scheme.objects.get(id=request.data["scheme"])
    except Scheme.DoesNotExist:
        return Response({"error": "Scheme not found"}, status=status.HTTP_404_NOT_FOUND)
    
    existing_entry = CashCollection.objects.filter(scheme=scheme, customer=customer).exists()
    if existing_entry:
        return Response({"error": "Customer is already enrolled in this scheme"}, status=status.HTTP_400_BAD_REQUEST)
    
    # Prepare data for serializer
    data = request.data.copy()
    
    serializer = CashCollectionSerializer(data=data)
    if serializer.is_valid():
        # Pass customer and scheme directly, don't try to add customer afterwards
        cash_collection = serializer.save(
            created_by=request.user,
            customer=customer,
            scheme=scheme
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cash_collection_list(request):
    cash_collections = CashCollection.objects.all()
    serializer = CashCollectionSerializer(cash_collections, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cash_collection_detail(request, id):
    try:
        cash_collection = CashCollection.objects.get(id=id)
    except CashCollection.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = CashCollectionSerializer(cash_collection)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def cashcollection_delete(request, id):
    try:
        cash_collection = CashCollection.objects.get(id=id)
    except CashCollection.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    cash_collection.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cash_collection_entry_create(request):
    data = request.data
    serializer = CashCollectionEntrySerializer(data=data)
    if serializer.is_valid():
        serializer.save(created_by=request.user, updated_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# List view function
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cash_collection_entry_list(request):
    entries = CashCollectionEntry.objects.all()
    serializer = CashCollectionEntrySerializer(entries, many=True)
    return Response(serializer.data)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def customer_scheme_payment_list(request):
    entries = CashCollectionEntry.objects.all()
    serializer = CustomerSchemePaymentSerializer(entries, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# @api_view(["GET"])
# @permission_classes([IsAuthenticated])
# def customer_scheme_payment_list(request):
#     # Get unique (customer, scheme) pairs
#     unique_entries = (
#         CashCollectionEntry.objects.order_by("customer", "scheme")
#         .distinct("customer", "scheme")
#     )

#     # Serialize the data
#     serializer = CustomerSchemePaymentSerializer(unique_entries, many=True)

#     return Response(serializer.data, status=status.HTTP_200_OK)
# Detail view function
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cash_collection_entry_detail(request, pk):
    try:
        entry = CashCollectionEntry.objects.get(pk=pk)
    except CashCollectionEntry.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = CashCollectionEntrySerializer(entry)
    return Response(serializer.data)

# Update view function
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def cash_collection_entry_update(request, pk):
    try:
        entry = CashCollectionEntry.objects.get(pk=pk)
    except CashCollectionEntry.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = CashCollectionEntrySerializer(entry, data=request.data)
    if serializer.is_valid():
        serializer.save(updated_by=request.user)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Delete view function
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def cash_collection_entry_delete(request, pk):
    try:
        entry = CashCollectionEntry.objects.get(pk=pk)
    except CashCollectionEntry.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    entry.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)





# ...........................................................................................................

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_customer_schemes(request):
    """Get all customer-scheme enrollments (CashCollection records)."""
    scheme_id = request.query_params.get('scheme', None)
    queryset = CashCollection.objects.all()

    if scheme_id:
        queryset = queryset.filter(scheme_id=scheme_id)
    serializer = CashCollectionSerializer(queryset, many=True)
    
    return Response(serializer.data)