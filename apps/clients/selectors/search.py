from dataclasses import dataclass

from django.db import models
from django.db.models import OuterRef, Subquery
from django.db.models.expressions import RawSQL

from apps.clients.selectors import sql
from apps.dash import models as dash_model
from apps.dash.models import managers


@dataclass
class SearchSelector:
    j_manager: managers.JourneyManager

    def get_search(self):
        return self.j_manager.select_related("route", "route__node").annotate(
            where_to=models.F("route__node__town"),
            j_class=self.get_cls_name(),
            j_class_id=self.get_cls_id(),
            total_price=self.get_total_price(),
            where_from=RawSQL("SELECT town  FROM dash_covercity WHERE id = 2",
                              params=[],
                              output_field=models.CharField()
                              )
        )

    def ptt(self, name: str = "adult"):
        """ prix toutes taxe confondu """
        return models.F(name) * ((models.F("taxe") / 100) + 1)

    def f_total_price(self, adult: int = 1, child: int = 0, inf: int = 0):
        return (
            models.F("tp_ad") * adult
        ) + (models.F("tp_chd") * child) + (models.F("tp_inf") * inf)

    def get_total_price(self, *args, **kwargs):
        return Subquery(
            queryset=self.get_cls().annotate(
                tp_ad=self.ptt(),
                tp_chd=self.ptt("child"),
                tp_inf=self.ptt("baby")
            ).annotate(
                total_price=self.f_total_price(*args, **kwargs)
            ).values("total_price"),
            output_field=models.FloatField()
        )

    def get_cls(self):
        return dash_model.JourneyTarif.objects.filter(
            route=OuterRef("route")
        )

    def get_cls_name(self):
        return Subquery(
            queryset=self.get_cls().select_related("journey_class").annotate(
                j_class=models.F("journey_class__name")
            ).values("j_class"),
            output_field=models.CharField()
        )

    def get_cls_id(self):
        return Subquery(
            queryset=self.get_cls().values("journey_class"),
            output_field=models.IntegerField()
        )
