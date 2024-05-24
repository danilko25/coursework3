from django.urls import reverse
from rest_framework import status
from gymadmin.models import User, Subscription, Visit
from gymadmin.serializers import SubscriptionSerializer
from django.test import TransactionTestCase


class UserTests(TransactionTestCase):
    reset_sequences = True

    def test_all_users(self):
        user = User.objects.create_superuser(email='test@gmail.com', first_name="test_first_name", last_name="test_last_name", password='testpassword')
        user = User.objects.create_user(email='second@gmail.com', first_name="sec", last_name="ond", password='testtest')
        response = self.client.get(reverse("users"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["users"]), 2)

    def test_create_user(self):
        url = reverse("register")
        data = {"email": "creation@gmil.com", "first_name": "creationfirst", "last_name": "creationlast", "password": "create"}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().id, 1)
        self.assertEqual(User.objects.get().first_name, data["first_name"])
        self.assertEqual(User.objects.get().last_name, data["last_name"])


    def test_get_user(self):
        url = reverse("users", kwargs={"pk": 1})
        user = User.objects.create_superuser(email='test@gmail.com', first_name="test_first_name", last_name="test_last_name", password='testpassword')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get().email, response.data["user"]["email"])
        self.assertEqual(User.objects.get().first_name, response.data["user"]["first_name"])
        self.assertEqual(User.objects.get().last_name, response.data["user"]["last_name"])

    def test_fail_get_user(self):
        url = reverse("users", kwargs={"pk": 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_user(self):
        user = User.objects.create_superuser(email='test@gmail.com', first_name="test_first_name", last_name="test_last_name", password='testpassword')
        url = reverse("users", kwargs={"pk": 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get(reverse("users"))
        self.assertEqual(len(response.data["users"]), 0)

    def test_fail_delete_subscription(self):
        url = reverse("users", kwargs={"pk": 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class SubscriptionTests(TransactionTestCase):
    reset_sequences = True

    def test_end_date_validator(self):
        data = {"user_id": 4, "start_date": "2025-01-01", "end_date": "2023-02-02", "price": 9500, "type": "sport"}
        serializer = SubscriptionSerializer(data=data)
        self.assertEqual(serializer.is_valid(), False)

    def test_all_subscriptions(self):
        user = User.objects.create_superuser(email='test@gmail.com', first_name="test_first_name", last_name="test_last_name", password='testpassword')
        subscription = Subscription.objects.create(user_id=1,start_date="2023-01-01",end_date="2024-01-01",price=10000,type="sport")
        response = self.client.get(reverse("subscriptions"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["subscriptions"]), 1)

    def test_create_subscription(self):
        url = reverse("subscriptions")
        user = User.objects.create_superuser(email='test@gmail.com', first_name="test_first_name", last_name="test_last_name", password='testpassword')
        data = {"user_id": 1, "start_date": "2022-01-01", "end_date": "2023-02-02", "price": 9500, "type": "sport"}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Subscription.objects.count(), 1)
        self.assertEqual(Subscription.objects.get().user.id, data["user_id"])
        self.assertEqual(Subscription.objects.get().start_date.strftime("%Y-%m-%d"), data["start_date"])
        self.assertEqual(Subscription.objects.get().end_date.strftime("%Y-%m-%d"), data["end_date"])
        self.assertEqual(Subscription.objects.get().price, data["price"])
        self.assertEqual(Subscription.objects.get().type, data["type"])

    def test_get_subscription(self):
        url = reverse("subscriptions", kwargs={"pk": 1})
        user = User.objects.create_superuser(email='test@gmail.com', first_name="test_first_name", last_name="test_last_name", password='testpassword')
        subscription = Subscription.objects.create(user_id=1,start_date="2023-01-01",end_date="2024-01-01",price=10000,type="sport")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Subscription.objects.get().user.id, response.data["subscription"]["user_id"])
        self.assertEqual(Subscription.objects.get().start_date.strftime("%Y-%m-%d"), response.data["subscription"]["start_date"])
        self.assertEqual(Subscription.objects.get().end_date.strftime("%Y-%m-%d"), response.data["subscription"]["end_date"])
        self.assertEqual(Subscription.objects.get().price, response.data["subscription"]["price"])
        self.assertEqual(Subscription.objects.get().type, response.data["subscription"]["type"])

    def test_fail_get_subscription(self):
        url = reverse("subscriptions", kwargs={"pk": 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_subscription(self):
        user = User.objects.create_superuser(email='test@gmail.com', first_name="test_first_name", last_name="test_last_name", password='testpassword')
        subscription = Subscription.objects.create(user_id=1,start_date="2023-01-01",end_date="2024-01-01",price=10000,type="sport")
        url = reverse("subscriptions", kwargs={"pk": 1})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(reverse("subscriptions"))
        self.assertEqual(len(response.data["subscriptions"]), 0)

    def test_fail_delete_subscription(self):
        url = reverse("subscriptions", kwargs={"pk": 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class VisitTests(TransactionTestCase):
    reset_sequences = True

    def test_get_visits_of_particular_subscription(self):
        user = User.objects.create_superuser(email='test@gmail.com', first_name="test_first_name", last_name="test_last_name", password='testpassword')
        user = User.objects.create_user(email='second@gmail.com', first_name="sec", last_name="ond", password='testpassword')
        subscription = Subscription.objects.create(user_id=1, start_date="2023-01-01", end_date="2024-01-01", price=10000, type="sport")
        subscription = Subscription.objects.create(user_id=2, start_date="2023-01-01", end_date="2024-01-01", price=10000, type="sport")
        visit = Visit.objects.create(subscription_id=1, date="2023-02-02")
        visit = Visit.objects.create(subscription_id=2, date="2023-02-03")
        visit = Visit.objects.create(subscription_id=1, date="2025-05-05")
        url = reverse("subscription-visits", kwargs={"pk": 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["visits"]), 2)

    def test_all_visits(self):
        user = User.objects.create_superuser(email='test@gmail.com', first_name="test_first_name", last_name="test_last_name", password='testpassword')
        subscription = Subscription.objects.create(user_id=1,start_date="2023-01-01",end_date="2024-01-01",price=10000,type="sport")
        visit = Visit.objects.create(subscription_id=1, date="2023-02-02")
        visit = Visit.objects.create(subscription_id=1, date="2023-02-03")

        response = self.client.get(reverse("visits"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["visits"]), 2)

    def test_create_visit(self):
        url = reverse("visits")
        user = User.objects.create_superuser(email='test@gmail.com', first_name="test_first_name", last_name="test_last_name", password='testpassword')
        subscription = Subscription.objects.create(user_id=1,start_date="2023-01-01",end_date="2024-01-01",price=10000,type="sport")
        data={"subscription_id":1, "date":"2023-02-02"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Visit.objects.count(), 1)
        self.assertEqual(Visit.objects.get().subscription.id, data["subscription_id"])
        self.assertEqual(Visit.objects.get().date.strftime("%Y-%m-%d"), data["date"])

    def test_get_visit(self):
        url = reverse("visits", kwargs={"pk": 1})
        user = User.objects.create_superuser(email='test@gmail.com', first_name="test_first_name", last_name="test_last_name", password='testpassword')
        subscription = Subscription.objects.create(user_id=1,start_date="2023-01-01",end_date="2024-01-01",price=10000,type="sport")
        visit = Visit.objects.create(subscription_id=1, date="2023-02-02")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Visit.objects.get().subscription.id, response.data["visit"]["subscription_id"])
        self.assertEqual(Visit.objects.get().date.strftime("%Y-%m-%d"), response.data["visit"]["date"])

    def test_fail_get_visit(self):
        url = reverse("visits", kwargs={"pk": 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_subscription(self):
        user = User.objects.create_superuser(email='test@gmail.com', first_name="test_first_name", last_name="test_last_name", password='testpassword')
        subscription = Subscription.objects.create(user_id=1,start_date="2023-01-01",end_date="2024-01-01",price=10000,type="sport")
        visit = Visit.objects.create(subscription_id=1, date="2023-02-02")
        url = reverse("visits", kwargs={"pk": 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get(reverse("visits"))
        self.assertEqual(len(response.data["visits"]), 0)

    def test_fail_delete_subscription(self):
        url = reverse("visits", kwargs={"pk": 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

