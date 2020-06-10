from rest_framework.serializers import Serializer, CharField, DecimalField, FloatField


class GeoPointSerializer(Serializer):
    lat1 = FloatField(required=True, max_value=90.0, min_value=-90.0)
    lat2 = FloatField(required=True, max_value=90.0, min_value=-90.0)
    lng1 = FloatField(required=True, max_value=180.0, min_value=-180.0)
    lng2 = FloatField(required=True, max_value=180.0, min_value=-180.0)


class DistanceSerializer(Serializer):
    start = CharField(required=True)
    end = CharField(required=True)
    kilometers = DecimalField(required=True, decimal_places=2, max_digits=7)
    miles = DecimalField(required=True, decimal_places=2, max_digits=7)
