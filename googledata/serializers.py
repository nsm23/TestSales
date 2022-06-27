from rest_framework import serializers

from googledata.models import NumbersModel


class NumbersSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        sale = NumbersModel.objects.update_or_create(
            order=validated_data.get("order", None),
            defaults={
                "cost_usd": validated_data.get("cost_usd"),
                "cost_rub": validated_data.get("cost_rub"),
                "delivery_date": validated_data.get("delivery_date"),
            }
        )

        return sale

    class Meta:
        model = NumbersModel
        fields = ("order", "cost_usd", "cost_rub", "delivery_date")

