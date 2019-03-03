import unittest 
import datetime


class BikeRental:
    """
    Contiene todos los datos del modelo de negocios
    """

    total_number_of_rents = 0
    types = ["hours", "days", "weeks"]
    hour_price = 5
    day_price = 20
    week_price = 60


    def rent(self, name=None, type=None, date=None):

        """
        Renta un bicicleta con base a las propiedades de la clase 
        """

        rent = Rent(name, type, date)

        self.__class__.total_number_of_rents += 1

        return rent 


    def family_rent(self, name=None, family_members=None):
        """
        Crea una promocion Family rent, que permite descuento a partir de 3 rentas
        por familia 
        """
        return FamilyRental(name, family_members)


    @classmethod
    def total_rents(cls):

        """
        Retorna el numero de veces que se ha instanciado una clase Rent
        """

        return cls.total_number_of_rents





class Rent(BikeRental):

    total_rented = 0

    total_hours_rented = 0


    def __init__(self, client, type, date=None):


        self.client = client
        self.start_date = None
        self.end_date = None
        self.type = self._check_type(type)
        self.get_price = None
        self.usetime = 0 
        self.price = 0
        self.__class__.total_rented += 1 
        self.id = self.__class__.total_rented
        self.get_start_date(date)
        self.get_type_of_billing()


    def __repr__(self):

        return f"<{self.__class__.__name__}({self.id}), {self.client},  $ {self.price} >"


    def get_usetime(self):

        return f"{self.usetime} {self.type}"


    def _check_type(self, type):
        """
        Verifica que no haya errores en el tipo de arrendmiento
        """

        if type not in super().types: 

            raise ValueError("Invalid type")

        return type


    def get_start_date(self, date):

        """
        Obtiene la fecha si es proporcionada de lo contrario agrega la fecha actual
        """

        if date is not None:


            if isinstance(date, datetime.datetime):

                self.start_date = date
            else:

                raise ValueError("Start time has to be datetime instance")
        else: 

            self.start_date = datetime.datetime.now()




    def get_type_of_billing(self):

        """
        Retorna la funcion adecuada al tipo de arrendamiento
        """

        if self.type == "hours":

            self.get_price = self._get_total_hours_price

        elif self.type == "days":

            self.get_price = self._get_total_days_price

        elif self.type == "weeks":

            self.get_price = self._get_total_weeks_price


    def _get_total_hours_price(self, end_date=None):

        """
        Retorna el precio si el tipo de arrendamiento es por hora
        """

        if not end_date:

            raise ValueError("Must enter return date")

        if not isinstance(end_date, datetime.datetime):

            raise ValueError("Return date must be a datetime object")

        total_time = end_date - self.start_date

        self.usetime = self._get_hours(total_time.total_seconds())
        
        print("Total hours are ", self.usetime)

        self.price = self.usetime * self.hour_price

        return self.price 

    def _get_total_days_price(self, end_date=None):
        """
        Retorna el precio si el tipo de arrendamiento es por dia
        """

        if not end_date:

            raise ValueError("Must enter return date")

        if not isinstance(end_date, datetime.datetime):

            raise ValueError("Return date must be a datetime object")

        total_time = end_date - self.start_date

        print(total_time.total_seconds())

        self.usetime = self._get_days(total_time.total_seconds())

        print("Total days are ", self.usetime)

        self.price = round(self.usetime * self.day_price, 2)

        return self.price

    def _get_total_weeks_price(self, end_date=None):
        """
        Retorna el precio si el tipo de arrendamiento es por semana
        """

        if not end_date:

            raise ValueError("Must enter return date")

        if not isinstance(end_date, datetime.datetime):

            raise ValueError("Return date must be a datetime object")


        total_time = end_date - self.start_date

        print(total_time.total_seconds())

        self.usetime = self._get_weeks(total_time.total_seconds())

        print("Total weeks are ", self.usetime)

        self.price = self.usetime * self.week_price

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
        """
        Suma todos los arrendamientos de la promocion y agrega el descuento correspondiente 
        """

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

        """
        Verifica que la promosion no tenga bicicletas sin devolver
        """

        for item in self.rent_list:

            if item.price == 0:

                return False 

        return True





# bike_rental = BikeRental()

# new_rent = bike_rental.rent("Alberto", "weeks")


# print(new_rent.__dict__)


# end_date = datetime.datetime(2019, 3, 10, 21, 40, 42, 0)
# price = new_rent.get_price(end_date)

# print(bike_rental.total_rents())

# print(price)

# print(new_rent)

# print("-------------")


# family_members = [
#   ("Carlos", "brother"),
#   ("Olga", "mother"),
#   ("Argenis", "father")

# ]

# family_rent = FamilyRental(representant="Alberto", family_members=family_members)

# rent = family_rent.rent("Argenis", "hous")
# end_date = datetime.datetime(2019, 3, 10, 21, 40, 42, 0)
# family_rent.return_bike(rent, end_date)


# rent = family_rent.rent("Olga", "days")
# end_date = datetime.datetime(2019, 3, 10, 21, 40, 42, 0)
# family_rent.return_bike(rent, end_date)


# rent = family_rent.rent("Argenis", "weeks")
# end_date = datetime.datetime(2019, 3, 10, 21, 40, 42, 0)
# family_rent.return_bike(rent, end_date)


# rent = family_rent.rent("Alberto", "days")
# end_date = datetime.datetime(2019, 3, 10, 21, 40, 42, 0)
# family_rent.return_bike(rent, end_date)

# rent = family_rent.rent("Olga", "hours")
# end_date = datetime.datetime(2019, 3, 10, 21, 40, 42, 0)
# family_rent.return_bike(rent, end_date)

# promotion_price = family_rent.get_promotion_price()

#     print("promotion price ", promotion_price)


# print(family_rent.__dict__)


class Test(unittest.TestCase):

    def test_bike_rental_rent(self):

        client = 'Alberto'
        type_ = "hours"

        bike_rental = BikeRental()
        new_rent = bike_rental.rent(client, type_)



        self.assertEqual(new_rent.client, "Alberto")
        self.assertTrue(new_rent.start_date)
        self.assertIsInstance(new_rent.start_date, datetime.datetime)
        self.assertEqual(new_rent.type, "hours")
        self.assertEqual(new_rent.get_price, new_rent._get_total_hours_price)
        self.assertEqual(new_rent.price, 0)
        # self.assertEqual(new_rent.total_rented, 1)

    def test_bike_rental_by_day(self):

        client = 'Carlos'
        type_ = "days"
        start_date = datetime.datetime(2019, 3, 3, 2, 45)

        bike_rental = BikeRental()
        new_rent = bike_rental.rent(client, type_, start_date)

        end_date = datetime.datetime(2019, 3, 4, 2, 46)

        total_price = new_rent.get_price(end_date)

        usetime = new_rent.get_usetime()


        self.assertEqual(total_price, 40)
        self.assertEqual(new_rent.usetime, 2)
        self.assertEqual(new_rent.start_date, start_date)

    def test_bike_rental_by_day_one_minute_left(self):

        client = "Raul"
        type="days"

        start_date = datetime.datetime(2019, 3, 3, 4, 20)

        bike_rental = BikeRental()

        new_rent = bike_rental.rent(client, type, start_date)

        end_date = datetime.datetime(2019, 3, 4, 4, 19)

        total_price = new_rent.get_price(end_date)

        self.assertEqual(total_price, 20)


    def test_bike_rental_by_hour(self):

        client = 'Carlos'
        type_ = "hours"
        start_date = datetime.datetime(2019, 3, 3, 2, 30)

        bike_rental = BikeRental()
        new_rent = bike_rental.rent(client, type_, start_date)

        end_date = datetime.datetime(2019, 3, 3, 5, 30)

        total_price = new_rent.get_price(end_date)

        usetime = new_rent.get_usetime()

        self.assertEqual(usetime, "3 hours")
        self.assertEqual(total_price, 15)


    def test_bike_rental_by_hour_one_minute_pass(self):

        client = 'Carlos'
        type_ = "hours"
        start_date = datetime.datetime(2019, 3, 3, 2, 30)

        bike_rental = BikeRental()
        new_rent = bike_rental.rent(client, type_, start_date)

        end_date = datetime.datetime(2019, 3, 3, 5, 31)

        total_price = new_rent.get_price(end_date)

        usetime = new_rent.get_usetime()

        self.assertEqual(usetime, "4 hours")
        self.assertEqual(total_price, 20)



    def test_bike_rental_by_week(self):

        client = 'Carlos'
        type_ = "weeks"
        start_date = datetime.datetime(2019, 3, 3, 2, 30)

        bike_rental = BikeRental()
        new_rent = bike_rental.rent(client, type_, start_date)

        end_date = datetime.datetime(2019, 3, 10, 2, 29)

        total_price = new_rent.get_price(end_date)

        usetime = new_rent.get_usetime()

        self.assertEqual(usetime, "1 weeks")
        self.assertEqual(total_price, 60)


    def test_bike_rental_by_week_one_minute_pass(self):

        client = 'Carlos'
        type_ = "weeks"
        start_date = datetime.datetime(2019, 3, 3, 2, 30)

        bike_rental = BikeRental()
        new_rent = bike_rental.rent(client, type_, start_date)

        end_date = datetime.datetime(2019, 3, 10, 2, 31)

        total_price = new_rent.get_price(end_date)

        usetime = new_rent.get_usetime()

        self.assertEqual(usetime, "2 weeks")
        self.assertEqual(total_price, 120)


    def test_family_rental(self):

        representant = "Alberto"
        family_members = [
            ("Carlos", "brother"),
            ("Olga", "mother"),
            ("Argenis", "father")

        ]

        bike_rental = BikeRental()      

        family_rent = bike_rental.family_rent(representant, family_members)


        self.assertEqual(family_rent.representant, "Alberto")
        self.assertEqual(family_rent.rent_list, [])
        self.assertEqual(family_rent.family_members, family_members)
        self.assertEqual(family_rent.total_price, 0)

    def test_rent_by_a_representant_member(self):


        representant = "Alberto"
        family_members = [
            ("Carlos", "brother"),
            ("Olga", "mother"),
            ("Argenis", "father")

        ]

        bike_rental = BikeRental()      

        family_rent = bike_rental.family_rent(representant, family_members)

        alberto_rent = family_rent.rent(representant, "days")

        self.assertIsInstance(alberto_rent, Rent)
        self.assertEqual(alberto_rent.client, "Alberto")
        self.assertEqual(alberto_rent.type, "days")
        self.assertEqual(len(family_rent.rent_list), 1)





        # self.representant = representant
        # self.rent_list = []
        # self.family_members = family_members
        # self.total_price = 0


    # self.client = client
    # self.start_date = datetime.datetime.now()
    # self.end_date = None
    # self.type = self.__check_type(type)
    # self.get_price = self.get_type_of_billing()
    # self.price = 0
    # self.__class__.total_rented += 1 
    # self.id = self.__class__.total_rented


    # def test_longer_sentence(self):
    #     input = 'Chocolate cake for dinner and pound cake for dessert'

    #     word_cloud = WordCloudData(input)
    #     actual = word_cloud.words_to_counts

    #     expected = {
    #         'and': 1,
    #         'pound': 1,
    #         'for': 2,
    #         'dessert': 1,
    #         'Chocolate': 1,
    #         'dinner': 1,
    #         'cake': 2,
    #     }
    #     self.assertEqual(actual, expected)

    # def test_punctuation(self):
    #     input = 'Strawberry short cake? Yum!'

    #     word_cloud = WordCloudData(input)
    #     actual = word_cloud.words_to_counts

    #     expected = {'cake': 1, 'Strawberry': 1, 'short': 1, 'Yum': 1}
    #     self.assertEqual(actual, expected)

    # def test_hyphenated_words(self):
    #     input = 'Dessert - mille-feuille cake'

    #     word_cloud = WordCloudData(input)
    #     actual = word_cloud.words_to_counts

    #     expected = {'cake': 1, 'Dessert': 1, 'mille-feuille': 1}
    #     self.assertEqual(actual, expected)

    # def test_ellipses_between_words(self):
    #     input = 'Mmm...mmm...decisions...decisions'

    #     word_cloud = WordCloudData(input)
    #     actual = word_cloud.words_to_counts

    #     expected = {'mmm': 2, 'decisions': 2}
    #     self.assertEqual(actual, expected)

    # def test_apostrophes(self):
    #     input = "Allie's Bakery: Sasha's Cakes"

    #     word_cloud = WordCloudData(input)
    #     actual = word_cloud.words_to_counts

    #     expected = {"Bakery": 1, "Cakes": 1, "Allie's": 1, "Sasha's": 1}
    #     self.assertEqual(actual, expected)


unittest.main(verbosity=2)