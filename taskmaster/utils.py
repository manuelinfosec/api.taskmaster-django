import uuid
from typing import Type

from django.core.paginator import EmptyPage, Paginator
from django.db import models
from django.http import Http404
from rest_framework import exceptions, status
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework_simplejwt.tokens import RefreshToken


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


def paginate_queryset(
    request,
    queryset,
    serializer_class: Type[Serializer],
    page: int,
    page_size: int = 10,
) -> Response:
    # Handle the 'page' parameter with a default value of 1
    try:
        page_number = int(page)
    except (TypeError, ValueError):
        page_number = 1
    paginator = Paginator(queryset, page_size)  # Set page_size per page here

    try:
        paginated_data = paginator.page(page_number)
    except EmptyPage:
        raise Http404("No items found on this page")

    serializer = serializer_class(paginated_data, many=True).data

    next_page_number = (
        paginated_data.next_page_number() if paginated_data.has_next() else None
    )
    if next_page_number:
        current_path = request.path
        next_url = f"{current_path}?page={next_page_number}"
        full_next_url = request.build_absolute_uri(next_url)
    else:
        full_next_url = None

    prev_page_number = (
        paginated_data.previous_page_number() if paginated_data.has_previous() else None
    )
    if prev_page_number:
        current_path = request.path
        prev_url = f"{current_path}?page={prev_page_number}"
        full_prev_url = request.build_absolute_uri(prev_url)
    else:
        full_prev_url = None

    # Include "next" and "previous" URLs at the top of the serialized data
    serializer_data = {
        "count": len(queryset),
        "previous": full_prev_url,
        "next": full_next_url,
        "results": serializer,
    }

    return Response(serializer_data)


def remove_none_values(obj):
    """Remove none values from dict/list"""

    if isinstance(obj, dict):
        return {k: remove_none_values(v) for k, v in obj.items() if v is not None}
    elif isinstance(obj, list):
        return [remove_none_values(v) for v in obj if v is not None]
    else:
        return obj


def get_object_or_error(model, **kwargs):
    """
    Retrieve a single object from the database based on given filter criteria,
    or raise appropriate error if the object is not found or multiple objects are found.

    Args:
        model: The Django model class from which to retrieve the object.
        **kwargs: Keyword arguments representing the filter criteria.

    Returns:
        The retrieved object if found.

    Raises:
        NotFound: If the object matching the filter criteria does not exist.
        ValidationError: If multiple objects are found matching the filter criteria.
        Exception: Any other unexpected error that may occur during the retrieval process.
                   Note: It's generally not recommended to catch generic Exception,
                   but this is done here to ensure that any unexpected errors are properly raised.

    Examples:
        >>> user = get_object_or_error(User, username='john_doe')
        >>> task = get_object_or_error(Task, id=42)
    """
    try:
        # Attempt to retrieve a single object based on the provided filter criteria
        return model.objects.get(**kwargs)
    except model.DoesNotExist as error:
        # If no object is found matching the criteria, raise NotFound error
        raise exceptions.NotFound(detail=f"{model.__name__} not found") from error
    except model.MultipleObjectsReturned as error:
        # If multiple objects are found matching the criteria, raise ValidationError
        raise exceptions.ValidationError(
            detail=f"{model.__name__} has multiple objects",
            code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        ) from error
    except Exception as error:
        # If any other unexpected error occurs, raise the original error
        raise error


def generate_user_tokens(user):
    """Generate JWT token to authenticate a user."""

    refresh = RefreshToken.for_user(user)
    return {"access": str(refresh.access_token), "refresh": str(refresh)}
