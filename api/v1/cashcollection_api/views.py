from rest_framework import viewsets
from .serializers import SchemeSerializer, CashCollectionSerializer, CashCollectionEntrySerializer, CustomerSchemePaymentSerializer,CollectionEntrySerializer
from rest_framework.response import Response
from rest_framework import status
from collectionplans.models import CashCollection, Scheme
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import permission_classes
from customer.models import Customer
from collectionplans.models import CashCollectionEntry,CollectionEntry
from django.db.models import Sum, Case, When, DecimalField, F
from django.db.models.functions import Coalesce
from decimal import Decimal


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
        serializer.save(created_by=request.user)
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
        serializer.save(updated_by=request.user)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  


@api_view(['POST'])
@permission_classes([IsAuthenticated])
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
    

    data = request.data.copy()
    
    serializer = CashCollectionSerializer(data=data)
    if serializer.is_valid():
        
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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cash_collection_entry_list(request):
    entries = CashCollectionEntry.objects.all().order_by('-created_at')  
    serializer = CashCollectionEntrySerializer(entries, many=True)
    return Response(serializer.data)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def customer_scheme_payment_list(request):
    entries = CashCollectionEntry.objects.all()
    serializer = CustomerSchemePaymentSerializer(entries, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def customer_scheme_payment_list_logged_in_user(request):
    user = request.user
    try:
        customer = Customer.objects.get(user=user)  
    except Customer.DoesNotExist:
        return Response({"detail": "Customer profile not found."}, status=status.HTTP_404_NOT_FOUND)

    entries = CashCollectionEntry.objects.filter(customer=customer)
    serializer = CustomerSchemePaymentSerializer(entries, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cash_collection_entry_detail(request, pk):
    try:
        entry = CashCollectionEntry.objects.get(pk=pk)
    except CashCollectionEntry.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = CashCollectionEntrySerializer(entry)
    return Response(serializer.data)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def cash_collection_entry_update(request, pk):
    try:
        entry = CashCollectionEntry.objects.get(pk=pk)
    except CashCollectionEntry.DoesNotExist:
        return Response({"error": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND)
    

    data = {
        'amount': request.data.get('amount', entry.amount),
        'payment_method': request.data.get('payment_method', entry.payment_method)
    }
    
    serializer = CashCollectionEntrySerializer(entry, data=data, partial=True)
    if serializer.is_valid():
        serializer.save(updated_by=request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def cash_collection_entry_delete(request, pk):
    try:
        entry = CashCollectionEntry.objects.get(pk=pk)
    except CashCollectionEntry.DoesNotExist:
        return Response({"error": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND)
    
    entry.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def customer_transaction_list(request):
    """Get all customer transaction entries."""
    entries = CashCollectionEntry.objects.all().order_by('-created_at')
    serializer = CashCollectionEntrySerializer(entries, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def customer_transaction_update(request, pk):
    """Update a customer transaction entry."""
    try:
        entry = CashCollectionEntry.objects.get(pk=pk)
    except CashCollectionEntry.DoesNotExist:
        return Response({"error": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND)
    
    
    data = {
        'amount': request.data.get('amount', entry.amount),
        'payment_method': request.data.get('payment_method', entry.payment_method)
    }
    
    serializer = CashCollectionEntrySerializer(entry, data=data, partial=True)
    if serializer.is_valid():
        serializer.save(updated_by=request.user)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def customer_transaction_delete(request, pk):
    """Delete a customer transaction entry."""
    try:
        entry = CashCollectionEntry.objects.get(pk=pk)
    except CashCollectionEntry.DoesNotExist:
        return Response({"error": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND)
    
    entry.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


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






@api_view(['GET'])
@permission_classes([IsAuthenticated])
def collection_list(request):
    """Get all collection entries with running totals"""
    entries = CollectionEntry.objects.all().order_by('date', 'created_at')
    
    
    running_total = Decimal('0.00')
    entries_with_totals = []
    
    for entry in entries:
        if entry.type == 'credit':
            running_total += entry.amount
        else:  
            running_total -= entry.amount
        
        entry_data = CollectionEntrySerializer(entry).data
        entry_data['running_total'] = running_total
        entries_with_totals.append(entry_data)
    
    return Response(entries_with_totals, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def collection_create(request):
    """Create a new collection entry"""
    serializer = CollectionEntrySerializer(data=request.data, context={'request': request})
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def collection_detail(request, pk):
    """Get details of a specific collection entry"""
    try:
        entry = CollectionEntry.objects.get(pk=pk)
    except CollectionEntry.DoesNotExist:
        return Response({"error": "Collection entry not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = CollectionEntrySerializer(entry)
    return Response(serializer.data)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def collection_update(request, pk):
    """Update a collection entry"""
    try:
        entry = CollectionEntry.objects.get(pk=pk)
    except CollectionEntry.DoesNotExist:
        return Response({"error": "Collection entry not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = CollectionEntrySerializer(
        entry, 
        data=request.data, 
        partial=True,
        context={'request': request}
    )
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def collection_delete(request, pk):
    """Delete a collection entry"""
    try:
        entry = CollectionEntry.objects.get(pk=pk)
    except CollectionEntry.DoesNotExist:
        return Response({"error": "Collection entry not found"}, status=status.HTTP_404_NOT_FOUND)
    
    entry.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def collection_summary(request):
    """Get summary statistics for collections"""
    
    summary = CollectionEntry.objects.aggregate(
        total_credit=Coalesce(
            Sum(Case(When(type='credit', then=F('amount')), output_field=DecimalField())), 
            Decimal('0.00')
        ),
        total_debit=Coalesce(
            Sum(Case(When(type='debit', then=F('amount')), output_field=DecimalField())), 
            Decimal('0.00')
        )
    )
    
    summary['balance'] = summary['total_credit'] - summary['total_debit']
    
    return Response(summary, status=status.HTTP_200_OK)


@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def collection_detail_or_update_or_delete(request, pk):
    """Handle GET, PATCH, DELETE for a collection entry at the same endpoint"""
    try:
        entry = CollectionEntry.objects.get(pk=pk)
    except CollectionEntry.DoesNotExist:
        return Response({"error": "Collection entry not found"}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = CollectionEntrySerializer(entry)
        return Response(serializer.data)
    
    elif request.method == 'PATCH':
        serializer = CollectionEntrySerializer(
            entry, 
            data=request.data, 
            partial=True,
            context={'request': request}
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        entry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)