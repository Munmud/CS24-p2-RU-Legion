from rest_framework import serializers
from .models import TrainUser, Station, Train, Stop, Wallet, Route


class TrainUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainUser
        fields = '__all__'

class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = '__all__'

class StopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stop
        fields = ['station_id', 'arrival_time', 'departure_time', 'fare']

class WalletSerializer(serializers.ModelSerializer):
    wallet_user = TrainUserSerializer()
    class Meta:
        model = Wallet
        fields = '__all__'

    def create(self, validated_data):
        # Extracting nested data for wallet_user
        wallet_user = validated_data.pop('wallet_user')
        user = TrainUser.objects.get(user_id = wallet_user["user_id"])
        # Create Wallet instance with associated TrainUser
        wallet = Wallet.objects.create(wallet_user=user, **validated_data)
        return wallet

class TrainSerializer(serializers.ModelSerializer):
    stops = StopSerializer(many=True)

    class Meta:
        model = Train
        fields = ['train_id', 'train_name', 'capacity', 'stops']
    
    def create(self, validated_data):
        stops_data = validated_data.pop('stops')
        train = Train.objects.create(**validated_data)
        for i in range(len(stops_data)):
            if (i == 0): continue
            print(stops_data[i-1])
            print(stops_data[i])
            route = Route.objects.create(
                from_station = stops_data[i-1]['station_id'],
                to_station = stops_data[i]['station_id'],
                fare = stops_data[i]['fare'],
                train = train,
                start_time = stops_data[i-1]['departure_time'],
                end_time = stops_data[i]['arrival_time']
            )
        for stop_data in stops_data:
            Stop.objects.create(train=train, **stop_data)
        return train

# # class RecipeSerializer(serializers.ModelSerializer):
#     """Serialize a recipe"""
#     ingredients = serializers.PrimaryKeyRelatedField(
#         many=True,
#         queryset=Ingredient.objects.all()
#     )
#     tags = serializers.PrimaryKeyRelatedField(
#         many=True,
#         queryset=Tag.objects.all()
#     )

#     class Meta:
#         model = Train
#         fields = (
#             'id', 'title', 'ingredients', 'tags', 'time_minutes',
#             'price', 'link'
#         )
#         read_only_fields = ('id',)

