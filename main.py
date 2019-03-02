from date import datetime



class Rent:

	total_rented = 0
	availabe_cars = 0
	total_hours_rented = 0
	types = ["hour", "day", "week"]
	hour_price = 5
	day_price = 20
	week_price = 60

	def __init__(self, client, type):

		self.client = client
		self.start_date = datetime.datetime.Now()
		self.end_date = None
		self.type = self.__check_type(type)
		self.get_price = self.get_type_of_billing()
		self.price = None


	def __repr__(self):

		return f"<{self.__class__,}>"

	@classmethod
	def __check_type(cls, type):

		if type not in self.types: 

			raise ValueError("Invalid type")

		return type


	def get_type_of_billing():

		if self.type == "hour":

			return __get_total_hours_price

		elif self.type == "day":

			return __get_total_days_price

		elif self.type == "week":

			return __get_total_weeks_price


	def __get_total_hours_price(self, end_date):

		self.price = price

		return self.price

	def __get_total_days_price(self, end_date):

		self.price = price

		return self.price

	def __get_total_weeks_price(self, end_date)

		self.price = price
		return self.price 




class FamilyRental(Rent): 



	def __init__(self)

		self.rent_list = []
		self.family_members = []
		self.__append_representant(family_representant)


	def __append_representant(name):

		self.family_members.append((name, "representant"))

	def get_price(self):

		if len(self.rent_list) < 3:

			raise ValueError("You have to have at least 3 rents to get the discount")


	def append_rent(self, rent): 

		if len(self.family_members) == 5:

			raise ValueError("Not more rents available")

		for family_member, relation in self.family_members:

			if rent.name == family_member:

				self.rent_list.append(rent) 

				break 

		raise ValueError("Not family member")		
		

	def append_family(self, name, relation):

		self.family_members.append((name, relation))



bike_rent = new BikeRent(name="Alberto Rincones", start_date="2019-02-01", end_date="2019-03-01", type="")

family_rent = new FamilyRental()


.is_family_rental() 

