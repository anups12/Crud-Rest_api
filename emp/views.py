from django.shortcuts import redirect, render
from emp.models import Employee
from . forms import EmployeeForm
from django.db.models import Q
from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework.response import Response
from . serializers import EmployeeSerializer

# Create your views here.

def CreateTask(request):
    form =EmployeeForm()
    data = Employee.objects.all()
    paginator = Paginator(data, 5)
    page = request.GET.get('page')
    page_num = paginator.get_page(page)

    if request.method=='POST':
       form= EmployeeForm(request.POST)
       if form.is_valid():
         form.save()
         form= EmployeeForm()
    context={'form':form,'data':page_num}
    return render(request, 'emp/home.html', context)

# Update employee data from data base
def UpdateEmployee(request, pk):
    emp = Employee.objects.get(id=pk)
    form =EmployeeForm(instance=emp)
    if request.method=='POST':
        form = EmployeeForm(request.POST, instance=emp)
        if form.is_valid():
            form.save()
            return redirect('/')

    context={'emp':emp, 'form':form}
    return render(request, 'emp/details.html', context)

# Delete employee data from data base
def DeleteDetail(request, pk):
    emp = Employee.objects.get(id=pk)
    emp.delete()
    return redirect('/')

# Search employee data from data base
def SearchField(request):
    form =EmployeeForm()
    if request.method=='POST':
        search= request.POST.get('search')
        data = Employee.objects.filter(Q(name__contains=search))
    else:
        data = Employee.objects.all()
    paginator = Paginator(data, 5)
    page = request.GET.get('page')
    page_num = paginator.get_page(page)
    context={ 'data':page_num, 'form':form}
    return render(request, 'emp/home.html', context)




# Code for api 
class EmpCrudApi(APIView):
    def get(self, request, pk=None, format=None):
# <----------------------GET DATA FROM THE DATABASE --------------->
        if pk is not None:
            try:
                emp = Employee.objects.get(id=pk)
                serializer = EmployeeSerializer(emp)
                return Response(serializer.data)
            except:
                return Response({'message': "The data you are requesting is not available or deleted "})
        else:       
            emp = Employee.objects.all()
            serializer=EmployeeSerializer(emp, many=True)
            return Response(serializer.data )

# <----------------------To add data  (POST request) --------------->
    def post(self, request, format=None):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid(): 
            serializer.save()
            return Response({'message':'Your data has been added successfully '})
        return Response(serializer.errors)

# <----------------------FOR COMPLETE DATA UPDATE --------------->
    def put(self, request,pk, format=None):
        try:
            emp = Employee.objects.get(id=pk)
            serializer = EmployeeSerializer(emp, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message':'Your data has been Updated successfully '})
        except:
            return Response({"Error message": "Check the id of the post you are trying to update "})
        return Response(serializer.errors)


# <----------------------FOR  PARTIAL DATA UPDATE --------------->
    def patch(self, request,pk, format=None):
        try:
            emp = Employee.objects.get(id=pk)
            serializer = EmployeeSerializer(emp, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message':'Your data has been Updated successfully '})
        except:
            return Response({"Error message": "Check the id of the post you are trying to update "})
        return Response(serializer.errors)

    def delete(self, request,pk, format=None):
        try:
            emp = Employee.objects.get(id=pk)
            emp.delete()
            return Response({'message':'Your data has been Deleted  '})
        except:
            return Response({'message': "The data you are requesting is not available or deleted "})