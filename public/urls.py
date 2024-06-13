
from django.urls import path,include
from .import views

urlpatterns=[
    path('',views.index),
    path('login',views.dologin),
    path('logout',views.dologout),
    path('add_staff',views.staffadd),
    path('view_staff',views.staffview),
    path('edit_staff/<int:id>',views.staffedit),
    path('delete_staff/<int:id>',views.staffdelete),
    path('add_project',views.projectadd),
    path('view_project',views.projectview ),
    path('view_staff_project_index',views.view_staff_project_index, name='view_staff_project_index' ),
    path('edit_project/<int:id>',views.projectedit),
    path('delete_project/<int:id>',views.projectdelete),
    path('add_task/<int:id>/',views.taskadd),
    path('view_task/<int:id>/',views.view_task),
    path('view_timesheet/<int:id>/',views.view_timesheet),
    path('add_timesheet/<int:id>/',views.add_timesheet),
    path('respond/<int:id>/',views.respond),
    path('updatetask/<int:id>/',views.updatetask),
    path('add_complaint/',views.add_complaint),
    path('view_complaint/',views.view_complaint),
    path('view_leave/',views.view_leave),
    path('add_leave/',views.add_leave),
    path('respondleave/<int:id>/<str:dec>',views.respondleave),
    path('add_department/',views.add_department),
    path('view_department/',views.view_department),
    path('view_Attendence/',views.view_Attendence),
    path('updatesalary/<int:id>',views.updatesalary),
    path('deletetask/<int:id>',views.deletetask),
    path('deletedep/<int:id>',views.deletedep),
    path('Salary',views.calculate_salary),
    path('profile',views.profile),
    path('profileedit',views.editprof),


]