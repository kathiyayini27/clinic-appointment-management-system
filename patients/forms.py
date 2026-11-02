
from django import forms
from .models import Patient, Appointment, Doctor


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'name', 'age', 'gender', 'phone', 'email', 'address'
        ]
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }


class AppointmentForm(forms.ModelForm):

    doctor_name = forms.ChoiceField(
        choices=[],
        label="Select Doctor"
    )

    class Meta:
        model = Appointment
        fields = [
            'patient', 'doctor_name', 'appointment_date',
            'appointment_time', 'reason'
        ]
        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date'}),
            'appointment_time': forms.TimeInput(attrs={'type': 'time'}),
            'reason': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        choices = [('', 'Select Doctor')]

        for doctor in Doctor.objects.all():
            choices.append((doctor.doctor_name, doctor.doctor_name))

        if self.instance and self.instance.pk:
            old_doctor = self.instance.doctor_name

            if old_doctor and old_doctor not in dict(choices):
                choices.append((old_doctor, old_doctor))

        self.fields['doctor_name'].choices = choices


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = [
            'doctor_name', 'specialization', 'phone',
            'email', 'experience'
        ]
