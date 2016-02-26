from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import fromstr
from django.contrib.gis.measure import D
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .models import Feedback
from .serializers import FeedbackSerializer


# TODO: move from view to other place
def get_feedbacks(service_codes, service_request_ids,
                  start_date, end_date,
                  statuses, description,
                  service_object_type, service_object_id,
                  updated_after, updated_before,
                  lat, lon, radius,
                  order_by):
    queryset = Feedback.objects.all()
    if service_request_ids:
        queryset = queryset.filter(service_request_id__in=service_request_ids.split(','))
    if service_codes:
        queryset = queryset.filter(service_code__in=service_codes.split(','))
    if start_date:
        queryset = queryset.filter(requested_datetime__gt=start_date)
    if end_date:
        queryset = queryset.filter(requested_datetime__lt=end_date)
    if statuses:
        queryset = queryset.filter(status__in=statuses.split(','))

    # start CitySDK Helsinki specific filtration
    if description:
        queryset = queryset.filter(description__icontains=description)
    if service_object_type:
        queryset = queryset.filter(service_object_type__icontains=service_object_type)
    if service_object_id:
        queryset = queryset.filter(service_object_id=service_object_id)
    if updated_after:
        queryset = queryset.filter(updated_datetime__gt=updated_after)
    if updated_before:
        queryset = queryset.filter(updated_datetime__lt=updated_before)

    if lat and lon and radius:
        point = fromstr('SRID=4326;POINT(%s %s)' % (lon, lat))
        queryset = Feedback.objects.annotate(distance=Distance('location', point)) \
            .filter(location__distance_lte=(point, D(m=radius)))

    # end CitySDK Helsinki specific filtration

    if order_by:
        queryset = queryset.order_by(order_by)

    return queryset


class FeedbackViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """

    def list(self, request):
        service_object_id = request.query_params.get('service_object_id', None)
        service_object_type = request.query_params.get('service_object_type', None)

        if service_object_id is not None and service_object_type is None:
            raise ValidationError(
                    "If service_object_id is included in the request, then service_object_type must be included.")

        queryset = get_feedbacks(
                service_request_ids=request.query_params.get('service_request_id', None),
                service_codes=request.query_params.get('service_code', None),
                start_date=request.query_params.get('start_date', None),
                end_date=request.query_params.get('end_date', None),
                statuses=request.query_params.get('status', None),
                service_object_type=service_object_type,
                service_object_id=service_object_id,
                lat=request.query_params.get('lat', None),
                lon=request.query_params.get('long', None),
                radius=request.query_params.get('radius', None),
                updated_after=request.query_params.get('updated_after', None),
                updated_before=request.query_params.get('updated_before', None),
                description=request.query_params.get('description', None),
                order_by=request.query_params.get('order_by', None)
        )

        serializer = FeedbackSerializer(queryset, many=True,
                                        context={'extensions': request.query_params.get('extensions', 'false')})
        return Response(serializer.data)
