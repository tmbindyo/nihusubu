import re

from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.db.models import Q
from django.db.models.query import QuerySet
from django.utils.translation import gettext_lazy as _
from graphql.type.definition import GraphQLResolveInfo
from graphql_jwt.utils import get_payload, get_user_by_payload
from guardian.shortcuts import assign_perm
from typing import Any, Iterable, Tuple, Union

User = settings.AUTH_USER_MODEL


def return_paginator(
    queryset: Union[QuerySet, list],
    page: int,
    per_page: int,
    paginated_graphql_type: Any,
    **kwargs,
) -> Tuple[int, int, bool, bool, int, Any]:
    """
    Helper function that provides for an easy implementation of pagination
    using built-in Django pagination functions.
    Used in query resolvers.
    Inspired by:
    https://gist.github.com/Khongchai/a8c90b6735474d33e13ccb9b98c7c32f

    Parameters:
    queryset : django.db.models.query.QuerySet or list, required
        A Django queryset or a list.
    page : int, required
        The desired page number. Set to 0 to fetch all records.
    per_page : int, required
        The number of items to show per page.
    paginated_graphql_type: graphene.ObjectType, required
        The desired paginated GraphQL object.

    Returns:
    tuple
        A tuple made up of
            - the current page
            - the number of pages
            - has next page
            - has previous page
            - total number of objects in the queryset
            - objects
    """

    pagination_obj = Paginator(queryset, per_page)

    try:
        page_obj = pagination_obj.page(page)
    except PageNotAnInteger:
        # Should the page parameter passed not be an integer, fetch the first page
        page_obj = pagination_obj.page(1)
    except EmptyPage:
        # Should the fetched page be empty, fetch the last page (num_pages)
        page_obj = pagination_obj.page(pagination_obj.num_pages)

    if page == 0:
        return paginated_graphql_type(
            page=1,
            pages=1,
            total=len(queryset),
            next_page=None,
            previous_page=None,
            has_next=False,
            has_previous=False,
            objects=queryset,
            **kwargs,
        )

    else:
        return paginated_graphql_type(
            page=page_obj.number,
            pages=pagination_obj.num_pages,
            total=len(queryset),
            next_page=page_obj.number + 1 if page_obj.has_next() else None,
            previous_page=page_obj.number - 1
            if page_obj.has_previous()
            else None,
            has_next=page_obj.has_next(),
            has_previous=page_obj.has_previous(),
            objects=page_obj.object_list,
            **kwargs,
        )


def return_authenticated_user(resolver_info: GraphQLResolveInfo) -> User:
    """
    Helper function that returns the database record of the
    currently-authenticated user.

    Parameters:
    resolver_info: GraphQLResolveInfo, required
        Collection of information passed to a resolver.
    
    Returns:
    User:
        The instance of User that's currently authenticated.
    
    Raises:
    AttributeError:
        Raised when user is not authenticated or auth header is missing.
    graphql_jwt.exceptions.JSONWebTokenExpired
        Raised when token has expired.
    graphql_jwt.exceptions.JSONWebTokenError
        Raised when an error is encountered decoding the signature or
        the user has been deactivated.
    """

    # Handle cases where this function is called when the user is
    # not authenticated.
    auth_header = resolver_info.context.META.get("HTTP_AUTHORIZATION", None)
    if not auth_header:
        raise AttributeError(_("User not authenticated"))
    
    # Fetch the user's Authorization header and split at the space to
    # separate Bearer from the actual token.
    bearer, auth_token = (auth_header.split(" "))

    # Use a built-in Django GraphQL JWT function to generate a payload
    user_payload = get_payload(auth_token, resolver_info.context)

    # Use another built-in Django GraphQL JWT function to retrieve the user
    user = get_user_by_payload(user_payload)

    return user


def return_config_constant_tuple(
    tuple_id: Union[int, str], config_constant: Tuple
) -> Tuple:
    """
    Helper function that returns a single tuple with ID `tuple_id`
    from a `config_constant`.

    Usage:
    ---
    ```
    CONST_A = settings.CONST_A

    return_config_constant_tuple(1, CONST_A)
    ```
    """

    tuple_instance = None
    for obj in config_constant:
        if tuple_id == obj[0]:
            tuple_instance = obj

    return tuple_instance


def return_config_constant_tuple_name(
    tuple_id: Union[int, str], config_constant: Tuple
) -> str:
    """
    Helper function that returns the name of a single tuple in
    a `config_constant`.
    """

    if not tuple_id:
        return None
    else:
        return return_config_constant_tuple(tuple_id, config_constant)[1]


def return_qs_multiple(qs: QuerySet):
    """
    Helper function that returns the results of a query for multiple records
    and handles the caching of the results of the query.
    """

    def _return_qs(qs: QuerySet) -> QuerySet:
        return qs.all()
    
    return _return_qs(qs)

def return_qs_single(qs: QuerySet):
    """
    Helper function that returns the results of a query for a single record
    and handles the caching of the results of the query.
    """

    def _return_qs(qs: QuerySet) -> QuerySet:
        return qs.first()

    return _return_qs(qs)


def return_model_perms(model: models.Model) -> list:
    """
    Helper function that returns all permissions available for a model.

    Parameters
    ---
    model: models.Model, required
        Model for which to fetch permissions.
    """

    from django.contrib.auth.models import Permission

    perm_qs = Permission.objects.filter(
        content_type__app_label=model._meta.app_label,
        content_type__model=model._meta.model_name
    ).all()

    model_perms = [
        f"{model._meta.app_label}.{single.codename}"
        for single in perm_qs
    ]

    return model_perms


def assign_model_perms(model: models.Model, assignee, obj, perms : Iterable = None):
    """
    Helper function that assigns all `obj` permissions to an `assignee`, 
    who is either a user or a role.

    Parameters
    ---
    model: models.Model, required
        Model for which to fetch permissions.
    assignee: User | Role, required
        The user or role to assign permissions.
    obj: required
        Instance to which permissions are associated.
    perms: Iterable, optional
        Permissions to assign.
        Defaults to all available model permissions.
    """

    if not perms:
        perms = return_model_perms(model)
    
    for perm in perms:
        assign_perm(perm, assignee, obj)


def normalise_query_string(
    query_string: str,
    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
    normspace=re.compile(r"\s{2,}").sub,
):
    """
    Splits the query string in invidual keywords, getting rid of unecessary spaces
    and grouping quoted words together.
    Copied as-is from:
    https://www.julienphalip.com/blog/adding-search-to-a-django-site-in-a-snap/
    """

    return [
        normspace(" ", (t[0] or t[1]).strip()) for t in findterms(query_string)
    ]


def or_get_query(query_string: str, search_fields: list):
    """
    Returns a query that is a combination of Q objects. That combination
    aims to search keywords within a model by testing the given search fields.
    """

    query = None
    terms = normalise_query_string(query_string)
    
    # Check if the value of `search_fields` is either a list or a tuple.
    # If so, then only a list of fields has been provided.
    if isinstance(search_fields, tuple) or isinstance(search_fields, list):
        sub_keys = False
    # If not, then a list of fields and a corresponding list of lookups has
    # been provided.
    elif isinstance(search_fields, dict):
        sub_keys = True

    for term in terms:
        or_query = None
        
        for field_name in search_fields:
            # If there are multiple lookups, get all of them.
            if sub_keys:
                lookups = search_fields.get(field_name)
            # Otherwise, default to `icontains`
            else:
                lookups = ["icontains"]
            
            for lookup in lookups:
                q = Q(**{f"{field_name}__{lookup}": term})
                if or_query is None:
                    or_query = q
                else:
                    or_query = or_query | q
        
        if query is None:
            query = or_query
        else:
            query = query | or_query

    return query
