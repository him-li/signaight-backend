import uuid
from taskiq import TaskiqScheduler
from taskiq.serializers import JSONSerializer
from taskiq_redis import RedisAsyncResultBackend, RedisScheduleSource

from .config import settings, BrokersEnum
from .middlewares import TimeoutStateSaveMiddleware, SimpleRetryMiddleware

broker = None
scheduler = None

middlewares = [
    #TimeoutStateSaveMiddleware()
    SimpleRetryMiddleware()
]


match settings.TASKIQ_BROKER:
    # RabbitMQ broker
    case BrokersEnum.amqp:
        from taskiq_aio_pika import AioPikaBroker
        broker = AioPikaBroker(
            url=str(settings.RABBITMQ_URI),
            qos=settings.TASKIQ_AIOPIKABROKER_QOS,
            declare_exchange=settings.TASKIQ_AIOPIKABROKER_DECLARE_EXCHANGE,
            queue_name=settings.TASKIQ_QUEUE_NAME,
            max_priority=settings.TASKIQ_AIOPIKABROKER_MAX_PRIORITY,
            declare_queues_kwargs={
                "durable": settings.TASKIQ_AIOPIKABROKER_QUEUE_DURABLE
            }
        ).with_id_generator(
            lambda: str(uuid.uuid4())
        ).with_result_backend(
            RedisAsyncResultBackend(
                redis_url=settings.REDIS_URI,
                result_ex_time=18000,
            )
        ).with_middlewares(
            *middlewares
        )
        scheduler = TaskiqScheduler(
            broker=broker,
            sources=[RedisScheduleSource(settings.REDIS_URI)],
        )

    # PostgreSQL broker
    case BrokersEnum.postgres:
        from taskiq_postgresql import PostgresqlBroker, PostgresqlResultBackend
        from taskiq_postgresql.scheduler_source import PostgresqlSchedulerSource
        broker = PostgresqlBroker(
            dsn=str(settings.POSTGRES_URI),
            table_name="taskiq_messages",
            channel_name=settings.TASKIQ_QUEUE_NAME,
            driver="asyncpg",
            run_migrations=True
        ).with_result_backend(
            PostgresqlResultBackend(
                dsn=str(settings.POSTGRES_URI),
                serializer=JSONSerializer(),
                keep_results=True,
                table_name="taskiq_results",
                driver="asyncpg",
                run_migrations=True
            )
        ).with_middlewares(
            *middlewares
        )
        scheduler = TaskiqScheduler(
            broker=broker,
            sources=[
                PostgresqlSchedulerSource(
                    dsn=str(settings.POSTGRES_URI),
                    table_name="taskiq_schedules",
                    driver="asyncpg",
                    run_migrations=True
                )
            ],
        )

    # NATS broker
    case BrokersEnum.nats:
        from taskiq_nats import NatsBroker
        broker = NatsBroker(
            servers=str(settings.NATS_URI),
            subject="taskiq_service",
            queue=settings.TASKIQ_QUEUE_NAME,
        ).with_id_generator(
            lambda: str(uuid.uuid4())
        ).with_result_backend(
            RedisAsyncResultBackend(
                redis_url=settings.REDIS_URI,
                result_ex_time=18000,
            )
        ).with_middlewares(
            *middlewares
        )
        scheduler = TaskiqScheduler(
            broker=broker,
            sources=[RedisScheduleSource(settings.REDIS_URI)],
        )

    # Redis broker
    case _:
        from taskiq_redis import RedisStreamBroker
        broker = RedisStreamBroker(
            url=settings.REDIS_URI,
            queue_name=settings.TASKIQ_QUEUE_NAME,
        ).with_result_backend(
            RedisAsyncResultBackend(
                redis_url=settings.REDIS_URI,
                result_ex_time=18000,
            )
        ).with_middlewares(
            *middlewares
        )
        scheduler = TaskiqScheduler(
            broker=broker,
            sources=[RedisScheduleSource(settings.REDIS_URI)],
        )
