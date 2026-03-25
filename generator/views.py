from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .utils import generate_listing, describe_image

def landing(request):
    if request.user.is_authenticated:
        return redirect('generator:app_view')
    return render(request, 'generator/landing.html')

@login_required
def app_view(request):
    profile = request.user.profile
    if profile.listing_count >= 3 and profile.plan == 'free':
        return redirect('generator:upgrade_view')
        
    context = {
        'listing_count': profile.listing_count,
        'remaining': max(0, 3 - profile.listing_count),
    }

    if request.method == 'POST':
        prop_type = request.POST.get('prop_type')
        area = request.POST.get('area')
        floor = request.POST.get('floor')
        location = request.POST.get('location')
        price = request.POST.get('price')
        facing = request.POST.get('facing')
        language = request.POST.get('language')
        amenities = request.POST.getlist('amenities')
        photo = request.FILES.get('photo')
        
        photo_description = ""
        if photo:
            photo_bytes = photo.read()
            photo_description = describe_image(photo_bytes, photo.content_type)
            
        details = {
            "type": prop_type, "location": location.strip(), "area": area.strip(),
            "price": price.strip(), "floor": floor.strip() if floor else "Not specified",
            "facing": facing, "amenities": amenities, "photo_description": photo_description
        }
        
        result = generate_listing(details, language=language)
        
        if not result.startswith("Error:"):
            profile.listing_count += 1
            profile.save()
            
        parts = result.split("---WHATSAPP---")
        full_listing = parts[0].strip()
        if len(parts) > 1:
            rest = parts[1].split("---EMAIL---")
            whatsapp_msg = rest[0].strip()
            email_template = rest[1].strip() if len(rest) > 1 else full_listing
        else:
            whatsapp_msg = full_listing
            email_template = full_listing
            
        context['result'] = True
        context['full_listing'] = full_listing
        context['whatsapp_msg'] = whatsapp_msg
        context['email_template'] = email_template
        context['listing_count'] = profile.listing_count
        context['remaining'] = max(0, 3 - profile.listing_count)

    context['amenities_list'] = [
        "Covered parking", "Gym", "Swimming pool", "24hr security", "Lift / Elevator",
        "Power backup", "Garden / Terrace", "CCTV", "Clubhouse", "Children play area",
        "Jogging track", "Intercom", "Solar panels", "Rainwater harvesting", "EV charging"
    ]

    return render(request, 'generator/app_view.html', context)

@login_required
def upgrade_view(request):
    return render(request, 'generator/upgrade.html')
