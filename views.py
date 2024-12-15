from django.http import JsonResponse  
from django.contrib.auth.models import User  
def get_user(request):
   
    
    user_id = request.GET.get('id')  

    
    if user_id:  
        user_id = user_id.strip()  
        if user_id.isdigit():  
            user_id = int(user_id)  
            
            
            user = User.objects.filter(id=user_id).first()  
            
            if user:  
                return JsonResponse({
                    'username': user.username,
                    'email': user.email
                })
            else:  
                return JsonResponse({'error'})
    
    
    return JsonResponse({'error'})