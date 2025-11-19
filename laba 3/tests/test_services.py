from pydantic import ValidationError
import pytest
from unittest.mock import Mock, AsyncMock
from uuid import UUID
from app.repositories.user_repository import UserRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.order_repository import OrderRepository
from app.repositories.address_repository import AddressRepository
from app.services.order_service import OrderService
from app.services.product_service import ProductService
from app.DTO.ProductCreate import ProductCreate

class TestOrderService:
    @pytest.mark.asyncio
    async def test_create_order_success(self):
        """Тест успешного создания заказа"""
        mock_order_repo = AsyncMock(spec=OrderRepository)
        mock_product_repo = AsyncMock(spec=ProductRepository)
        mock_user_repo = AsyncMock(spec=UserRepository)
        mock_address_repo = AsyncMock(spec=AddressRepository)

        mock_user_repo.get_by_id.return_value = Mock(id=UUID('12345678-1234-5678-1234-567812345678'))
        mock_product_repo.get_by_id.return_value = Mock(id=UUID('12345678-1234-5678-1234-567812345678'))
        mock_address_repo.get_by_id.return_value = Mock(id=UUID('12345678-1234-5678-1234-567812345678'))
        mock_order_repo.create.return_value = Mock(
            id=UUID('12345678-1234-5678-1234-567812345678'), 
            user_id=UUID('12345678-1234-5678-1234-567812345678'),
            address_id=UUID('12345678-1234-5678-1234-567812345678'),
            product_id=UUID('12345678-1234-5678-1234-567812345678'),
            date="2023-01-01T00:00:00"
        )

        order_service = OrderService(order_repository=mock_order_repo)
        
        order_data = Mock(
            user_id=UUID('12345678-1234-5678-1234-567812345678'),
            address_id=UUID('12345678-1234-5678-1234-567812345678'),
            product_id=UUID('12345678-1234-5678-1234-567812345678'),
            date="2023-01-01T00:00:00"
        )
        
        result = await order_service.create(order_data)

        assert result is not None
        assert result.user_id == UUID('12345678-1234-5678-1234-567812345678')
        mock_order_repo.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_order_by_id(self):
        """Тест получения заказа по ID"""
        mock_order_repo = AsyncMock(spec=OrderRepository)
        
        order_id = UUID('12345678-1234-5678-1234-567812345678')
        mock_order_repo.get_by_id.return_value = Mock(
            id=order_id,
            user_id=UUID('12345678-1234-5678-1234-567812345678'),
            address_id=UUID('12345678-1234-5678-1234-567812345678'),
            product_id=UUID('12345678-1234-5678-1234-567812345678')
        )

        order_service = OrderService(order_repository=mock_order_repo)
        
        result = await order_service.get_by_id(order_id)

        assert result is not None
        assert result.id == order_id
        mock_order_repo.get_by_id.assert_called_once_with(order_id)

    @pytest.mark.asyncio
    async def test_update_order(self):
        """Тест обновления заказа"""
        mock_order_repo = AsyncMock(spec=OrderRepository)
        
        order_id = UUID('12345678-1234-5678-1234-567812345678')
        updated_order_data = Mock(
            date="2023-02-01T00:00:00",
            user_id=UUID('12345678-1234-5678-1234-567812345678'),
            address_id=UUID('12345678-1234-5678-1234-567812345678'),
            product_id=UUID('12345678-1234-5678-1234-567812345678')
        )
        
        mock_order_repo.update.return_value = Mock(
            id=order_id,
            date="2023-02-01T00:00:00"
        )

        order_service = OrderService(order_repository=mock_order_repo)
        
        result = await order_service.update(order_id, updated_order_data)

        assert result is not None
        assert result.date == "2023-02-01T00:00:00"
        mock_order_repo.update.assert_called_once_with(order_id, updated_order_data)

    @pytest.mark.asyncio
    async def test_delete_order(self):
        """Тест удаления заказа"""
        mock_order_repo = AsyncMock(spec=OrderRepository)
        
        order_id = UUID('12345678-1234-5678-1234-567812345678')

        order_service = OrderService(order_repository=mock_order_repo)
        
        await order_service.delete(order_id)

        mock_order_repo.delete.assert_called_once_with(order_id)

    @pytest.mark.asyncio
    async def test_get_orders_by_filter(self):
        """Тест получения заказов по фильтру"""
        mock_order_repo = AsyncMock(spec=OrderRepository)
        
        mock_orders = [
            Mock(id=UUID('12345678-1234-5678-1234-567812345678'), user_id=UUID('11111111-1111-1111-1111-111111111111')),
            Mock(id=UUID('22345678-1234-5678-1234-567812345678'), user_id=UUID('22222222-2222-2222-2222-222222222222'))
        ]
        mock_order_repo.get_by_filters.return_value = mock_orders

        order_service = OrderService(order_repository=mock_order_repo)
        
        result = await order_service.get_by_filter(skip=0, limit=10, user_id=UUID('11111111-1111-1111-1111-111111111111'))

        assert len(result) == 2
        mock_order_repo.get_by_filters.assert_called_once_with(0, 10, user_id=UUID('11111111-1111-1111-1111-111111111111'))


class TestProductService:
    @pytest.mark.asyncio
    async def test_create_product_success(self):
        """Тест успешного создания продукта"""
        mock_product_repo = AsyncMock(spec=ProductRepository)

        mock_product = Mock()
        mock_product.id = UUID('12345678-1234-5678-1234-567812345678')
        mock_product.name = "Test Product"
        mock_product.quantity = 10

        mock_product_repo.create.return_value = mock_product

        product_service = ProductService(product_repository=mock_product_repo)

        product_data = ProductCreate(
            name="Test Product",
            quantity=10
        )
        result = await product_service.create(product_data)

        assert result is not None
        assert result.name == "Test Product"
        assert result.id == UUID('12345678-1234-5678-1234-567812345678')

    @pytest.mark.asyncio
    async def test_get_product_by_id(self):
        """Тест получения продукта по ID"""
        mock_product_repo = AsyncMock(spec=ProductRepository)
        
        product_id = UUID('12345678-1234-5678-1234-567812345678')
        mock_product_repo.get_by_id.return_value = Mock(
            id=product_id,
            name="Test Product"
        )

        product_service = ProductService(product_repository=mock_product_repo)
        
        result = await product_service.get_by_id(product_id)

        assert result is not None
        assert result.id == product_id
        mock_product_repo.get_by_id.assert_called_once_with(product_id)

    @pytest.mark.asyncio
    async def test_update_product(self):
        """Тест обновления продукта"""
        mock_product_repo = AsyncMock(spec=ProductRepository)

        product_id = UUID('12345678-1234-5678-1234-567812345678')

        updated_product_data = ProductCreate(
            name="Updated Product",
            quantity=20
        )

        # Создаем Mock и устанавливаем атрибуты отдельно
        mock_updated_product = Mock()
        mock_updated_product.id = product_id
        mock_updated_product.name = "Updated Product"
        mock_updated_product.quantity = 20

        mock_product_repo.update.return_value = mock_updated_product

        product_service = ProductService(product_repository=mock_product_repo)

        result = await product_service.update(product_id, updated_product_data)

        assert result is not None
        assert result.name == "Updated Product"
        assert result.quantity == 20


    @pytest.mark.asyncio
    async def test_delete_product(self):
        """Тест удаления продукта"""
        mock_product_repo = AsyncMock(spec=ProductRepository)
        
        product_id = UUID('12345678-1234-5678-1234-567812345678')

        product_service = ProductService(product_repository=mock_product_repo)
        
        await product_service.delete(product_id)

        mock_product_repo.delete.assert_called_once_with(product_id)

    @pytest.mark.asyncio
    async def test_get_products_by_filter(self):
        """Тест получения продуктов по фильтру"""
        mock_product_repo = AsyncMock(spec=ProductRepository)
        
        mock_products = [
            Mock(id=UUID('12345678-1234-5678-1234-567812345678'), name="Product 1"),
            Mock(id=UUID('22345678-1234-5678-1234-567812345678'), name="Product 2")
        ]
        mock_product_repo.get_by_filters.return_value = mock_products

        product_service = ProductService(product_repository=mock_product_repo)
        
        result = await product_service.get_by_filter(skip=0, limit=10)

        assert len(result) == 2
        mock_product_repo.get_by_filters.assert_called_once_with(0, 10)