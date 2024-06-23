from datetime import datetime
from django.db.models import Sum
from utils.responses import success
from .models import Talon, Branch, Organization
from .schemas import get_talons_1_2_schema, get_branches_schema, get_organizations_schema, create_talon_schema, \
    update_talon_schema
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import BranchGetSerializer, OrganizationGetSerializer, TalonCreateSerializer, TalonUpdateSerializer


@get_branches_schema
@api_view(['GET'])
def get_branches(request):
    branches = Branch.objects.all()
    serializer = BranchGetSerializer(branches, many=True)
    return Response(serializer.data, 200)


@get_organizations_schema
@api_view(['GET'])
def get_organizations(request):
    branch = request.query_params.get('branch')
    organizations = Organization.objects.filter(branch__name=branch).all()
    serializer = OrganizationGetSerializer(organizations, many=True)
    return Response(serializer.data, 200)


@create_talon_schema
@api_view(['POST'])
def create_talon(request):
    serializer = TalonCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return success


@update_talon_schema
@api_view(['PUT'])
def update_talon(request):
    pk = request.query_params.get('pk')
    talon = Talon.objects.get(id=pk)
    serializer = TalonUpdateSerializer(talon, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return success


@get_talons_1_2_schema
@api_view(['GET'])
def get_talons_1_2(request):
    from_date = request.query_params.get('from_date')
    to_date = request.query_params.get('to_date')
    if from_date and to_date:
        try:
            from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
            to_date = datetime.strptime(to_date, '%Y-%m-%d').date()
        except ValueError:
            return Response({'detail': 'from_date and to_date date format is wrong!'}, status=422)

        if from_date > to_date:
            return Response({'detail': 'from_date must be less than to_date!'}, status=422)

        talons = Talon.objects.filter(date__range=[from_date, to_date])
        text = f"{from_date} - {to_date}"
    else:
        today = datetime.now().date()
        start_of_month = today.replace(day=1)
        talons = Talon.objects.filter(date__range=[start_of_month, today])
        text = f'{start_of_month} - {today}'

    branches = [
        'Тошкент РЖУ',
        'Қўқон РЖУ',
        'Бухоро РЖУ',
        'Қарши РЖУ',
        'Термиз РЖУ',
        'Қўнғирот РЖУ'
    ]

    table1_data = {}
    table2_data = {}

    for branch in branches:
        # Talonlarni hisoblash
        talons_1 = talons.filter(branch__name=branch, talon_number__contains='1').count()
        talons_2 = talons.filter(branch__name=branch, talon_number__contains='2').count()
        talons_3 = talons.filter(branch__name=branch, talon_number__contains='3').count()
        jami = talons_1 + talons_2 + talons_3

        # branch uchun jadval1 ma'lumotlari
        table1_data[branch] = {
            '1': talons_1,
            '2': talons_2,
            '3': talons_3,
            'jami': jami
        }

        # branch uchun jadval2 ma'lumotlari
        summa = talons.filter(branch__name=branch).aggregate(Sum('consequence_amount'))['consequence_amount__sum']
        table2_data[branch] = summa if summa is not None else 0

    return Response({
        'text': text,
        'table1': table1_data,
        'table2': table2_data
    }, status=200)
