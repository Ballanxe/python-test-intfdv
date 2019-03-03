import datetime


class BikeRental:
	"""
	Contiene todos los datos del modelo de negocios
	"""

	total_number_of_rents = 0
	types = ["hour", "day", "week"]
	hour_price = 5
	day_price = 20
	week_price = 60


	def rent(self, name=None, type=None):

		"""
		Renta un bicicleta con base a las propiedades de la clase 
		"""

		rent = Rent(name, type)

		self.__class__.total_number_of_rents += 1

		return rent 


	def family_rent(name=None, type=None):
		"""
		Crea una promocion Family rent, que permite descuento a partir de 3 rentas
		por familia 
		"""

		family = FamilyRental(name, type)

		return family

	@classmethod
	def total_rents(cls):

		"""
		Retorna el numero de veces que se ha instanciado una clase Rent
		"""

		return cls.total_number_of_rents





class Rent(BikeRental):

	total_rented = 0

	total_hours_rented = 0


	def __init__(self, client, type):


		self.client = client
		self.start_date = datetime.datetime.now()
		self.end_date = None
		self.type = self.__check_type(type)
		self.get_price = self.get_type_of_billing()
		self.price = 0
		self.__class__.total_rented += 1 
		self.id = self.__class__.total_rented


	def __repr__(self):

		return f"<{self.__class__.__name__}({self.id}), {self.client},  $ {self.price} >"


	def __check_type(self, type):
		"""
		Verifica que no haya errores en el tipo de arrendmiento
		"""

		if type not in super().types: 

			raise ValueError("Invalid type")

		return type


	def get_type_of_billing(self):

		"""
		Retorna la funcion adecuada al tipo de arrendamiento
		"""

		if self.type == "hour":

			return self.__get_total_hours_price

		elif self.type == "day":

			return self.__get_total_days_price

		elif self.type == "week":

			return self.__get_total_weeks_price


	def __get_total_hours_price(self, end_date=None):

		"""
		Retorna el precio si el tipo de arrendamiento es por hora
		"""

		if not end_date:

			raise ValueError("Must enter return date")

		if not isinstance(end_date, datetime.datetime):

			raise ValueError("Return date must be a datetime object")

		total_time = end_date - self.start_date

		total_hours = self._get_hours(total_time.total_seconds())
		
		print("Total hours are ", total_hours)

		self.price = total_hours * self.hour_price

		return self.price 

	def __get_total_days_price(self, end_date=None):
		"""
		Retorna el precio si el tipo de arrendamiento es por dia
		"""

		if not end_date:

			raise ValueError("Must enter return date")

		if not isinstance(end_date, datetime.datetime):

			raise ValueError("Return date must be a datetime object")

		total_time = end_date - self.start_date

		print(total_time.total_seconds())

		total_days = self._get_days(total_time.total_seconds())

		print("Total days are ", total_days)

		self.price = round(total_days * self.day_price, 2)

		return self.price

	def __get_total_weeks_price(self, end_date=None):
		"""
		Retorna el precio si el tipo de arrendamiento es por semana
		"""

		if not end_date:

			raise ValueError("Must enter return date")

		if not isinstance(end_date, datetime.datetime):

			raise ValueError("Return date must be a datetime object")


		total_time = end_date - self.start_date

		print(total_time.total_seconds())

		total_weeks = self._get_weeks(total_time.total_seconds())

		print("Total weeks are ", total_weeks)

		self.price = total_weeks * self.week_price

		return self.price 


	def _get_days(self, seconds):
		"""
		convierte segundos en dias
		"""

		days = seconds / 86400 

		if days % 1 != 0:

			days += 1 

		return int(days)  


	def _get_hours(self, seconds):
		"""
		Convierte segundos en horas
		"""

		hours = seconds / 3600 

		if hours % 1 != 0:

			hours += 1 

		return int(hours)



	def _get_weeks(self, seconds):

		"""
		Convierte segundos en semanas
		"""


		weeks = seconds / 604800

		if weeks % 1 != 0: 

			weeks += 1

		return int(weeks)




class FamilyRental(BikeRental): 


	allowed_relations = ["daugther", "son", "husband", "wife", "grandchildren", "grandfather", "uncle"]
	discount = 0.3


	def __init__(self, representant, family_members):

		self.representant = representant
		self.rent_list = []
		self.family_members = family_members
		self.total_price = 0


	def rent(self, member, type):

		"""
		Agrega un nuevo arrendamiento a la promocion
		"""

		if len(self.rent_list) == 5:

			raise ValueError("Not more rents available")

		if self._check_member(member):

			new_rent = Rent(client=member, type=type)

			self.rent_list.append(new_rent)

		return new_rent

	def _check_member(self, member):
		"""
		Valida que el miembro que solicita el arrendamiento pertenece a la lista
		de parientes del representante
		"""

		if len(self.family_members) == 0:

			raise ValueError("This rent does not have representant")

		if member == self.representant:

			return True 

		if not member in [item[0] for item in self.family_members]:

			raise ValueError("Invalid Member")


		return True 

	def append_family(self, name, relation):

		"""
		Agrega un nuevuo miembro a la lista de parientes autorizados en la promocion
		"""

		self.family_members.append((name, relation))


	def return_bike(self, rent, end_date=None):
		"""
		Regresa una bicileta de la promocion

		"""

		if not end_date:

			raise ValueError("Must enter return date")

		if not isinstance(end_date, datetime.datetime):

			raise ValueError("Return date must be a datetime object")


		if rent.id in [obj.id for obj in self.rent_list]:

			price = rent.get_price(end_date)

			self.total_price += price

			
		else:

			return ValueError("Invalid ID") 



	def get_promotion_price(self):

		if len(self.rent_list) < 3:

			raise ValueError("You need at least 3 rents to get discount")

		else:

			if self.check_devolutions(): 

				total_price = sum(item.price for item in self.rent_list)

			else:

				raise ValueError("This promotion has no returned bikes")


		promotion_price = total_price - (total_price * self.__class__.discount)

		return promotion_price



	def check_devolutions(self):

		for item in self.rent_list:

			if item.price == 0:

				return False 

		return True





bike_rental = BikeRental()

new_rent = bike_rental.rent("Alberto", "week")


print(new_rent.__dict__)


end_date = datetime.datetime(2019, 3, 10, 21, 40, 42, 0)
price = new_rent.get_price(end_date)

print(bike_rental.total_rents())

print(price)

print(new_rent)

print("-------------")


family_members = [
	("Carlos", "brother"),
	("Olga", "mother"),
	("Argenis", "father")

]

family_rent = FamilyRental(representant="Alberto", family_members=family_members)

rent = family_rent.rent("Argenis", "hour")
end_date = datetime.datetime(2019, 3, 10, 21, 40, 42, 0)
family_rent.return_bike(rent, end_date)


rent = family_rent.rent("Olga", "day")
end_date = datetime.datetime(2019, 3, 10, 21, 40, 42, 0)
family_rent.return_bike(rent, end_date)


rent = family_rent.rent("Argenis", "week")
end_date = datetime.datetime(2019, 3, 10, 21, 40, 42, 0)
family_rent.return_bike(rent, end_date)


rent = family_rent.rent("Alberto", "day")
end_date = datetime.datetime(2019, 3, 10, 21, 40, 42, 0)
family_rent.return_bike(rent, end_date)

# rent = family_rent.rent("Olga", "hour")
# end_date = datetime.datetime(2019, 3, 10, 21, 40, 42, 0)
# family_rent.return_bike(rent, end_date)

promotion_price = family_rent.get_promotion_price()

print("promotion price ", promotion_price)


print(family_rent.__dict__)