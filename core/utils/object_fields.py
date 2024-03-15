import functools
import graphene
import importlib

from django.db import models
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _
from graphql.error import GraphQLError
from uuid import UUID

from .helper_functions import (
    return_paginator,
    return_authenticated_user,
    return_qs_multiple,
    return_qs_single,
    or_get_query,
)


class SingleObjectField(graphene.Field):
    """
    Implementation of `graphene.Field` to be used in when returning a
    single database record.
    
    When using this field type, there is no need to specify a resolver method.
    """

    def __init__(
            self,
            type_,
            args=None,
            resolver=None,
            source=None,
            deprecation_reason=None,
            name=None,
            description=None,
            required=False,
            _creation_counter=None,
            default_value=None,
            login_required: bool =False,
            permissions: tuple =(),
            check_obj_perms: bool =False,
            **extra_args
        ):
            """
            Implementation of `graphene.Field` to be used in place of `ListField`
            objects that return database records.
            
            When using this field type, there is no need to specify a resolver method.

            Parameters:
            ---
            In addition to the default graphene.Field parameters, you can pass the following.

            login_required: `bool`, optional
                Indicates whether field can be queried while unauthenticated.  
                Default `false`
            permissions: `tuple` | `list`, optional
                Permissions required to query the field.  
            check_obj_perms: `bool`, optional
                Indicates whether to check if user has `permissions`on record.  
                Default: `false`
            """

            if not login_required and check_obj_perms:
                raise AttributeError(
                    "check_obj_perms requires that login_required be True in"
                    f" ListObjectField({type_})"
                )

            self.login_required = login_required
            self.permissions = permissions
            self.check_obj_perms = check_obj_perms
            
            # If the value passed is a string, try and import it.
            if isinstance(type_, str):
                path_to_class = type_.split(".")
                classname = path_to_class[len(path_to_class) - 1]
                _mod_path = type_.replace(f".{classname}", "")

                mod = importlib.import_module(_mod_path)
                type_ = getattr(mod, classname)
            
            self.model = type_._meta.model
            
            super().__init__(
                type_,
                args,
                resolver,
                source,
                deprecation_reason,
                name,
                description,
                required,
                _creation_counter,
                default_value,
                **extra_args
            )

    def get_model(self) -> models.Model:
        """
        Get the object model.
        """

        return self.model
    
    def get_queryset(self, pk):
        """
        The list of items to be returned.
        """

        _Model = self.get_model()

        qs = _Model.objects.filter(pk=pk)

        return qs

    
    def resolve_object(self, *info, **kwargs):
        _user = None
        login_required = self.login_required
        permissions = self.permissions
        check_obj_perms = self.check_obj_perms

        # Is login required?
        if login_required:
            # If the user is not authenticated or the token has expired,
            # the following will raise an exception.
            _user = return_authenticated_user(info[1])
        
        pk = kwargs.get("id")
        
        qs = self.get_queryset(pk)
        
        # Required permissions
        if _user:
            # Is check_obj_perms?
            if check_obj_perms:
                if not _user.has_perms(permissions, qs):
                    raise GraphQLError(
                        _("Not permitted to make this query on this object.")
                    )

            if permissions:
                if not _user.has_perms(permissions):
                    raise GraphQLError(_("Not permitted to make this query."))

        return return_qs_single(qs)
    
    def wrap_resolve(self, parent_resolver):
        if isinstance(parent_resolver, functools.partial):
            parent_resolver = self.resolve_object

        return super().wrap_resolve(parent_resolver)



class ListObjectField(graphene.Field):
    """
    Implementation of `graphene.Field` to be used in place of `ListField`
    objects that return database records.
    
    When using this field type, there is no need to specify a resolver method.
    """

    def __init__(
            self,
            type_,
            args=None,
            resolver=None,
            source=None,
            deprecation_reason=None,
            name=None,
            description=None,
            required=False,
            _creation_counter=None,
            default_value=None,
            login_required: bool =False,
            permissions: tuple =(),
            user_objects: bool =False,
            qs=None,
            **extra_args
        ):
            """
            Implementation of `graphene.Field` to be used in place of `ListField`
            objects that return database records.
            
            When using this field type, there is no need to specify a resolver method.

            Parameters:
            ---
            In addition to the default graphene.Field parameters, you can pass the following.

            login_required: `bool`, optional
                Indicates whether field can be queried while unauthenticated.  
                Default `false`
            permissions: `tuple` | `list`, optional
                Permissions required to query the field.  
            user_objects: `bool`, optional
                Indicates whether to limit objects returned to objects a user
                has access to.  
                Default: `false`
            qs: `QuerySet` | `function`, optional
                A queryset or callable function that returns the database 
                objects to display.
            """

            if not login_required and user_objects:
                raise AttributeError(
                    "user_objects requires that login_required be True in"
                    f" ListObjectField({type_})"
                )
            
            if user_objects:
                # Check if the manager has the `get_user_objects` method.
                if not hasattr(type_._meta.model.objects, "get_user_objects"):
                    raise AttributeError(
                        f"Cannot query user objects on model {type_._meta.model.__name__}. "
                        "Does its manager have the get_user_objects() method?"
                    )
            
            self.login_required = login_required
            self.permissions = permissions
            self.user_objects = user_objects
            self.qs = qs

            # If the value passed is a string, try and import it.
            if isinstance(type_, str):
                path_to_class = type_.split(".")
                classname = path_to_class[len(path_to_class) - 1]
                _mod_path = type_.replace(f".{classname}", "")

                mod = importlib.import_module(_mod_path)
                type_ = getattr(mod, classname)
            
            self.model = type_._meta.model

            type_ = graphene.List(type_)
            
            super().__init__(
                type_,
                args,
                resolver,
                source,
                deprecation_reason,
                name,
                description,
                required,
                _creation_counter,
                default_value,
                **extra_args
            )

    def get_model(self) -> models.Model:
        """
        Get the object model.
        """

        return self.model
    
    def get_queryset(self):
        """
        The list of items to be returned.
        """

        _Model = self.get_model()

        qs = _Model.objects

        return qs

    
    def resolve_objects(self, *info, **kwargs):
        _user = None
        login_required = self.login_required
        permissions = self.permissions
        user_objects = self.user_objects
        queryset = self.qs

        if queryset:
            if not callable(queryset) and not isinstance(queryset, QuerySet):
                raise AttributeError(
                    "qs must be a callable function or instance of "
                    "django.db.models.query.QuerySet in "
                    f"ListObjectField {self._type}"
                )

        # Is login required?
        if login_required:
            # If the user is not authenticated or the token has expired,
            # the following will raise an exception.
            _user = return_authenticated_user(info[1])
        
        # Required permissions
        if _user and permissions:
            if not _user.has_perms(permissions):
                raise GraphQLError(_("Not permitted to make this query."))

        if queryset:
            if callable(queryset):
                qs = queryset()
            elif isinstance(queryset, QuerySet):
                qs = queryset
        else:
            qs = self.get_queryset()

        # Is user_objects?
        if user_objects:
            qs = qs.get_user_objects(_user)

        return return_qs_multiple(qs)
    
    def wrap_resolve(self, parent_resolver):
        if isinstance(parent_resolver, functools.partial):
            parent_resolver = self.resolve_objects

        return super().wrap_resolve(parent_resolver)


class PaginatedObjectField(graphene.Field):
    """
    Implementation of `graphene.Field` to be used with paginated records.

    When using this field type, there is no need to specify a resolver method.
    However, should you choose to, it would look like:

    ```python
    def resolve_records(self, info, page, per_page, search_keyword):
        pass
    ```
    """

    def __init__(
            self,
            type_,
            args=None,
            resolver=None,
            source=None,
            deprecation_reason=None,
            name=None,
            description=None,
            required=False,
            _creation_counter=None,
            default_value=None,
            login_required: bool =False,
            permissions: tuple =(),
            user_objects: bool =False,
            qs=None,
            **extra_args,
        ):
        """
        Implementation of `graphene.Field` to be used with paginated records.
        
        When using this field type, there is no need to specify a resolver method.
        However, should you choose to, it would look like:

        ```python
        def resolve_records(self, info, page, per_page, search_keyword):
            pass
        ```

        Parameters:
        ---
        In addition to the default graphene.Field parameters, you can pass
        the following.

        login_required: `bool`, optional
            Indicates whether field can be queried while unauthenticated.  
            Default `false`
        permissions: `tuple` | `list`, optional
            Permissions required to query the field.  
        user_objects: `bool`, optional
            Indicates whether to limit objects returned to objects a user
            has access to.  
            Default: `false`
        qs: `QuerySet` | `function`, optional
            A queryset or callable function that returns the database 
            objects to display.
        """
        
        extra_args["page"] = graphene.Int(
            default_value=1,
            description="Page to retrieve. Set to 0 to fetch all. Default: 1",
        )
        extra_args["per_page"] = graphene.Int(
            default_value=30,
            description="Number of records per page. Default: 30"
        )
        extra_args["search_keyword"] = graphene.String(
            required=False,
            default_value=None,
            description="Desired term/phrase to search by."
        )

        if not login_required and user_objects:
            raise AttributeError(
                "user_objects requires that login_required be True in"
                f" ListObjectField({type_})"
            )
        
        if user_objects:
            # Check if the manager has the `get_user_objects` method.
            if not hasattr(
                type_._meta.objects._meta.model.objects, "get_user_objects"
            ):
                raise AttributeError(
                    "Cannot query user objects on model "
                    f"{type_._meta.objects._meta.model.objects}. "
                    "Does its manager have the get_user_objects() method?"
                )
        
        self.login_required = login_required
        self.permissions = permissions
        self.user_objects = user_objects
        self.qs = qs
        
        super().__init__(
            type_,
            args,
            resolver,
            source,
            deprecation_reason,
            name,
            description,
            required,
            _creation_counter,
            default_value,
            **extra_args
        )

    def get_lookups(self, search_keyword):
        filter_fields = self.type._meta.filter_fields

        return or_get_query(search_keyword, filter_fields)
    
    def resolve_objects(self, *info, **kwargs):
        _user = None
        login_required = self.login_required
        permissions = self.permissions
        user_objects = self.user_objects
        queryset = self.qs
        search_keyword = kwargs.get("search_keyword")

        if queryset:
            if not callable(queryset) and not isinstance(queryset, QuerySet):
                raise AttributeError(
                    "qs must be a callable function or instance of "
                    "django.db.models.query.QuerySet in "
                    f"PaginatedObjectField {self._type}"
                )

        # Is login required?
        if login_required:
            # If the user is not authenticated or the token has expired,
            # the following will raise an exception.
            _user = return_authenticated_user(info[1])
        
        # Required permissions
        if _user and permissions:
            if not _user.has_perms(permissions):
                raise GraphQLError(_("Not permitted to make this query."))

        if queryset:
            if callable(queryset):
                qs = queryset()
            elif isinstance(queryset, QuerySet):
                qs = queryset
        else:
            qs = self.type.get_queryset()

        # Is user_objects?
        if user_objects:
            qs = qs.get_user_objects(_user)
        
        if search_keyword:
            filter_statements = self.get_lookups(search_keyword)
            qs = qs.filter(filter_statements)

        return return_paginator(
            queryset=return_qs_multiple(qs),
            page=kwargs.get("page"),
            per_page=kwargs.get("per_page"),
            paginated_graphql_type=self.type,
        )
    
    def wrap_resolve(self, parent_resolver):
        if isinstance(parent_resolver, functools.partial):
            parent_resolver = self.resolve_objects

        return super().wrap_resolve(parent_resolver)
