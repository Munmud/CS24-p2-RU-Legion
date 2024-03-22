from django.shortcuts import render
from .models import Book
from .serializers import BookSerializer
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

# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
class BookListView(APIView):
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

            title = request.query_params.get('title', None)
            author = request.query_params.get('author', None)
            genre = request.query_params.get('genre', None)

            sort_by = request.query_params.get('sort', 'id')  # Default sorting field
            sort_order = request.query_params.get('order', 'ASC')  # Default sorting order

            # Query the database
            query = Book.objects.all()

            # Apply search filter
            if title:
                query = query.filter(title__icontains=title)
            elif author:
                query = query.filter(author__icontains=author)
            elif genre:
                query = query.filter(genre__icontains=genre)

            # Apply sorting
            if sort_order == 'ASC':
                query = query.order_by(sort_by)
            elif sort_order == 'DESC':
                query = query.order_by(f'-{sort_by}')

            # Serialize the queryset
            serializer_class = BookSerializer(query, many=True)

            return Response({'books': serializer_class.data}, status=status.HTTP_200_OK)
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
            serializer_class = BookSerializer(data=request.data)
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
class BookDetailedView(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            return Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return None

    def get(self, request, pid):
        response={
            'status_code': status.HTTP_400_BAD_REQUEST,
            'message': 'Bad Request',
            'data': None,
            'error': None,
            'timestamp': datetime.now()
        }
        try:
            product = self.get_object(pid)
            if product:
                serializer = BookSerializer(product)
                return Response(serializer.data, status=status.HTTP_200_OK)
                response['data'] = {'ProductList': serializer.data}
                response['error'] = None
                response['message'] = f"Success"
                response['status_code'] = status.HTTP_200_OK
            else:
                return Response({"message": f"book with id: {pid} was not found" }, status=status.HTTP_404_NOT_FOUND)
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

    def put(self, request, pid):
        response={
            'status_code': status.HTTP_400_BAD_REQUEST,
            'message': 'Bad Request',
            'data': None,
            'error': None,
            'timestamp': datetime.now()
        }
        try:
            product = self.get_object(pid)
            if product:
                requested_data = request.data
                requested_data['id'] = pid
                serializer = BookSerializer(product, data=requested_data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                    response['data'] = {'ProductList': serializer.data}
                    response['error'] = None
                    response['message'] = f"Update Successful"
                    response['status_code'] = status.HTTP_200_OK
            else:
                return Response({"message": f"book with id: {pid} was not found" }, status=status.HTTP_404_NOT_FOUND)
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

    def delete(self, request, pid):
        response={
            'status_code': status.HTTP_400_BAD_REQUEST,
            'message': 'Bad Request',
            'data': None,
            'error': None,
            'timestamp': datetime.now()
        }
        try:
            product = self.get_object(pid)
            if product:
                product.delete()
                response['error'] = None
                response['message'] = f"Delete Successful"
                response['status_code'] = status.HTTP_204_NO_CONTENT
            else:
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
        return Response(serializer.data)
