from datetime import timezone

from django.db.models import Count, Q
from django.http import Http404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import response, status
from rest_framework.response import Response
from rest_framework.views import APIView
from gymadmin.models import Subscription, Visit, User
from gymadmin.serializers import UserSerializer, SubscriptionSerializer, VisitSerializer


class RegisterUser(APIView):

    @swagger_auto_schema(operation_description="Register a new user", request_body=UserSerializer, responses={
        201: openapi.Response("Created user", UserSerializer),
        400: 'Bad Request. Invalid input or missing required fields.',
    })
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'user': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserList(APIView):

    @swagger_auto_schema(operation_description="Get a list of users with filter", responses={
        200: openapi.Response("List of users", UserSerializer(many=True))
    })

    def get(self, request):
         users = User.objects.all()
         first_name = request.query_params.get('first_name')
         if first_name:
             users = users.filter(first_name=first_name)

         last_name = request.query_params.get('last_name')
         if last_name:
             users = users.filter(last_name=last_name)

         email = request.query_params.get('email')
         if email:
             users = users.filter(email=email)
         serializer = UserSerializer(users, many=True)
         return Response({"users": serializer.data}, status.HTTP_200_OK)


class UserDetail(APIView):

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    @swagger_auto_schema(operation_description="Get details of a particular user", responses={
        200: openapi.Response("Founded user", UserSerializer),
        404: "User does not exist"
    })
    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response({'user': serializer.data}, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_description="Update details of a particular user",
                         request_body=UserSerializer, responses={
            200: openapi.Response("Updated user", UserSerializer),
            400: 'Bad Request. Invalid input or missing required fields.',
        })
    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'user': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_description="Delete a user by id", responses={
        204: "User was successfully deleted"
    })
    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubscriptionList(APIView):
    @swagger_auto_schema(operation_description="Get a list of subscriptions with filter", responses={
        200: openapi.Response("List of subscriptions", SubscriptionSerializer(many=True))
    })
    def get(self, request):
        subscriptions = Subscription.objects.select_related('client', 'type')
        type = request.query_params.get('type')
        if type:
            subscriptions = subscriptions.filter(type__title=type)
        client_id = request.query_params.get('client_id')
        if client_id:
            subscriptions = subscriptions.filter(client_id=client_id)
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return Response({"subscriptions":serializer.data}, status.HTTP_200_OK)

    @swagger_auto_schema(operation_description="Create a new subscription", request_body=SubscriptionSerializer, responses={
        201: openapi.Response("Created subscription", SubscriptionSerializer),
        400: 'Bad Request. Invalid input or missing required fields.',
    })
    def post(self, request, format=None):
        serializer = SubscriptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'subscriptions': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SubscriptionDetail(APIView):

    def get_object(self, pk):
        try:
            return Subscription.objects.get(pk=pk)
        except Subscription.DoesNotExist:
            raise Http404

    @swagger_auto_schema(operation_description="Get details of a particular subscription", responses={
        200: openapi.Response("Founded subscription", SubscriptionSerializer),
        404: "Subscription does not exist"
    })
    def get(self, request, pk, format=None):
        subscription = self.get_object(pk)
        serializer = SubscriptionSerializer(subscription)
        return Response({'subscription': serializer.data}, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_description="Update details of a particular subscription",
                         request_body=SubscriptionSerializer, responses={
            200: openapi.Response("Updated subscription", SubscriptionSerializer),
            400: 'Bad Request. Invalid input or missing required fields.',
        })
    def put(self, request, pk, format=None):
        subscription = self.get_object(pk)
        serializer = SubscriptionSerializer(subscription, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'subscription': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_description="Delete a subscription by id", responses={
        204: "Subscription was successfully deleted"
    })
    def delete(self, request, pk, format=None):
        subscription = self.get_object(pk)
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class VisitList(APIView):

    @swagger_auto_schema(operation_description="Get a list of all visits with filter", responses={
        200: openapi.Response("List of visits", VisitSerializer(many=True))
    })
    def get(self, request):
        visits = Visit.objects.select_related('subscription', 'subscription__client', 'subscription__type')

        subscription_id = request.query_params.get('subscription_id')
        if subscription_id:
            visits = visits.filter(subscription_id=subscription_id)

        date = request.query_params.get('date')
        if date:
            visits = visits.filter(date=date)

        serializer = VisitSerializer(visits, many=True)
        return Response({"visits":serializer.data}, status.HTTP_200_OK)


    @swagger_auto_schema(operation_description="Create a new visit", request_body=VisitSerializer, responses={
        201: openapi.Response("Created visit", VisitSerializer),
        400: 'Bad Request. Invalid input or missing required fields.',
    })
    def post(self, request, format=None):
        serializer = VisitSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'visits': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VisitDetail(APIView):
    def get_object(self, pk):
        try:
            return Visit.objects.get(pk=pk)
        except Visit.DoesNotExist:
            raise Http404

    @swagger_auto_schema(operation_description="Get details of a particular visit", responses={
        200: openapi.Response("Founded visit", VisitSerializer),
        404: "Visit does not exist"
    })
    def get(self, request, pk, format=None):
        visit = self.get_object(pk)
        serializer = VisitSerializer(visit)
        return Response({'visit': serializer.data}, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_description="Update details of a particular visit",
                         request_body=VisitSerializer, responses={
            200: openapi.Response("Updated visit", VisitSerializer),
            400: 'Bad Request. Invalid input or missing required fields.',
        })
    def put(self, request, pk, format=None):
        visit = self.get_object(pk)
        serializer = VisitSerializer(visit, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'visit': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_description="Delete a visit by id", responses={
        204: "Visit was successfully deleted"
    })
    def delete(self, request, pk, format=None):
        visit = self.get_object(pk)
        visit.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class VisitListForSubscription(APIView):

    @swagger_auto_schema(operation_description="Get a list of visits of particular subscription", responses={
        200: openapi.Response("List of visits of particular subscription", VisitSerializer(many=True))
    })
    def get(self, request, pk, format=None):
        visits = Visit.objects.filter(subscription=Subscription.objects.get(pk=pk))
        serializer = VisitSerializer(visits, many=True)
        return Response({'visits': serializer.data}, status=status.HTTP_200_OK)


class ApplicationStatisticsView(APIView):
    @swagger_auto_schema(
        operation_description="Get statistics including total clients, total subscriptions per type, current visits, and optionally statistics for a specified date range.",
        responses={200: openapi.Response("Statistics data")},
    )
    def get(self, request, format=None):
        total_clients = User.objects.count()
        total_subscriptions_per_type = Subscription.objects.values('type__title').annotate(count=Count('id'))
        current_visits = Visit.objects.filter(exit_time__isnull=True).count()
        start_date = self.request.query_params.get('from')
        end_date = self.request.query_params.get('to')

        if start_date:
            if not end_date:
                end_date = timezone.now().date()

            visits_in_period = Visit.objects.filter(date__range=[start_date, end_date]).count()
            subscriptions_in_period_per_type = Subscription.objects.filter(
                Q(start_date__range=[start_date, end_date]) | Q(end_date__range=[start_date, end_date])
            ).values('type__title').annotate(count=Count('id'))

            return Response({
                'total_clients': total_clients,
                'total_subscriptions_per_type': list(total_subscriptions_per_type),
                'current_visits': current_visits,

                'STATISTIC start_date': start_date,
                'STATISTIC end_date': end_date,

                'visits_in_period': visits_in_period,
                'boughtsubscriptions_in_period_per_type': list(subscriptions_in_period_per_type),
            })
        else:
            return Response({
                'total_clients': total_clients,
                'total_subscriptions_per_type': list(total_subscriptions_per_type),
                'current_visits': current_visits,
            })
