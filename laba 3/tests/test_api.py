from litestar import Litestar
from litestar.di import Provide
import pytest
import pytest_asyncio
from unittest.mock import AsyncMock
import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, MagicMock
from uuid import UUID, uuid4
from litestar.testing import TestClient
from app.controllers.user_controller import UserController
from app.services.user_service import UserService
from app.DTO.UserCreate import UserCreate
from app.models import User


@pytest_asyncio.fixture
async def mock_user_service():
    return AsyncMock(spec=UserService)

@pytest.fixture
def sample_user_data():
    return {
        "login": "testuser",
        "email": "test@example.com", 
        "description": "Test user"
    }


class TestUserController:
    
    @pytest.fixture
    def mock_user_service(self):
        """Фикстура для мок-сервиса пользователей"""
        return AsyncMock(spec=UserService)

    @pytest.fixture
    def app(self, mock_user_service):
        """Создаем тестовое приложение Litestar"""
        def get_user_service() -> UserService:
            return mock_user_service

        return Litestar(
            route_handlers=[UserController],
            dependencies={"user_service": Provide(get_user_service, sync_to_thread=False)}
        )

    @pytest.fixture
    def test_client(self, app):
        """Фикстура для тестового клиента"""
        return TestClient(app=app)

    @pytest.fixture
    def sample_user(self):
        """Фикстура для тестового пользователя"""
        user_id = uuid4()
        return User(
            id=user_id,
            login="testuser",
            email="test@example.com",
            description="Test user description"
        )

    @pytest.fixture
    def sample_user_data(self):
        return {
            "login": "newuser",
            "email": "new@example.com",
            "description": "New user description"
        }

    def test_get_user_by_id_success(self, mock_user_service, test_client, sample_user):
        """Тест успешного получения пользователя по ID"""

        mock_user_service.get_by_id.return_value = sample_user
        

        response = test_client.get(f"/users/{sample_user.id}")
        

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(sample_user.id)
        assert data["login"] == sample_user.login
        assert data["email"] == sample_user.email
        mock_user_service.get_by_id.assert_called_once_with(sample_user.id)

    def test_get_all_users_success(self, mock_user_service, test_client, sample_user):
        """Тест успешного получения всех пользователей"""

        users = [sample_user]
        mock_user_service.get_by_filter.return_value = users
        
        response = test_client.get("/users")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["id"] == str(sample_user.id)
        mock_user_service.get_by_filter.assert_called_once()

    def test_create_user_success(self, mock_user_service, test_client, sample_user):
        user_data = {
            "login": "newuser",
            "email": "new@example.com",
            "description": "New user"
        }
        mock_user_service.create.return_value = sample_user
        
        response = test_client.post("/users/", json=user_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["id"] == str(sample_user.id)
        mock_user_service.create.assert_called_once()

    def test_update_user_success(self, mock_user_service, test_client, sample_user):
        """Тест успешного обновления пользователя"""
        update_data = {
            "login": "updateduser",
            "email": "updated@example.com",
            "description": "Updated description"
        }
        mock_user_service.update.return_value = sample_user
        
        response = test_client.put(f"/users/{sample_user.id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(sample_user.id)
        mock_user_service.update.assert_called_once()

    def test_delete_user_success(self, mock_user_service, test_client, sample_user):
        mock_user_service.delete.return_value = None
        
        response = test_client.delete(f"/users/{sample_user.id}")
        
        assert response.status_code == 204
        mock_user_service.delete.assert_called_once_with(sample_user.id)

    def test_get_user_by_id_not_found(self, mock_user_service, test_client):
        user_id = uuid4()
        mock_user_service.get_by_id.return_value = None
        
        try:
            response = test_client.get(f"/users/{user_id}")
        except Exception as e:
            assert e is ValueError
        mock_user_service.get_by_id.assert_called_once_with(user_id)