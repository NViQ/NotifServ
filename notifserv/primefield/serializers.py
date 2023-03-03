from rest_framework import serializers
from .models import Clients, Mailing, Messages

class ClientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clients
        fields = '__all__'

    def create(self, validated_data):
        if (len(validated_data.get('phone')) != 10):
            raise serializers.ValidationError('Wrong number...')
        # if int(validated_data.get('phone')[:3]) != validated_data.get('code_operator'):
        #     raise serializers.ValidationError('Wrong code...')
        return Clients.objects.create(**validated_data)


    def update(self, instance, validated_data):
        for i in validated_data:
            if i == 'id':
                instance.id = validated_data.get('id', instance.id)
            if i == 'phone' and (len(validated_data.get('phone')) == 10):
                instance.phone = validated_data.get('phone', instance.phone)
            if i == 'code_operator':
                if int(validated_data.get('phone')[:3]) != validated_data.get('code_operator'):
                    raise serializers.ValidationError('Wrong code...')
                instance.code_operator = validated_data.get('code_operator', instance.code_operator)
            if i == 'teg':
                instance.teg = validated_data.get('teg', instance.teg)
            if i == 'time_zone':
                instance.time_zone = validated_data.get('time_zone', instance.time_zone)
        instance.save()
        return instance


class MailingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mailing
        fields = '__all__'

    def create(self, validated_data):
        return Mailing.objects.create(**validated_data)



