from sqlalchemy import text, insert
from database import async_engine, sync_engine
from models import metadata_obj

async def get_123_async():
    async with async_engine.connect() as conn:
        result = await conn.execute(text('SELECT 1,2,3 union select 4,5,6'))
        print(f'{result.first()=}')

def get_123_sync():
    with sync_engine.connect() as conn:
        result = conn.execute(text('SELECT 1,2,3 union select 4,5,6'))
        print(f'{result.first()=}')


# def insert_data():
#     with sync_engine.connect() as conn:
#         stmt = insert(workers_table).values(
#             [
#                 {'username':'Bobr'},
#                 {'username':'Volk'}
#             ]
#         )
#         conn.execute(stmt)
#         conn.commit()