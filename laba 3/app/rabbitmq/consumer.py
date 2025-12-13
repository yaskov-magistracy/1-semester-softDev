import os
import json
import asyncio
from uuid import UUID
from typing import Any

try:
    import aio_pika
except Exception:
    aio_pika = None

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from ..repositories.product_repository import ProductRepository
from ..repositories.order_repository import OrderRepository
from ..models import Product
from ..DTO.ProductCreate import ProductCreate
from ..DTO.OrderCreate import OrderCreate

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:password@localhost:5432/python?async_fallback=True",
)

RABBIT_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost/")

engine = create_async_engine(DATABASE_URL, echo=False)
async_session_factory = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def _with_session(fn):
    async def wrapper(*args, **kwargs):
        async with async_session_factory() as session:
            return await fn(session, *args, **kwargs)

    return wrapper


async def _process_product_message(session: AsyncSession, payload: dict[str, Any]):
    repo = ProductRepository(session)

    action = payload.get("action")
    if action == "create":
        product_data = payload.get("product", {})
        dto = ProductCreate(**product_data)
        await repo.create(dto)
        return

    if action == "update":
        product_id = payload.get("product_id")
        product_data = payload.get("product", {})
        if not product_id:
            raise ValueError("product_id required for update")
        dto = ProductCreate(**product_data)
        await repo.update(UUID(product_id), dto)
        return

    if action == "mark_out_of_stock":
        product_id = payload.get("product_id")
        if not product_id:
            raise ValueError("product_id required for mark_out_of_stock")
        result = await session.execute(
            __import__("sqlalchemy").select(Product).where(Product.id == UUID(product_id))
        )
        product = result.scalar_one_or_none()
        if not product:
            raise ValueError("product not found")
        product.quantity = 0
        await session.commit()
        return


async def _process_order_message(session: AsyncSession, payload: dict[str, Any]):
    repo = OrderRepository(session)
    action = payload.get("action")
    if action == "create":
        order = payload.get("order", {})
        products = order.get("products", [])
        for item in products:
            pid = item.get("product_id")
            if not pid:
                raise ValueError("product_id required in order items")
            result = await session.execute(
                __import__("sqlalchemy").select(Product).where(Product.id == UUID(pid))
            )
            product = result.scalar_one_or_none()
            if not product or product.quantity == 0:
                raise ValueError(f"Product {pid} is out of stock or not found")

        user_id = order.get("user_id")
        address_id = order.get("address_id")
        date = order.get("date")
        from datetime import datetime
        if isinstance(date, str):
            date = datetime.fromisoformat(date)

        for item in products:
            pid = item.get("product_id")
            dto = OrderCreate(
                user_id=UUID(user_id),
                address_id=UUID(address_id),
                product_id=UUID(pid),
                date=date,
            )
            await repo.create(dto)

        for item in products:
            pid = item.get("product_id")
            qty = int(item.get("quantity", 1))
            result = await session.execute(
                __import__("sqlalchemy").select(Product).where(Product.id == UUID(pid))
            )
            product = result.scalar_one_or_none()
            if product:
                product.quantity = max(0, product.quantity - qty)
        await session.commit()
        return

    if action == "update_status":
        order_payload = payload.get("order", {})
        order_id = payload.get("order_id")
        if not order_id:
            raise ValueError("order_id required for update_status")
        return


async def _on_message_product(message: "aio_pika.IncomingMessage"):
    async with message.process(requeue=False):
        try:
            payload = json.loads(message.body.decode())
        except Exception as e:
            print("Invalid product message", e)
            return
        async with async_session_factory() as session:
            try:
                await _process_product_message(session, payload)
            except Exception as e:
                print("Error processing product message:", e)


async def _on_message_order(message: "aio_pika.IncomingMessage"):
    async with message.process(requeue=False):
        try:
            payload = json.loads(message.body.decode())
        except Exception as e:
            print("Invalid order message", e)
            return
        async with async_session_factory() as session:
            try:
                await _process_order_message(session, payload)
            except Exception as e:
                print("Error processing order message:", e)


async def start_consumers() -> None:
    if aio_pika is None:
        print("aio_pika is not installed; RabbitMQ consumers will not start")
        return

    try:
        connection = await aio_pika.connect_robust(RABBIT_URL)
    except Exception as e:
        print("Failed to connect to RabbitMQ:", e)
        return

    channel = await connection.channel()

    products_q = await channel.declare_queue("products", durable=True)
    orders_q = await channel.declare_queue("orders", durable=True)

    await products_q.consume(_on_message_product)
    await orders_q.consume(_on_message_order)

    print("RabbitMQ consumers started: products, orders")

    try:
        while True:
            await asyncio.sleep(1)
    finally:
        await connection.close()
import os
import json
import asyncio
from uuid import UUID
from typing import Any

try:
    import aio_pika
except Exception:  # pragma: no cover - aio_pika may not be installed in test env
    aio_pika = None

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from ..repositories.product_repository import ProductRepository
from ..repositories.order_repository import OrderRepository
from ..models import Product
from ..DTO.ProductCreate import ProductCreate
from ..DTO.OrderCreate import OrderCreate

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:password@localhost:5432/python?async_fallback=True",
)

RABBIT_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost/")

engine = create_async_engine(DATABASE_URL, echo=False)
async_session_factory = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def _with_session(fn):
    async def wrapper(*args, **kwargs):
        async with async_session_factory() as session:
            return await fn(session, *args, **kwargs)

    return wrapper


async def _process_product_message(session: AsyncSession, payload: dict[str, Any]):
    repo = ProductRepository(session)

    action = payload.get("action")
    if action == "create":
        product_data = payload.get("product", {})
        dto = ProductCreate(**product_data)
        await repo.create(dto)
        return

    if action == "update":
        product_id = payload.get("product_id")
        product_data = payload.get("product", {})
        if not product_id:
            raise ValueError("product_id required for update")
        # ProductCreate requires name and quantity, so pass both
        dto = ProductCreate(**product_data)
        await repo.update(UUID(product_id), dto)
        return

    if action == "mark_out_of_stock":
        product_id = payload.get("product_id")
        if not product_id:
            raise ValueError("product_id required for mark_out_of_stock")
        result = await session.execute(
            __import__("sqlalchemy").select(Product).where(Product.id == UUID(product_id))
        )
        product = result.scalar_one_or_none()
        if not product:
            raise ValueError("product not found")
        product.quantity = 0
        await session.commit()
        return


async def _process_order_message(session: AsyncSession, payload: dict[str, Any]):
    repo = OrderRepository(session)
    # Expect payload: {action: 'create'|'update_status', order: {...} }
    action = payload.get("action")
    if action == "create":
        order = payload.get("order", {})
        products = order.get("products", [])  # list of {product_id, quantity}
        # Validate stock: do not accept order if any product is finished (quantity == 0)
        for item in products:
            pid = item.get("product_id")
            if not pid:
                raise ValueError("product_id required in order items")
            result = await session.execute(
                __import__("sqlalchemy").select(Product).where(Product.id == UUID(pid))
            )
            product = result.scalar_one_or_none()
            if not product or product.quantity == 0:
                raise ValueError(f"Product {pid} is out of stock or not found")

        # All good: create one Order row per position (schema uses single product per Order)
        user_id = order.get("user_id")
        address_id = order.get("address_id")
        date = order.get("date")
        from datetime import datetime
        if isinstance(date, str):
            date = datetime.fromisoformat(date)

        for item in products:
            pid = item.get("product_id")
            dto = OrderCreate(
                user_id=UUID(user_id),
                address_id=UUID(address_id),
                product_id=UUID(pid),
                date=date,
            )
            await repo.create(dto)

        # Optionally decrement product quantities if payload requests consumption
        for item in products:
            pid = item.get("product_id")
            qty = int(item.get("quantity", 1))
            result = await session.execute(
                __import__("sqlalchemy").select(Product).where(Product.id == UUID(pid))
            )
            product = result.scalar_one_or_none()
            if product:
                product.quantity = max(0, product.quantity - qty)
        await session.commit()
        return

    if action == "update_status":
        # Current Order model has no status field; attempt to update allowed fields instead
        order_payload = payload.get("order", {})
        order_id = payload.get("order_id")
        if not order_id:
            raise ValueError("order_id required for update_status")
        # If later a status field is added to model, implement here.
        return


async def _on_message_product(message: "aio_pika.IncomingMessage"):
    async with message.process(requeue=False):
        try:
            payload = json.loads(message.body.decode())
        except Exception as e:
            print("Invalid product message", e)
            return
        async with async_session_factory() as session:
            try:
                await _process_product_message(session, payload)
            except Exception as e:
                print("Error processing product message:", e)


async def _on_message_order(message: "aio_pika.IncomingMessage"):
    async with message.process(requeue=False):
        try:
            payload = json.loads(message.body.decode())
        except Exception as e:
            print("Invalid order message", e)
            return
        async with async_session_factory() as session:
            try:
                await _process_order_message(session, payload)
            except Exception as e:
                print("Error processing order message:", e)


async def start_consumers() -> None:
    if aio_pika is None:
        print("aio_pika is not installed; RabbitMQ consumers will not start")
        return

    try:
        connection = await aio_pika.connect_robust(RABBIT_URL)
    except Exception as e:
        print("Failed to connect to RabbitMQ:", e)
        return

    channel = await connection.channel()

    # declare queues
    products_q = await channel.declare_queue("products", durable=True)
    orders_q = await channel.declare_queue("orders", durable=True)

    await products_q.consume(_on_message_product)
    await orders_q.consume(_on_message_order)

    print("RabbitMQ consumers started: products, orders")

    # keep running until application shutdown
    try:
        while True:
            await asyncio.sleep(1)
    finally:
        await connection.close()
