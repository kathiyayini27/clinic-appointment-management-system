
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    # Patients
    path('patients/', views.patient_list, name='patient_list'),
    path('patients/<int:id>/', views.patient_detail, name='patient_detail'),
    path('add/', views.add_patient, name='add_patient'),
    path('edit/<int:id>/', views.edit_patient, name='edit_patient'),
    path('delete/<int:id>/', views.delete_patient, name='delete_patient'),

    # Appointments
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('appointments/<int:id>/', views.appointment_detail, name='appointment_detail'),
    path('appointments/add/', views.add_appointment, name='add_appointment'),
    path('appointments/edit/<int:id>/', views.edit_appointment, name='edit_appointment'),
    path('appointments/delete/<int:id>/', views.delete_appointment, name='delete_appointment'),

    # Doctors
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('doctors/add/', views.add_doctor, name='add_doctor'),
    path('doctors/edit/<int:id>/', views.edit_doctor, name='edit_doctor'),
    path('doctors/delete/<int:id>/', views.delete_doctor, name='delete_doctor'),
]
