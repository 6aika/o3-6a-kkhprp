from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _


class Service(models.Model):
    jurisdictions = models.ManyToManyField("Jurisdiction", related_name="services")
    service_code = models.CharField(unique=True, null=False, max_length=120)
    service_name = models.CharField(max_length=120, blank=False)
    description = models.TextField(blank=True)
    metadata = models.BooleanField(default=False)
    type = models.CharField(
        max_length=140,
        default="realtime",
        choices=[
            ("realtime", _("Realtime")),
            ("batch", _("Batch")),
            ("blackbox", _("Black Box")),
        ]
    )
    keywords = models.TextField(blank=True)
    group = models.CharField(max_length=140, blank=True, default="")