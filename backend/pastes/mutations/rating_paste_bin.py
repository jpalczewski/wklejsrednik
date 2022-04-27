# Standard Library
import logging

# 3rd-Party
import graphene

# Project
from backend.mixins import ResultMixin

# Local
from ..models import Rating

logger = logging.getLogger(__file__)


class RatingPasteBin(graphene.relay.ClientIDMutation, ResultMixin):
    class Input:
        paste = graphene.ID()
        liked = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):  # type: ignore
        user = info.context.user
        if not user.is_authenticated:
            return RatingPasteBin(ok=False, error="User not authenticated")
        paste = input.get('paste')
        liked = input.get('liked')
        user = user.id
        rate_exists = Rating.is_unique(paste, user)
        if rate_exists:
            rate = Rating.objects.get(paste=paste, user=user)
            if rate.liked != liked:
                rate.liked = liked
                try:
                    rate.save()
                except Exception as e:
                    return RatingPasteBin(
                        ok=False, error=f"Couldn't save the rating {e}"
                    )
                else:
                    logger.debug(f'Rating saved {rate}')
                    return RatingPasteBin(ok=True, error="Rating changed")
            return RatingPasteBin(ok=False, error="Rating already exists")
        else:
            rate = Rating(liked=liked)
            rate.user_id = user
            rate.paste_id = paste
            try:
                rate.save()
            except Exception as e:
                return RatingPasteBin(ok=False, error=f"Couldn't save the rating {e}")
            else:
                return RatingPasteBin(ok=True, error="Rating created")


class RatingPasteBinID(graphene.relay.ClientIDMutation, ResultMixin):
    class Input:
        paste = graphene.ID()
        user = graphene.ID()
        liked = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):  # type: ignore
        paste = input.get('paste')
        user = input.get('user')
        liked = input.get('liked')
        rate_exists = Rating.is_unique(paste, user)
        if rate_exists:
            rate = Rating.objects.get(paste=paste, user=user)
            if rate.liked != liked:
                rate.liked = liked
                try:
                    rate.save()
                except Exception as e:
                    return RatingPasteBinID(
                        ok=False, error=f"Couldn't save the rating {e}"
                    )
                else:
                    logger.debug(f'Rating saved {rate}')
                    return RatingPasteBinID(ok=True, error="Rating changed")
            return RatingPasteBinID(ok=False, error="Rating already exists")
        else:
            rate = Rating(liked=liked)
            rate.user_id = user
            rate.paste_id = paste
            try:
                rate.save()
            except Exception as e:
                return RatingPasteBinID(ok=False, error=f"Couldn't save the rating {e}")
            else:
                return RatingPasteBinID(ok=True, error="Rating created")
