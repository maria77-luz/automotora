from datetime import date
from decimal import Decimal, InvalidOperation

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.shortcuts import render, redirect, get_object_or_404

from .models import Vehiculo


def inicio(request):
    return render(request, 'vehiculos/inicio.html')


def validar_datos(request):
    marca = request.POST.get('marca', '').strip()
    modelo = request.POST.get('modelo', '').strip()
    descripcion = request.POST.get('descripcion', '').strip()
    imagen_url = request.POST.get('imagen_url', '').strip()

    if not marca or not modelo:
        return None, "La marca y el modelo son obligatorios."

    try:
        anio = int(request.POST.get('anio', ''))
        if anio < 1886 or anio > date.today().year:
            return None, "El año del vehículo no es válido."
    except (ValueError, TypeError):
        return None, "El año debe ser un número válido."

    try:
        precio = Decimal(request.POST.get('precio', ''))
        if precio <= 0:
            return None, "El precio debe ser mayor que cero."
        if precio != precio.to_integral_value():
            return None, "El precio debe ser un número entero."
        if precio > Decimal('999999999999'):
            return None, "El precio supera el máximo permitido."
    except (InvalidOperation, ValueError, TypeError):
        return None, "Ingresa un precio válido."

    try:
        kilometraje = int(request.POST.get('kilometraje', ''))
        if kilometraje < 0:
            return None, "El kilometraje no puede ser negativo."
    except (ValueError, TypeError):
        return None, "El kilometraje debe ser un número válido."

    if imagen_url:
        try:
            URLValidator()(imagen_url)
        except ValidationError:
            return None, "La URL de la imagen no es válida."

    datos = {
        'marca': marca,
        'modelo': modelo,
        'anio': anio,
        'precio': precio,
        'kilometraje': kilometraje,
        'descripcion': descripcion,
        'imagen_url': imagen_url,
        'disponible': request.POST.get('disponible') == 'on'
    }

    return datos, None


def lista_vehiculos(request):
    vehiculos = Vehiculo.objects.all()

    return render(request, 'vehiculos/lista_vehiculos.html', {
        'vehiculos': vehiculos
    })


def crear_vehiculo(request):
    if request.method == 'POST':
        datos, error = validar_datos(request)

        if error:
            return render(request, 'vehiculos/crear.html', {
                'error': error
            })

        Vehiculo.objects.create(**datos)

        return redirect('lista_vehiculos')

    return render(request, 'vehiculos/crear.html')


def detalle_vehiculo(request, pk):
    vehiculo = get_object_or_404(Vehiculo, pk=pk)

    return render(request, 'vehiculos/detalle.html', {
        'vehiculo': vehiculo
    })


def editar_vehiculo(request, pk):
    vehiculo = get_object_or_404(Vehiculo, pk=pk)

    if request.method == 'POST':
        datos, error = validar_datos(request)

        if error:
            return render(request, 'vehiculos/editar.html', {
                'vehiculo': vehiculo,
                'error': error
            })

        for campo, valor in datos.items():
            setattr(vehiculo, campo, valor)

        vehiculo.save()

        return redirect('detalle_vehiculo', pk=vehiculo.pk)

    return render(request, 'vehiculos/editar.html', {
        'vehiculo': vehiculo
    })


def eliminar_vehiculo(request, pk):
    vehiculo = get_object_or_404(Vehiculo, pk=pk)

    if request.method == 'POST':
        vehiculo.delete()
        return redirect('lista_vehiculos')

    return render(request, 'vehiculos/eliminar.html', {
        'vehiculo': vehiculo
    })