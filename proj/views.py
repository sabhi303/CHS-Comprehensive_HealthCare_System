from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.http import HttpResponseRedirect,JsonResponse,HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from log.models import AddtionalDetails
from proj.models import Record,Orders,Messages,Prescription,Feedback
from django.db.models import Q
import json
from selenium import webdriver
from django.core.mail import EmailMultiAlternatives
from io import BytesIO

# _appname_=proj

from django.template.loader import get_template
from xhtml2pdf import pisa

# from django.shortcuts import render_to_response
from django.template import RequestContext
from .renderpdf import link_callback  
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

profession=""


#home page of web
def home(request):

	return render(request,'home/healthhome.html')

def about(request):

	return render(request,'home/about.html')

@csrf_exempt
def newmsg(request):
	user=request.user.username
	receiver=request.POST.get('id')
	mesg=request.POST.get('msg')
	msg = Messages(sender=user,receiver=receiver,message=mesg)
	msg.save()
	return HttpResponse("Sucess")

	
@csrf_exempt
def chatting(request):
	user=request.user.username	
	if request.method=="POST":
		other=request.POST.get('id')
		msgsend=Messages.objects.filter(Q(sender=user) & Q(receiver=other))
		msgrecv=Messages.objects.filter(Q(sender=other) & Q(receiver=user))
	# msg = Messages(sender=user,receiver="pha@a.c",message="Second Message")
	# msg.save()
		messages=[]
		for i in msgrecv:
			messages.append([i.message,i.time,0])
		for i in msgsend:
			messages.append([i.message,i.time,1])
		# print(messages)
		messages.sort(key = lambda x: x[1]) 

		msgs=[]
		for i in messages:
			msgs.append([i[0],i[2]])
		return HttpResponse(json.dumps(msgs))
	else:
		# contactlist=Messages.objects.filter(Q(sender=user)| Q(receiver=user))
		# msgrecv=Messages.objects.filter(Q(receiver=user) & Q(read=0))
		# new=len(msgrecv)
		# contacts=[]
			
		# for i in msgrecv:
		# 	contacts.append(AddtionalDetails.objects.filter(username=i.sender))

		contacts=[]
		user_rec=AddtionalDetails.objects.filter(username=user)
		global profession
		profession=(user_rec[0].profession)
			
		if profession=="user":
			contactlist=Record.objects.filter(user=user)
			contactlist2=set()
			for i in contactlist:
				contactlist2.add(i.doctor)
			# print(contactlist2)
			for i in contactlist2:
				contacts.append(AddtionalDetails.objects.filter(username=i))

		elif profession=="doctor":
			contactlist=Record.objects.filter(doctor=user)
			contactlist2=set()
			for i in contactlist:
				contactlist2.add(i.user)
			# print(contactlist2)
			for i in contactlist2:
				contacts.append(AddtionalDetails.objects.filter(username=i))

		# print(contacts)
		# print(type(contactlist))
		
		return render(request,'chat/chat.html',{'data':contacts})



#dashboard common to all user
@login_required
def dashboard(request):
	
	if request.user.is_authenticated:

		username=request.user.username
		if username=="admin@gmail.com":
			
			users=AddtionalDetails.objects.filter(~Q(profession ="user") & Q(verified=0))

			return render(request,'dashboard/admin/verify.html',{'data1':users})

		user_rec=AddtionalDetails.objects.filter(username=username)
		global profession
		profession=(user_rec[0].profession)
		# profession="doctor"

		if profession=="user":
			list1=[]
			requests=Record.objects.filter(user=username,status=0,adate__isnull=False)[:5]
			for i in requests:
				list1.append(AddtionalDetails.objects.filter(username=i.doctor))

			numbers=range(1,20)
			data1=zip(list1,requests,numbers)
			return render(request,'dashboard/user/user.html',{'data1':data1})
		elif profession=="doctor":
			list1=[]
			requests=Record.objects.filter(doctor=username,status=0,adate__isnull=False)[:5]
			for i in requests:
				list1.append(AddtionalDetails.objects.filter(username=i.user))
			clients=set()
			meetings=Record.objects.filter(doctor=username)
			for i  in meetings:
				clients.add(i.user)

			numbers=range(1,20)
			data1=zip(list1,requests,numbers)
			
			return render(request,'dashboard/doctor/doctor.html',{'data1':data1,'meetings':len(meetings),'clients':len(clients)})
		
		elif profession=="pharma":
			list1=[]
			requests=Orders.objects.filter(pharma=username,status=0,adate__isnull=False)[:5]
			for i in requests:
				list1.append(AddtionalDetails.objects.filter(username=i.user))
			clients=set()
			orders=Orders.objects.filter(pharma=username)
			for i  in orders:
				clients.add(i.user)

			numbers=range(1,20)
			data1=zip(list1,requests,numbers)
			
			return render(request,'dashboard/pharma/pharma.html',{'data1':data1,'orders':len(orders),'clients':len(clients)})

	else:
		return redirect("/log/login")
	


	#Funtion for Show Available doctors to user and request to doctor.

@csrf_exempt
def verify(request):
	username=request.POST.get('id')
	print(username)
	print("ha user")
	r=AddtionalDetails.objects.get(username=username)
	r.verified=1
	r.save()
	return HttpResponse("Requested")
	
	
@csrf_exempt
def reqdoc(request):

	if request.method=='POST':				#Request to doctor for an appointment

		print(request.POST)
		username=request.user.username
		userfname=request.user.get_full_name()
		doctor=request.POST.get('id')
		print(username,doctor)
		r = Record(user=username,doctor=doctor)
		r.save()
		r=AddtionalDetails.objects.get(username=doctor)
		noti=(" {user} Asked for an appointment ".format(user=userfname))
		r.notifications.append([noti,str(datetime.now())])
		r.save()
		return HttpResponse("Requested")

	else:					#show available doctors
		numbers=range(1,20)
		doctors=AddtionalDetails.objects.filter(profession='doctor', verified=1)
		# doctors={}
		data=zip(numbers,doctors)
		return render(request,'dashboard/user/show_doc.html',{'data':data})
		# return render(request,'dashboard/user/newuser.html',{'data':data})


	
	#funtions for show appointments of user

@csrf_exempt
def showreq(request):
	if request.method=='POST':  #to cancel appointment
		print(request.POST)
		doctor=request.user.username
		user=request.POST.get('id')
		tid=request.POST.get('tid')
		print(user,doctor,tid)
		Record.objects.filter(id=tid).delete()
		
		# redirect("/docshowappo")
		return HttpResponse("Requested")


	else:    					#to show all appointments
		username=request.user.username
		requests=Record.objects.filter(user=username,status=0,adate__isnull=False)
		proreq=Record.objects.filter(user=username,status=0,adate__isnull=True)
		list1=[]
		list2=[]
		for i in requests:
			list1.append(AddtionalDetails.objects.filter(username=i.doctor))
		
		for i in proreq:
			list2.append(AddtionalDetails.objects.filter(username=i.doctor))

		# print(list1)
		numbers=range(1,20)
		#zip data to display
		data1=zip(list1,requests,numbers)
		data2=zip(list2,proreq,numbers)
		print(data2)
		return render(request,'dashboard/user/show_req.html',{'data1':data1,'data2':data2})


@csrf_exempt
def completedreq(request):
	if request.method=='POST':  #to cancel appointment
		# print(request.POST)
		# doctor=request.user.username
		# user=request.POST.get('id')
		# tid=request.POST.get('tid')
		# print(user,doctor,tid)
		# Record.objects.filter(id=tid).delete()
		
		# redirect("/docshowappo")
		return HttpResponse("Requested")
 

	else:    					#to show all appointments
		username=request.user.username
		proreq=Record.objects.filter(user=username,status=1)
		list2=[]
		

		for i in proreq:
			# print(i.user)
			list2.append([(AddtionalDetails.objects.filter(username=i.user)),(AddtionalDetails.objects.filter(username=i.doctor))])

		# print(list1)
		numbers=range(1,20)
		#zip data to display
		data2=zip(list2,proreq,numbers)
		print(data2)
		return render(request,'dashboard/user/completedreq.html',{'data2':data2})

@csrf_exempt
def feedback(request):
	if request.method=="POST":
		print(request.POST)
		usrid=request.user.username
		print(usrid)
		rating=int(request.POST.get('rating'))
		comment=request.POST.get('comment')
		docid=request.POST.get('docid')
		tid=request.POST.get('tid')
		Record.objects.filter(id=tid).update(feedst=1)
		f=Feedback(tid=tid,user=usrid,doctor=docid,feedback=comment,rating=(rating))
		f.save()
		r= AddtionalDetails.objects.get(username=usrid)
		if (r.rating)==None:
			r.rating=[rating,1]
			r.save()
		else:
			a,b=map(int,r.rating)
			print(a,b)
			avgrating=(a*b+rating)/(b+1)
			r.rating=[avgrating,b+1]
			r.save()
		
		return redirect("/completedreq")
	else:

		user=request.GET.get('feddoc')
		tid=request.GET.get('fedtid')

		doctor=AddtionalDetails.objects.filter(username=user)
		print(doctor)
		return render(request,'dashboard/user/feedback.html',{'doctor':doctor,'tid':tid})

#fuction for make appointment with user 
@csrf_exempt
def docshowreq(request):
	if request.method=='POST':
		print(request.POST)
		doctor=request.user.username
		docname=request.user.first_name
		user=request.POST.get('id')
		tid=request.POST.get('tid')
		date=request.POST.get('date')
		print(user,doctor,date)
		# sdate=date.strftime("%m/%d/%Y")

		Record.objects.filter(id=tid,user=user,doctor=doctor).update(adate=date)
		r=AddtionalDetails.objects.get(username=user)
		noti=("Dr {doctor} Sceduled an appointent on {date} ".format(doctor=docname,date=date))
		r.notifications.append([noti,str(datetime.now())])
		r.save()
		return HttpResponse("Requested")

	else:
		username=request.user.username
		requests=Record.objects.filter(doctor=username,status=0,adate__isnull=True)
		proreq=Record.objects.filter(user=username,status=1)
		list1=[]
		for i in requests:
			list1.append([(AddtionalDetails.objects.filter(username=i.user)),(AddtionalDetails.objects.filter(username=i.doctor))])

		# print(list1)
		numbers=range(1,20)

		#zip data to display
		data1=zip(list1,requests,numbers)
		return render(request,'dashboard/doctor/show_req.html',{'data1':data1})




#funtion for show appointments of Doctor

@csrf_exempt
def docshowappo(request):

	if request.method=='POST': #to  cancel the appointment
		print(request.POST)
		doctor=request.user.username
		user=request.POST.get('id')
		tid=request.POST.get('tid')
		print(user,doctor,tid)
		Record.objects.filter(id=tid).delete()
		
		# redirect("/docshowappo")
		return HttpResponse("Requested")

	else:  #to show all appointments

		username=request.user.username
		requests=Record.objects.filter(doctor=username,status=0,adate__isnull=False)
		proreq=Record.objects.filter(doctor=username,status=1)
		list1=[]
		list2=[]
		for i in requests:
			list1.append([(AddtionalDetails.objects.filter(username=i.user)),(AddtionalDetails.objects.filter(username=i.doctor))])


		for i in proreq:
			# print(i.user)
			list2.append([(AddtionalDetails.objects.filter(username=i.user)),(AddtionalDetails.objects.filter(username=i.doctor))])

		# print(list1)
		numbers=range(1,20)
		print(list2)
		#zip data to display
		data1=zip(list1,requests,numbers)
		data2=zip(list2,proreq,numbers)
		return render(request,'dashboard/doctor/show_appo.html',{'data1':data1,'data2':data2})




#Funtion of pharmacist

@csrf_exempt
def reqpharma(request):

	if request.method=='POST':				#Request to doctor for an appointment

		print(request.POST)
		username=request.user.username
		userfname=request.user.get_full_name()
		pharma=request.POST.get('pharmaid')
		tid=request.POST.get('tid')
		# print(username,doctor)
		infotid=Record.objects.get(id=tid)
		prescription=infotid.prescription
		print(prescription)

		r = Orders(tid=tid,user=username,pharma=pharma,prescription=prescription)
		r.save()
		r=AddtionalDetails.objects.get(username=pharma)
		noti=(" {user} Placed an Order ".format(user=userfname))
		r.notifications.append([noti,str(datetime.now())])
		r.save()
		return HttpResponse("Requested")

	else:					#show available doctors
		user=request.GET.get('usrid')
		tid=request.GET.get('tid')
		print(user,tid)
		# list1=[]
		# list1.append(AddtionalDetails.objects.filter(username=user))

		numbers=range(1,20)
		pharmas=AddtionalDetails.objects.filter(profession='pharma', verified=1)
		# doctors={}
		data=zip(numbers,pharmas)
		return render(request,'dashboard/user/show_pharma.html',{'data':data,'tid':tid})


	
	#funtions for show appointments of user

@csrf_exempt
def showorders(request):
	if request.method=='POST':  #to cancel appointment
		print(request.POST)
		pharma=request.user.username
		user=request.POST.get('id')
		tid=request.POST.get('tid')
		print(user,pharma,tid)
		Orders.objects.filter(id=tid).delete()
		
		# redirect("/docshowappo")
		return HttpResponse("Requested")


	else:    					#to show all appointments
		username=request.user.username
		requests=Orders.objects.filter(user=username,status=0,adate__isnull=False)
		proreq=Orders.objects.filter(user=username,status=0,adate__isnull=True)
		list1=[]
		list2=[]
		for i in requests:
			list1.append(AddtionalDetails.objects.filter(username=i.pharma))
		
		for i in proreq:
			list2.append(AddtionalDetails.objects.filter(username=i.pharma))

		# print(list1)
		numbers=range(1,20)
		#zip data to display
		data1=zip(list1,requests,numbers)
		data2=zip(list2,proreq,numbers)
		print(data2)
		return render(request,'dashboard/user/show_orders.html',{'data1':data1,'data2':data2})





#fuction for make Schedule order with user 
@csrf_exempt
def pharmashoworders(request):
	if request.method=='POST':
		print(request.POST)
		pharma=request.user.username
		pharmaname=request.user.first_name
		user=request.POST.get('id')
		tid=request.POST.get('tid')
		date=request.POST.get('date')
		print(user,pharma,date)
		# sdate=date.strftime("%m/%d/%Y")

		Orders.objects.filter(id=tid,user=user,pharma=pharma).update(adate=date)
		r=AddtionalDetails.objects.get(username=user)
		noti=(" Ph.{pharma} Expect delivery of medicines on {date} ".format(pharma=pharmaname,date=date))
		r.notifications.append([noti,str(datetime.now())])
		r.save()
		return HttpResponse("Requested")

	else:
		username=request.user.username
		requests=Orders.objects.filter(pharma=username,status=0,adate__isnull=True)
		proreq=Orders.objects.filter(user=username,status=1)
		list1=[]
		for i in requests:
			list1.append([(AddtionalDetails.objects.filter(username=i.user)),(AddtionalDetails.objects.filter(username=i.pharma))])

		# print(list1)
		numbers=range(1,20)

		#zip data to display
		data1=zip(list1,requests,numbers)
		return render(request,'dashboard/pharma/show_req.html',{'data1':data1})




#funtion for show Orders (pharma function)

@csrf_exempt
def pharmashowinorders(request):

	if request.method=='POST': #to  cancel the appointment
		print(request.POST)
		pharma=request.user.username
		user=request.POST.get('id')
		tid=request.POST.get('tid')
		print(user,pharma,tid)
		Orders.objects.filter(id=tid).delete()
		
		# redirect("/docshowappo")
		return HttpResponse("Requested")

	else:  #to show all appointments

		username=request.user.username
		requests=Orders.objects.filter(pharma=username,status=0,adate__isnull=False)
		proreq=Orders.objects.filter(user=username,status=1)
		list1=[]
		for i in requests:
			list1.append([(AddtionalDetails.objects.filter(username=i.user)),(AddtionalDetails.objects.filter(username=i.pharma))])

		# print(list1)
		numbers=range(1,20)

		#zip data to display
		for i in requests:
			print(i.prescription)
		data1=zip(list1,requests,numbers)
		return render(request,'dashboard/pharma/show_orders.html',{'data1':data1})

@csrf_exempt
def prescription(request):

	if request.method=='POST': #to  print prescription
		print(request.POST)
		user=request.POST.get('email')
		tid=request.POST.get('tid')
		pres=request.POST.get('pres')
		print(user,pres,tid)
		# Orders.objects.filter(id=tid).delete()
		
		return redirect("/docshowappo")
		# return render(request,'dashboard/doctor/show_appo.html')
		# return HttpResponse("Requested")

	else:  #to write prescription
		user=request.GET.get('usrid')
		tid=request.GET.get('tid')
		print(user,tid)
		list1=[]
		list1.append(AddtionalDetails.objects.filter(username=user))

		# # print(list1)
		# numbers=range(1,20)

		# #zip data to display
		# data1=zip(list1,requests,numbers)
		return render(request,'dashboard/doctor/prescription.html',{'tid':tid,'list1':list1})

@csrf_exempt
def generatebill(request):
		user=request.GET.get('usrid')
		tid=request.GET.get('tid')
		print(user,tid)
		
		userdata=AddtionalDetails.objects.get(username=user)
		prescription=Prescription.objects.filter(tid=tid)
		num=range(1,len(prescription)+1)

		data1=zip(num,prescription)
		data={
		'n':len(prescription),
		'tid':tid,		
		'userdata' : userdata,
		'data1':data1
		}
		return render(request,'dashboard/pharma/bill.html',data)

@csrf_exempt
def printbill(request):
	
	print(request.POST)


	pharma=request.user.username
	
	user=request.POST.get('email')
	tid=(request.POST.get('tid'))
	other=int(request.POST.get('other'))

	cost=request.POST.get('array')
	cost= json.loads(cost)
	cost=list(map(int,cost))
	print(user,tid)
	print("printing Array here")
	print(cost)
	# meal=request.POST.get('meal')
	prescription= Prescription.objects.filter(tid=tid)
	bill=[]
	num=0
	for i in prescription:
		meditype =i.meditype
		mediname = i.mediname
		quantity = i.quantity
		price=cost[num]
		num+=1
		bill.append([meditype,mediname,quantity,price])

	pharmadata=AddtionalDetails.objects.filter(username=pharma)
	userdata=AddtionalDetails.objects.filter(username=user)
	template_path = 'bill.html'
	total=sum(cost)+other
	context = {
		'myvar': 'this is your template context',
		'user' : userdata,
		'pharma' :pharmadata,
		'bill' : bill,
		'other' : other,
		'subtotal':sum(cost),
		'total':total
		}

	name='bill'+tid+'.pdf'
	output_filename='static/media/'+user+'/'+name

	template = get_template("bill.html")
	html = template.render(context)
	response = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response)
	Record.objects.filter(id=tid).update(bill=output_filename)
	Orders.objects.filter(tid=tid).update(bill=output_filename)
	
	if not pdf.err:
		result = open(output_filename, "w+b")
		result.write(response.getvalue())
		result.close()
	    # return HttpResponse(response.getvalue(), content_type='application/pdf')
	else:
		print("Failed to render pdf")
	    # return HttpResponse("Error Rendering PDF", status=400)


	# img_save_path =  'media/'+str(request.user.username)+'/profile'+ img_extension
	# print(userdata.name)
	#to send email of prescription
	subject, from_email, to = 'Bill Of Order', 'chs390118@gmail.com', user
	text_content = 'This is an important message.'
	html_content = '<p>Hello '+userdata[0].name+',<br>\
	Hoping you and loved ones are doing good.<br>\
	As per Your Request We have deliverd Medicines to you .\
	<br>Please Find Bill as attachment below.</p>\
	<b>Total Bill to pay :'+str(total)+'Rs.</b>'
	
	msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
	msg.attach_alternative(html_content, "text/html")
	msg.attach_file(output_filename)
	msg.send()
	# if error then show some funy view
	# if pisa_status.err:
	#    return HttpResponse('We had some errors <pre>' + html + '</pre>')
	return redirect("/docshowappo")

	# img_save_path =  'media/'+str(request.user.username)+'/profile'+ img_extension

	Record.objects.filter(id=tid).update(bill=output_filename)
	Orders.objects.filter(tid=tid).update(bill=output_filename)
	
	return redirect("/pharmashoworders")

@csrf_exempt
def render_pdf_view(request):
	
	print(request.POST)


	doctor=request.user.username
	
	user=request.POST.get('email')
	tid=(request.POST.get('tid'))
	array=request.POST.get('array')
	array= json.loads(array)
	print(user,tid)
	print("printing Array here")
	print(array)
	# meal=request.POST.get('meal')
	prescription=[]
	for i in array:
		meditype =i[0]
		mediname = i[1]
		quantity = int(i[2])
		meal=i[3]
		time=i[4]
		prescription.append([meditype,mediname,quantity,meal,time])

		p=Prescription(tid=int(tid),meditype=meditype,mediname=mediname,quantity=quantity,meal=meal,time=time)
		p.save()

	docdata=AddtionalDetails.objects.filter(username=doctor)
	userdata=AddtionalDetails.objects.filter(username=user)
	template_path = 'prescription.html'
	context = {
		'myvar': 'this is your template context',
		'user' : userdata,
		'doc' :docdata,
		'pres' : prescription
		}

	# template = get_template(template_path)
	# html = template.render(context)

	name=tid+'.pdf'
	output_filename='static/media/'+user+'/'+name

	#location to save pdf 

	# # #save pdf funtion
	# pisa_status = pisa.CreatePDF(
	#    html, dest=result_file)

	# result_file.close()

	template = get_template("prescription.html")
	html = template.render(context)
	response = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response)
	Record.objects.filter(id=tid).update(status=1,prescription=output_filename)
	
	if not pdf.err:
		result = open(output_filename, "w+b")
		result.write(response.getvalue())
		result.close()
	    # return HttpResponse(response.getvalue(), content_type='application/pdf')
	else:
		print("Failed to render pdf")
	    # return HttpResponse("Error Rendering PDF", status=400)



	#to send email of prescription
	subject, from_email, to = 'Prescription', 'chs390118@gmail.com', user
	text_content = 'This is an important message.'
	html_content = '<p>Hello '+userdata[0].name+',<br>\
	Hoping you and loved ones are doing good.<br>\
	Prescription Of your Appointment is Attached below .'
	
	msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
	msg.attach_alternative(html_content, "text/html")
	msg.attach_file(output_filename)
	msg.send()
	# if error then show some funy view
	# if pisa_status.err:
	#    return HttpResponse('We had some errors <pre>' + html + '</pre>')
	return redirect("/docshowappo")
