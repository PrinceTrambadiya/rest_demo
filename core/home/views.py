from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from home.models import Person
from home.serializers import PeopleSerializers, LoginSerializers, RegisterSerializers
from rest_framework.views import APIView
from rest_framework import viewsets, status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication



class LoginAPI(APIView):
    def post(self,request):
        data = request.data
        serializer = LoginSerializers(data= data)
        if not serializer.is_valid():
            return Response({
                'status': False,
                'message': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(username = serializer.data['username'], password = serializer.data['password'])
        if not user:
            return Response({
                'status': False,
                'message': 'Invalid credentials'
            }, status=status.HTTP_400_BAD_REQUEST)
        token, _ = Token.objects.get_or_create(user= user)
        return Response({
                'status': True,
                'message': 'User Login',
                'token': str(token)
            }, status=status.HTTP_200_OK)

class RegisterAPI(APIView):
    def post(self, request):
        data = request.data
        serializer = RegisterSerializers(data= data)

        if not serializer.is_valid():
            return Response({
                'status': False,
                'message': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response({
                'status': True,
                'message': 'User Created'
            }, status=status.HTTP_201_CREATED)

from django.core.paginator import Paginator

class PersonAPIs(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        try:
            objs = Person.objects.all() 
            page = request.GET.get('page',1)
            page_size = 3
            paginator = Paginator(objs, page_size)
            print(paginator.page(page))
            serializer = PeopleSerializers(paginator.page(page), many = True)
            return Response(serializer.data)
        except Exception as e:
            return Response({
                    'status': False,
                    'message': 'Invalid Page Number'
                }, status=status.HTTP_400_BAD_REQUEST)
        

    def post(self, request):
        data = request.data
        serializer = PeopleSerializers(data= data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)
    
    def put(self, request):
        data = request.data
        serializer = PeopleSerializers(data= data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)
    
    
    def patch(self, request):
        data = request.data
        obj = Person.objects.get(id = data['id'])
        serializer = PeopleSerializers(obj, data= data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)
    
    def delete(self, request):
        data = request.data
        obj = Person.objects.get(id = data['id'])
        obj.delete()
        return Response({'message' : 'Person is deleted'})

@api_view(['GET','POST','PUT'])
def index(request):
    courses = {
            'name' : 'Python',
            'learn': ['Flask', 'Django', 'Tornado', 'FastApi'],
            'course_provider' : 'Prince'
        }
    if request.method == 'GET':
        print(request.GET.get('search'))
        print("GET method")
        return Response(courses)
    elif request.method == 'POST':
        data = request.data
        print('***********')
        print(data)
        print("POST method")
        return Response(courses)
    elif request.method == 'PUT':
        print("PUT method")
        return Response(courses)
        
@api_view(['GET','POST', 'PUT', 'PATCh', 'DELETE'])        
def person(request):
    if request.method == 'GET':
        objs = Person.objects.all() 
        serializer = PeopleSerializers(objs, many = True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        data = request.data
        serializer = PeopleSerializers(data= data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)
    
    elif request.method == 'PUT':
        data = request.data
        serializer = PeopleSerializers(data= data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)
    
    elif request.method == 'PATCH':
        data = request.data
        obj = Person.objects.get(id = data['id'])
        serializer = PeopleSerializers(obj, data= data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)
    
    else:
        data = request.data
        obj = Person.objects.get(id = data['id'])
        obj.delete()
        return Response({'message' : 'Person is deleted'})
    
@api_view(['POST'])
def login(request):
    data = request.data
    serializer = LoginSerializers(data= data)

    if serializer.is_valid():
        data = serializer.validated_data
        return Response({'message' : 'success'})
    return Response(serializer.errors)


class PeopleViewSet(viewsets.ModelViewSet):
    serializer_class = PeopleSerializers
    queryset = Person.objects.all()

    def list(self, request):
        search = request.GET.get('search')
        queryset = self.queryset
        if search:
            queryset = queryset.filter(name__startswith = search)

        serializer = PeopleSerializers(queryset, many = True)
        return Response({'status':'200', 'data': serializer.data}, status=status.HTTP_200_OK)
    
    # @action(detail= False, methods=['post'])
    # def send_mail_to_person(self, request):
    #     return Response({'status':'200', 'message': 'Email sent successfully'}, status=status.HTTP_200_OK)


    @action(detail= True, methods=['post'])
    def send_mail_to_person(self, request, pk):
        print(pk)
        return Response({'status':'200', 'message': 'Email sent successfully'}, status=status.HTTP_200_OK)
