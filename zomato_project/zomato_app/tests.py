from django.test import TestCase
from django.urls import reverse
from .models import Dish, Order

class HomeViewTestCase(TestCase):

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'zomato_app/home.html')


class MenuViewTestCase(TestCase):

    def test_menu_view(self):
        response = self.client.get(reverse('menu'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'zomato_app/menu.html')



class AddDishTestCase(TestCase):

    def test_add_dish(self):
        dish_data = {
            'name': 'New Dish',
            'price': '25.0',
            'availability': 'on',
        }
        response = self.client.post(reverse('add_dish'), dish_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'zomato_app/menu.html')
        # Check if the new dish is added to the menu
        self.assertContains(response, 'New Dish')

    


class RemoveDishTestCase(TestCase):

    def test_remove_dish(self):
        # Create a test dish
        dish = Dish.objects.create(name='Test Dish', price=10.0, availability=True)
        
        response = self.client.post(reverse('remove_dish', args=[dish.id]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'zomato_app/menu.html')
        # Check if the dish is removed from the menu
        self.assertNotContains(response, 'Test Dish')


class UpdateAvailabilityTestCase(TestCase):

    def test_update_availability(self):
        # Create a test dish
        dish = Dish.objects.create(name='Test Dish', price=10.0, availability=True)
        
        response = self.client.post(reverse('update_availability', args=[dish.id]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'zomato_app/menu.html')
        # Check if the availability of the dish is updated
        updated_dish = Dish.objects.get(id=dish.id)
        self.assertFalse(updated_dish.availability)  # Availability should be False now


class TakeOrderTestCase(TestCase):

    def test_take_order_valid_dishes(self):
        # Create test dishes
        dish1 = Dish.objects.create(name='Dish 1', price=15.0, availability=True)
        dish2 = Dish.objects.create(name='Dish 2', price=20.0, availability=True)
        
        order_data = {
            'customer_name': 'John',
            'selected_dishes': [dish1.id, dish2.id],
        }
        response = self.client.post(reverse('take_order'), order_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'zomato_app/review_orders.html')
        # Check if the order is created and dishes are added
        order = Order.objects.latest('id')
        self.assertEqual(order.customer_name, 'John')
        self.assertEqual(order.dishes.count(), 2)


class UpdateOrderStatusTestCase(TestCase):

    def test_update_order_status(self):
        # Create a test order
        order = Order.objects.create(customer_name='John', final_amount=30.0)
        
        new_status = 'Completed'
        response = self.client.post(reverse('update_order_status', args=[order.id]), {'new_status': new_status}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'zomato_app/review_orders.html')
        # Check if the order status is updated
        updated_order = Order.objects.get(id=order.id)
        self.assertEqual(updated_order.status, new_status)


class ReviewOrdersTestCase(TestCase):

    def test_review_orders(self):
        # Create test orders
        order1 = Order.objects.create(customer_name='Alice', final_amount=25.0)
        order2 = Order.objects.create(customer_name='Bob', final_amount=40.0)
        
        response = self.client.get(reverse('review_orders'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'zomato_app/review_orders.html')
        # Check if order information is displayed
        self.assertContains(response, 'Alice')
        self.assertContains(response, 'Bob')


class ExitSystemTestCase(TestCase):

    def test_exit_system(self):
        response = self.client.get(reverse('exit_system'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'zomato_app/menu.html')
        # Add assertions if needed for any additional behavior after exiting the system


