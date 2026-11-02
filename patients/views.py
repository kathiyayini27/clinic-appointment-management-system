
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Patient, Appointment
from .forms import PatientForm, AppointmentForm
from .models import Patient, Appointment, Doctor
from .forms import PatientForm, AppointmentForm, DoctorForm

@login_required
def dashboard(request):

    total_patients = Patient.objects.count()
    total_appointments = Appointment.objects.count()

    pending_appointments = Appointment.objects.filter(status='Pending').count()
    confirmed_appointments = Appointment.objects.filter(status='Confirmed').count()
    completed_appointments = Appointment.objects.filter(status='Completed').count()
    cancelled_appointments = Appointment.objects.filter(status='Cancelled').count()

    today_appointments = Appointment.objects.filter(
        appointment_date=timezone.localdate()
    ).count()

    return render(request, 'patients/dashboard.html', {
        'total_patients': total_patients,
        'total_appointments': total_appointments,
        'pending_appointments': pending_appointments,
        'confirmed_appointments': confirmed_appointments,
        'completed_appointments': completed_appointments,
        'cancelled_appointments': cancelled_appointments,
        'today_appointments': today_appointments,
    })


@login_required
def patient_list(request):

    search = request.GET.get('search', '')

    patients = Patient.objects.all().order_by('-id')

    if search:
        patients = patients.filter(name__icontains=search)

    return render(request, 'patients/patient_list.html', {
        'patients': patients,
        'search': search,
    })


@login_required
def add_patient(request):

    if request.method == 'POST':
        form = PatientForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('patient_list')
    else:
        form = PatientForm()

    return render(request, 'patients/add_patient.html', {
        'form': form
    })


@login_required
def edit_patient(request, id):

    patient = get_object_or_404(Patient, id=id)

    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)

        if form.is_valid():
            form.save()
            return redirect('patient_list')
    else:
        form = PatientForm(instance=patient)

    return render(request, 'patients/edit_patient.html', {
        'form': form,
        'patient': patient,
    })


@login_required
def delete_patient(request, id):

    patient = get_object_or_404(Patient, id=id)

    if request.method == 'POST':
        patient.delete()
        return redirect('patient_list')

    return redirect('patient_list')


@login_required
def appointment_list(request):

    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')
        status = request.POST.get('status')

        appointment = get_object_or_404(Appointment, id=appointment_id)

        if status in ['Pending', 'Confirmed', 'Completed', 'Cancelled']:
            appointment.status = status
            appointment.save()

        return redirect('appointment_list')

    search = request.GET.get('search', '')
    doctor = request.GET.get('doctor', '')
    date = request.GET.get('date', '')

    appointments = Appointment.objects.select_related(
        'patient'
    ).all().order_by('-appointment_date')

    if search:
        appointments = appointments.filter(
            patient__name__icontains=search
        )

    if doctor:
        appointments = appointments.filter(
            doctor_name__icontains=doctor
        )

    if date:
        appointments = appointments.filter(
            appointment_date=date
        )

    return render(request, 'patients/appointment_list.html', {
        'appointments': appointments,
        'search': search,
        'doctor': doctor,
        'date': date,
    })


@login_required
def add_appointment(request):

    if request.method == 'POST':
        form = AppointmentForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('appointment_list')
    else:
        form = AppointmentForm()

    return render(request, 'patients/add_appointment.html', {
        'form': form
    })


@login_required
def edit_appointment(request, id):

    appointment = get_object_or_404(Appointment, id=id)

    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)

        if form.is_valid():
            form.save()
            return redirect('appointment_list')
    else:
        form = AppointmentForm(instance=appointment)

    return render(request, 'patients/edit_appointment.html', {
        'form': form,
        'appointment': appointment,
    })


@login_required
def delete_appointment(request, id):

    appointment = get_object_or_404(Appointment, id=id)

    if request.method == 'POST':
        appointment.delete()

    return redirect('appointment_list')


@login_required
def patient_detail(request, id):

    patient = get_object_or_404(Patient, id=id)

    appointments = Appointment.objects.filter(
        patient=patient
    ).order_by('-appointment_date')

    return render(request, 'patients/patient_detail.html', {
        'patient': patient,
        'appointments': appointments,
    })

@login_required
def appointment_detail(request, id):
    appointment = get_object_or_404(
        Appointment.objects.select_related('patient'),
        id=id
    )

    return render(request, 'patients/appointment_detail.html', {
        'appointment': appointment,
    })

@login_required
def doctor_list(request):
    doctors = Doctor.objects.all().order_by('-id')

    return render(request, 'patients/doctor_list.html', {
        'doctors': doctors
    })


@login_required
def add_doctor(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('doctor_list')
    else:
        form = DoctorForm()

    return render(request, 'patients/add_doctor.html', {
        'form': form
    })

@login_required
def edit_doctor(request, id):
    doctor = get_object_or_404(Doctor, id=id)

    if request.method == 'POST':
        form = DoctorForm(request.POST, instance=doctor)

        if form.is_valid():
            form.save()
            return redirect('doctor_list')
    else:
        form = DoctorForm(instance=doctor)

    return render(request, 'patients/edit_doctor.html', {
        'form': form,
        'doctor': doctor,
    })


@login_required
def delete_doctor(request, id):
    doctor = get_object_or_404(Doctor, id=id)

    if request.method == 'POST':
        doctor.delete()

    return redirect('doctor_list')
