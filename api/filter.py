import uuid
from collections import defaultdict
from bson.binary import Binary as uuidBinary
from beanie.odm.queries.find import FindQuery
from fastapi_filter.base.filter import BaseFilterModel
from pydantic import field_validator, ValidationInfo
from typing import Any



class Filter(BaseFilterModel, extra='allow'):
    """Beanie ODM filter class.

    Provides the interface for filtering and ordering.

    Support base and nested document ordering for simple fields
    with values as:

    - string and any type based on string
    - integer
    - float
    - boolean

    WARNING: Related models ordering and filtering are not supported!!!

    # Filtering

    Nested filtering could provided as string of concatenated filed names and
    '__' as separator in between.

    ## Filter config example:
        class ArticlesFilter(Filter):
            article__title__in: Optional[str]

    ## Query string examples:
        >>> "?article__title__in=Noons,canabis"

        >>> "?article__title=Noons"
        >>> "?article__title__ilike=Noons"

    To shortenize search criteria variable name there is possible to use alias,
    but there recommended to avoid set any other params to Field object

    ## Filter config example:
        class ArticlesFilter(Filter):
            article__title__in: Optional[str] = Field(alias='title_in')

    ## Query string examples:
        >>> "?title_in=Noons,canabis"

    # Ordering

    Nested fields ordering could provided as string of concatenated filed
    names and '__' as separator in between

    ## Query string examples:

        >>> "?order_by=-created_at"
        >>> "?order_by=created_at,updated_at"
        >>> "?order_by=+created_at,-name"
        >>> "?order_by=created_at,articles__updated_at"
    """

    _operators = [
        'neq',
        'gt',
        'gte',
        'isnull',
        'lt',
        'lte',
        'not',
        'ne',
        'in',
        'not_in',
        'nin',
        'like',
        'ilike'
    ]

    def sort(self, query: FindQuery) -> FindQuery:
        if not self.ordering_values:
            return query
        # swap __ into mongodb . notation
        return query.sort(*[ordering_value.replace('__', '.')
                            for ordering_value
                            in self.ordering_values])

    @field_validator("*", mode='before')
    @classmethod
    def split_str(cls, value: Any, info: ValidationInfo):
        if (
            info.field_name == cls.Constants.ordering_field_name
            or info.field_name.endswith("__in")
            or info.field_name.endswith("__nin")
        ) and isinstance(value, str):
            return [v for v in value.split(",")]
        return value

    # TODO[pydantic]: check order field validation!!!!
    @field_validator("*", mode='before')
    @classmethod
    def validate_order_by(cls, value: Any, info: ValidationInfo):
        if info.field_name != cls.Constants.ordering_field_name:
            return value

        if not value:
            return None

        field_name_usages = defaultdict(list)
        duplicated_field_names = set()

        for field_name_with_direction in value:
            field_name = field_name_with_direction.replace(
                "-", "").replace("+", "")
            # NOTE: nested data fields stay nit validated until we find way
            # to validate them recursively
            try:
                field_name = field_name.split('__')[0]
            except Exception:
                raise ValueError(f"{field_name} first part of complex sorting is not a valid ordering field.")  # noqa
            if not hasattr(cls.Constants.model, field_name):
                raise ValueError(
                    f"{field_name} is not a valid ordering field.")

            field_name_usages[field_name].append(field_name_with_direction)
            if len(field_name_usages[field_name]) > 1:
                duplicated_field_names.add(field_name)

        if duplicated_field_names:
            ambiguous_field_names = ", ".join(
                [
                    field_name_with_direction
                    for field_name in sorted(duplicated_field_names)
                    for field_name_with_direction in field_name_usages[field_name]  # noqa
                ]
            )
            raise ValueError(
                f"Field names can appear at most once for {cls.Constants.ordering_field_name}."  # noqa
                f"The following was ambiguous: {ambiguous_field_names}."
            )

        return value

    def filter(self, query: FindQuery) -> FindQuery:
        for field_name, value in self.filtering_fields:
            field_value = getattr(self, field_name)
            if isinstance(field_value, Filter):
                # TODO: maybe sometime we add support for linked Beanie models
                continue
                # if not field_value.model_dump(exclude_none=True, exclude_unset=True): # noqa
                #    continue
                # print(field_value.Constants.model.objects())
                # query = query.find({field_name: {"$in": field_value.filter(
                #    field_value.Constants.model.objects())}})
            else:
                if field_name.endswith("__isnull"):
                    field_name = field_name.replace("__isnull", "")
                    if value is False:
                        field_name = f"{field_name}__ne"
                    value = None

                if field_name == self.Constants.search_field_name and hasattr(
                        self.Constants, "search_model_fields"):
                    search_filter = []
                    for search_field in self.Constants.search_model_fields:
                        '''
                        # TODO: maybe fulltext search detection possible or
                        direct customization in Filter class
                        search_filter.append({search_field: {
                            "$text": {
                                "$search": value,
                                "$caseSensitive": False,
                                "$diacriticSensitive": False
                            }
                        }})
                        '''
                        search_field = search_field.replace('__', '.')
                        search_filter.append({search_field: {"$regex": value,
                                                             "$options": "i"}})
                    query.find({"$or": search_filter})
                else:
                    field_chunks = field_name.split("__")
                    if field_chunks[-1] in self._operators:
                        operator = field_chunks.pop()
                        if operator in ['in', 'not_in', 'nin']:
                            if isinstance(value, str):
                                value = value.split(",")
                            else:
                                value = [value]
                        # TODO: maybe add detection for id type UUID or str
                        if field_chunks[-1] == 'id':
                            value = [uuidBinary.from_uuid(
                                        item if isinstance(item, uuid.UUID)
                                        else uuid.UUID(item))
                                    for item in value]
                            field_chunks[-1] = ('_id'
                                    if len(field_chunks) == 1
                                    else '$id')
                        query_dict = {".".join(
                            field_chunks): {f"${operator}": value}}
                        # Override query dict for specific operators
                        if operator == 'like':
                            query_dict = {".".join(field_chunks): {
                                "$regex": value,
                                "$options": "i"}}
                        if operator == 'ilike':
                            query_dict = {".".join(
                                field_chunks): {"$regex": value}}
                    else:
                        if field_chunks[-1] == 'id':
                            # TODO: maybe add detection for id type UUID or str
                            value = uuidBinary.from_uuid(
                                        value if isinstance(value, uuid.UUID)
                                        else uuid.UUID(value))
                            field_chunks[-1] = ('_id'
                                    if len(field_chunks) == 1
                                    else '$id')
                        query_dict = {".".join(field_chunks): value}
                    query.find(query_dict)
        return query
