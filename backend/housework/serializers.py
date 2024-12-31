from rest_framework import serializers
from .models import HouseworkRecord, Contributor

class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ['id', 'name']

class HouseworkRecordSerializer(serializers.ModelSerializer):
    contributor_name = serializers.CharField(write_only=True)
    contributor = ContributorSerializer(read_only=True)
    image = serializers.FileField(required=False)

    class Meta:
        model = HouseworkRecord
        fields = ['contributor', 'contributor_name', 'scale', 'note', 'image']

    def create(self, validated_data):
        contributor_name = validated_data.pop('contributor_name')
        contributor, _ = Contributor.objects.get_or_create(name=contributor_name)
        validated_data['contributor'] = contributor
        return super().create(validated_data)
