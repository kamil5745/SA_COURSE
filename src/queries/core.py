from sqlalchemy import text, insert, select, update
from database import async_engine, sync_engine
from models import metadata_obj, workers_table

async def get_123_async():
    async with async_engine.connect() as conn:
        result = await conn.execute(text('SELECT 1,2,3 union select 4,5,6'))
        print(f'{result.first()=}')

def get_123_sync():
        with sync_engine.connect() as conn:
            result = conn.execute(text('SELECT 1,2,3 union select 4,5,6'))
            print(f'{result.first()=}')

class SyncCore:
    @staticmethod
    def create_tables():
        sync_engine.echo=False
        metadata_obj.metadata.drop_all(sync_engine) # type: ignore
        metadata_obj.metadata.create_all(sync_engine) # type: ignore
        sync_engine.echo=False

    @staticmethod
    def insert_data():
        with sync_engine.connect() as conn:
            stmt = insert(workers_table).values(
                [
                    {'username':'Jack'},
                    {'username':'Michael'}
                ]
            )
            conn.execute(stmt)
            conn.commit()
    
    @staticmethod
    def select_workers():
        with sync_engine.connect() as conn:
            query = select(workers_table)
            result = conn.execute(query)
            workers = result.all()
            print(f'{workers}')

    @staticmethod
    def update_workers(worker_id: int = 2, new_username: str = "Misha"):
        with sync_engine.connect() as conn:
            # stmt = text("UPDATE workers SET username=:username WHERE workers_id=:workers_id")
            # stmt = stmt.bindparams(username = new_username, workers_id = worker_id)
            stmt = (
                update(workers_table)
                .values(username = new_username)
                # .where(workers_table.c.workers_id == worker_id)
                .filter_by(workers_id = worker_id)
            )
            conn.execute(stmt)
            conn.commit()


class AsyncCore:
    # Асинхронный вариант, не показанный в видео
    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(metadata_obj.drop_all)
            await conn.run_sync(metadata_obj.create_all)