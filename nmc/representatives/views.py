from django.shortcuts import render, redirect
from .models import Representative, Ward, Position, County
from .forms import RepresentativeForm, CountyForm, WardForm
from django.http import HttpResponse
from django.http import JsonResponse
from django.db.models import Prefetch
from itertools import groupby
from operator import attrgetter
import csv


def index(request):
    return render(request, 'index.html')


def noveu(request):
    return render(request, 'noveu.html')


def add_representative(request):
    if request.method == 'POST':
        form = RepresentativeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = RepresentativeForm()
    return render(request, 'add_representative.html', {'form': form, 'counties': County.objects.all()})


def representative_list(request):
    representatives = Representative.objects.select_related('ward', 'position').order_by('ward__name', 'name')
    grouped_representatives = {}
    for ward, group in groupby(representatives, key=attrgetter('ward')):
        grouped_representatives[ward] = list(group)
    return render(request, 'representative_list.html', {'grouped_representatives': grouped_representatives})


def representative_table(request):
    representatives = Representative.objects.all()
    return render(request, 'representative_table.html', {'representatives': representatives})


def edit_positions(request):
    positions = Position.objects.all()
    if request.method == 'POST':
        new_position = request.POST.get('new_position')
        if new_position:
            Position.objects.create(title=new_position)
        positions_to_delete = request.POST.getlist('positions_to_delete')
        Position.objects.filter(id__in=positions_to_delete).delete()
    return render(request, 'edit_positions.html', {'positions': positions})


def export_representatives_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="representatives.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Ward', 'Position', 'Phone Number', 'ID Number'])

    representatives = Representative.objects.all()
    for representative in representatives:
        writer.writerow(
            [representative.name, representative.ward.name, representative.position.title, representative.phone_number,
             representative.id_number])

    return response


def export_representatives_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="representatives.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Ward', 'Position', 'Phone Number', 'ID Number'])

    representatives = Representative.objects.all()
    for representative in representatives:
        writer.writerow(
            [representative.name, representative.ward.name, representative.position.title, representative.phone_number,
             representative.id_number])

    return response


def get_wards(request, county_id):
    wards = Ward.objects.filter(county_id=county_id).values('id', 'name')
    return JsonResponse(list(wards), safe=False)


def manage_counties(request):
    counties = County.objects.all()
    if request.method == 'POST':
        form = CountyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_counties')
    else:
        form = CountyForm()
    return render(request, 'manage_counties.html', {'counties': counties, 'form': form})


def manage_wards(request, county_id):
    county = County.objects.get(id=county_id)
    wards = Ward.objects.filter(county=county)
    if request.method == 'POST':
        form = WardForm(request.POST)
        if form.is_valid():
            ward = form.save(commit=False)
            ward.county = county
            ward.save()
            return redirect('manage_wards', county_id=county.id)
    else:
        form = WardForm()
    return render(request, 'manage_wards.html', {'wards': wards, 'form': form, 'county': county})
