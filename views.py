from django.shortcuts import render
import base64
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from .models import *

@csrf_exempt
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        face_image_data = request.POST['face_image']
        print(face_image_data)
        face_image_data = face_image_data.split(",")[1]
        face_image = ContentFile(base64.b64decode(face_image_data),name=f'{username}_.jpg')
        try:
            user = user.objects.create(username=username)
        except Exception as e:
            return JsonResponse({
            'status':'error','message':'Username already taken'
        })
        UserImages.objects.create(uer=user,face_image=face_image)
        return JsonResponse({
            'status':'success','message':'User registered Sucessfully'
        })
    return render(request, 'register.html')

def login_user(request):
    if request.method=="POST":
        username=request.POST.get('username')
        face_image_data = request.POST['face_image']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({
            'status':'error','message':'invalid username'
        })
        face_image_data = face_image_data.split(",")[1]
        uploaded_image = ContentFile(base64.b64decode(face_image_data),name=f'{username}_.jpg')
        uploaded_face_image = face_recognition.load_image_file(uploaded_image)
        uploaded_face_encoding = face_recognition.face_encondings(uploaded_face_image)

        if uploaded_face_encoding:
            uploaded_face_encoding = uploaded_face_encoding[0]
            user_image = UserImages.objects.filter(user=user).last()
            stored_face_image = face_recognition.load_image_file(uploaded_image.face_image.path)
            stored_face_encoding = face_recognition.load_image_file(uploaded_image.face_image.path)
            match = face_recognition.compare_faces([stored_face_encoding],uploaded_face_encoding)
            if match[0]:
                return JsonResponse({'status':'success','message':'Logged in successfully!!'})
        return JsonResponse({'status':'error','message':'Not Logged in...'})
            
    return render(request, 'login.html')