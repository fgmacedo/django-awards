from .internals import badges
from .base import Badge, BadgeDetail, BadgeAwarded  # NOQA

__version__ = '0.1.0'

default_app_config = 'awards.apps.AwardsConfig'


possibly_award_badge = badges.possibly_award_badge
