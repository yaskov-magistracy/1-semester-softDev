import pytest
from app.models import User
from app.repositories.user_repository import UserRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.order_repository import OrderRepository
from app.repositories.address_repository import AddressRepository
from app.DTO.UserCreate import UserCreate
from app.DTO.ProductCreate import ProductCreate
from app.DTO.OrderCreate import OrderCreate
from app.DTO.AddressCreate import AddressCreate
from datetime import datetime


class TestUserRepository:
    @pytest.mark.asyncio
    async def test_create_user(self, user_repository: UserRepository):
        """Тест создания пользователя в репозитории"""
        user_data = UserCreate(
            email="test@example.com",
            login="john_doe",
            description="test"
        )
        user = await user_repository.create(user_data)

        assert user.id is not None
        assert user.email == "test@example.com"
        assert user.login == "john_doe"

    @pytest.mark.asyncio
    async def test_get_all_users(self, user_repository: UserRepository):
        """Тест получения всех пользователей"""
        user1_data = UserCreate(
            email="user1@example.com",
            login="user1",
            description="test1"
        )
        user2_data = UserCreate(
            email="user2@example.com",
            login="user2", 
            description="test2"
        )
        
        await user_repository.create(user1_data)
        await user_repository.create(user2_data)
        
        users = await user_repository.get_by_filters()
        
        assert len(users) == 2
        assert users[0].email in ["user1@example.com", "user2@example.com"]
        assert users[1].email in ["user1@example.com", "user2@example.com"]

    @pytest.mark.asyncio
    async def test_update_user(self, user_repository: UserRepository):
        """Тест обновления пользователя"""
        user_data = UserCreate(
            email="test@example.com",
            login="john_doe",
            description="test"
        )
        user = await user_repository.create(user_data)
        
        updated_user = await user_repository.update(
            user.id, 
            UserCreate(login=user.login, email="updated@example.com", description="updated")
        )
        
        assert updated_user.id == user.id
        assert updated_user.email == "updated@example.com"
        assert updated_user.description == "updated"

    @pytest.mark.asyncio
    async def test_delete_user(self, user_repository: UserRepository):
        """Тест удаления пользователя"""
        user_data = UserCreate(
            email="test@example.com",
            login="john_doe",
            description="test"
        )
        user = await user_repository.create(user_data)
        
        result = await user_repository.delete(user.id)
        
        assert result is None
        
        # Проверяем, что пользователь действительно удален
        users = await user_repository.get_by_filters()
        assert len(users) == 0
    
class TestProductRepository:
    @pytest.mark.asyncio
    async def test_create_product(self, product_repository: ProductRepository):
        """Тест создания продукта"""
        product_data = ProductCreate(
            name="Test Product",
            quantity=10
        )
        product = await product_repository.create(product_data)

        assert product.id is not None
        assert product.name == "Test Product"
        assert product.quantity == 10

    @pytest.mark.asyncio
    async def test_get_all_products(self, product_repository: ProductRepository):
        """Тест получения всех продуктов"""
        product1_data = ProductCreate(name="Product 1", quantity=5)
        product2_data = ProductCreate(name="Product 2", quantity=15)
        
        await product_repository.create(product1_data)
        await product_repository.create(product2_data)
        
        products = await product_repository.get_by_filters()
        
        assert len(products) == 2
        assert products[0].name in ["Product 1", "Product 2"]
        assert products[1].name in ["Product 1", "Product 2"]

    @pytest.mark.asyncio
    async def test_update_product(self, product_repository: ProductRepository):
        """Тест обновления продукта"""
        product_data = ProductCreate(name="Test Product", quantity=10)
        product = await product_repository.create(product_data)
        
        updated_product = await product_repository.update(
            product.id, 
            ProductCreate(name="Updated Product", quantity=20)
        )
        
        assert updated_product.id == product.id
        assert updated_product.name == "Updated Product"
        assert updated_product.quantity == 20

    @pytest.mark.asyncio
    async def test_delete_product(self, product_repository: ProductRepository):
        """Тест удаления продукта"""
        product_data = ProductCreate(name="Test Product", quantity=10)
        product = await product_repository.create(product_data)
        
        result = await product_repository.delete(product.id)
        
        assert result is None
        
        products = await product_repository.get_by_filters()
        assert len(products) == 0


class TestOrderRepository:
    @pytest.mark.asyncio
    async def test_create_order(self, order_repository: OrderRepository, user_repository: UserRepository, product_repository: ProductRepository, address_repository: AddressRepository):
        """Тест создания заказа"""
        # Создаем пользователя
        user_data = UserCreate(
            email="user@example.com",
            login="test_user",
            description="test"
        )
        user = await user_repository.create(user_data)

        # Создаем продукт
        product_data = ProductCreate(name="Test Product", quantity=10)
        product = await product_repository.create(product_data)

        # Создаем адрес
        address_data = AddressCreate(
            user_id=user.id,
            street="Test Street"
        )
        address = await address_repository.create(address_data)

        # Создаем заказ
        order_data = OrderCreate(
            date=datetime.now(),
            user_id=user.id,
            product_id=product.id,
            address_id=address.id  # Добавляем address_id
        )
        order = await order_repository.create(order_data)

        assert order.id is not None
        assert order.user_id == user.id
        assert order.product_id == product.id
        assert order.address_id == address.id

    @pytest.mark.asyncio
    async def test_get_all_orders(self, order_repository: OrderRepository, user_repository: UserRepository, product_repository: ProductRepository, address_repository: AddressRepository):
        """Тест получения всех заказов"""
        # Создаем пользователя
        user_data = UserCreate(
            email="user@example.com",
            login="test_user",
            description="test"
        )
        user = await user_repository.create(user_data)

        # Создаем продукты
        product1_data = ProductCreate(name="Product 1", quantity=5)
        product2_data = ProductCreate(name="Product 2", quantity=15)
        product1 = await product_repository.create(product1_data)
        product2 = await product_repository.create(product2_data)

        # Создаем адрес
        address_data = AddressCreate(
            user_id=user.id,
            street="Test Street"
        )
        address = await address_repository.create(address_data)

        # Создаем заказы
        order1_data = OrderCreate(
            date=datetime.now(),
            user_id=user.id,
            product_id=product1.id,
            address_id=address.id
        )
        order2_data = OrderCreate(
            date=datetime.now(),
            user_id=user.id,
            product_id=product2.id,
            address_id=address.id
        )
        
        await order_repository.create(order1_data)
        await order_repository.create(order2_data)
        
        orders = await order_repository.get_by_filters()
        
        assert len(orders) == 2
        assert orders[0].user_id == user.id
        assert orders[1].user_id == user.id

    @pytest.mark.asyncio
    async def test_get_order_by_id(self, order_repository: OrderRepository, user_repository: UserRepository, product_repository: ProductRepository, address_repository: AddressRepository):
        """Тест получения конкретного заказа"""
        # Создаем пользователя и продукт
        user_data = UserCreate(
            email="user@example.com",
            login="test_user",
            description="test"
        )
        user = await user_repository.create(user_data)

        product_data = ProductCreate(name="Test Product", quantity=10)
        product = await product_repository.create(product_data)

        # Создаем адрес
        address_data = AddressCreate(
            user_id=user.id,
            street="Test Street"
        )
        address = await address_repository.create(address_data)

        # Создаем заказ
        order_data = OrderCreate(
            date=datetime.now(),
            user_id=user.id,
            product_id=product.id,
            address_id=address.id
        )
        created_order = await order_repository.create(order_data)

        # Получаем заказ по ID
        found_order = await order_repository.get_by_id(created_order.id)

        assert found_order is not None
        assert found_order.id == created_order.id
        assert found_order.user_id == user.id
        assert found_order.product_id == product.id
        assert found_order.address_id == address.id

    @pytest.mark.asyncio
    async def test_update_order(self, order_repository: OrderRepository, user_repository: UserRepository, product_repository: ProductRepository, address_repository: AddressRepository):
        """Тест обновления заказа"""
        # Создаем пользователя
        user_data = UserCreate(
            email="user@example.com",
            login="test_user",
            description="test"
        )
        user = await user_repository.create(user_data)

        # Создаем продукты
        product1_data = ProductCreate(name="Product 1", quantity=5)
        product2_data = ProductCreate(name="Product 2", quantity=15)
        product1 = await product_repository.create(product1_data)
        product2 = await product_repository.create(product2_data)

        # Создаем адрес
        address_data = AddressCreate(
            user_id=user.id,
            street="Test Street"
        )
        address = await address_repository.create(address_data)

        # Создаем заказ
        order_data = OrderCreate(
            date=datetime.now(),
            user_id=user.id,
            product_id=product1.id,
            address_id=address.id
        )
        order = await order_repository.create(order_data)
        
        # Обновляем заказ
        new_date = datetime.now()
        updated_order = await order_repository.update(
            order.id, 
            OrderCreate(
                date=new_date, 
                user_id=user.id, 
                product_id=product2.id,
                address_id=address.id
            )
        )
        
        assert updated_order.id == order.id
        assert updated_order.product_id == product2.id

    @pytest.mark.asyncio
    async def test_delete_order(self, order_repository: OrderRepository, user_repository: UserRepository, product_repository: ProductRepository, address_repository: AddressRepository):
        """Тест удаления заказа"""
        # Создаем пользователя и продукт
        user_data = UserCreate(
            email="user@example.com",
            login="test_user",
            description="test"
        )
        user = await user_repository.create(user_data)

        product_data = ProductCreate(name="Test Product", quantity=10)
        product = await product_repository.create(product_data)

        # Создаем адрес
        address_data = AddressCreate(
            user_id=user.id,
            street="Test Street"
        )
        address = await address_repository.create(address_data)

        # Создаем заказ
        order_data = OrderCreate(
            date=datetime.now(),
            user_id=user.id,
            product_id=product.id,
            address_id=address.id
        )
        order = await order_repository.create(order_data)
        
        result = await order_repository.delete(order.id)
        
        assert result is None
        
        orders = await order_repository.get_by_filters()
        assert len(orders) == 0