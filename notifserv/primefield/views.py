import datetime, time
import schedule


from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response

from .models import Mailing, Clients, Messages, Status
from .forms import ClientsForm, MailingForm
from django.views.decorators.csrf import csrf_exempt
import json, requests
from .serializers import ClientsSerializer, MailingSerializer
from django.core.serializers.json import DjangoJSONEncoder
from rest_framework.views import APIView
from rest_framework import status, serializers



class Client(APIView):

    def delete(self, request):
        delete_body = request.data.get('id')
        clients = Clients.objects.get(id=delete_body)
        clients.delete()
        return HttpResponse(content={"status_delete": 0})

    def post(self, request):
        post_body = request.data
        serializers = ClientsSerializer(data=post_body)
        if serializers.is_valid():
            serializers.save()
            return HttpResponse(content={"status_post": 0}, status=status.HTTP_201_CREATED)
        return HttpResponse(content={"status_error_400": 0}, status=400)

    def put(self, request):
        put_body = request.data
        id = put_body.get('id')
        clients = Clients.objects.get(id=id)
        serializer = ClientsSerializer(clients, data=request.data, partial=True)
        if (serializer.is_valid()):
            serializer.save()
            return HttpResponse(content={"status_put": 0}, status=status.HTTP_200_OK)
        return HttpResponse(content={"status_error_400": 0}, status=400)

    def get(self, request):
        clients = Clients.objects.all().values()
        context = {
            'clients': list(clients),
            'title': 'клиенты',
        }
        return HttpResponse(content=json.dumps(context, cls=DjangoJSONEncoder))


class Mailings(APIView):

    def post(self, request):

        post_body = request.data
        start_mailing = post_body.get('start_mailing')
        finish_mailing = post_body.get('finish_mailing')
        text_message = post_body.get('text_message')
        mailing_data = {
            'start_mailing': start_mailing,
            'finish_mailing': finish_mailing,
            'text_message': text_message,
        }
        mailing_obj = Mailing.objects.create(**mailing_data)
        status_mailing = Status.objects.create(mailings_id=mailing_obj)
        self.start_messages(mailing_obj)
        # self.do_messages(mailing_obj)
        return HttpResponse(content={"status_post": 0}, status=status.HTTP_201_CREATED)
        # return HttpResponse(content={"status_error_400": 0}, status=400)

    def do_messages(self, mailing_obj):
        url = 'https://probe.fbrq.cloud/v1/send/1'
        api_requests = requests.post(url)

        clients = Clients.objects.all()
        start_m = mailing_obj.start_mailing
        finish_m = mailing_obj.finish_mailing
        time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        header = {
            'accept': 'application/json',
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDYxODQ1MDcsImlzcyI6ImZhYnJpcXVlIiwibmFtZSI6Imh0dHBzOi8vdC5tZS9OYWFWZWVRIn0.TmLDumXwhDm0hSbNHSXrrg8zjDEhQl45UNPm5c4kAi0',
            'Content-Type': 'application/json'
            }

        if start_m <= time_now <= finish_m:
            for client in clients:
                url = f'https://probe.fbrq.cloud/v1/send/{client.id}'
                api_requests = requests.post(url, headers=header, json={'id': client.id, 'phone': str(client.phone),
                                                                        'text': mailing_obj.text_message})
                messages_obj = Messages.objects.create(time_maling=time_now, id_clients=client, id_mailing=mailing_obj)
                print(api_requests.json())
                print(client.phone)
                print(mailing_obj.text_message)
        else:
            for client in clients:
                messages_obj = Messages.objects.create(status=1, time_maling=time_now,
                                                       id_clients=client, id_mailing=mailing_obj)

                print('не время отправлять!')


    def start_messages(self, mailing_obj):
        schedule.every().minute.do(self.do_messages, mailing_obj=mailing_obj)

        while True:
            print('work')
            st_m = Status.objects.get(mailings_id=mailing_obj)
            if not st_m:
                print('break')
                break
            schedule.run_pending()
            time.sleep(30)


    def delete(self, request):
        delete_body = request.data.get('id')
        mailings = Mailing.objects.get(id=delete_body)
        mailings.delete()
        return HttpResponse(content={"status_delete": 0})


    def put(self, request):
        put_body = request.data
        id = put_body.get('id')
        mailing = Mailing.objects.get(id=id)
        serializer = MailingSerializer(mailing, data=request.data, partial=True)
        if (serializer.is_valid()):
            serializer.save()
            return HttpResponse(content={"status_put": 0}, status=status.HTTP_200_OK)
        return HttpResponse(content={"status_error_400": 0}, status=400)


    def get(self, request):
        mailing = Mailing.objects.all().values()
        context = {
            'clients': list(mailing),
            'title': 'Рассылки',
        }
        return HttpResponse(content=json.dumps(context, cls=DjangoJSONEncoder))
