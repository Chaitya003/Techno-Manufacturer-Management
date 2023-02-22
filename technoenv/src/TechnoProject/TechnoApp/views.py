from django.shortcuts import render
from TechnoApp.models import *
from django.core import serializers
from django.db.models import Count
from django.db.models import Min

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

import json
import math
from decimal import *
from datetime import datetime




from django.contrib.auth import logout, authenticate, login
# Create your views here.

class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return

def LogIn(request):
    return render(request, 'login.html')

class LogInSubmitAPI(APIView):

    authentication_classes = (
           CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, *args, **kwargs):

       response = {}
       response['status'] = 500
       try:

           data = request.data

           username = data['username']
           password = data['password']

           user = authenticate(username=username, password=password)

           login(request, user)

           usertype = TechnoUser.objects.get(username=username).user_type
           response['usertype']=usertype
           response['status'] = 200

       except Exception as e:
           print("Error while logging in!", str(e))

       return Response(data=response)

def Store(request):
    context = {
        'pipe_alloy': list(AlloyMaster.objects.filter(alloy_class='PIPE')),
        'mgo_alloy': list(AlloyMaster.objects.filter(alloy_class='MGO')),
        'conductor_alloy': list(AlloyMaster.objects.filter(alloy_class='CONDUCTOR'))
    }
    return render(request, 'store.html',context)

## Pipe
class FetchElementMappingPipeAPI(APIView):
    authentication_classes = (
           CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, *args, **kwargs):

       response = {}
       response['status'] = 500
       response['error-msg'] = ""
       try:

           data = request.data
           alloy_obj = AlloyMaster.objects.get(alloy_name=data['alloy'])
           mapping_obj = list(PipeAlloyElementMappingMaster.objects.filter(alloy_obj=alloy_obj).values())
           response['alloy_element_mapping'] = mapping_obj
           response['status'] = 200

       except Exception as e:
           response['error-msg']="Error while fetching the element mapping for the alloy you selected!"
           print(response['error-msg'], str(e))

       return Response(data=response)

class SavePipeAPI(APIView):
    authentication_classes = (
           CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, *args, **kwargs):

       response = {}
       response['status'] = 500
       try:
           data = request.data
           already_exists = False
           error_msg = "Error while saving the information for pipe."
           lot_number = data["lotnumber"]
           supplier_name = data["suppliername"]
           alloy_name=data["alloyname"]
           alloy_elements=json.loads(data["alloyelements"])
           print(data)
           quantity = data["quantity"]
           diameter = data["diameter"]
           existing_pipe_obj = Pipe.objects.filter(lot_number=lot_number)
           if len(existing_pipe_obj)>0:
               already_exists = True
               error_msg = "There is already a pipe with this lot number. You can not save it again."
               raise Exception(error_msg)
               
           alloy_obj = AlloyMaster.objects.get(alloy_name=alloy_name)
           pipe_obj = Pipe.objects.create(lot_number=lot_number,qty=math.floor(float(quantity)) ,supplier_name=supplier_name,alloy_obj=alloy_obj, diameter=float(diameter))
           for mapping in alloy_elements:
               element_obj = ElementMaster.objects.get(metal_code=mapping['id'])
               pipe_alloy_elements = PipeAlloyElementQuantity.objects.create(pipe_obj=pipe_obj,element_obj=element_obj, quantity=mapping['value'])    
               
           response['status'] = 200
            
       except Exception as e:
           response["error-msg"] = error_msg
           if not already_exists:
               delete_pipe_obj = Pipe.objects.filter(lot_number=lot_number)
               delete_pipe_obj.delete()
           print(error_msg, str(e))

       return Response(data=response)     


## Conductor
class FetchElementMappingConductorAPI(APIView):
    authentication_classes = (
           CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, *args, **kwargs):

       response = {}
       response['status'] = 500
       response['error-msg'] = ""
       try:

           data = request.data
           alloy_obj = AlloyMaster.objects.get(alloy_name=data['alloy'])
           mapping_obj = list(ConductorAlloyElementMappingMaster.objects.filter(alloy_obj=alloy_obj).values())
           response['alloy_element_mapping'] = mapping_obj
           response['status'] = 200

       except Exception as e:
           response['error-msg']="Error while fetching the element mapping for the alloy you selected!"
           print(response['error-msg'], str(e))

       return Response(data=response) 


class SaveConductorAPI(APIView):
    authentication_classes = (
           CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, *args, **kwargs):

       response = {}
       response['status'] = 500
       try:
           data = request.data
           already_exists = False
           error_msg = "Error while saving the information for conductor."
           lot_number = data["lotnumber"]
           supplier_name = data["suppliername"]
           alloy_name=data["alloyname"]
           alloy_elements=json.loads(data["alloyelements"])
           print(alloy_elements)
           quantity = data["quantity"]
           diameter = data["diameter"]
           existing_conductor_obj = Conductor.objects.filter(lot_number=lot_number)
           if len(existing_conductor_obj)>0:
               already_exists = True
               error_msg = "There is already an conductor with this lot number. You can not save it again."
               raise Exception(error_msg)
               
           alloy_obj = AlloyMaster.objects.get(alloy_name=alloy_name)
           conductor_obj = Conductor.objects.create(lot_number=lot_number,qty=float(quantity) ,supplier_name=supplier_name,alloy_obj=alloy_obj, diameter=float(diameter))
           for mapping in alloy_elements:
               if(alloy_name=="Nickel" or alloy_name=="Copper"):
                element_obj = ElementMaster.objects.get(metal_code=mapping['id'])
                conductor_alloy_elements = ConductorAlloyElementQuantity.objects.create(conductor_obj=conductor_obj,element_obj=element_obj, positive_quantity=mapping['positive_value'])    
               else:
                element_obj = ElementMaster.objects.get(metal_code=mapping['id'])
                conductor_alloy_elements = ConductorAlloyElementQuantity.objects.create(conductor_obj=conductor_obj,element_obj=element_obj, positive_quantity=mapping['positive_value'],negative_quantity=mapping['negative_value'])    
           response['status'] = 200
            
       except Exception as e:
           response["error-msg"] = error_msg
           if not already_exists:
               delete_conductor_obj = Conductor.objects.filter(lot_number=lot_number)
               delete_conductor_obj.delete()
           print(error_msg, str(e))

       return Response(data=response)              

## MGO
class FetchElementMappingMGOAPI(APIView):
    authentication_classes = (
           CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, *args, **kwargs):

       response = {}
       response['status'] = 500
       response['error-msg'] = ""
       try:

           data = request.data
           alloy_obj = AlloyMaster.objects.get(alloy_name=data['alloy'])
           mapping_obj = list(MGOAlloyElementMappingMaster.objects.filter(alloy_obj=alloy_obj).values())
           response['alloy_element_mapping'] = mapping_obj
           response['status'] = 200

       except Exception as e:
           response['error-msg']="Error while fetching the element mapping for the alloy you selected!"
           print(response['error-msg'], str(e))

       return Response(data=response)

class SaveMGOAPI(APIView):
    authentication_classes = (
           CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, *args, **kwargs):

       response = {}
       response['status'] = 500
       try:
           data = request.data
           already_exists = False
           error_msg = "Error while saving the information for mgo."
           lot_number = data["lotnumber"]
           supplier_name = data["suppliername"]
           alloy_name=data["alloyname"]
           alloy_elements=json.loads(data["alloyelements"])
           print(alloy_elements)
           quantity = data["quantity"]
           existing_mgo_obj = MGO.objects.filter(lot_number=lot_number)
           if len(existing_mgo_obj)>0:
               already_exists = True
               error_msg = "There is already an mgo with this lot number. You can not save it again."
               raise Exception(error_msg)
               
           alloy_obj = AlloyMaster.objects.get(alloy_name=alloy_name)
           mgo_obj = MGO.objects.create(lot_number=lot_number,qty=float(quantity) ,supplier_name=supplier_name,alloy_obj=alloy_obj)
           for mapping in alloy_elements:
               element_obj = ElementMaster.objects.get(metal_code=mapping['id'])
               mgo_alloy_elements = MGOAlloyElementQuantity.objects.create(mgo_obj=mgo_obj,element_obj=element_obj, quantity=mapping['value'])    
               
           response['status'] = 200
            
       except Exception as e:
           response["error-msg"] = error_msg
           if not already_exists:
               delete_mgo_obj = MGO.objects.filter(lot_number=lot_number)
               delete_mgo_obj.delete()
           print(error_msg, str(e))

       return Response(data=response) 

## Coil
def Production(request):
   
    context = {
        'item': list(ItemMaster.objects.all()),
        'pipe_lotnumber': list(Pipe.objects.filter(qty__gte=1)),
        'mgo_lotnumber': list(MGO.objects.filter(qty__gt=0)),
        'conductor_lotnumber': list(Conductor.objects.filter(qty__gt=0)),
        'coil_list':list(Coil.objects.filter(coil_diameter__isnull=True)),
        'drawbenches':list(DrawBenchMaster.objects.all()),
        'furnaces':list(FurnaceMaster.objects.all())
    }
    return render(request, 'production.html', context)

class StartCoilProductionAPI(APIView):
    authentication_classes = (
           CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, *args, **kwargs):

       response = {}
       response['status'] = 500
       try:
           data = request.data
           already_exists = False
           error_msg = ""
           coil=data["coil"]
           item=data["item"]
           pipe_lotnumber=data["pipeLotNumber"]
           pipe_qty=int(data["pipeQty"])
           conductor_lotnumber=data["conductorLotNumber"]
           conductor_qty=Decimal(data["conductorQty"])
           mgo_lotnumber=data["mgoLotNumber"]
           mgo_qty=Decimal(data["mgoQty"])

           existing_coil_obj = Coil.objects.filter(coil_number=coil)
           if len(existing_coil_obj)>0:
               already_exists = True
               error_msg="There is already a coil with this coil number. You can not save it again."
               raise Exception(error_msg)
               
           pipe_obj = Pipe.objects.get(lot_number=pipe_lotnumber)
           pipe_remainder = pipe_obj.qty - pipe_qty

           conductor_obj = Conductor.objects.get(lot_number=conductor_lotnumber)
           conductor_remainder = conductor_obj.qty - conductor_qty

           mgo_obj = MGO.objects.get(lot_number=mgo_lotnumber)
           mgo_remainder = mgo_obj.qty - mgo_qty

           item_obj = ItemMaster.objects.get(item_code=item)
           
           if(pipe_remainder<0):
               error_msg = "The available quantity for pipe with lot number "+pipe_lotnumber + " is "+ str(pipe_obj.qty)+ ". You can't specify quantity more than this.\n"

           if (conductor_remainder<0):
               error_msg += "The available quantity for conductor with lot number "+conductor_lotnumber + " is "+ str(conductor_obj.qty )+ ". You can't specify quantity more than this.\n"

           if(mgo_remainder<0):
               error_msg += "The available quantity for mgo with lot number "+mgo_lotnumber + " is "+ str(mgo_obj.qty)+ ". You can't specify quantity more than this.\n"      

           if(error_msg!=""):
               raise Exception(error_msg)
     
           error_msg="Error while saving the information for Coil."

           pipe_obj.qty = pipe_obj.qty - pipe_qty
           conductor_obj.qty = conductor_obj.qty - conductor_qty
           mgo_obj.qty = mgo_obj.qty - mgo_qty
           

           coil_obj = Coil.objects.create(coil_number=coil, item_obj=item_obj, pipe_obj=pipe_obj, pipe_qty=pipe_qty, mgo_obj=mgo_obj, mgo_qty=mgo_qty, conductor_obj=conductor_obj, conductor_qty=conductor_qty)
        
           coil_obj.save()
           pipe_obj.save()
           conductor_obj.save()
           mgo_obj.save()
           

           response['status'] = 200
            
       except Exception as e:
           print(e)
           response["error-msg"] = error_msg
           if not already_exists:
               delete_coil_obj = Coil.objects.filter(coil_number=coil)
               delete_coil_obj.delete()
           print(error_msg)

       return Response(data=response)

class FetchCoilStatusAPI(APIView):
    authentication_classes = (
           CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, *args, **kwargs):

       response = {}
       response['status'] = 500
       try:
           data = request.data
           coil=data["coil"]
           error_msg="Error while fetching the status for Coil."

           coil_obj = Coil.objects.get(coil_number=coil)
           coil_status_obj=CoilStatus.objects.filter(coil_number=coil_obj)
           

           if(len(coil_status_obj)==0):
               coil_status="DRAW"
               started_flag="NO"
               can_move_QA="NO"
           elif(len(coil_status_obj)%2==1):
               if(len(coil_status_obj.filter(end_time__isnull=True))==1):
                   coil_status="DRAW"
                   started_flag="YES"
                   can_move_QA="NO"
               else:
                   coil_status="ANNEALING"
                   started_flag="NO"
                   can_move_QA="NO" 
           else:
               if(len(coil_status_obj.filter(end_time__isnull=True))==1):        
                   coil_status="ANNEALING"
                   started_flag="YES"
                   can_move_QA="NO"
               else:
                   coil_status="DRAW"
                   started_flag="NO"
                   can_move_QA="YES"
          

           response["coil_status"]=coil_status
           response["started_flag"]=started_flag
           response["can_move_QA"]=can_move_QA 
        
           

           response['status'] = 200
            
       except Exception as e:
           print(e)
           response["error-msg"] = error_msg
           print(error_msg)

       return Response(data=response)         

class StartProcessForCoilAPI(APIView):
    authentication_classes = (
           CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, *args, **kwargs):

       response = {}
       response['status'] = 500
       try:
           error_msg="Error while saving coil information."
           data = request.data
           coil=data["coil"]
           status=data["status"]
           machine=data["machine"]

           coil_obj = Coil.objects.get(coil_number=coil) 
           start_time= datetime.now()
           if(status=="DRAW"):
            draw_bench_obj=DrawBenchMaster.objects.get(draw_bench_name=machine)   
            coil_status_obj = CoilStatus.objects.create(coil_number=coil_obj,start_time=start_time,status_class=status,draw_bench_name=draw_bench_obj)
            coil_status_obj.save()
           else:
            furnace_obj=FurnaceMaster.objects.get(furnace_name=machine)   
            coil_status_obj = CoilStatus.objects.create(coil_number=coil_obj,start_time=start_time,status_class=status,furnace_name=furnace_obj)
            coil_status_obj.save()

           response['status'] = 200
            
       except Exception as e:
           print(e)
           response["error-msg"] = error_msg
           print(error_msg)

       return Response(data=response) 

class StopProcessForCoilAPI(APIView):
    authentication_classes = (
           CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, *args, **kwargs):

       response = {}
       response['status'] = 500
       try:
           error_msg="Error while saving coil information."
           data = request.data
           coil=data["coil"]
           status=data["status"]
           diameter=Decimal(data["diameter"])

           coil_obj = Coil.objects.get(coil_number=coil)
           coil_status_obj= CoilStatus.objects.filter(coil_number=coil_obj)
           end_time= datetime.now()

           if(len(coil_status_obj)==1):
               if(coil_obj.pipe_obj.diameter <= diameter):
                   error_msg="The diameter after draw should be lesser than "+str(coil_obj.pipe_obj.diameter)+"."
                   raise Exception(error_msg)
               else:
                   current_status_obj=coil_status_obj.filter(status_class="DRAW").filter(end_time__isnull=True)[0]
                   current_status_obj.end_time=end_time
                   current_status_obj.coil_diameter=diameter
                   current_status_obj.save()
           elif(status=="DRAW"):
                current_draw_diameter=coil_status_obj.filter(status_class="DRAW").aggregate(Min('coil_diameter'))['coil_diameter__min']
                if(current_draw_diameter <= diameter):
                   error_msg="The diameter after draw should be lesser than "+str(current_draw_diameter)+" as per the last draw."
                   raise Exception(error_msg)
                else:
                   current_status_obj=coil_status_obj.filter(status_class="DRAW").filter(end_time__isnull=True)[0]
                   current_status_obj.end_time=end_time
                   current_status_obj.coil_diameter=diameter
                   current_status_obj.save()
           elif(status=="ANNEALING"):
                current_draw_diameter=coil_status_obj.filter(status_class="DRAW").aggregate(Min('coil_diameter'))['coil_diameter__min']
                if(current_draw_diameter != diameter):
                   error_msg="The diameter after draw should be equal to "+str(current_draw_diameter)+" as per the last draw."
                   raise Exception(error_msg)
                else:
                   current_status_obj=coil_status_obj.filter(status_class="ANNEALING").filter(end_time__isnull=True)[0]
                   current_status_obj.end_time=end_time
                   current_status_obj.coil_diameter=diameter
                   current_status_obj.save()


           response['status'] = 200
            
       except Exception as e:
           print(e)
           response["error-msg"] = error_msg
           print(error_msg)

       return Response(data=response)          

class EndCoilProductionAPI(APIView):
    authentication_classes = (
           CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, *args, **kwargs):

       response = {}
       response['status'] = 500
       try:
           data = request.data
           error_msg = "Error while saving the information for mgo."
           coil_number = data["coil"]
           coil_obj = Coil.objects.get(coil_number=coil_number)
           final_coil_diameter=CoilStatus.objects.filter(coil_number=coil_obj).filter(status_class="ANNEALING").aggregate(Min('coil_diameter'))['coil_diameter__min']
           coil_obj.coil_diameter=final_coil_diameter
           coil_obj.save()

           response['status'] = 200
            
       except Exception as e:
           data["error-msg"] = error_msg
           print(error_msg, str(e))

       return Response(data=response)


LogInSubmit = LogInSubmitAPI.as_view()
FetchElementMappingPipe = FetchElementMappingPipeAPI.as_view()
SavePipe = SavePipeAPI.as_view()
FetchElementMappingConductor = FetchElementMappingConductorAPI.as_view()
SaveConductor = SaveConductorAPI.as_view()
FetchElementMappingMGO = FetchElementMappingMGOAPI.as_view()
SaveMGO = SaveMGOAPI.as_view()
StartCoilProduction = StartCoilProductionAPI.as_view()
FetchCoilStatus = FetchCoilStatusAPI.as_view()
StartProcessForCoil = StartProcessForCoilAPI.as_view()
StopProcessForCoil=StopProcessForCoilAPI.as_view()
EndCoilProduction = EndCoilProductionAPI.as_view()