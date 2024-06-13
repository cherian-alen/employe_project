from django.shortcuts import render
from django.shortcuts import render,redirect
from .forms import *
from django.contrib import auth
from django.contrib.auth import authenticate,login
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.
from datetime import datetime
from Machinelearning.models import *
from datetime import datetime, timedelta
import calendar
from django.contrib import messages

def index(request):
    today = timezone.now().date()
    employ=Register.objects.filter(usertype=2)
    print('emplou',employ)

    for i in employ:
            data=Register.objects.get(id=i.id)
            uni=Attendence.objects.filter(current_date=today,emid=i.id).first()
            print(uni)
            if not uni:   
                Attendence.objects.create(
                    emid=data,
                    current_date=today
                )
    return render(request,'index.html')
def dologin(request):
    form = LoginForm()
    if request.method == "POST":
        user = authenticate(request,username=request.POST["username"],password=request.POST["password"] )
        if user is None:
            return render(request,'index.html',{'a':True})
        else:
            login(request, user)
            data = Register.objects.get(username=user.username)
            request.session['ut']=data.usertype
            data.usertype
            request.session['userid']=data.id
            return redirect('/add_department')
        
    else:
        form = LoginForm()
    return render(request,'login.html',{'form':form})
def dologout(request):
    auth.logout(request)
    return redirect('/')
def staffadd(request):
  
        if request.method == 'POST':
            
            form = StaffAddForm(request.POST, request.FILES)
            try:
                Register.objects.get(username=request.POST['email'])
                return render(request,'add_staff.html',{'form':form,'x':True})
            except Register.DoesNotExist:
               
                print(form.is_valid())
                print(form.errors)
                if form.is_valid():
                    Register.objects.create_user(
                    role = form.cleaned_data['role'],
                    username = form.cleaned_data['username'],
                    name = form.cleaned_data['username'],
                    password=form.cleaned_data['password'],
                    email=form.cleaned_data['email'],
                    contact=form.cleaned_data['contact'],
                    registrationid=form.cleaned_data['registrationid'],
                    Department=Departments.objects.get(id=request.POST['dep']), 
                    usertype=2 
                    )
                    return redirect('/')
                else:
                    return render(request, 'went_wrong.html') 
             
        else:
            form = StaffAddForm()
            dep=Departments.objects.all()
            return render(request, 'add_staff.html', {'form': form,'dep':dep})
  
@login_required(login_url='/login')
def staffedit(request, id):
    data = Register.objects.get(id=id)
    if request.user.usertype != 1:
        return render(request, 'access_denied.html')
    if request.method == 'POST':
        form = StaffEditForm(request.POST, instance=data)    
        if form.is_valid():
            email = form.cleaned_data['email']
            form.save()
            return redirect('/view_staff')
    else:
        form = StaffEditForm(instance=data)
    return render(request, 'Edit_staff.html', {'form': form})
@login_required(login_url='/login')
def staffdelete(request,id):
    data=Register.objects.get(id=id)
    data.delete()
    return redirect('/view_staff')   
@login_required(login_url='/login')
def staffview(request):
    if request.user.usertype != 1:
        return render(request, 'access_denied.html')
    a = Register.objects.exclude(usertype="1")
    search = request.GET.get('search','')
    if search:
        a = a.filter(Q(name__icontains=search)|Q(role__icontains=search)|Q(email__icontains=search))
        print(a)
    return render(request,'view_staff.html',{'a':a})
@login_required(login_url='/login')
def projectadd(request):
    if request.method == 'POST':
        form = ProjectAddForm(request.POST, request.FILES)
        if form.is_valid():
            Projects.objects.create(
             title=form.cleaned_data['title'],
             description=form.cleaned_data['description'],
             start_date=form.cleaned_data['start_date'],
             due_date=form.cleaned_data['due_date'],
             file=form.cleaned_data['file']
            )
            # send_mail(
            #     subject="Assigned Project",
            #     message=f"Admin Assigned a project: {project.title} And Your Due Date is: {project.due_date}",
            #     from_email=settings.EMAIL_HOST_USER,
            #     recipient_list=[i.email for i in team_members]
            # )
            return redirect('/view_project')
    else:
        form = ProjectAddForm()

    return render(request, 'add_project.html', {'form': form})
def projectview(request):
    all_projects = Projects.objects.all()
    f = Task.objects.all()
    search = request.GET.get('search', '')
    selected_project_title = request.GET.get('filter', '') 
    selected_staff_member_name = request.GET.get('staff_filter', '')
    if search:
        all_projects = all_projects.filter(Q(title__icontains=search) | Q(team__team_members__name__icontains=search))
    if selected_project_title:
        all_projects = all_projects.filter(title=selected_project_title)
    staff_members = Register.objects.exclude(usertype=1)
    distinct_project_titles = Projects.objects.values_list('title', flat=True).distinct()
    distinct_staff_member = Register.objects.exclude(usertype=1).values_list('name', flat=True).distinct()
    if selected_staff_member_name:
        all_projects = all_projects.filter(Q(team__team_members__name__icontains=selected_staff_member_name))
    
    context = {
        'all_projects': all_projects,
        'selected_project_title': selected_project_title,
        'distinct_project_titles': distinct_project_titles,
        'staff_member': staff_members,
        'distinct_staff_member': distinct_staff_member,
        'selected_staff_member': selected_staff_member_name,
        
    }
    return render(request,'view_project.html', context)
@login_required(login_url='/login')
def projectedit(request, id):
    project = Projects.objects.get(id=id)
    related_files = project.file.all()
    if request.method == 'POST':
        form = ProjectEditForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            updated_project = form.save(commit=False)
            updated_project.current_date = timezone.now()
            updated_project.updated_by = request.user
            updated_project.save()
            team_members = project.team.team_members.all()

            files = request.FILES.getlist('file_field') 
            for file in files:
                upload_file = UploadFile(file=file)
                upload_file.save()
                updated_project.file.add(upload_file)

            files_to_remove = request.POST.getlist('remove_files')
            for file_id in files_to_remove:
                file_to_remove = UploadFile.objects.get(id=file_id)
                file_to_remove.file.delete()
                updated_project.file.remove(file_to_remove)

            send_mail(
                subject="Updated Project",
                message=f"Admin Updated a project: {project.title} And Your Due Date is: {project.due_date}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[i.email for i in team_members]
            )
            return redirect(reverse('view_project_index', args=[project.id]))
    else:
        form = ProjectEditForm(instance=project)
    return render(request, 'edit_project.html', {'form': form, 'project': project, 'related_files': related_files})

@login_required(login_url='/login')    
def projectdelete(request,id):
    a = Projects.objects.get(id=id)
    a.delete()
    return redirect('/view_project')

def view_staff_project_index(request):
    a = request.user.id
    all_projects=  Projects.objects.all()
    selected_project_title = request.GET.get('filter', '')
    selected_staff_member_name = request.GET.get('staff_filter', '')
    search = request.GET.get('search', '')
    if search:
        all_projects = Projects.objects.filter(Q(title__icontains=search))
    if selected_project_title:
        all_projects = Projects.objects.filter(title=selected_project_title)
      
    staff_members = Register.objects.exclude(usertype=1)
    distinct_project_titles = Projects.objects.values_list('title', flat=True).distinct()
    distinct_staff_member = Register.objects.exclude(usertype=1).values_list('name', flat=True).distinct()
    if selected_staff_member_name:
        all_projects = all_projects.filter(Q(team__team_members__name__icontains=selected_staff_member_name))
        c = c.filter(Q(team__team_members__name=selected_staff_member_name))

    context = {
        'all_projects': all_projects,
        'selected_project_title': selected_project_title,
        'distinct_project_titles': distinct_project_titles,
        'staff_member': staff_members
    }
    return render(request,'view_staff_project_index.html',context)
@login_required(login_url='/login')
def taskadd(request, id):
    project = Projects.objects.get(id=id)
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        start_date = request.POST.get('start_date')
        due_date = request.POST.get('due_date')
        file=request.FILES.get('file')
        task = Task.objects.create(
            title=title,
            description=description,
            start_date=start_date,
            due_date=due_date,
            project=project,
            assigned_staff= Register.objects.get(id=request.POST.get('staff')),
            file=file
        )
        return redirect('/')
    else:
        member=Register.objects.filter(usertype=2)
        return render(request, 'add_subtask.html', {'members': member})
@login_required(login_url='/login')
def view_task(request, id):
        if request.user.usertype == 2:
            tasks=Task.objects.filter(project=id,assigned_staff=request.user.id)
            return render(request, 'view_subtasks.html', {'tasks': tasks})
        else:    
            tasks=Task.objects.filter(project=id)
            return render(request, 'view_subtasks.html', {'tasks': tasks})
@login_required(login_url='/login')
def view_timesheet(request, id):
            timesheets=timesheet.objects.filter(task=id)
            return render(request, 'view_timesheet.html', {'timesheet': timesheets})
@login_required(login_url='/login')
def add_timesheet(request, id):
        form=timesheetAddForm(request.POST)
        if request.method== "POST":
           if form.is_valid():
               timesheet.objects.create(
                   task=Task.objects.get(id=id),
                   assigned_staff=Register.objects.get(id=request.user.id),
                   workinghours=form.cleaned_data['workinghours']
               )
               return redirect('/view_timesheet')
        else:    
            tasks=Task.objects.filter(project=id)
            form=timesheetAddForm()
            return render(request, 'add_timesheet.html', {'tasks': tasks,'form':form})
        
@login_required(login_url='/login')
def add_complaint(request):
        form=complaintAddForm(request.POST,request.FILES)
        if request.method== "POST":
           if form.is_valid():
               complaints.objects.create(
                   userid=Register.objects.get(id=request.user.id),
                   title=form.cleaned_data['title'],
                   description=form.cleaned_data['description'],
                   file=form.cleaned_data['file']
               )
               return redirect('/view_complaint')
        else:    
            form=complaintAddForm()
            return render(request, 'add_complaints.html', {'form':form})        
@login_required(login_url='/login')
def view_complaint(request):
    if request.user.usertype == 2:
        view=complaints.objects.filter(userid=request.user.id)
        return render(request,'view_complaints.html',{'data':view})    
    else:     
        view=complaints.objects.all()
        return render(request,'view_complaints.html',{'data':view})   
@login_required(login_url='/login')
def respond(request,id):
    if request.method =="POST":    
        com=complaints.objects.get(id=id)
        com.response=request.POST['response']
        com.status=1
        com.save()
        return redirect('/view_complaint') 
    else:
        return render(request,'respond.html')    
@login_required(login_url='/login')
def updatetask(request,id):
    if request.method =="POST":    
        tas=Task.objects.get(id=id)
        tas.status=request.POST['status']
        tas.save()
        return redirect('/view_task/'+str(id)) 
    else:
        return render(request,'taskstatus.html') 
@login_required(login_url='/login')
def view_leave(request):
    if request.user.usertype == 2:
        lv=leave.objects.filter(userid=request.user.id)
        return render(request,'leave.html',{'data':lv})    
    else:     
        lv=leave.objects.all()
        return render(request,'leave.html',{'data':lv})       

@login_required(login_url='/login')
def add_leave(request):
        form=leaveAddForm(request.POST,request.FILES)
        if request.method== "POST":
           if form.is_valid():
               leave.objects.create(
                   userid=Register.objects.get(id=request.user.id),
                   reason=form.cleaned_data['reason'],
                   date=form.cleaned_data['date'],
                   ltype=form.cleaned_data['ltype'],
               )
               return redirect('/view_leave')
        else:    
            form=leaveAddForm()
            return render(request, 'applyleave.html', {'form':form})      
        
@login_required(login_url='/login')
def respondleave(request,id,dec):
        if dec == "approve":
            lv=leave.objects.get(id=id)
            lv.status=1
            lv.save()   
            return redirect('/view_leave') 

        
        elif dec == "reject":
            lv=leave.objects.get(id=id)
            lv.status=2
            lv.save()
            return redirect('/view_leave') 
@login_required(login_url='/login')
def add_department(request):
    if(request.method=='POST'):
        form = departmentaddform(request.POST,request.FILES)
        try:
            Departments.objects.get(departmentname=request.POST['departmentname'])
            return render(request,'add_department.html',{'form':form,'c':True})
        except Departments.DoesNotExist:
            if form.is_valid():               
                Departments.objects.create(
                    departmentname = form.cleaned_data['departmentname'],
                  
                )
              
              
            return redirect('/view_department')
    else:
        form = departmentaddform()
        return render(request,'add_department.html',{'form':form})

@login_required(login_url='/login')
def view_department(request):
    dep=Departments.objects.all()
    return render(request,'view_department.html',{'dep':dep})    


@login_required(login_url='/login')
def view_Attendence(request):
    if request.user.usertype == 2:
        att=Attendence.objects.filter(emid=request.user.id)
        return render(request,'view_attendence.html',{'att':att})    
    elif request.user.usertype == 1:
        att=Attendence.objects.all()
        return render(request,'view_attendence.html',{'att':att})      

@login_required(login_url='/login')
def updatesalary(request,id):
    if request.method =="POST":    
        user=Register.objects.get(id=id)
        user.salary=request.POST['salary']
        user.save()
        return redirect('/view_staff') 
    else:
        return render(request,'add_salary.html') 

@login_required(login_url='/login')
def calculate_salary(request):
    today = datetime.today()
    if today.day == 1:
        last_month = today - timedelta(days=today.day)
        employees = Register.objects.filter(usertype=2)
        num_days = monthrange(last_month.year, last_month.month)[1]
        for employee in employees:
            attendance_count = Attendance.objects.filter(
                emid=employee,
                current_date__month=last_month.month,
                attendence="Present"
            ).count()            
            per_day_salary = employee.salary            
            total_salary = attendance_count * per_day_salary            
            Salary.objects.create(
                eid=employee,
                salary=total_salary,
                month=last_month.strftime("%B"),
                current_date=timezone.now()
            )
    elif request.user.usertype == 1:
                sl=Salary.objects.all()
                if sl:
                    return render(request, 'view_salary.html', {'salary':sl})
                else:
                    return render(request, 'view_salary.html')



    elif request.user.usertype == 2:
                sl=Salary.objects.filter(eid=request.user.id)
                if sl:
                    return render(request, 'view_salary.html', {'salary':sl})
                else:
                    return render(request, 'view_salary.html')
    # else:                
    #     return render(request, 'view_salary.html')        



@login_required(login_url='/login')
def deletetask(request,id):
    ts=Task.objects.get(id=id)
    ts.delete()
    referring_url = request.META.get('HTTP_REFERER')
    return redirect(referring_url or '/')

@login_required(login_url='/login')
def deletedep(request,id):
    ts=Departments.objects.get(id=id)
    ts.delete()
    referring_url = request.META.get('HTTP_REFERER')
    return redirect(referring_url or '/')





def profile(request):
    us=Register.objects.get(id=request.user.id)
    return render(request,'profile.html',{'us':us})    


def editprof(request):
    data=Register.objects.get(id=request.user.id)
    if request.method == 'POST':
        form = profiledit(request.POST, instance=data)    
        if form.is_valid():
            form.save()
            return redirect('/profile')
    else:
        form = profiledit(instance=data)
    return render(request, 'Edit_profile.html', {'form': form})