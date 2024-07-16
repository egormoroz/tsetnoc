from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


engine = create_async_engine(
    url="",
    echo=False,
)

session = async_sessionmaker(engine)




