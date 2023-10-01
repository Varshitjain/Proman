from django.db import models
from django.contrib.auth.models import User
from projects.models import Project


salary = (('1','Low'),('2','Medium'),('3','High'))

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

# Create your models here.
class Company(models.Model):
    social_name = models.CharField(max_length=80)
    name = models.CharField(max_length=80)
    email = models.EmailField()
    city = models.CharField(max_length=50)

    found_date = models.DateField()

    class Meta:
        verbose_name_plural = 'Companies'
        ordering = ('name',)

    def __str__(self):
        return (self.name)

class UserProfile(models.Model):
    user    = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    project = models.ManyToManyField(Project, blank=True)
    friends = models.ManyToManyField('self', blank=True)
    img    = models.ImageField(upload_to='core/avatar', blank=True, default='core/avatar/blank_profile.png')
    age = models.IntegerField(blank=True, default=25)
    gender = models.CharField(blank=True, max_length=6, default='Male')
    joining =  models.DateField(auto_now_add=False, auto_now=True)
    depart = models

    def __str__(self):
        return (str(self.user))

    def invite(self, invite_profile):
        invite = Invite(inviter=self, invited=invite_profile)
        invites = invite_profile.received_invites.filter(inviter_id=self.id)
        if not len(invites) > 0:    # don't accept duplicated invites
            invite.save()

    def remove_friend(self, profile_id):
        friend = UserProfile.objects.filter(id=profile_id)[0]
        self.friends.remove(friend)

class WorkProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class SelfEval(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    technical_skills = models.CharField(max_length=10,choices=appOp, default=0)
    technical_knowledge  = models.CharField(max_length=10,choices=appOp, default=0)
    quality_of_work = models.CharField(max_length=10,choices=appOp, default=0)
    productivity = models.CharField(max_length=10,choices=appOp, default=0)
    project_management_skills = models.CharField(max_length=10,choices=appOp, default=0)
    technology_skills = models.CharField(max_length=10,choices=appOp, default=0)
    time_management = models.CharField(max_length=10,choices=appOp, default=0)
    interpersonal_skills = models.CharField(max_length=10,choices=appOp, default=0)
    communication_skills = models.CharField(max_length=10,choices=appOp, default=0)
    innovation = models.CharField(max_length=10,choices=appOp, default=0)
    collaboration = models.CharField(max_length=10,choices=appOp, default=0)
    employee_policies = models.CharField(max_length=10,choices=appOp, default=0)
    leadership_skills = models.CharField(max_length=10,choices=appOp, default=0)
    professionalism = models.CharField(max_length=10,choices=appOp, default=0)

class EmpProfile(models.Model):
    emp = models.ForeignKey(User, on_delete=models.CASCADE, related_name="EmpID", default=1)
    satisfaction_level = models.FloatField(null=True)
    last_evaluation = models.FloatField(null=True)
    num_projects = models.IntegerField(default=1)
    avg_monthly_hrs = models.IntegerField(default=210)
    time_spent_company = models.IntegerField(default=10)
    work_accident = models.IntegerField(default=0)
    promotion_last_5_years = models.IntegerField(default=0)
    departments = models.CharField(max_length=7, choices=departments, default=1)
    salary_level = models.CharField(max_length=7, choices=salary, default=1)

class EmpAppraisal(models.Model):
    emp = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Employee", default=1)
    job = models.CharField(max_length=7,choices=appOp, default=0)
    attend = models.CharField(max_length=7,choices=appOp, default=0)
    commu = models.CharField(max_length=7,choices=appOp, default=0)
    attitude = models.CharField(max_length=7,choices=appOp, default=0)
    group_work = models.CharField(max_length=7,choices=appOp, default=0)
    creativity = models.CharField(max_length=7,choices=appOp, default=0)
    dependibility = models.CharField(max_length=7,choices=appOp, default=0)
    coworker_relations = models.CharField(max_length=7,choices=appOp, default=0)
    independent_work = models.CharField(max_length=7,choices=appOp, default=0)
    comment = models.CharField(max_length=250, null=True)


class Invite(models.Model):
    inviter = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='made_invites')
    invited = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='received_invites')

    def accept(self):
        self.invited.friends.add(self.inviter)
        self.inviter.friends.add(self.invited)
        self.delete()

    def __str__(self):
        return str(self.inviter)
