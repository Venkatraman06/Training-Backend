from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('CEO', 'CEO'),
        ('OPS_MGR', 'Operations Manager'),
        ('SALES', 'Sales Team'),
        ('MARKETING', 'Marketing Team'),
        ('TRAINER', 'Trainer'),
        ('FINANCE', 'Finance'),
        ('HR', 'HR'),
        ('INTERN', 'Intern'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='INTERN')
    phone = models.CharField(max_length=20, blank=True, null=True)
    whatsapp = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

class Task(models.Model):
    STATUS_CHOICES = [
        ('TODO', 'To Do'),
        ('IN_PROGRESS', 'In Progress'),
        ('REVIEW', 'Testing / Review'),
        ('COMPLETED', 'Completed'),
    ]

    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='TODO')
    tags = models.JSONField(default=list, blank=True)
    comments_count = models.IntegerField(default=0)
    attachments_count = models.IntegerField(default=0)
    avatar_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Lead(models.Model):
    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    ]
    STATUS_CHOICES = [
        ('LEAD', 'Lead'),
        ('CONTACTED', 'Contacted'),
        ('PROPOSAL_SENT', 'Proposal Sent'),
        ('WON', 'Won'),
        ('LOST', 'Lost'),
    ]
    name = models.CharField(max_length=255)
    company = models.CharField(max_length=255, blank=True, null=True)
    college = models.CharField(max_length=255, blank=True, null=True)
    contact_person = models.CharField(max_length=255, blank=True, null=True)
    designation = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    whatsapp = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    lead_source = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='LEAD')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='MEDIUM')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='assigned_leads')
    remarks = models.TextField(blank=True, null=True)
    expected_deal_value = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    training_requirement = models.TextField(blank=True, null=True)
    follow_up_date = models.DateField(blank=True, null=True)
    next_follow_up = models.DateField(blank=True, null=True)
    last_contact_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.company or self.college or ''}"

class Client(models.Model):
    name = models.CharField(max_length=255)
    company = models.CharField(max_length=255, blank=True, null=True)
    college = models.CharField(max_length=255, blank=True, null=True)
    contact_person = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    whatsapp = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    relationship_score = models.IntegerField(default=100)
    assigned_employee = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='assigned_clients')
    status = models.CharField(max_length=50, default='Active')
    next_follow_up = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Proposal(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('WON', 'Won'),
        ('LOST', 'Lost'),
    ]
    title = models.CharField(max_length=255)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='proposals')
    training_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    gst = models.DecimalField(max_digits=5, decimal_places=2, default=18.00)
    payment_terms = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    lost_reason = models.TextField(blank=True, null=True)
    contract_details = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class ActivityLog(models.Model):
    ACTIVITY_TYPES = [
        ('CALL', 'Call'),
        ('MEETING', 'Meeting'),
        ('EMAIL', 'Email'),
        ('WHATSAPP', 'WhatsApp'),
        ('NOTE', 'Note'),
        ('REMINDER', 'Reminder'),
    ]
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, blank=True, null=True, related_name='activities')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, blank=True, null=True, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.activity_type} - {self.created_at.strftime('%Y-%m-%d')}"

class College(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    
    principal_name = models.CharField(max_length=255, blank=True, null=True)
    principal_phone = models.CharField(max_length=20, blank=True, null=True)
    principal_email = models.EmailField(blank=True, null=True)
    
    placement_officer_name = models.CharField(max_length=255, blank=True, null=True)
    placement_officer_phone = models.CharField(max_length=20, blank=True, null=True)
    placement_officer_email = models.EmailField(blank=True, null=True)
    
    coordinator_name = models.CharField(max_length=255, blank=True, null=True)
    coordinator_phone = models.CharField(max_length=20, blank=True, null=True)
    coordinator_email = models.EmailField(blank=True, null=True)
    
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Trainer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='trainer_profile')
    skills = models.TextField(blank=True, null=True) # comma separated skills
    availability = models.BooleanField(default=True)
    salary_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Trainer: {self.user.first_name} {self.user.last_name}"

class Training(models.Model):
    STATUS_CHOICES = [
        ('PLANNED', 'Planned'),
        ('ACTIVE', 'Active'),
        ('COMPLETED', 'Completed'),
    ]
    MODE_CHOICES = [
        ('ONLINE', 'Online'),
        ('OFFLINE', 'Offline'),
    ]
    name = models.CharField(max_length=255)
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name='trainings')
    department = models.CharField(max_length=255, blank=True, null=True)
    trainer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, limit_choices_to={'role': 'TRAINER'})
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    venue = models.CharField(max_length=255, blank=True, null=True)
    mode = models.CharField(max_length=20, choices=MODE_CHOICES, default='OFFLINE')
    student_count = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PLANNED')
    daily_progress = models.TextField(blank=True, null=True)
    completion_percentage = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.college.name}"

class Student(models.Model):
    PLACEMENT_CHOICES = [
        ('PLACED', 'Placed'),
        ('UNPLACED', 'Unplaced'),
        ('SELECTED', 'Selected'),
    ]
    name = models.CharField(max_length=255)
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name='students')
    department = models.CharField(max_length=255, blank=True, null=True)
    year = models.CharField(max_length=20, blank=True, null=True) # 1st, 2nd, 3rd, 4th
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    placement_status = models.CharField(max_length=20, choices=PLACEMENT_CHOICES, default='UNPLACED')
    progress_percentage = models.IntegerField(default=0)
    skills = models.JSONField(default=list, blank=True)
    notes = models.TextField(blank=True, null=True)
    trainings = models.ManyToManyField(Training, blank=True, related_name='enrolled_students')

    def __str__(self):
        return f"{self.name} ({self.college.name})"

class PersonalStudent(models.Model):
    CERT_STATUS_CHOICES = [
        ('NONE', 'None'),
        ('PENDING', 'Pending'),
        ('ISSUED', 'Issued'),
    ]
    PAYMENT_STATUS_CHOICES = [
        ('UNPAID', 'Unpaid'),
        ('PARTIAL', 'Partial'),
        ('PAID', 'Paid'),
    ]
    student_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    certification_name = models.CharField(max_length=255)
    trainer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, limit_choices_to={'role': 'TRAINER'})
    course_duration = models.CharField(max_length=100, blank=True, null=True) # e.g. "3 months"
    fees = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    installments = models.JSONField(default=list, blank=True) # list of installments
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='UNPAID')
    exam_date = models.DateField(blank=True, null=True)
    certificate_status = models.CharField(max_length=20, choices=CERT_STATUS_CHOICES, default='NONE')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_name} - {self.certification_name}"
