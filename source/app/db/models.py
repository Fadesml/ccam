from sqlalchemy import Table, Column, Integer, MetaData, Boolean

metadata = MetaData()
users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, unique=True),
    Column("vk_id", Integer, unique=True, nullable=False),
    Column("subscribed_to_newsletter", Boolean(False), nullable=False),
)
