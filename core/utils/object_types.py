import graphene

from django.db import models
from django.db.models import QuerySet
from graphene.types.objecttype import ObjectTypeOptions
from typing import Union


class PaginatedObjectTypeOptions(ObjectTypeOptions):
    """
    Attributes that can be passed in the metaclass of any object types that
    subclass `PaginatedObjectType`.
    """

    objects = None

    filter_fields = ()


class PaginatedObjectType(graphene.ObjectType):
    """
    Custom object type that adds support for pagination to an ObjectType.

    Meta class options:
    ---
    objects: `graphene.ObjectType`, required
        Object type to be returned in `objects` query field.
    filter_fields: `tuple` | `dict`, optional
        The fields evaluated when a value is provided for `search_keyword` in
        a query.
        When a tuple of fields is provided, the query defaults to `icontains`
        for the provided fields.  
        When a dict is provided, one can specify the fields and the lookup.
        https://docs.djangoproject.com/en/5.0/ref/models/querysets/#field-lookups
        
        Example Usage:
        ```python
        filter_fields = ("name", "email",)

        filter_fields = {
            "name": ["icontains", "istartswith",],
            "email: ["contains"],
        }
        ```
    """

    page = graphene.Int(
        description="The current page number. Set to 0 to view all records."
    )
    pages = graphene.Int(description="The number of pages.")
    total = graphene.Int(description="The total number of records.")
    next_page = graphene.Int(description="The next page number.")
    previous_page = graphene.Int(description="The previous page number.")
    has_next = graphene.Boolean(
        description="Boolean indicating whether a next page exists."
    )
    has_previous = graphene.Boolean(
        description="Boolean indicating whether a previous page exists."
    )

    @classmethod
    def __init_subclass_with_meta__(
        cls,
        objects: Union[graphene.ObjectType, str] = None,
        filter_fields: Union[tuple, dict] = (),
        interfaces=(),
        possible_types=(),
        default_resolver=None,
        _meta=None,
        **options,
    ):
        if not objects:
            raise AttributeError(
                f"Metaclass attribute objects not defined in {cls.__name__}"
            )
        
        # While not explicitly mounted as a class attribute above,
        # we mount the `objects` field and set its type here.
        cls.objects = graphene.List(objects)
        
        # If no value for `_meta` is passed, init `PaginatedObjectTypeOptions`
        # with the current instance of `cls`.
        # To modify the Meta attributes available, add them as class values
        # to `PaginatedObjectTypeOptions` above
        if not _meta:
            _meta = PaginatedObjectTypeOptions(cls)

        _meta.objects = objects
        _meta.filter_fields = filter_fields

        return super().__init_subclass_with_meta__(
            interfaces=interfaces,
            possible_types=possible_types,
            default_resolver=default_resolver,
            _meta=_meta,
            **options,
        )

    @classmethod
    def get_objects(cls) -> graphene.ObjectType:
        """
        Get the ObjectType that is returned in the `objects` field.
        """

        return cls._meta.objects

    @classmethod
    def get_model(cls) -> models.Model:
        """
        Get the object model.
        """
        
        obj = cls.get_objects()

        # Validation of the model isn't necessary here since it is taken care
        # of at the point of defining the base object type.
        return obj._meta.model
    
    @classmethod
    def get_queryset(cls) -> Union[QuerySet, list]:
        """
        The list of items to be returned.
        """

        _Model = cls.get_model()

        qs = _Model.objects
        
        return qs
