"""
Contains common mixins that can be utilised across different apps.
"""

from .manager_mixins import (
    BasePermissionManager,
    SoftDeletionManager,
)
from .model_mixins import (
    BasePermissionMixin,
    DeletionMarkerMixin,
    HistoricalDataMixin,
    TimestampMixin,
)
