from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_booking_confirmation_email(booking_id, guest_email, guest_name, room_number, hotel_name, check_in, check_out):
    """
    Sends a confirmation email asynchronously via Celery.
    """
    subject = f"Confirmação de Reserva - {hotel_name}"
    message = (
        f"Olá {guest_name},\n\n"
        f"Sua reserva foi confirmada com sucesso!\n\n"
        f"Detalhes da Reserva:\n"
        f"Hotel: {hotel_name}\n"
        f"Quarto: {room_number}\n"
        f"Check-in: {check_in}\n"
        f"Check-out: {check_out}\n\n"
        f"Agradecemos a preferência,\nEquipe {hotel_name}"
    )
    from_email = "no-reply@staymanagersystem.com"
    recipient_list = [guest_email]

    send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        fail_silently=False,
    )

    return f"Confirmation email sent for Booking {booking_id} to {guest_email}"


@shared_task
def verify_room_statuses_from_bookings():
    """
    Periodic task to check bookings and conditionally update room status.
    - If a booking is CANCELLED and room is OCCUPIED -> free to AVAILABLE
    - If a booking is CHECKED_OUT and room is OCCUPIED -> change to CLEANING
    """
    from .models.booking import Booking

    # Process CHECKED_OUT bookings
    checked_out_bookings = Booking.objects.filter(
        status="CHECKED_OUT",
        room__status="OCCUPIED",
    )
    for booking in checked_out_bookings:
        room = booking.room
        room.status = "CLEANING"
        room.save(update_fields=["status"])

    # Process CANCELLED bookings
    cancelled_bookings = Booking.objects.filter(
        status="CANCELLED",
        room__status="OCCUPIED",
    )
    for booking in cancelled_bookings:
        room = booking.room
        room.status = "AVAILABLE"
        room.save(update_fields=["status"])

    return f"Processed {checked_out_bookings.count()} check-outs and {cancelled_bookings.count()} cancellations."
