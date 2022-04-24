# Standard Library

# 3rd-Party
import graphene
from graphene import relay
from graphene_django import DjangoObjectType

# Project
from backend.filters import PasteBinFilterFields
from pastes.models import Attachment, PasteBin


class PasteBinNode(DjangoObjectType):
    id = graphene.ID(source='pk', required=True)

    class Meta:
        model = PasteBin
        filter_fields = PasteBinFilterFields
        interfaces = (relay.Node,)
        exclude = ("attachment_token",)

    total_rating = graphene.Int()

    def resolve_total_rating(self, info: dict) -> int:  # type: ignore
        return self.get_total_rating()


class AttachmentNode(DjangoObjectType):
    id = graphene.ID(source='pk', required=True)
    url = graphene.String()

    def resolve_url(root, info, **kwargs) -> str:  # type: ignore
        return f"http://{info.context.META['HTTP_HOST']}{root.image.url}"

    class Meta:
        model = Attachment
        interfaces = (relay.Node,)
        exclude = ("paste",)
