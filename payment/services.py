from datetime import datetime
from management.models import HotelRoom

import stripe

stripe.api_key = "sk_test_26PHem9AhJZvU623DfE1x4sd"


application_fee_amount = 123


def calculate_reservation_total_price(check_in, check_out, price):

	delta  = check_out - check_in
	days   = delta.days

	return price * days

def get_room_price(room_number):

	room = HotelRoom.objects.get(room_number=room_number)

	return int(room.room_type.price)

def create_payment_intent(amount, stripe_account):

	payment_intent = stripe.PaymentIntent.create(

		payment_method_types=["card"],
		amount=amount,
		currency='usd',
		application_fee_amount=application_fee_amount,
		stripe_account=stripe_account,
	)

	return payment_intent

def create_connected_account():
	return stripe.Account.create(type="standard").id