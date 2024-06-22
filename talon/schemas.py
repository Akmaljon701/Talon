from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from talon.serializers import BranchGetSerializer, OrganizationGetSerializer, TalonCreateSerializer, \
    TalonUpdateSerializer
from utils.responses import response_schema

get_branches_schema = extend_schema(
    request=None,
    responses=BranchGetSerializer,
    summary="Get branches",
)

get_organizations_schema = extend_schema(
    request=None,
    responses=OrganizationGetSerializer,
    summary="Get organizations",
    parameters=[
        OpenApiParameter(name='branch', required=True, type=OpenApiTypes.STR,
                         enum=[
                             'Тошкент РЖУ',
                             'Қўқон РЖУ',
                             'Бухоро РЖУ',
                             'Қарши РЖУ',
                             'Термиз РЖУ',
                             'Қўнғирот РЖУ'
                         ]),
    ]
)

create_talon_schema = extend_schema(
    summary="Create talon",
    request=TalonCreateSerializer,
    responses=response_schema
)

update_talon_schema = extend_schema(
    summary="Update Talon",
    request=TalonUpdateSerializer,
    responses=response_schema,
    parameters=[
        OpenApiParameter(name='pk', description='Talon ID', required=True, type=OpenApiTypes.INT),
    ]
)

get_talons_1_2_schema = extend_schema(
    summary="Get talons",
    responses=None,
    parameters=[
        OpenApiParameter(name='from_date', description='from_date', required=False, type=OpenApiTypes.DATE),
        OpenApiParameter(name='to_date', description='to_date', required=False, type=OpenApiTypes.DATE),
    ]
)
