import unittest 
from rental.main import (BikeRental, Rent)
import datetime



class TestBikeRental(unittest.TestCase):

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

        self.assertEqual(usetime, 3)
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

        self.assertEqual(usetime, 4)
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

        self.assertEqual(usetime, 1)
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

        self.assertEqual(usetime, 2)
        self.assertEqual(total_price, 120)



    def test_errors(self):

        bike_rental = BikeRental()

        with self.assertRaises(ValueError) as context:
            family_rent = bike_rental.family_rent("Alberto", "Hermano")
            self.assertTrue('Invalid family_member format' in context.exception)

            miguel_rent = bike_rental.rent("Miguel", "minutes")
            self.assertTrue('Invalid type' in context.exception)

        
            alberto_rent = bike_rental.rent("Alberto","hours", "2019-03-20")
            self.assertTrue('Start time has to be datetime instance' in context.exception)

            olga_rent= bike_rental.rent("Olga", "days")
            carlos_rent= bike_rental.rent("Carlos", "hours")
            sonia_rent = bike_rental.rent("Sonia", "weeks")
            

            end_date = datetime.datetime(2019, 3, 10, 2, 31)

            olga_rent.get_price("2019-4-10")
            self.assertTrue('Return date must be a datetime object' in context.exception)

            carlos_rent.get_price("2019-4-10")
            self.assertTrue('Return date must be a datetime object' in context.exception)

            sonia_rent.get_price("2019-4-10")
            self.assertTrue('Return date must be a datetime object' in context.exception)

        with self.assertRaises(ValueError) as context:
            day_rent =  bike_rental.rent("Raul", "days")
            day_rent.get_price()
            self.assertTrue('Must enter return date' in context.exception)

            hour_rent = bike_rental.rent("Raul", "hours")
            hour_rent.get_price()
            self.assertTrue('Must enter return date' in context.exception)

            week_rent = bike_rental.rent("Raul", "weeks")
            week_rent.get_price()
            self.assertTrue('Must enter return date' in context.exception)


       

class TestFamilyRental(unittest.TestCase):

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
        self.assertEqual(family_rent.total_price, [])

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


    def test_rent_by_a_family_member(self):


        representant = "Alberto"
        family_members = [
            ("Carlos", "brother"),
            ("Olga", "mother"),
            ("Argenis", "father")

        ]

        bike_rental = BikeRental()      

        family_rent = bike_rental.family_rent(representant, family_members)

        alberto_rent = family_rent.rent("Carlos", "days")

        self.assertIsInstance(alberto_rent, Rent)
        self.assertEqual(alberto_rent.client, "Carlos")
        self.assertEqual(alberto_rent.type, "days")
        self.assertEqual(len(family_rent.rent_list), 1)
        self.assertEqual(family_rent.rent_list[0].client, "Carlos")


    def test_full_family_promotion(self):

        representant = "Alberto"
        family_members = [
            ("Carlos", "brother"),
            ("Olga", "mother"),
            ("Argenis", "father")

        ]

        bike_rental = BikeRental()      
        family_rent = bike_rental.family_rent(representant, family_members)

        # First Rent
        start_date = datetime.datetime(2019, 3, 10, 21, 40, 42, 0)
        end_date = datetime.datetime(2019, 3, 28, 21, 41, 42, 0)
        carlos_rent = family_rent.rent("Carlos", "days", start_date)
        family_rent_price_list = family_rent.return_bike(carlos_rent, end_date=end_date)
        self.assertEqual(carlos_rent.price, 380) 
        print("This is carlos rent price ",carlos_rent.price)

        # Second Rent
        start_date = datetime.datetime(2019, 3, 10, 21, 40, 42, 0)
        end_date = datetime.datetime(2019, 3, 10, 23, 40, 42, 0)
        olga_rent = family_rent.rent("Olga", "hours", start_date=start_date)
        family_rent_price_list = family_rent.return_bike(olga_rent, end_date=end_date)
        self.assertEqual(olga_rent.price, 10) 
        print("This is olga rent price ",olga_rent.price)

    
        with self.assertRaises(ValueError) as context:
            family_rent.get_promotion_price()
            self.assertTrue('You need at least 3 rents to get discount' in context.exception)
        # Third Rent
        start_date = datetime.datetime(2019, 3, 10, 21, 40, 42, 0)
        end_date = datetime.datetime(2019, 3, 20, 21, 40, 42, 0)
        argenis_rent = family_rent.rent("Argenis", "days", start_date)
        family_rent_price_list = family_rent.return_bike(argenis_rent, end_date)
        self.assertEqual(argenis_rent.price, 200) 
        # print(argenis_rent.price)
        print("This is arg rent price ",argenis_rent.price)

        #Fourth Rent
        start_date = datetime.datetime(2019, 3, 10, 21, 40, 42, 0)
        end_date = datetime.datetime(2019, 5, 10, 21, 40, 42, 0)
        alberto_rent = family_rent.rent("Alberto", "weeks")

        

        # Fourth Rent has not returned the bike      
        with self.assertRaises(ValueError) as context:
            family_rent.get_promotion_price()
            self.assertTrue('This promotion has no returned bikes' in context.exception)

        # Now is returned
        family_rent_price_list = family_rent.return_bike(alberto_rent, end_date)
        self.assertEqual(alberto_rent.price, 600)


        expected_total_price = (
            alberto_rent.price + 
            argenis_rent.price + 
            olga_rent.price +
            carlos_rent.price
            )

        expeced_promotion_price = expected_total_price - (expected_total_price * 0.3)

        self.assertEqual(family_rent.get_total_price(), expected_total_price)
        self.assertEqual(family_rent.get_promotion_price(), expeced_promotion_price)



        # Fifth Rent 
        start_date = datetime.datetime(2019, 3, 10, 21, 40, 42, 0)
        end_date = datetime.datetime(2019, 3, 11, 12, 40, 42, 0)
        alberto2_rent = family_rent.rent("Argenis", "hours", start_date)

        # Test error when introducing rent object that does not belong to this promotion
        invalid_rent = bike_rental.rent("Invalid", "hours")
        with self.assertRaises(ValueError) as context:
            family_rent.return_bike(invalid_rent, end_date)
            self.assertTrue("Invalid ID" in context.exception)



        alberto2_rent = family_rent.return_bike(alberto2_rent, end_date)

        # Test more than five rents error
        with self.assertRaises(ValueError) as context:
            family_rent.rent("Invalid", "hours")
            self.assertTrue("Not more rents available" in context.exception)

    def test_append_family_member(self):

        representant = "Alberto"
        family_members = [
            ("Carlos", "brother"),
            ("Olga", "mother"),
            ("Argenis", "father")

        ]

        bike_rental = BikeRental()

        family_rent = bike_rental.family_rent(representant, family_members)

        family_rent.append_family("Juan", "grandfather")

        expected = [
            ("Carlos", "brother"),
            ("Olga", "mother"),
            ("Argenis", "father"),
            ("Juan", "grandfather")

        ]

        self.assertEqual(family_rent.family_members, expected)

    def test_return_bike_errors(self):

        representant = "Alberto"
        family_members = [
            ("Carlos", "brother"),
            ("Olga", "mother"),
            ("Argenis", "father")

        ]

        bike_rental = BikeRental()

        family_rent = bike_rental.family_rent(representant, family_members)


        with self.assertRaises(ValueError) as context:
            brother_rent = family_rent.rent("Carlossss", "hours")

            self.assertTrue('Invalid Member' in context.exception)

            invalid_rent = family_rent.rent("Carlos", "hours")
            price_list = family_rent.return_bike(invalid_rent)
            self.assertTrue('Must enter return date' in context.exception)

            price_list = family_rent.return_bike(invalid_rent,"2019-03-20")
            self.assertTrue('Return date must be a datetime object' in context.exception)








