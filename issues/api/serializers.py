from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.gis.geos import GEOSGeometry
from rest_framework import serializers

from issues.analysis import calc_fixing_time
from issues.models import Issue, Service, Task


class ServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Service
        fields = ['service_code', 'service_name', 'description', 'metadata', 'type', 'keywords', 'group']


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ['task_state', 'task_type', 'owner_name', 'task_modified', 'task_created']


class IssueSerializer(serializers.ModelSerializer):
    distance = serializers.SerializerMethodField()
    extended_attributes = serializers.SerializerMethodField()
    media_urls = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='media_url'
    )
    tasks = TaskSerializer(many=True)

    class Meta:
        model = Issue

    def get_distance(self, obj):
        if hasattr(obj, 'distance'):
            return int(obj.distance.m)
        else:
            return ''

    def get_extended_attributes(self, instance):

        media_urls = self.fields['media_urls']
        media_urls_value = media_urls.to_representation(
            media_urls.get_attribute(instance)
        )

        tasks = self.fields['tasks']
        tasks_value = tasks.to_representation(
            tasks.get_attribute(instance)
        )

        representation = {
            'service_object_type': instance.service_object_type,
            'service_object_id': instance.service_object_id,
            'detailed_status': instance.detailed_status,
            'title': instance.title,
            'media_urls': media_urls_value,
            'tasks': tasks_value
        }

        return representation

    def to_representation(self, instance):
        distance = self.fields['distance']
        distance_value = distance.to_representation(
            distance.get_attribute(instance)
        )

        representation = {
            'id': instance.id,
            'distance': distance_value,
            'service_request_id': instance.service_request_id,
            'status_notes': instance.status_notes,
            'status': instance.status,
            'service_code': instance.service_code,
            'service_name': instance.service_name,
            'description': instance.description,
            'agency_responsible': instance.agency_responsible,
            'service_notice': instance.service_notice,
            'requested_datetime': instance.requested_datetime,
            'updated_datetime': instance.updated_datetime,
            'expected_datetime': instance.expected_datetime,
            'address': instance.address_string,
            'lat': instance.lat,
            'long': instance.lon,
            'media_url': instance.media_url,
            'vote_counter': instance.vote_counter,
            'title': instance.title
        }

        extensions = self.context.get('extensions')
        if extensions:
            ext_attribute = self.fields['extended_attributes']
            ext_attribute_value = ext_attribute.to_representation(
                ext_attribute.get_attribute(instance)
            )
            representation['extended_attributes'] = ext_attribute_value

        return representation


class IssueDetailSerializer(serializers.ModelSerializer):
    api_key = serializers.CharField(required=True)
    service_code = serializers.IntegerField(required=True)
    description = serializers.CharField(required=True, min_length=10, max_length=5000)
    title = serializers.CharField(required=False)
    lat = serializers.FloatField(required=False)
    long = serializers.FloatField(required=False)
    service_object_type = serializers.CharField(required=False)
    service_object_id = serializers.CharField(required=False)
    address_string = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    phone = serializers.CharField(required=False)
    media_url = serializers.CharField(required=False)

    def validate(self, data):
        """
        Check location fields.
        """
        lat = data.get('lat')
        long = data.get('long')
        service_object_id = data.get('service_object_id')
        if (lat is None or long is None) and service_object_id is None:
            raise serializers.ValidationError("Currently all service types require location, "
                                              "either lat/long or service_object_id.")
        return data

    def create(self, validated_data):
        validated_data['location'] = GEOSGeometry(
            'SRID=4326;POINT(%s %s)' % (
                validated_data.pop('long', 0),
                validated_data.pop('lat', 0)
            )
        )

        fixing_time = calc_fixing_time(validated_data["service_code"])
        waiting_time = timedelta(milliseconds=fixing_time)

        if waiting_time.total_seconds() >= 0:
            validated_data['expected_datetime'] = datetime.now() + waiting_time

        if settings.SYNCHRONIZE_WITH_OPEN_311 is False:
            validated_data['status'] = 'moderation'

        issue = Issue.objects.create(**validated_data)
        issue = Issue.objects.get(pk=issue.pk)
        return issue

    class Meta:
        model = Issue
