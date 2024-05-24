from rest_framework import serializers

from gymadmin.models import User, Subscription, Visit


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User(email=validated_data['email'], first_name=validated_data["first_name"], last_name=validated_data["last_name"])
        user.set_password(validated_data["password"])
        user.save()
        return user

    def update(self, instance, validated_data):
        if "last_name" in validated_data:
            instance.last_name = validated_data['last_name']
        if "first_name" in validated_data:
            instance.first_name = validated_data['first_name']
        instance.save()
        return instance

class SubscriptionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user_id = serializers.IntegerField()
    start_date = serializers.DateField()
    end_date =serializers.DateField()
    price=serializers.IntegerField()
    type=serializers.CharField()

    def validate(self, data):
        if data["start_date"] > data["end_date"]:
            raise serializers.ValidationError("End of the subscription cannot be earlier than start date.")
        else:
            return data

    def create(self, validated_data):
        return Subscription.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if "start_date" in validated_data:
            instance.start_date = validated_data['start_date']
        if "end_date" in validated_data:
            instance.first_name = validated_data['end_date']
        if "price" in validated_data:
            instance.first_name = validated_data['price']
        if "type" in validated_data:
            instance.first_name = validated_data['type']

        instance.save()
        return instance

class VisitSerializer(serializers.Serializer):
    subscription_id = serializers.PrimaryKeyRelatedField(queryset=Subscription.objects.all())
    date = serializers.DateField()
    enter_time = serializers.TimeField()
    exit_time = serializers.TimeField(allow_null=True, required=False)

    def validate(self, data):
        enter_time = data.get('enter_time')
        exit_time = data.get('exit_time')

        if exit_time and enter_time >= exit_time:
            raise serializers.ValidationError("Enter time must be before exit time")

        return data

    def create(self, validated_data):
        return Visit.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if 'subscription_id' in validated_data:
            instance.subscription_id = validated_data['subscription_id']
        if 'date' in validated_data:
            instance.date = validated_data['date']
        if 'enter_time' in validated_data:
            instance.enter_time = validated_data['enter_time']
        if 'exit_time' in validated_data:
            instance.exit_time = validated_data['exit_time']

        instance.save()
        return instance
