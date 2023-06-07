from django.contrib.auth.models import Group

def custom_context(request):
    user = request.user

    pañol_visible = False
    if user.is_authenticated and Group.objects.filter(user=user, name='pañol').exists():
        pañol_visible = True

    tecnicos_visible = False
    if user.is_authenticated and Group.objects.filter(user=user, name='tecnicos').exists():
        tecnicos_visible = True
    
    oficina_visible = False
    if user.is_authenticated and Group.objects.filter(user=user, name='oficina').exists():
        oficina_visible = True


    return {
        'pañol_visible': pañol_visible,
        'tecnicos_visible': tecnicos_visible,
        'oficina_visible':oficina_visible
    }
