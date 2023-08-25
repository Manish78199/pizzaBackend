import os
from django.shortcuts import render
import json
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from django.core import serializers	

import jwt  
from .models import Vendor,Product,Cart,User
import razorpay



# vendor serialier for 
class VendorSer(serializers.ModelSerializer):
    class Meta:
        model=Vendor
        fields='__all__'
        
class ProductSer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields='__all__'
                
tokenHeader={  
  "alg": "HS256",  
  "typ": "JWT"  
}    

tokenSecret="manishpawlikhurd@gmail.com"
      
# Create your views here.

# create order id from razorpay

@api_view(["POST"])
def OrderApi(request):
	global client
	data=json.loads(request.body)["data"]
	amount=int(data["amount"])
 
	
 client=razorpay.Client(auth=("key_id","secret_key"))
	data={"amount":amount,"currency":"INR"}
	payment=client.order.create(data=data)
	print(payment)
	return Response({"order_id":payment["id"],"amount":payment["amount"],"status":payment["status"]})

@api_view(['POST'])

# verify payment

def verifySignature(request):
    res = json.loads(request.body)["data"]
    
    params_dict = {
        'razorpay_payment_id' : res['razorpay_paymentId'],
        'razorpay_order_id' : res['razorpay_orderId'],
        'razorpay_signature' : res['razorpay_signature']
    }

    # verifying the signature
    res = client.utility.verify_payment_signature(params_dict)

    if res == True:
        return Response({'status':'Payment Successful'})
    return Response({'status':'Payment Failed'})








def index(request):
	return HttpResponse("oj")

# user ogin

@api_view(["POST"])
def userlogin(request):
	data=json.loads(request.body)
	user_email=data["email"]
	user_password=data["password"]
	checkuser=User.objects.filter(user_email=user_email).values()[0]
   
	if len(checkuser)>0:
		payload={"email":checkuser["user_email"]}
		token=jwt.encode(payload, tokenSecret, algorithm='HS256', headers=tokenHeader) 
		print(token)
		return Response({"success":"login successfully","user":{"username":checkuser["user_name"],"token":token}})
	else:
		return Response({"error":"acount already exists"})

# handle user
@api_view(["GET","POST"])
def myuser(request):
	if request.method=="GET":
		
		token=request.headers["Token"]
		user=jwt.decode(token, tokenSecret, algorithms=['HS256']) 
		
		checkuser=User.objects.filter(user_email=user["email"]).values()[0]
		if len(checkuser)>0:
			return Response({"success":"your details","username":checkuser["user_name"]})
		else:
			return Response({"error":"acount not exists"})



	if request.method=="POST":
		data=json.loads(request.body)
		user_name=data["name"]
		user_email=data["email"]
		user_password=data["password"]
		checkuser=User.objects.filter(user_email=user_email)
		print(checkuser)
		if len(checkuser)>0:
			return Response({"error":"acount already exists"})
		else:
			passhash=user_password
			try:
				newuser=User(user_name=user_name,user_email=user_email,user_password=passhash)
				newuser.save()
				newcart=Cart(user=newuser,items=json.dumps({[]}))
				return Response({"status":"acount successfully created"})
			except Exception as e:
				print(e)
				return Response({"error":"internal error please try after some time"})
	
@api_view(["POST"])
def vendorLogin(request):
	user=json.loads(request.body)
	# print(user)/
	if request.method=="POST":
		ven=Vendor.objects.filter(user_email__exact=user["email"],user_password__exact=user["password"])[0]
		print(ven.user_email)		
		payload={"email":ven.user_email}
		token=jwt.encode(payload, tokenSecret, algorithm='HS256', headers=tokenHeader) 
		
		return Response({"reslt":{"name":ven.user_name,"token":token}})
	else:
	 return HttpResponse("not permitted")

# vendor product add delete  etc
@api_view(["POST","DELETE"])
def vendor(request):
	token=request.headers["Vtoken"]
	user_email=jwt.decode(token, tokenSecret, algorithms=['HS256'])["email"]	
	if request.method=="POST":
		pname,pcat,pdet,pprice=request.POST["product_name"],request.POST["product_category"],request.POST["product_details"],request.POST["product_price"]
		if pname and pcat and pdet and pprice:
			if Vendor.objects.filter(user_email=user_email).exists():
				newprod=Product(product_name=pname,product_category=pcat,product_details=pdet,product_price=pprice,product_image=request.FILES["product_image"])
			else:
				return Response({"error":"you are not authorized to add producut"})
			try:
				newprod.save()
				print(newprod)
				return Response({"success":"product  successfully saved"})
			except:
				return Response({"error":"internal server errot"})
			
		else:
			return Response({"error":"all field must be fill"})
        
		# proddetails=json.loads(request.body)
		print(request.FILES)
	if request.method=="DELETE":

		pid=json.loads(request.body)["id"]
		if pid:
			try:
				
				if Vendor.objects.filter(user_email=user_email).exists():
					prod=Product.objects.get(id=pid)
					if len(prod.product_image)>0:
						os.remove(prod.product_image.path)
					if prod:
						prod.delete()
						return Response({"success":"product succesfully deleted "})
					else:
						return Response({"error":"product not found"})
				else:
					return Response({"error":"you are not authorized to add producut"})

			except Exception as ex :
				print(ex)
				return Response({"error":"internal error"})
		else:
			return Response({"error":"please choose a product to delete"})
	return HttpResponse("invalid request")

@api_view(["GET"])
def allprod(request):
    
	allp=Product.objects.all().order_by("product_name","product_details","product_price","product_category","product_image")
	print("without ",allp)
	result=ProductSer(allp,many=True)
	print("with",result.data)
	return Response({"success":result.data})

@api_view(["GET"])
def prod(request,id):
	allp=Product.objects.filter(id=id).order_by("product_name","product_details","product_price","product_category","product_image")
	
	result=ProductSer(allp,many=True)
	print("with",result.data)
	return Response({"success":result.data})


# handle cart in backend 

class cartSerializer(serializers.ModelSerializer):
    model=Cart
    fields='__all__'

@api_view(["GET","PUT"])
def mycart(request):
	if not request.headers["Token"]:
		return Response({"you are not login":result})
	token=request.headers["Token"]
	print("token :",token)
	user_email=jwt.decode(token, tokenSecret, algorithms=['HS256'])["email"]	
	print("user:",user_email)
	if request.method=="GET":
		items=json.loads(Cart.objects.filter(user__user_email=user_email).values()[0]["items"])
		
		result=[]
		for id in items.keys():
			prod=ProductSer(Product.objects.filter(id=id),many=True)
			if len(prod.data)>0:
				result.append({"product":prod.data[0],"quantity":items[id]})
		return Response({"mycart":result})

	if request.method=="PUT":
		newitems=json.loads(request.body)["items"]
		items2=Cart.objects.filter(user__user_email=user_email)[0]
		items2.items=json.dumps(newitems)
		items2.save()
		print(newitems.keys())  
		result=[]
		for id in newitems.keys():
			prod=ProductSer(Product.objects.filter(id=id),many=True)
			if len(prod.data)>0:
				result.append({"product":prod.data[0],"quantity":newitems[id]})
		return Response({"mycart":result})
def index(request):
    
	return HttpResponse("tezst")