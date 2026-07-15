import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trainops_backend.settings')
django.setup()

from django.contrib.auth import get_user_model
from core.models import Task, Lead, Client, Proposal, ActivityLog, College, Trainer, Training, Student, PersonalStudent

User = get_user_model()

# Create tasks
Task.objects.all().delete()
Task.objects.create(title='Prepare React Slides', subtitle='Due: Tomorrow', tags=['High Priority'], status='TODO', avatar_url='https://i.pravatar.cc/150?img=11')
Task.objects.create(title='Call Stanford Lead', subtitle='Due: Jul 15', tags=['Sales'], status='TODO', avatar_url='https://i.pravatar.cc/150?img=33')
Task.objects.create(title='Grade Python Assignments', subtitle='Due: Today', tags=['Evaluation'], status='IN_PROGRESS', avatar_url='https://i.pravatar.cc/150?img=5')
Task.objects.create(title='Review New UI Mockups', subtitle='Due: Jul 12', tags=['Design'], status='REVIEW')
Task.objects.create(title='Send MIT MoU', subtitle='Completed', tags=['Legal'], status='COMPLETED', avatar_url='https://i.pravatar.cc/150?img=12')

# Create users
User.objects.all().delete()

users_data = [
    {'username': 'ceo', 'email': 'ceo@hackersinfotech.com', 'role': 'CEO', 'first_name': 'Sarah', 'last_name': 'CEO'},
    {'username': 'ops', 'email': 'ops@hackersinfotech.com', 'role': 'OPS_MGR', 'first_name': 'John', 'last_name': 'Operations'},
    {'username': 'sales', 'email': 'sales@hackersinfotech.com', 'role': 'SALES', 'first_name': 'Alice', 'last_name': 'Sales'},
    {'username': 'marketing', 'email': 'marketing@hackersinfotech.com', 'role': 'MARKETING', 'first_name': 'Bob', 'last_name': 'Marketing'},
    {'username': 'trainer', 'email': 'trainer@hackersinfotech.com', 'role': 'TRAINER', 'first_name': 'Alan', 'last_name': 'Trainer'},
    {'username': 'finance', 'email': 'finance@hackersinfotech.com', 'role': 'FINANCE', 'first_name': 'Dave', 'last_name': 'Finance'},
    {'username': 'hr', 'email': 'hr@hackersinfotech.com', 'role': 'HR', 'first_name': 'Eve', 'last_name': 'HR'},
    {'username': 'intern', 'email': 'intern@hackersinfotech.com', 'role': 'INTERN', 'first_name': 'Jack', 'last_name': 'Intern'},
]

for ud in users_data:
    user = User.objects.create_user(
        username=ud['username'],
        email=ud['email'],
        password='password123',
        role=ud['role'],
        first_name=ud['first_name'],
        last_name=ud['last_name']
    )
    if ud['role'] == 'CEO':
        user.is_superuser = True
        user.is_staff = True
        user.save()

# Get CEO and Sales users for associations
ceo_user = User.objects.get(username='ceo')
sales_user = User.objects.get(username='sales')

# Seed Leads
Lead.objects.all().delete()
l1 = Lead.objects.create(
    name='Stanford University', company='Stanford Group', college='Computer Science Dept',
    contact_person='Dr. Alan', designation='Dean', phone='+12345678', whatsapp='+12345678',
    email='alan@stanford.edu', location='USA', lead_source='Website', status='LEAD',
    priority='HIGH', assigned_to=sales_user, remarks='Interested in Cloud/AI Bootcamp',
    expected_deal_value=15000.00, training_requirement='10-day hands-on Cloud workshop'
)
l2 = Lead.objects.create(
    name='Oxford College', company='Oxford Group', college='Engineering College',
    contact_person='Prof. Emma', designation='HOD', phone='+44654321', whatsapp='+44654321',
    email='emma@oxford.edu', location='UK', lead_source='LinkedIn', status='CONTACTED',
    priority='MEDIUM', assigned_to=sales_user, remarks='Requested syllabus for Python',
    expected_deal_value=12000.00, training_requirement='Python fullstack curriculum'
)
l3 = Lead.objects.create(
    name='Cambridge Institute', company='Cambridge Science', college='Science Division',
    contact_person='Dr. Isaac', designation='Director', phone='+44998877', whatsapp='+44998877',
    email='isaac@cambridge.edu', location='UK', lead_source='Email Campaign', status='PROPOSAL_SENT',
    priority='HIGH', assigned_to=sales_user, remarks='Sent customized package quotation',
    expected_deal_value=22000.00, training_requirement='AI/ML Bootcamp with certifications'
)

# Seed Clients
Client.objects.all().delete()
c1 = Client.objects.create(
    name='MIT Pune', company='MAEER Group', college='MIT Pune Campus',
    contact_person='Dr. Karad', phone='+919876543', whatsapp='+919876543',
    email='admin@mitpune.edu', relationship_score=95, assigned_employee=ceo_user,
    status='Active', notes='Long term partner. Highly satisfied.'
)
c2 = Client.objects.create(
    name='VIT Vellore', company='Vellore Tech', college='VIT main',
    contact_person='Prof. Viswanathan', phone='+919999999', whatsapp='+919999999',
    email='placement@vit.ac.in', relationship_score=90, assigned_employee=ceo_user,
    status='Active', notes='Good potential for corporate training'
)

# Seed Proposals
Proposal.objects.all().delete()
p1 = Proposal.objects.create(
    title='React Training Proposal', client=c1, training_cost=18000.00,
    discount=2000.00, gst=18.00, payment_terms='50% advance, 50% post-training',
    status='WON', contract_details='MoU signed on June 15.'
)
p2 = Proposal.objects.create(
    title='Data Science Quotation', client=c2, training_cost=25000.00,
    discount=3000.00, gst=18.00, payment_terms='100% post-invoice within 30 days',
    status='PENDING'
)

# Seed Colleges
College.objects.all().delete()
col1 = College.objects.create(
    name='MIT Pune', address='Kothrud, Pune', district='Pune', state='Maharashtra',
    website='https://mitpune.edu.in', principal_name='Dr. Prasad',
    placement_officer_name='Prof. Deshmukh', coordinator_name='Mrs. Kulkarni'
)
col2 = College.objects.create(
    name='VIT Vellore', address='Katpadi, Vellore', district='Vellore', state='Tamil Nadu',
    website='https://vit.ac.in', principal_name='Dr. Rambabu',
    placement_officer_name='Prof. Suresh', coordinator_name='Dr. Parthasarathy'
)

# Seed Trainer Profile
Trainer.objects.all().delete()
trainer_user = User.objects.get(username='trainer')
t_profile = Trainer.objects.create(
    user=trainer_user, skills='React, Python, Django, Cloud Computing',
    availability=True, salary_rate=50.00
)

# Seed Trainings
Training.objects.all().delete()
tr1 = Training.objects.create(
    name='Fullstack Web Development with React', college=col1, department='Computer Science',
    trainer=trainer_user, start_date='2026-06-01', end_date='2026-07-30',
    venue='Lab 3, MIT campus', mode='OFFLINE', student_count=45,
    status='ACTIVE', completion_percentage=65, daily_progress='Completed React components and state management.'
)
tr2 = Training.objects.create(
    name='Python AI/ML Foundation', college=col2, department='Information Technology',
    trainer=trainer_user, start_date='2026-07-15', end_date='2026-08-15',
    venue='Google Meet', mode='ONLINE', student_count=60,
    status='PLANNED', completion_percentage=0
)

# Seed Students
Student.objects.all().delete()
s1 = Student.objects.create(
    name='Rohan Sharma', college=col1, department='Computer Science', year='3rd Year',
    phone='+919876543210', email='rohan@gmail.com', linkedin='https://linkedin.com/in/rohan',
    github='https://github.com/rohan', placement_status='SELECTED', progress_percentage=75,
    skills=['React', 'JavaScript', 'HTML/CSS']
)
s1.trainings.add(tr1)

s2 = Student.objects.create(
    name='Priya Patel', college=col1, department='Computer Science', year='3rd Year',
    phone='+919876543211', email='priya@gmail.com', linkedin='https://linkedin.com/in/priya',
    github='https://github.com/priya', placement_status='UNPLACED', progress_percentage=60,
    skills=['JavaScript', 'HTML/CSS']
)
s2.trainings.add(tr1)

s3 = Student.objects.create(
    name='Aditya Kumar', college=col2, department='Information Technology', year='4th Year',
    phone='+919876543212', email='aditya@gmail.com', linkedin='https://linkedin.com/in/aditya',
    github='https://github.com/aditya', placement_status='PLACED', progress_percentage=10,
    skills=['Python', 'SQL']
)
s3.trainings.add(tr2)

# Seed Personal Certification Students
PersonalStudent.objects.all().delete()
ps1 = PersonalStudent.objects.create(
    student_name='Abhishek Rao', phone='+919000000001', email='abhishek@gmail.com',
    certification_name='AWS Certified Solutions Architect', trainer=trainer_user,
    course_duration='2 months', fees=450.00, payment_status='PARTIAL',
    certificate_status='PENDING', notes='Installment 1 paid. Exam scheduled for August.'
)
ps2 = PersonalStudent.objects.create(
    student_name='Divya Nair', phone='+919000000002', email='divya@gmail.com',
    certification_name='Certified React Professional', trainer=trainer_user,
    course_duration='1 month', fees=250.00, payment_status='PAID',
    certificate_status='ISSUED', notes='Successfully passed the exam with 92% score.'
)

# Seed ActivityLogs
ActivityLog.objects.all().delete()
ActivityLog.objects.create(
    lead=l1, activity_type='EMAIL', description='Sent introductory email with brochure.',
    created_by=sales_user
)
ActivityLog.objects.create(
    lead=l1, activity_type='CALL', description='Discussed curriculum and pricing.',
    created_by=sales_user
)

print("Database seeded with Tasks, Users, Leads, Clients, Proposals, Activities, Colleges, Trainers, Trainings, Students, and Personal Students.")
