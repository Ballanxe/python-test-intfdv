import unittest 
import datetime

class BikeRental:
    """
    Contiene todos los datos del modelo de negocios
    """
    total_number_of_rents = 0
    total_number_of_promotions = 0
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
        if type(family_members) != list:
            raise ValueError("Invalid family_member format")
        self.__class__.total_number_of_promotions += 1
        return FamilyRental(name, family_members)


    @classmethod
    def total_rents(cls):
        """
        Retorna el numero de veces que se ha instanciado una clase Rent
        """
        return cls.total_number_of_rents

    @classmethod
    def total_promotion(cls):
        """
        Retorna el numero de veces que se ha instanciado una clase Rent
        """
        return cls.total_number_of_promotions

class Rent(BikeRental):

    total_rented = 0
    total_hours_rented = 0

    def __init__(self, client, type, start_date=None):

        self.client = client
        self.start_date = None
        self.end_date = None
        self.type = self._check_type(type)
        self.get_price = None
        self.usetime = 0 
        self.price = 0
        self.__class__.total_rented += 1 
        self.id = self.__class__.total_rented
        self._get_start_date(start_date)
        self._get_type_of_billing()

    def __repr__(self):

        return f"<{self.__class__.__name__}({self.id}), {self.client},  $ {self.price} >"

    def get_id(self):

        return self.id

    def get_usetime(self):
        """
        Retorna el tiempo de uso dependiendo del valor de self.type
        """
        return self.usetime


    def _check_type(self, type):
        """
        Verifica que no haya errores en el tipo de arrendmiento
        """
        if type not in super().types: 

            raise ValueError("Invalid type")

        return type


    def _get_start_date(self, date):
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




    def _get_type_of_billing(self):
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
        if end_date == None:

            raise ValueError("Must enter return date")

        if not isinstance(end_date, datetime.datetime):

            raise ValueError("Return date must be a datetime object")

        total_time = end_date - self.start_date
        self.usetime = self._get_hours(total_time.total_seconds())
        self.price = self.usetime * self.hour_price
        return self.price 

    def _get_total_days_price(self, end_date=None):
        """
        Retorna el precio si el tipo de arrendamiento es por dia
        """
        if end_date == None:

            raise ValueError("Must enter return date")
        if not isinstance(end_date, datetime.datetime):

            raise ValueError("Return date must be a datetime object")
        total_time = end_date - self.start_date
        self.usetime = self._get_days(total_time.total_seconds())
        self.price = round(self.usetime * self.day_price, 2)
        return self.price

    def _get_total_weeks_price(self, end_date=None):
        """
        Retorna el precio si el tipo de arrendamiento es por semana
        """
        if end_date == None:

            raise ValueError("Must enter return date")

        if not isinstance(end_date, datetime.datetime):

            raise ValueError("Return date must be a datetime object")
        total_time = end_date - self.start_date
        self.usetime = self._get_weeks(total_time.total_seconds())
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
    DISCOUNT = 0.3

    def __init__(self, representant, family_members=[]):

        self.representant = representant
        self.rent_list = []
        self.family_members = family_members
        self.total_price = []

    def __setattr__(self, name, value):

        if name == 'DISCOUNT':
            raise AttributeError('Protected attr.')
        else:
            object.__setattr__(self, name, value)

    def __repr__(self):

        return "<{}, {}>".format(self.__class__.__name__,self.rent_list.__repr__)


    def rent(self, member, type, start_date=None):
        """
        Agrega un nuevo arrendamiento a la promocion
        """
        if len(self.rent_list) == 5:
            raise ValueError("Not more rents available")

        if self._check_member(member):

            new_rent = Rent(client=member, type=type, start_date=start_date)
            self.rent_list.append(new_rent)
            BikeRental.total_number_of_rents += 1

        return new_rent

    def _check_member(self, member):
        """
        Valida que el miembro que solicita el arrendamiento pertenece a la lista
        de parientes del representante
        """
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
        if end_date == None:

            raise ValueError("Must enter return date")
        if not isinstance(end_date, datetime.datetime):

            raise ValueError("Return date must be a datetime object")
        if rent.id in [obj.id for obj in self.rent_list]:

            price = rent.get_price(end_date) 
            self.total_price.append(price)
            
        else:

            raise ValueError("Invalid ID") 
        return self.total_price



    def get_promotion_price(self):
        """
        Suma todos los arriendos de la promocion y agrega el descuento correspondiente 
        """
        if len(self.rent_list) < 3:

            raise ValueError("You need at least 3 rents to get discount")

        else:

            if self._has_non_returned_bikes(): 
                total_price = sum(self.total_price)

            else:

                raise ValueError("This promotion has no returned bikes")
        promotion_price = total_price - (total_price * self.__class__.DISCOUNT)
        return promotion_price
    
    def get_total_price(self):

        return sum(self.total_price)

    def _has_non_returned_bikes(self):
        """
        Verifica que la promosion no tenga bicicletas sin devolver
        """
        for item in self.rent_list:
            if item.price == 0:
                return False  

        return True


