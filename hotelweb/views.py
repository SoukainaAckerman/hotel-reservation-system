from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Room, Booking, RoomType
from datetime import datetime
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.utils import timezone
from signup.models import User
from hotelweb.models import RoomType

# Create your views here.

# Vues pour les réservations
def booking_page(request):
    message = None
    available_rooms = []
    selected_type = request.POST.get('room_type')
    check_in = request.POST.get('check_in_date')
    check_out = request.POST.get('check_out_date')
    room_selected = request.POST.get('room_number')
    user_id = request.session.get('user_id')
    user = None
    if user_id:
        from signup.models import User
        user = User.objects.filter(id=user_id).first()
        # Debug: if user_id is an email, try to fetch by email
        if user is None and '@' in str(user_id):
            user = User.objects.filter(email=user_id).first()
            # Optionally, update session to store the correct user id
            if user:
                request.session['user_id'] = user.id

    # Handle booking cancellation
    if request.method == 'POST' and 'cancel_booking' in request.POST:
        cancel_id = request.POST.get('cancel_booking_id')
        if cancel_id:
            try:
                booking = Booking.objects.get(id=cancel_id)
                if booking.status == 'confirmed':
                    booking.status = 'annulee'
                    booking.save()
                    message = "Votre réservation a été annulée avec succès."
            except Booking.DoesNotExist:
                message = "Réservation introuvable."
        return redirect('hotelweb:booking')

    # Handle room availability check
    if request.method == 'POST' and 'check_availability' in request.POST:
        if selected_type and check_in and check_out:
            # Affiche toutes les chambres actives du type sélectionné, triées par numéro croissant
            rooms = Room.objects.filter(room_type__name=selected_type, is_active=True).order_by('room_number')
            for room in rooms:
                overlap = Booking.objects.filter(
                    room=room,
                    status='confirmed',
                    check_out_date__gt=check_in,
                    check_in_date__lt=check_out
                ).exists()
                available_rooms.append({
                    'room_number': room.room_number,
                    'status': 'indisponible' if overlap else 'disponible'
                })

    # Handle room booking
    elif request.method == 'POST' and 'book_room' in request.POST:
        # Réserver la chambre sélectionnée
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        gender = request.POST.get('gender')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        try:
            room = Room.objects.get(room_number=room_selected, room_type__name=selected_type)
        except Room.DoesNotExist:
            message = "Chambre introuvable."
        else:
            overlap = Booking.objects.filter(
                room=room,
                status='confirmed',
                check_out_date__gt=check_in,
                check_in_date__lt=check_out
            ).exists()
            if overlap:
                message = f"La chambre {room_selected} n'est pas disponible pour ces dates."
            else:
                from signup.models import User
                user = User.objects.filter(id=user_id).first() if user_id else None
                # Calculate total price based on number of nights and room price
                check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
                check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()
                nights = (check_out_date - check_in_date).days
                total_price = float(room.room_type.price_per_night) * nights
                # Create the booking with calculated total price
                booking = Booking.objects.create(
                    user=user,
                    room=room,
                    check_in_date=check_in,
                    check_out_date=check_out,
                    status='confirmed',
                    guest_first_name=first_name,
                    guest_last_name=last_name,
                    guest_gender=gender,
                    guest_phone=phone,
                    guest_email=email,
                    total_price=total_price
                )
                message = f"La chambre {room_selected} a été réservée avec succès !"
                last_booking_id = booking.id

    else:
        last_booking_id = None

    # Afficher les réservations de l'utilisateur connecté
    user_bookings = []
    if user:
        user_bookings = Booking.objects.filter(user=user).order_by('-booking_date')

    context = {
        'message': message,
        'available_rooms': available_rooms,
        'selected_type': selected_type,
        'check_in': check_in,
        'check_out': check_out,
        'user_bookings': user_bookings,
        'last_booking_id': last_booking_id if 'last_booking_id' in locals() else None,
    }
    return render(request, 'booking.html', context)

def booking_list(request):
    """Vue pour la liste des réservations"""
    context = {
        'page_title': 'Réservations',
        'active_tab': 'booking'
    }
    return render(request, 'booking_list.html', context)

def booking_create(request):
    """Vue pour créer une nouvelle réservation"""
    if request.method == 'POST':
        # Logique pour créer une réservation
        pass
    return render(request, 'booking_create.html')

# Vues pour les chambres
def room_page(request):
    # Récupère dynamiquement les 6 types principaux avec leur prix et description
    main_types = [
        'Superior Room',
        'Deluxe Room',
        'Family Room',
        'Executive Room',
        'Ocean View Room',
        'Standard Room',
    ]
    room_types = RoomType.objects.filter(name__in=main_types)
    
    # Déboguer : afficher les prix des chambres dans les logs
    print("Types de chambres et prix dans room_page:")
    for rt in room_types:
        print(f"{rt.name}: {rt.price_per_night}$")
    
    # Créer un dictionnaire structuré comme dans welcome
    room_types_dict = {}
    for rt in room_types:
        key = rt.name.replace(' ', '_')
        room_types_dict[key] = {
            'name': rt.name,
            'price_per_night': rt.price_per_night,
            'description': rt.description
        }
    
    return render(request, 'room.html', {'room_types_dict': room_types_dict})

def room_list(request):
    """Vue pour la liste des chambres"""
    context = {
        'page_title': 'Nos Chambres',
        'active_tab': 'room'
    }
    return render(request, 'room_list.html', context)

def room_detail(request, room_id):
    """Vue pour les détails d'une chambre"""
    context = {
        'room_id': room_id
    }
    return render(request, 'room_detail.html', context)

@login_required
def booking(request):
    room_types = RoomType.objects.all()
    user_id = request.session.get('user_id')
    user = None
    if user_id:
        from signup.models import User
        user = User.objects.filter(id=user_id).first()
    if user:
        user_bookings = Booking.objects.filter(user=user).order_by('-booking_date')
    else:
        user_bookings = []
    context = {
        'room_types': room_types,
        'user_bookings': user_bookings,
    }
    return render(request, 'booking.html', context)

def check_room_availability(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        check_in = datetime.strptime(data['check_in'], '%Y-%m-%d').date()
        check_out = datetime.strptime(data['check_out'], '%Y-%m-%d').date()
        room_type = data.get('room_type')

        # Get all rooms of the specified type
        rooms = Room.objects.filter(room_type__name=room_type) if room_type else Room.objects.all()
        
        # Get all bookings that overlap with the requested dates
        unavailable_rooms = Booking.objects.filter(
            room__in=rooms,
            status='confirmed',
            check_out_date__gt=check_in,
            check_in_date__lt=check_out
        ).values_list('room_id', flat=True)

        # Prepare room availability data
        availability_data = []
        for room in rooms:
            availability_data.append({
                'room_number': room.room_number,
                'floor': room.get_floor_display(),
                'is_available': room.id not in unavailable_rooms,
                'room_type': room.room_type.name,
                'price': str(room.room_type.price_per_night)
            })

        return JsonResponse({'rooms': availability_data})
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def create_booking(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            required_fields = ['room_number', 'check_in_date', 'check_out_date', 'first_name', 'last_name', 'gender', 'phone', 'email']
            for field in required_fields:
                if not data.get(field):
                    return JsonResponse({'success': False, 'error': f'Missing required field: {field}'}, status=400)
            try:
                room = Room.objects.get(room_number=data['room_number'])
            except Room.DoesNotExist:
                return JsonResponse({'success': False, 'error': f'Room {data["room_number"]} not found'}, status=404)
            try:
                check_in = datetime.strptime(data['check_in_date'], '%Y-%m-%d').date()
                check_out = datetime.strptime(data['check_out_date'], '%Y-%m-%d').date()
            except ValueError:
                return JsonResponse({'success': False, 'error': 'Invalid date format. Use YYYY-MM-DD'}, status=400)
            if check_in >= check_out:
                return JsonResponse({'success': False, 'error': 'Check-out date must be after check-in date'}, status=400)
            if Booking.objects.filter(room=room, status='confirmed', check_out_date__gt=check_in, check_in_date__lt=check_out).exists():
                return JsonResponse({'success': False, 'error': 'Room is not available for these dates'}, status=400)
            nights = (check_out - check_in).days
            total_price = float(room.room_type.price_per_night) * nights
            user = request.user if request.user.is_authenticated else None
            booking = Booking.objects.create(
                user=user,
                room=room,
                check_in_date=check_in,
                check_out_date=check_out,
                status='confirmed',
                guest_first_name=data['first_name'],
                guest_last_name=data['last_name'],
                guest_gender=data['gender'],
                guest_phone=data['phone'],
                guest_email=data['email'],
                total_price=total_price
            )
            return JsonResponse({'success': True, 'message': 'Booking created successfully', 'booking_id': booking.id, 'total_price': total_price})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

def get_available_rooms(request):
    if request.method == 'GET':
        room_type = request.GET.get('room_type')
        if not room_type:
            return JsonResponse({'error': 'Room type is required'}, status=400)

        # Fetch rooms of the selected type that are available
        available_rooms = Room.objects.filter(room_type__name=room_type, is_active=True).exclude(booking__status='confirmed')
        room_data = [
            {
                'room_number': room.room_number,
                'is_available': not Room.objects.filter(room_number=room.room_number, booking__status='confirmed').exists()
            }
            for room in available_rooms
        ]

        return JsonResponse({'rooms': room_data})

    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def update_booking(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            booking_id = data.get('booking_id')
            from signup.models import User
            booking = Booking.objects.get(id=booking_id)
            booking.guest_first_name = data.get('first_name', booking.guest_first_name)
            booking.guest_last_name = data.get('last_name', booking.guest_last_name)
            booking.guest_email = data.get('email', booking.guest_email)
            booking.guest_phone = data.get('phone', booking.guest_phone)
            booking.check_in_date = data.get('check_in_date', booking.check_in_date)
            booking.check_out_date = data.get('check_out_date', booking.check_out_date)
            if 'status' in data:
                booking.status = data['status']
            if 'payment_status' in data:
                booking.payment_status = data['payment_status']
                if data['payment_status'] == 'paid' and not booking.payment_date:
                    booking.payment_date = timezone.now()
            booking.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def about_us(request):
    """Vue pour la page About Us"""
    return render(request, 'about_us.html')

def admin_dashboard(request):
    total_bookings = Booking.objects.count()
    rooms_available = Room.objects.filter(is_active=True).count()
    new_users = User.objects.count()  # Affiche tous les utilisateurs inscrits
    last_reservations = Booking.objects.select_related('room').order_by('-booking_date')[:4]
    
    # Calcul du revenu total à partir des réservations payées
    paid_bookings = Booking.objects.filter(payment_status='paid')
    total_revenue = sum(booking.total_price for booking in paid_bookings if booking.total_price)
    
    # Récupérer les réservations payées les plus récentes pour la section "Payment Transactions"
    recent_paid_bookings = Booking.objects.filter(payment_status='paid').select_related('room').order_by('-payment_date')[:5]
    
    reservations = [
        {
            'type': b.room.room_type.name,
            'number': b.room.room_number,
            'price': float(b.room.room_type.price_per_night),
            'status': b.status.capitalize()
        }
        for b in last_reservations
    ]
    # Aperçu des types de chambres avec image et disponibilité
    # map room types to static image filenames
    image_map = {
        'Superior Room': 'room1.jpg',
        'Deluxe Room': 'room2.jpg',
        'Family Room': 'room3.jpg',
        'Executive Room': 'room4.jpg',
        'Ocean View Room': 'room5.jpg',
        'Standard Room': 'room6.jpg',
    }
    room_types = RoomType.objects.all()
    room_overview = []
    for rt in room_types:
        available = Room.objects.filter(room_type=rt, is_active=True).count()
        total_count = Room.objects.filter(room_type=rt).count()
        percent_available = int((available / total_count) * 100) if total_count else 0
        # choose matching image or fallback
        image_file = image_map.get(rt.name, 'hotel.jpg')
        room_overview.append({
            'name': rt.name,
            'available': available,
            'price': float(rt.price_per_night),
            'percent_available': percent_available,
            'image': image_file,
        })
    
    # Reorganize room_overview to move Family Room to a specific position (highlighted in yellow)
    # Find Family Room in the list
    family_room = None
    for room in room_overview:
        if room['name'] == 'Family Room':
            family_room = room
            room_overview.remove(room)
            break
    
    # Insert Family Room after the 3rd position (index 2) if it exists
    # This will place it in the yellow highlighted area (assuming it's the 4th position in the grid)
    if family_room:
        room_overview.insert(3, family_room)  # Insert at the 4th position (index 3)
    
    context = {
        'total_bookings': total_bookings,
        'rooms_available': rooms_available,
        'new_users': new_users,
        'total_revenue': total_revenue,
        'total_revenue_percent': 100,
        'expenses': 79.35,
        'reservations': reservations,
        'room_overview': room_overview,
        'paid_bookings': recent_paid_bookings  # Ajout des données de paiement à afficher
    }
    return render(request, 'admin_dashboard.html', context)

def admin_booking(request):
    from signup.models import User
    all_bookings = Booking.objects.select_related('room', 'user').all().order_by('-booking_date')
    return render(request, 'admin_booking.html', {'user_bookings': all_bookings})

def admin_about_us(request):
    return render(request, 'admin_about_us.html')

def admin_room(request):
    rooms = list(Room.objects.select_related('room_type').all())
    for room in rooms:
        room.is_reserved = room.booking_set.filter(status='confirmed').exists()
    # Placer la chambre A1 en premier si elle existe
    a1_room = next((room for room in rooms if room.room_number == 'A1'), None)
    if a1_room:
        rooms.remove(a1_room)
        rooms = [a1_room] + rooms
    # Suppression d'une chambre
    delete_message = None
    if request.method == 'POST' and 'delete_room_id' in request.POST:
        try:
            room = Room.objects.get(id=request.POST['delete_room_id'])
            room.delete()
            delete_message = f"La chambre {room.room_number} a été supprimée avec succès."
        except Room.DoesNotExist:
            delete_message = "La chambre n'existe pas ou a déjà été supprimée."
        rooms = list(Room.objects.select_related('room_type').all())
        for room in rooms:
            room.is_reserved = room.booking_set.filter(status='confirmed').exists()
        a1_room = next((room for room in rooms if room.room_number == 'A1'), None)
        if a1_room:
            rooms.remove(a1_room)
            rooms = [a1_room] + rooms
        return render(request, 'admin_room.html', {'rooms': rooms, 'delete_message': delete_message})
    # Affichage du formulaire d'ajout
    if request.method == 'POST' and 'show_add_room' in request.POST:
        return render(request, 'admin_room.html', {'rooms': rooms, 'show_add_room': True})
    # Ajout d'une chambre
    if request.method == 'POST' and 'add_room' in request.POST:
        room_number = request.POST.get('room_number')
        room_type_name = request.POST.get('room_type')
        floor = request.POST.get('floor')
        price = request.POST.get('price')
        is_active = request.POST.get('status') == 'disponible'
        try:
            room_type, created = RoomType.objects.get_or_create(name=room_type_name)
            if price:
                room_type.price_per_night = price
                room_type.save()
            new_room = Room.objects.create(
                room_number=room_number,
                room_type=room_type,
                floor=floor,
                is_active=is_active
            )
        except Exception:
            pass
        rooms = list(Room.objects.select_related('room_type').all())
        for room in rooms:
            room.is_reserved = room.booking_set.filter(status='confirmed').exists()
        a1_room = next((room for room in rooms if room.room_number == 'A1'), None)
        if a1_room:
            rooms.remove(a1_room)
            rooms = [a1_room] + rooms
        return render(request, 'admin_room.html', {'rooms': rooms, 'add_message': f"La chambre {room_number} a été ajoutée avec succès."})
    # Affichage du formulaire d'édition (modale Edit)
    if request.method == 'POST' and 'edit_room_id' in request.POST and 'price' not in request.POST:
        try:
            edit_room = Room.objects.select_related('room_type').get(id=request.POST['edit_room_id'])
            edit_room.is_reserved = edit_room.booking_set.filter(status='confirmed').exists()
        except Room.DoesNotExist:
            edit_room = None
        return render(request, 'admin_room.html', {'rooms': rooms, 'edit_room': edit_room})
    # Mise à jour du prix (modale Edit)
    if request.method == 'POST' and 'edit_room_id' in request.POST and 'price' in request.POST:
        edit_message = None
        try:
            room = Room.objects.select_related('room_type').get(id=request.POST['edit_room_id'])
            price = request.POST['price']
            if price:
                room.room_type.price_per_night = price
                room.room_type.save()
            edit_message = f"Le prix du type de chambre '{room.room_type.name}' a été modifié pour toutes les chambres de ce type."
        except Room.DoesNotExist:
            edit_message = "Erreur lors de la modification de la chambre."
        rooms = list(Room.objects.select_related('room_type').all())
        for room in rooms:
            room.is_reserved = room.booking_set.filter(status='confirmed').exists()
        a1_room = next((room for room in rooms if room.room_number == 'A1'), None)
        if a1_room:
            rooms.remove(a1_room)
            rooms = [a1_room] + rooms
        return render(request, 'admin_room.html', {'rooms': rooms, 'edit_message': edit_message})
    return render(request, 'admin_room.html', {'rooms': rooms})

def welcome(request):
    main_types = [
        'Superior Room',
        'Deluxe Room',
        'Family Room',
        'Executive Room',
        'Ocean View Room',
        'Standard Room',
    ]
    # Récupérer tous les types de chambres depuis la base de données
    room_types = RoomType.objects.filter(name__in=main_types)
    
    # Déboguer : afficher les prix des chambres dans les logs
    print("Types de chambres et prix:")
    for rt in room_types:
        print(f"{rt.name}: {rt.price_per_night}$")
    
    # Créer un dictionnaire avec clés formatées (remplacer espaces par underscores)
    # et valeurs simples (juste le prix) pour éviter les problèmes d'accès aux attributs
    room_types_dict = {}
    for rt in room_types:
        key = rt.name.replace(' ', '_')
        room_types_dict[key] = {
            'name': rt.name,
            'price_per_night': rt.price_per_night,
            'description': rt.description
        }
    
    # Get the user's name from the session
    user_name = "Admin Admin"  # Default name
    user_id = request.session.get('user_id')
    if user_id:
        from signup.models import User
        user = User.objects.filter(id=user_id).first()
        if user:
            user_name = f"{user.first_name} {user.last_name}"
    
    return render(request, 'welcome.html', {
        'room_types_dict': room_types_dict,
        'user_name': user_name
    })

def payement(request):
    """Vue pour la page de paiement"""
    # Get the latest booking for the current user
    user_id = request.session.get('user_id')
    latest_booking = None
    paid_bookings = []
    
    if user_id:
        from signup.models import User
        user = User.objects.filter(id=user_id).first()
        if user:
            # Get latest unpaid booking
            latest_booking = Booking.objects.filter(
                user=user,
                status='confirmed',
                payment_status__isnull=True
            ).order_by('-booking_date').first()
            
            # If no unpaid booking is found, try to get any confirmed booking
            if not latest_booking:
                latest_booking = Booking.objects.filter(
                    user=user,
                    status='confirmed'
                ).order_by('-booking_date').first()
            
            # Calculate total price again to be sure it's correct
            if latest_booking:
                nights = (latest_booking.check_out_date - latest_booking.check_in_date).days
                room_price = float(latest_booking.room.room_type.price_per_night)
                latest_booking.total_price = room_price * nights
                latest_booking.total_nights = nights  # Add this to the booking object
                
            # Get all paid bookings for this user
            paid_bookings = Booking.objects.filter(
                user=user,
                payment_status='paid'
            ).order_by('-payment_date')
    
    context = {
        'booking': latest_booking,
        'paid_bookings': paid_bookings
    }
    return render(request, 'payement.html', context)

def process_payment(request):
    """Handle payment processing and update booking status"""
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        payment_method = request.POST.get('payment_method', 'credit-card')
        
        if booking_id:
            try:
                from django.utils import timezone
                booking = Booking.objects.get(id=booking_id)
                
                # Update booking payment status
                booking.payment_status = 'paid'
                booking.payment_date = timezone.now()
                booking.save()
                
                return JsonResponse({
                    'success': True,
                    'message': 'Payment successful!',
                    'booking_id': booking_id,
                    'payment_date': booking.payment_date.strftime('%Y-%m-%d %H:%M')
                })
            except Booking.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': 'Booking not found.'
                }, status=404)
        else:
            return JsonResponse({
                'success': False,
                'message': 'Booking ID is required.'
            }, status=400)
            
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method.'
    }, status=405)

def admin_payment(request):
    """View for the admin payment page that shows all completed payments"""
    # Get all bookings with payment_status='paid', ordered by payment date (most recent first)
    paid_bookings = Booking.objects.filter(payment_status='paid').order_by('-payment_date')
    
    # Calculate total revenue
    total_revenue = sum(booking.total_price for booking in paid_bookings if booking.total_price)
    
    # Group payments by month for statistics
    payments_by_month = {}
    for booking in paid_bookings:
        if booking.payment_date:
            month_key = booking.payment_date.strftime('%B %Y')
            if month_key in payments_by_month:
                payments_by_month[month_key] += booking.total_price
            else:
                payments_by_month[month_key] = booking.total_price
    
    context = {
        'paid_bookings': paid_bookings,
        'total_revenue': total_revenue,
        'payments_by_month': payments_by_month,
        'total_payments': paid_bookings.count()
    }
    return render(request, 'admin_payment.html', context)
