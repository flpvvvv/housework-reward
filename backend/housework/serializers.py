from rest_framework import serializers
from .models import HouseworkRecord, Contributor

class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ['id', 'name']

class HouseworkRecordSerializer(serializers.ModelSerializer):
    contributor_name = serializers.CharField(write_only=True)
    contributor = ContributorSerializer(read_only=True)
    image = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = HouseworkRecord
        fields = ['id', 'contributor', 'contributor_name', 'record_time', 'points', 'note', 'image']

    def create(self, validated_data):
        contributor_name = validated_data.pop('contributor_name')
        contributor, _ = Contributor.objects.get_or_create(name=contributor_name)
        return HouseworkRecord.objects.create(contributor=contributor, **validated_data)

    def update(self, instance, validated_data):
        if 'contributor_name' in validated_data:
            contributor_name = validated_data.pop('contributor_name')
            contributor, _ = Contributor.objects.get_or_create(name=contributor_name)
            instance.contributor = contributor
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance
