# Standard Library
from datetime import datetime, timezone

# 3rd-Party
import graphene
from graphene import relay
from graphene_django import DjangoObjectType

# Project
from backend.filters import PasteBinFilterFields
from pastes.models import MTMTags, PasteBin, PasteTag

# Local
from ..models import PasteBin  # noqa: F811
from .nodes import PasteTagNode, TotalCount, TotalRatingNode


class ActivePasteBin(DjangoObjectType, TotalRatingNode):
    id = graphene.ID(source='pk', required=True)
    tags = graphene.List(PasteTagNode)

    class Meta:
        model = PasteBin
        filter_fields = PasteBinFilterFields
        interfaces = (relay.Node,)
        connection_class = TotalCount

    def resolve_tags(self, info):  # type: ignore
        tag_ids = MTMTags.objects.filter(paste_id=self.id)
        tags = []
        for ids in tag_ids:
            tags.append(PasteTag.objects.filter(id=ids.tag_id).last())
        return tags

    @classmethod
    def get_queryset(cls, queryset, info):  # type: ignore
        active = queryset.filter(
            date_of_expiry__gte=datetime.now().replace(tzinfo=timezone.utc)
        )
        return active
