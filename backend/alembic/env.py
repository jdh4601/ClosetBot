from logging.config import fileConfig

from sqlalchemy import pool, create_engine
from alembic import context

import sys
import os

# Add app directory to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.db.database import Base
from app.core.config import settings

# Import all models so Alembic can detect them
from app.models import (
    User,
    BrandProfile,
    InfluencerProfile,
    MediaSnapshot,
    HashtagAggregate,
    AnalysisJob,
    AnalysisResult,
    CategoryTaxonomy,
)

# this is the Alembic Config object
config = context.config

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Add your model's MetaData object here for 'autogenerate' support
target_metadata = Base.metadata

# Override sqlalchemy.url with settings (prefer psycopg driver for sync)
sync_url = settings.DATABASE_URL
if sync_url.startswith("postgresql+asyncpg://"):
    sync_url = sync_url.replace("postgresql+asyncpg://", "postgresql+psycopg://")
elif sync_url.startswith("postgresql://"):
    # Ensure explicit psycopg driver for SQLAlchemy 2.x
    sync_url = sync_url.replace("postgresql://", "postgresql+psycopg://")
config.set_main_option("sqlalchemy.url", sync_url)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    # Use sync driver (psycopg) for migrations
    connectable = create_engine(sync_url, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
