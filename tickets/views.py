from django.shortcuts import render
from django.http import JsonResponse

from .models import *
from rest_framework.decorators import api_view
from .serializers import GuestSerializer,MovieSerializer,ReservationSerializer
from rest_framework import status ,filters
from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework import mixins, generics, viewsets


# Create your views here.


#  1 without Rest and No model Query FBV

def no_rest_no_model(erquest):
    guests=[
        {
            'id':1,
            'name':'mahmoud',
            'mobile':1234567,
        },
        {
            'id':2,
            'name':'hhhhhh',
            'mobile':1234567,
        },
        {
            'id':3,
            'name':'jjjjjjjj',
            'mobile':1234567,
        },
    ]
    
    return JsonResponse(guests,safe=False)


#2 no rest from model
def no_rest_from_model(requerst):
    data = Guest.objects.all()
    response={
        'guests': list(data.values("name",'mobile'))
    }
    
    return JsonResponse(response)


# 3  Function Based view
# 3.1 GET POST
@api_view(["GET","POST"]) 
def FBV_List(request):
    #GET
    if request.method=="GET":
        guests = Guest.objects.all()
        serializer=GuestSerializer(guests,many=True)
        
        return Response(serializer.data)
    
    #POST
    elif request.method == 'POST':
        serializer =GuestSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)
        
#3.2 GET PUT DELETE
@api_view(['GET','PUT','DELETE'])
def FBV_pk(request,pk):
    try:
        guest=Guest.objects.get(pk=pk)
    except Guest.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
        
    #GET
    if request.method=="GET":
        
        serializer=GuestSerializer(guest)
        return Response(serializer.data)
    
    #PUT
    elif request.method == 'PUT':
        serializer =GuestSerializer(guest,data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    # DELETE
    elif request.method == 'DELETE':
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
    
# CBV class based view
# 4.1 GET POST
class CBV_List(APIView):
    def get(self,request):
        guests=Guest.objects.all()
        serializer = GuestSerializer(guests,many=True)
        
        return Response(serializer.data)
    
    def post(self,request):
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)
       
#4.2 GET PUT DELETE class based view --pk
class CBV_pk(APIView):
    
    def get_object(self,pk):
        try:
            return Guest.objects.get(pk=pk)
        except Guest.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def get(self,request,pk):
        guest=self.get_object(pk)
        serializer=GuestSerializer(guest)
        return Response(serializer.data)
    
    def put(self, request,pk):
        guest=self.get_object(pk)
        serializer=GuestSerializer(guest,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request,pk):
        guest=self.get_object(pk)
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#5.1 mixins GET POST   
class Mixins_list(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView,):
    queryset=Guest.objects.all()
    serializer_class=GuestSerializer
    def get(self,request):
        return self.list(request)
    def post(self, request):
        return self.create(request)
    
#5.2 mixins GET DELETE UPDATE
class Mixins_pk(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
    queryset=Guest.objects.all()
    serializer_class = GuestSerializer
    
    def get(self,request,pk):
        return self.retrieve(request)
    
    def put(self, request,pk):
        return self.update(request)
    
    def delete(self, request,pk):
        return self.destroy(request)
    
    
#6 Generics    
#6.1 GET POST
class Generic_list(generics.ListCreateAPIView):
    
    queryset = Guest.objects.all()
    serializer_class =GuestSerializer 
     
class Generic_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset = Guest.objects.all()
    serializer_class =GuestSerializer 
    
    
# 7 viewSets
class ViewSet_gusts(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class =GuestSerializer 
    
class ViewSet_movi(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class =MovieSerializer 
    filter_backends =[filters.SearchFilter]
    search_fields=['movie']
    
class ViewSet_reservation(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class =ReservationSerializer 
    
    

#8 find movie
@api_view(['GET'])
def find_movie(request):
    movies=Movie.objects.filter(
        movie=request.data['movie'],
        hall=request.data['hall'],
    )
    
    serializer= MovieSerializer(movies,many=True)
    return Response(serializer.data)


# 9 create new ewservation

@api_view(['POST'])
def new_reservation(request):
    movie=Movie.objects.get(
        movie=request.data['movie'],
        hall=request.data['hall'], 
    )
    
    guest = Guest()
    guest.name=request.data['name']
    guest.mobile=request.data['mobile']
    
    guest.save()
    
    reservation= Reservation()
    reservation.guest=guest
    reservation.movie=movie
    
    reservation.save()
    
    return Response(status=status.HTTP_201_CREATED)
