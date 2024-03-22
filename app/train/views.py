from django.shortcuts import render
from rest_framework.response import Response
from datetime import datetime
from rest_framework import status
from rest_framework.views import APIView
from core.serializers import GeneralResponseSerializer
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework import generics
from django.db.models import Q
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from user.utils import get_user_from_token
from django.db.models import Case, When, Value, CharField
from django.db.models import F, Value
from .models import TrainUser, Station, Train
from .serializers import TrainUserSerializer, StationSerializer, TrainSerializer, WalletSerializer


class WalletDetailedView(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            return TrainUser.objects.get(pk=pk)
        except TrainUser.DoesNotExist:
            return None

    def get(self, request, wallet_id):
        response={
            'status_code': status.HTTP_400_BAD_REQUEST,
            'message': 'Bad Request',
            'data': None,
            'error': None,
            'timestamp': datetime.now()
        }
        try:
            user = self.get_object(wallet_id)
            if user:
                
                return Response({
                    
                    "wallet_id": user.user_id, # user's wallet id
                    "balance": user.balance, # user's wallet balance
                    "wallet_user":
                    {
                        "user_id": user.user_id, # user's numeric id
                        "user_name": user.user_name # user's full name
                    }
                }, status=status.HTTP_200_OK)
                response['data'] = {'ProductList': serializer.data}
                response['error'] = None
                response['message'] = f"Success"
                response['status_code'] = status.HTTP_200_OK
            else:
                return Response({"message": f"wallet with id: {wallet_id} was not found" }, status=status.HTTP_404_NOT_FOUND)
                response['message'] = f"Can't Find Requested Item"
                response['status_code'] = status.HTTP_404_NOT_FOUND
        except Exception as e:
            if isinstance(e, DRFValidationError):
                errors = {}
                for field, field_errors in e.detail.items():
                    errors[field] = str(field_errors[0])
                response['error'] = errors
            else:
                response['message'] = str(e)
        serializer = GeneralResponseSerializer(data=response)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=response['status_code'])

    def put(self, request, wallet_id):
        response={
            'status_code': status.HTTP_400_BAD_REQUEST,
            'message': 'Bad Request',
            'data': None,
            'error': None,
            'timestamp': datetime.now()
        }
        try:
            user = self.get_object(wallet_id)
            if user:
                requested_data = request.data
                cc1 = int(requested_data["recharge"])

                if (cc1 <100 or cc1 >10000):
                    return Response({"message": f"invalid amount: {cc1}" }, status=status.HTTP_400_BAD_REQUEST)
                cc2 = user.balance
                user.balance = cc1 + cc2
                user.save()

                return Response({
                    "wallet_id": user.user_id, # user's wallet id
                    "balance": user.balance, # user's wallet balance
                    "wallet_user":
                    {
                        "user_id": user.user_id, # user's numeric id
                        "user_name": user.user_name # user's full name
                    }
                }, status=status.HTTP_200_OK)
                response['data'] = {'ProductList': serializer.data}
                response['error'] = None
                response['message'] = f"Update Successful"
                response['status_code'] = status.HTTP_200_OK
            else:
                return Response({"message": f"wallet with id: {wallet_id} was not found" }, status=status.HTTP_404_NOT_FOUND)
                response['message'] = f"Can't Find Requested Item"
                response['status_code'] = status.HTTP_404_NOT_FOUND

        except Exception as e:
            if isinstance(e, DRFValidationError):
                errors = {}
                for field, field_errors in e.detail.items():
                    errors[field] = str(field_errors[0])
                response['error'] = errors
            else:
                response['message'] = str(e)
        serializer = GeneralResponseSerializer(data=response)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=response['status_code'])


class StationListView(APIView):

    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        response={
            'status_code': status.HTTP_400_BAD_REQUEST,
            'message': 'Bad Request',
            'data': None,
            'error': None,
            'timestamp': datetime.now()
        }
        try:
            query = Station.objects.all()
            serializer_class = StationSerializer(query, many=True)

            return Response({"stations": serializer_class.data}, status=status.HTTP_200_OK)
            response['data'] = {'ProductList': serializer_class.data}
            response['error'] = None
            response['message'] = f"Success"
            response['status_code'] = status.HTTP_200_OK
        except AuthenticationFailed as e:
            # Handle authentication failure
            return Response({'detail': 'Authentication failed.'}, status=401)
        except Exception as e:
            if isinstance(e, DRFValidationError):
                errors = {}
                for field, field_errors in e.detail.items():
                    errors[field] = str(field_errors[0])
                response['error'] = errors
            else:
                response['message'] = str(e)
        
        serializer = GeneralResponseSerializer(data=response)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=response['status_code'])


    def post(self, request):
        response={
            'status_code': status.HTTP_400_BAD_REQUEST,
            'message': 'Bad Request',
            'data': None,
            'error': None,
            'timestamp': datetime.now()
        }
        try:
            serializer_class = StationSerializer(data=request.data)
            if serializer_class.is_valid(raise_exception=True):
                serializer_class.save()
                return Response(serializer_class.data, status=status.HTTP_201_CREATED)
                response['data'] = {'Product': serializer_class.data}
                response['error'] = None
                response['status_code'] = status.HTTP_201_CREATED
                response['message'] = f"Created Successful"
            pass
        except Exception as e:
            if isinstance(e, DRFValidationError):
                errors = {}
                for field, field_errors in e.detail.items():
                    errors[field] = str(field_errors[0])
                response['error'] = errors
            else:
                response['message'] = str(e)
        serializer = GeneralResponseSerializer(data=response)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=response['status_code'])

# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
class TrainUserListView(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    # def get(self, request, *args, **kwargs):
    #     response={
    #         'status_code': status.HTTP_400_BAD_REQUEST,
    #         'message': 'Bad Request',
    #         'data': None,
    #         'error': None,
    #         'timestamp': datetime.now()
    #     }
    #     try:

    #         title = request.query_params.get('title', None)
    #         author = request.query_params.get('author', None)
    #         genre = request.query_params.get('genre', None)

    #         sort_by = request.query_params.get('sort', 'id')  # Default sorting field
    #         sort_order = request.query_params.get('order', 'ASC')  # Default sorting order

    #         # Query the database
    #         query = TrainUser.objects.all()

    #         # Apply search filter
    #         if title:
    #             query = query.filter(title__icontains=title)
    #         elif author:
    #             query = query.filter(author__icontains=author)
    #         elif genre:
    #             query = query.filter(genre__icontains=genre)

    #         # Apply sorting
    #         if sort_order == 'ASC':
    #             query = query.order_by(sort_by)
    #         elif sort_order == 'DESC':
    #             query = query.order_by(f'-{sort_by}')

    #         # Serialize the queryset
    #         serializer_class = TrainUserSerializer(query, many=True)

    #         return Response({'books': serializer_class.data}, status=status.HTTP_200_OK)
    #         response['data'] = {'ProductList': serializer_class.data}
    #         response['error'] = None
    #         response['message'] = f"Success"
    #         response['status_code'] = status.HTTP_200_OK
    #     except AuthenticationFailed as e:
    #         # Handle authentication failure
    #         return Response({'detail': 'Authentication failed.'}, status=401)
    #     except Exception as e:
    #         if isinstance(e, DRFValidationError):
    #             errors = {}
    #             for field, field_errors in e.detail.items():
    #                 errors[field] = str(field_errors[0])
    #             response['error'] = errors
    #         else:
    #             response['message'] = str(e)
        
    #     serializer = GeneralResponseSerializer(data=response)
    #     serializer.is_valid(raise_exception=True)
    #     return Response(serializer.data, status=response['status_code'])

    def post(self, request):
        response={
            'status_code': status.HTTP_400_BAD_REQUEST,
            'message': 'Bad Request',
            'data': None,
            'error': None,
            'timestamp': datetime.now()
        }
        try:
            serializer_class = TrainUserSerializer(data=request.data)
            if serializer_class.is_valid(raise_exception=True):
                serializer_class.save()
                return Response(serializer_class.data, status=status.HTTP_201_CREATED)
                response['data'] = {'Product': serializer_class.data}
                response['error'] = None
                response['status_code'] = status.HTTP_201_CREATED
                response['message'] = f"Created Successful"
            pass
        except Exception as e:
            if isinstance(e, DRFValidationError):
                errors = {}
                for field, field_errors in e.detail.items():
                    errors[field] = str(field_errors[0])
                response['error'] = errors
            else:
                response['message'] = str(e)
        serializer = GeneralResponseSerializer(data=response)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=response['status_code'])

class TrainListView(APIView):
    def post(self, request):
        response={
            'status_code': status.HTTP_400_BAD_REQUEST,
            'message': 'Bad Request',
            'data': None,
            'error': None,
            'timestamp': datetime.now()
        }
        try:
            serializer_class = TrainSerializer(data=request.data)
            if serializer_class.is_valid(raise_exception=True):
                serializer_class.save()
                train = serializer_class.data

                return Response({
                    "train_id": train['train_id'],
                    "train_name": train['train_name'],
                    "capacity": train['capacity'],
                    "service_start": train['stops'][0]['departure_time'],
                    "service_ends": train['stops'][len(train['stops'])-1]['arrival_time'],
                    "num_stations": len(train['stops'])
                }, 
                status=status.HTTP_201_CREATED)
                response['data'] = {'Product': serializer_class.data}
                response['error'] = None
                response['status_code'] = status.HTTP_201_CREATED
                response['message'] = f"Created Successful"
            pass
        except Exception as e:
            if isinstance(e, DRFValidationError):
                errors = {}
                for field, field_errors in e.detail.items():
                    errors[field] = str(field_errors[0])
                response['error'] = errors
            else:
                response['message'] = str(e)
        serializer = GeneralResponseSerializer(data=response)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=response['status_code'])

class StationDetailedView(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    # def get_object(self, pk):
    #     try:
    #         return Book.objects.get(pk=pk)
    #     except Book.DoesNotExist:
    #         return None

    def get(self, request, station_id):
        response={
            'status_code': status.HTTP_400_BAD_REQUEST,
            'message': 'Bad Request',
            'data': None,
            'error': None,
            'timestamp': datetime.now()
        }
        try:
            station = Station.objects.filter(station_id = station_id)
            if len(station) != 0:
                trains_at_station = Train.objects.filter(stops__station_id=station_id).distinct().annotate(
                    arrival_time=Case(
                        When(stops__station_id=station_id, then=F('stops__arrival_time')),
                        default=Value(None),
                        output_field=CharField()
                    ),
                    departure_time=Case(
                        When(stops__station_id=station_id, then=F('stops__departure_time')),
                        default=Value(None),
                        output_field=CharField()
                    )
                ).values('train_id', 'arrival_time', 'departure_time')



                return Response({
                    "station_id": station_id,
                    "trains":  trains_at_station
                }, status=status.HTTP_200_OK)
            # if product:
            #     serializer = BookSerializer(product)
            #     return Response(serializer.data, status=status.HTTP_200_OK)
            #     response['data'] = {'ProductList': serializer.data}
            #     response['error'] = None
            #     response['message'] = f"Success"
            #     response['status_code'] = status.HTTP_200_OK
            else:
                return Response({"message": f"station with id: {station_id} was not found" }, status=status.HTTP_404_NOT_FOUND)
                response['message'] = f"Can't Find Requested Item"
                response['status_code'] = status.HTTP_404_NOT_FOUND
        except Exception as e:
            if isinstance(e, DRFValidationError):
                errors = {}
                for field, field_errors in e.detail.items():
                    errors[field] = str(field_errors[0])
                response['error'] = errors
            else:
                response['message'] = str(e)
        serializer = GeneralResponseSerializer(data=response)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=response['status_code'])

    # def put(self, request, pid):
    #     response={
    #         'status_code': status.HTTP_400_BAD_REQUEST,
    #         'message': 'Bad Request',
    #         'data': None,
    #         'error': None,
    #         'timestamp': datetime.now()
    #     }
    #     try:
    #         product = self.get_object(pid)
    #         if product:
    #             requested_data = request.data
    #             requested_data['id'] = pid
    #             serializer = BookSerializer(product, data=requested_data)
    #             if serializer.is_valid(raise_exception=True):
    #                 serializer.save()
    #                 return Response(serializer.data, status=status.HTTP_200_OK)
    #                 response['data'] = {'ProductList': serializer.data}
    #                 response['error'] = None
    #                 response['message'] = f"Update Successful"
    #                 response['status_code'] = status.HTTP_200_OK
    #         else:
    #             return Response({"message": f"book with id: {pid} was not found" }, status=status.HTTP_404_NOT_FOUND)
    #             response['message'] = f"Can't Find Requested Item"
    #             response['status_code'] = status.HTTP_404_NOT_FOUND

    #     except Exception as e:
    #         if isinstance(e, DRFValidationError):
    #             errors = {}
    #             for field, field_errors in e.detail.items():
    #                 errors[field] = str(field_errors[0])
    #             response['error'] = errors
    #         else:
    #             response['message'] = str(e)
    #     serializer = GeneralResponseSerializer(data=response)
    #     serializer.is_valid(raise_exception=True)
    #     return Response(serializer.data, status=response['status_code'])

    # def delete(self, request, pid):
    #     response={
    #         'status_code': status.HTTP_400_BAD_REQUEST,
    #         'message': 'Bad Request',
    #         'data': None,
    #         'error': None,
    #         'timestamp': datetime.now()
    #     }
    #     try:
    #         product = self.get_object(pid)
    #         if product:
    #             product.delete()
    #             response['error'] = None
    #             response['message'] = f"Delete Successful"
    #             response['status_code'] = status.HTTP_204_NO_CONTENT
    #         else:
    #             response['message'] = f"Can't Find Requested Item"
    #             response['status_code'] = status.HTTP_404_NOT_FOUND
    #     except Exception as e:
    #         if isinstance(e, DRFValidationError):
    #             errors = {}
    #             for field, field_errors in e.detail.items():
    #                 errors[field] = str(field_errors[0])
    #             response['error'] = errors
    #         else:
    #             response['message'] = str(e)
    #     serializer = GeneralResponseSerializer(data=response)
    #     serializer.is_valid(raise_exception=True)
    #     return Response(serializer.data)

class BuyTicketListView(APIView):

    def post(self, request):
        response={
            'status_code': status.HTTP_400_BAD_REQUEST,
            'message': 'Bad Request',
            'data': None,
            'error': None,
            'timestamp': datetime.now()
        }
#         try:
        wallet_id = request.data.get('wallet_id')
        time_after = request.data.get('time_after')
        station_from = request.data.get('station_from')
        station_to = request.data.get('station_to')
        return Response({
                "message": f"no ticket available for station: {station_from} to station: {station_to}"
            }, status=status.HTTP_403_FORBIDDEN)

class RRRListView(APIView):

    def get(self, request):
        response={
            'status_code': status.HTTP_400_BAD_REQUEST,
            'message': 'Bad Request',
            'data': None,
            'error': None,
            'timestamp': datetime.now()
        }
#         try:
        station_from = request.query_params.get('from')
        station_to = request.query_params.get('to')
        optimize = request.query_params.get('optimize')
        return Response({
                "message": f"no routes available from station: {station_from} to station: {station_to}"
            }, status=status.HTTP_403_FORBIDDEN)

