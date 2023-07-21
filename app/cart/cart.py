from decimal import Decimal
from django.conf import settings
from ..product import models
from ..product.serializers import ProductSerializer


class Cart(object):
    def __init__(self, request) -> None:
        ''' Инициализировать корзину. 
        Текущий сеанс сохраняется посредством инструкции self.session = request.session
        '''
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # сохранить пустую корзину в сеансе
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        '''
        Прокрутить товарные позиции корзины в цикле и получить товары из базы данных.
        '''
        product_ids = self.cart.keys()
        # получить объекты product и добавить их в корзину
        # products = models.Product.objects.filter(id__in=product_ids)
        products = ProductSerializer(models.Product.objects.filter(id__in=product_ids), many=True)
        product_data = products.data

        cart = self.cart.copy()
        
        for product in product_data:
            cart[str(product.id)['product']] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']

            yield item

    def __len__(self):
        '''
        Count all items in the cart.
        '''
        return sum(item['quantity'] for item in self.cart.values())
    
    
    def add(self, product, quantity=1, override_quantity=False):
        '''Добавить товар в корзину либо обновить его количество.

        add() принимает на входе следующие ниже параметры
        
        •• product: экземпляр product для его добавления в корзину либо его обновления;
        •• quantity: опциональное целое число с количеством товара. По умолчанию равен 1;
        •• override_quantity: это булево значение, указывающее, нужно ли заменить 
            количество переданным количеством (True) л
        '''

        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)}
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def remove(self, product):
        '''
        Удалить товар из корзины.
        '''
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    
    def clear(self):
        # удалить корзину из сеанса
        del self.session[settings.CART_SESSION_ID]
        self.save()
