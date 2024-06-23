from datetime import datetime
from django.contrib.auth import logout, authenticate, login
from django.db import transaction
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.utils.dateparse import parse_date
from django.contrib import messages
from export_to_docx import create_docx_with_tables
from talon_template.forms import TalonForm
from talon.models import Talon, Branch, Organization
from django.contrib.auth.decorators import login_required


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('get_talons_1_2_3_view')  # Redirect to your main page after successful login
        else:
            error_message = "Username yoki Password noto'g'ri!"
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login_page')


@login_required
def get_talons_1_2_3_view(request):
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')

    if from_date and to_date:
        try:
            from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
            to_date = datetime.strptime(to_date, '%Y-%m-%d').date()
        except ValueError:
            return JsonResponse({'detail': 'from_date and to_date date format is wrong!'}, status=422)

        if from_date > to_date:
            return JsonResponse({'detail': 'from_date must be less than to_date!'}, status=422)

        talons = Talon.objects.filter(date__range=[from_date, to_date])
        date_range_text = f"{from_date} - {to_date}"
    else:
        today = datetime.now().date()
        start_of_month = today.replace(day=1)
        talons = Talon.objects.filter(date__range=[start_of_month, today])
        date_range_text = f'{start_of_month} - {today}'

    branches = [
        'Тошкент РЖУ',
        'Қўқон РЖУ',
        'Бухоро РЖУ',
        'Қарши РЖУ',
        'Термиз РЖУ',
        'Қунгирот РЖУ'
    ]

    table1_data = {}
    table2_data = {}

    for branch_name in branches:
        # Table 1: Count of talons 1, 2, 3 and their total
        talons_1 = talons.filter(branch__name=branch_name, talon_number__contains='1').count()
        talons_2 = talons.filter(branch__name=branch_name, talon_number__contains='2').count()
        talons_3 = talons.filter(branch__name=branch_name, talon_number__contains='3').count()
        jami = talons_1 + talons_2 + talons_3

        table1_data[branch_name.replace(' ', '_')] = {
            '1': talons_1,
            '2': talons_2,
            '3': talons_3,
            'jami': jami
        }

        # Table 2: Sum of consequence_amount for each branch
        summa = talons.filter(branch__name=branch_name).aggregate(summa=Sum('consequence_amount'))['summa'] or 0
        table2_data[branch_name.replace(' ', '_')] = summa

    table2_data['total_summa'] = sum(table2_data.values())

    # Table 3

    context = {
        'text': date_range_text,
        'table1_data': table1_data,
        'table2_data': table2_data,
        'talons': talons.all(),
        'branches': Branch.objects.all(),
    }
    return render(request, 'talons.html', context)


@login_required
def export_docx(request):
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')

    talons = Talon.objects.all()

    from_date = parse_date(from_date)
    to_date = parse_date(to_date)
    talons = talons.filter(date__range=[from_date, to_date])
    buffer = create_docx_with_tables(talons, from_date, to_date)

    response = HttpResponse(buffer,
                            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename="talon_list.docx"'

    return response


@login_required
@transaction.atomic
def talon_add(request):
    if request.method == 'POST':
        form = TalonForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Talon muvaffaqiyatli qo\'shildi.')
            return HttpResponseRedirect(reverse('get_talons_1_2_view'))
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = TalonForm()

    context = {
        'form': form,
        'branches': Branch.objects.all(),
    }
    return render(request, 'talon_add.html', context)


@login_required
@transaction.atomic
def talon_update(request, talon_id):
    talon = Talon.objects.get(id=talon_id)

    if request.method == 'POST':
        form = TalonForm(request.POST, instance=talon)
        if form.is_valid():
            form.save()
            messages.success(request, 'Talon muvaffaqiyatli yangilandi.')
            return HttpResponseRedirect(reverse('get_talons_1_2_3_view'))
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = TalonForm(instance=talon)

    context = {
        'form': form,
        'branches': Branch.objects.all(),
        'talon': talon,
    }
    return render(request, 'talon_update.html', context)


def load_organizations(request):
    branch_id = request.GET.get('branch_id')
    organizations = Organization.objects.filter(branch_id=branch_id).order_by('name')
    html_options = render_to_string('organization_options.html', {'organizations': organizations})
    return JsonResponse({'html_options': html_options})
