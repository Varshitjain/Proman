from django import forms
from register.models import Company as Comp
from register.models import UserProfile, EmpAppraisal, SelfEval, EmpProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

appOp = (('0','NA'),('1','Inexperienced'),('2','Satisfactory'),('3','Very Competent'),('4','Outstanding'))
departments = (("0","IT"),("1","R&D"),("2","Accounting"),
    ("3","HR"),
    ("4","Management"),
    ("5","Marketing"),
    ("6","Product Management"),
    ("7","Sales"),
    ("8","Support"),
    ("9","Technical")
)

salary = (('1','Low'),('2','Medium'),('3','High'))
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(label='E-mail', required=True)
    company = forms.ModelChoiceField(queryset=Comp.objects.all())
    departments = forms.ChoiceField(choices=departments)
    salary_level = forms.ChoiceField(choices=salary)

    class Meta:
        model = User
        fields = {
            'username',
            'first_name',
            'last_name',
            'email',
            'company',
            'password1',
            'password2',
            'departments',
            'salary_level',
        }

        labels = {
            'first_name': 'Name',
            'last_name': 'Last Name',
            'company': 'Company',
        }

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        company = self.cleaned_data['company']
        departments = self.cleaned_data['departments']
        salary = self.cleaned_data['salary_level']

        if commit:
            user.save()
            user_profile = UserProfile.objects.create(user=user, company=Comp.objects.get(name=company))
            user_profile.save()
            empProfile = EmpProfile.objects.create(emp=user, departments=departments, salary_level=salary)
            empProfile.save()

        return user

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['placeholder'] = 'First name'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last name'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'E-mail'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Retype Password'
        self.fields['company'].widget.attrs['class'] = 'form-control'
        self.fields['departments'].widget.attrs['class'] = 'form-control'
        self.fields['salary_level'].widget.attrs['class'] = 'form-control'

class CompanyRegistrationForm(forms.Form):
    social_name = forms.CharField(max_length=80)
    name = forms.CharField(max_length=80)
    email = forms.EmailField()
    city = forms.CharField(max_length=50)
    found_date = forms.DateField()

    class Meta:
        model = Comp


    def save(self, commit=True):
        company = Comp()
        company.social_name = self.cleaned_data['social_name']
        company.name = self.cleaned_data['name']
        company.email = self.cleaned_data['email']
        company.city = self.cleaned_data['city']
        company.found_date = self.cleaned_data['found_date']

        if commit:
            company.save()


    def __init__(self, *args, **kwargs):
        super(CompanyRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['social_name'].widget.attrs['class'] = 'form-control'
        self.fields['social_name'].widget.attrs['placeholder'] = 'Social Name'
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['placeholder'] = 'Name'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['city'].widget.attrs['class'] = 'form-control'
        self.fields['city'].widget.attrs['placeholder'] = 'City'
        self.fields['found_date'].widget.attrs['class'] = 'form-control'
        self.fields['found_date'].widget.attrs['placeholder'] = 'Found date'

class ProfilePictureForm(forms.Form):
    img = forms.ImageField()
    class Meta:
        model = UserProfile
        fields = ['img']

    def save(self, request, commit=True):
        user = request.user.userprofile_set.first()
        user.img = self.cleaned_data['img']

        if commit:
            user.save()

        return user

    def __init__(self, *args, **kwargs):
        super(ProfilePictureForm, self).__init__(*args, **kwargs)
        self.fields['img'].widget.attrs['class'] = 'custom-file-input'
        self.fields['img'].widget.attrs['id'] = 'validatedCustomFile'

class EmpAppraisalForm(forms.ModelForm):
    emp = forms.ModelChoiceField(queryset=User.objects.all())
    job = forms.ChoiceField(choices=appOp)
    attend = forms.ChoiceField(choices=appOp)
    commu = forms.ChoiceField(choices=appOp)
    attitude = forms.ChoiceField(choices=appOp)
    comment = forms.CharField(widget=forms.Textarea)
    group_work = forms.ChoiceField(choices=appOp)
    creativity = forms.ChoiceField(choices=appOp)
    dependibility = forms.ChoiceField(choices=appOp)
    coworker_relations = forms.ChoiceField(choices=appOp)
    independent_work = forms.ChoiceField(choices=appOp)

    class Meta:
        model = EmpAppraisal
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EmpAppraisalForm, self).__init__(*args, **kwargs)
        self.fields['emp'].widget.attrs['class'] = 'form-control'
        self.fields['emp'].widget.attrs['placeholder'] = 'Employee'
        self.fields['job'].widget.attrs['class'] = 'form-control'
        self.fields['job'].widget.attrs['placeholder'] = 'Job Satisfaction'
        self.fields['attend'].widget.attrs['class'] = 'form-control'
        self.fields['attend'].widget.attrs['placeholder'] = 'Attendance'
        self.fields['commu'].widget.attrs['class'] = 'form-control'
        self.fields['commu'].widget.attrs['placeholder'] = 'Communication'
        self.fields['attitude'].widget.attrs['class'] = 'form-control'
        self.fields['attitude'].widget.attrs['placeholder'] = 'Attitude'
        self.fields['comment'].widget.attrs['class'] = 'form-control'
        self.fields['comment'].widget.attrs['placeholder'] = 'Comments'
        self.fields['group_work'].widget.attrs['class'] = 'form-control'
        self.fields['group_work'].widget.attrs['placeholder'] = 'Group Work'
        self.fields['creativity'].widget.attrs['class'] = 'form-control'
        self.fields['creativity'].widget.attrs['placeholder'] = 'Creativity'
        self.fields['dependibility'].widget.attrs['class'] = 'form-control'
        self.fields['dependibility'].widget.attrs['placeholder'] = 'Dependibility'
        self.fields['coworker_relations'].widget.attrs['class'] = 'form-control'
        self.fields['coworker_relations'].widget.attrs['placeholder'] = 'Coworker Relations'
        self.fields['independent_work'].widget.attrs['class'] = 'form-control'
        self.fields['independent_work'].widget.attrs['placeholder'] = 'Independent Work'

class SelfEvalForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all())
    technical_skills  = forms.ChoiceField(choices=appOp)
    technical_knowledge  = forms.ChoiceField(choices=appOp)
    quality_of_work = forms.ChoiceField(choices=appOp)
    productivity = forms.ChoiceField(choices=appOp)
    project_management_skills = forms.ChoiceField(choices=appOp)
    technology_skills = forms.ChoiceField(choices=appOp)
    time_management = forms.ChoiceField(choices=appOp)
    interpersonal_skills = forms.ChoiceField(choices=appOp)
    communication_skills = forms.ChoiceField(choices=appOp)
    innovation = forms.ChoiceField(choices=appOp)
    collaboration = forms.ChoiceField(choices=appOp)
    employee_policies = forms.ChoiceField(choices=appOp)
    leadership_skills = forms.ChoiceField(choices=appOp)
    professionalism = forms.ChoiceField(choices=appOp)

    class Meta:
        model = SelfEval
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(SelfEvalForm, self).__init__(*args, **kwargs)
        self.fields['user'].widget.attrs['class'] = 'form-control'
        self.fields['user'].widget.attrs['placeholder'] = 'Employee'
        self.fields['technical_skills'].widget.attrs['class'] = 'form-control'
        self.fields['technical_skills'].widget.attrs['placeholder'] = 'Technical Skills'
        self.fields['technical_knowledge'].widget.attrs['class'] = 'form-control'
        self.fields['technical_knowledge'].widget.attrs['placeholder'] = 'technical_knowledge'
        self.fields['quality_of_work'].widget.attrs['class'] = 'form-control'
        self.fields['quality_of_work'].widget.attrs['placeholder'] = 'quality_of_work'
        self.fields['productivity'].widget.attrs['class'] = 'form-control'
        self.fields['productivity'].widget.attrs['placeholder'] = 'quality_of_work'
        self.fields['project_management_skills'].widget.attrs['class'] = 'form-control'
        self.fields['project_management_skills'].widget.attrs['placeholder'] = 'quality_of_work'
        self.fields['technology_skills'].widget.attrs['class'] = 'form-control'
        self.fields['technology_skills'].widget.attrs['placeholder'] = 'quality_of_work'
        self.fields['time_management'].widget.attrs['class'] = 'form-control'
        self.fields['time_management'].widget.attrs['placeholder'] = 'quality_of_work'
        self.fields['interpersonal_skills'].widget.attrs['class'] = 'form-control'
        self.fields['interpersonal_skills'].widget.attrs['placeholder'] = 'quality_of_work'
        self.fields['communication_skills'].widget.attrs['class'] = 'form-control'
        self.fields['communication_skills'].widget.attrs['placeholder'] = 'quality_of_work'
        self.fields['innovation'].widget.attrs['class'] = 'form-control'
        self.fields['innovation'].widget.attrs['placeholder'] = 'quality_of_work'
        self.fields['collaboration'].widget.attrs['class'] = 'form-control'
        self.fields['collaboration'].widget.attrs['placeholder'] = 'quality_of_work'
        self.fields['employee_policies'].widget.attrs['class'] = 'form-control'
        self.fields['employee_policies'].widget.attrs['placeholder'] = 'quality_of_work'
        self.fields['leadership_skills'].widget.attrs['class'] = 'form-control'
        self.fields['leadership_skills'].widget.attrs['placeholder'] = 'quality_of_work'
        self.fields['professionalism'].widget.attrs['class'] = 'form-control'
        self.fields['professionalism'].widget.attrs['placeholder'] = 'quality_of_work'