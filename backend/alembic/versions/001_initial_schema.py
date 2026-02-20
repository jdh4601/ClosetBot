"""Initial schema with 8 tables

Revision ID: 001_initial_schema
Revises:
Create Date: 2026-02-20 12:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "001_initial_schema"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create users table
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )

    # Create brand_profiles table
    op.create_table(
        "brand_profiles",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("ig_username", sa.String(length=30), nullable=False),
        sa.Column("ig_id", sa.String(length=50), nullable=True),
        sa.Column("name", sa.String(length=100), nullable=True),
        sa.Column("followers_count", sa.Integer(), nullable=True),
        sa.Column("media_count", sa.Integer(), nullable=True),
        sa.Column("biography", sa.Text(), nullable=True),
        sa.Column("website", sa.String(length=255), nullable=True),
        sa.Column("profile_picture_url", sa.String(length=500), nullable=True),
        sa.Column("is_verified", sa.Boolean(), nullable=True),
        sa.Column("categories", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column(
            "extracted_keywords", postgresql.JSONB(astext_type=sa.Text()), nullable=True
        ),
        sa.Column("last_fetched_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("ig_username"),
    )
    op.create_index(
        op.f("ix_brand_profiles_ig_username"),
        "brand_profiles",
        ["ig_username"],
        unique=False,
    )

    # Create influencer_profiles table
    op.create_table(
        "influencer_profiles",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("ig_username", sa.String(length=30), nullable=False),
        sa.Column("ig_id", sa.String(length=50), nullable=True),
        sa.Column("name", sa.String(length=100), nullable=True),
        sa.Column("followers_count", sa.Integer(), nullable=True),
        sa.Column("follows_count", sa.Integer(), nullable=True),
        sa.Column("media_count", sa.Integer(), nullable=True),
        sa.Column("biography", sa.Text(), nullable=True),
        sa.Column("website", sa.String(length=255), nullable=True),
        sa.Column("profile_picture_url", sa.String(length=500), nullable=True),
        sa.Column("is_verified", sa.Boolean(), nullable=True),
        sa.Column("categories", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("avg_engagement_rate", sa.Integer(), nullable=True),
        sa.Column("last_fetched_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("ig_username"),
    )
    op.create_index(
        op.f("ix_influencer_profiles_ig_username"),
        "influencer_profiles",
        ["ig_username"],
        unique=False,
    )

    # Create category_taxonomy table
    op.create_table(
        "category_taxonomy",
        sa.Column("slug", sa.String(length=50), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("keywords", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("weight", sa.Integer(), nullable=True),
        sa.Column("parent_slug", sa.String(length=50), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["parent_slug"],
            ["category_taxonomy.slug"],
        ),
        sa.PrimaryKeyConstraint("slug"),
    )

    # Create analysis_jobs table
    op.create_table(
        "analysis_jobs",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("brand_profile_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "influencer_usernames",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
        ),
        sa.Column("status", sa.String(length=20), nullable=True),
        sa.Column("api_calls_used", sa.Integer(), nullable=True),
        sa.Column("api_calls_estimated", sa.Integer(), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["brand_profile_id"],
            ["brand_profiles.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create media_snapshots table
    op.create_table(
        "media_snapshots",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("profile_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("profile_type", sa.String(length=10), nullable=False),
        sa.Column("ig_media_id", sa.String(length=50), nullable=False),
        sa.Column("caption", sa.Text(), nullable=True),
        sa.Column("comments_count", sa.Integer(), nullable=True),
        sa.Column("like_count", sa.Integer(), nullable=True),
        sa.Column("media_type", sa.String(length=20), nullable=True),
        sa.Column("permalink", sa.String(length=500), nullable=True),
        sa.Column("posted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "fetched_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create hashtag_aggregates table
    op.create_table(
        "hashtag_aggregates",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("profile_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("profile_type", sa.String(length=10), nullable=False),
        sa.Column("hashtag", sa.String(length=100), nullable=False),
        sa.Column("count", sa.Integer(), nullable=True),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_hashtag_aggregates_hashtag"),
        "hashtag_aggregates",
        ["hashtag"],
        unique=False,
    )

    # Create analysis_results table
    op.create_table(
        "analysis_results",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("job_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "influencer_profile_id", postgresql.UUID(as_uuid=True), nullable=False
        ),
        sa.Column("similarity_score", sa.Integer(), nullable=True),
        sa.Column("engagement_score", sa.Integer(), nullable=True),
        sa.Column("category_score", sa.Integer(), nullable=True),
        sa.Column("final_score", sa.Integer(), nullable=True),
        sa.Column("grade", sa.String(length=1), nullable=True),
        sa.Column("top_posts", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column(
            "collab_signals", postgresql.JSONB(astext_type=sa.Text()), nullable=True
        ),
        sa.Column(
            "common_hashtags", postgresql.JSONB(astext_type=sa.Text()), nullable=True
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["influencer_profile_id"],
            ["influencer_profiles.id"],
        ),
        sa.ForeignKeyConstraint(
            ["job_id"],
            ["analysis_jobs.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("analysis_results")
    op.drop_index(
        op.f("ix_hashtag_aggregates_hashtag"), table_name="hashtag_aggregates"
    )
    op.drop_table("hashtag_aggregates")
    op.drop_table("media_snapshots")
    op.drop_table("analysis_jobs")
    op.drop_table("category_taxonomy")
    op.drop_index(
        op.f("ix_influencer_profiles_ig_username"), table_name="influencer_profiles"
    )
    op.drop_table("influencer_profiles")
    op.drop_index(op.f("ix_brand_profiles_ig_username"), table_name="brand_profiles")
    op.drop_table("brand_profiles")
    op.drop_table("users")
