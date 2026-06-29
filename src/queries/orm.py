from sqlalchemy import Integer, and_, select, text, insert, func, cast
from database import async_engine, sync_engine, session_factory, async_session_factory, Base
from models import ResumesOrm, WorkersOrm
from sqlalchemy.orm import aliased, joinedload, selectinload, contains_eager

        
class SyncORM:
    @staticmethod
    def create_tables():
        sync_engine.echo = False
        Base.metadata.drop_all(sync_engine)
        Base.metadata.create_all(sync_engine)
        sync_engine.echo = False

    @staticmethod
    def select_workers():
        with session_factory() as session:
            query = select(WorkersOrm)
            result = session.execute(query)
            workers = result.scalars().all()
            print(f'{workers=}')
            return workers            

    @staticmethod
    def update_workers(worker_id: int = 2, new_username: str = "Misha"):
        with session_factory() as session:
            worker_michael = session.get(WorkersOrm, worker_id) # worker_id OR {"id": worker_id} OR (worker_id) OR (worker_id, 2) 
            worker_michael.username = new_username # type: ignore
            session.refresh(worker_michael)
            session.commit()

    @staticmethod
    def insert_workers():
        with session_factory() as session:
            worker_jack = WorkersOrm(username="Jack")
            worker_michael = WorkersOrm(username="Michael")
            session.add_all([worker_jack, worker_michael])
            # flush отправляет запрос в базу данных
            # После flush каждый из работников получает первичный ключ id, который отдала БД
            session.flush()
            session.commit()

    @staticmethod
    def insert_resumes():
        with session_factory() as session:
            resume_jack_1 = ResumesOrm(
                title='Python Junior Developer', compensation=50000, workload='fulltime', worker_id=1)
            resume_jack_2 = ResumesOrm(
                title='Python Разработчик', compensation=150000, workload='fulltime', worker_id=1)
            resume_michael_1 = ResumesOrm(
                title='Python Data Engineer', compensation=250000, workload='parttime',  worker_id=2)
            resume_michael_2 = ResumesOrm(
                title='Data Scientist', compensation=300000, workload='fulltime', worker_id=2)
            session.add_all([resume_jack_1, resume_jack_2, 
                             resume_michael_1, resume_michael_2])
            session.commit()
    
    @staticmethod
    def select_resumes_avg_compensation(like_language: str = "Python"):
        """SELECT workload, avg(c)::int as  avg_compensation
        FROM resumes
        where title like '%Python%' and compensation > 40000 
        group by workload"""
        with session_factory() as session:
            query = (
                select(
                    ResumesOrm.workload,
                    cast(func.avg(ResumesOrm.compensation), Integer).label('avg_compensation'),
                )
                .select_from(ResumesOrm)
                .filter(and_(
                    ResumesOrm.title.contains(like_language),
                    ResumesOrm.compensation > 40000,
                ))
                .group_by(ResumesOrm.workload)
                .having(cast(func.avg(ResumesOrm.compensation), Integer) > 70000)
            )
            print(query.compile(compile_kwargs={'literal_binds': True}))
            res = session.execute(query)
            result = res.all()
            print(result[0].avg_compensation)

    @staticmethod
    def select_workers_with_lazy_relationship():
        with session_factory() as session:
            query = (
                select(WorkersOrm)
            )
            res = session.execute(query)
            result = res.scalars().all()

            workers_1_resumes = result[0].resumes
            print(workers_1_resumes)

            workers_2_resumes = result[1].resumes
            print(workers_2_resumes)

    @staticmethod
    def select_workers_with_joined_relationship():
        with session_factory() as session:
            query = (
                select(WorkersOrm)
                .options(joinedload(WorkersOrm.resumes))
            )
            res = session.execute(query)
            result = res.unique().scalars().all()

            workers_1_resumes = result[0].resumes
            print(workers_1_resumes)

            workers_2_resumes = result[1].resumes
            print(workers_2_resumes)

    @staticmethod
    def select_workers_with_selectin_relationship():
        with session_factory() as session:
            query = (
                select(WorkersOrm)
                .options(selectinload(WorkersOrm.resumes))
            )
            res = session.execute(query)
            result = res.unique().scalars().all()

            workers_1_resumes = result[0].resumes
            print(workers_1_resumes)

            workers_2_resumes = result[1].resumes
            print(workers_2_resumes)
            
    @staticmethod
    def select_workers_with_condition_relationship():
        with session_factory() as session:
            query = (
                select(WorkersOrm)
                .options(selectinload(WorkersOrm.resumes_parttime))
            )
            res = session.execute(query)
            result = res.unique().scalars().all()
            print(result)

    @staticmethod
    def select_workers_with_condition_relationship_contains_eager():
        with session_factory() as session:
            query = (
                select(WorkersOrm)
                .join(WorkersOrm.resumes)
                .options(contains_eager(WorkersOrm.resumes))
                .filter(ResumesOrm.workload == "parttime")
            )
            res = session.execute(query)
            result = res.unique().scalars().all()
            print(result)
            
    @staticmethod
    def select_workers_with_relationship_contains_eager_with_limit():
        with session_factory() as session:
            subq = (
                select(ResumesOrm.resumes_id.label("parttime_resume_id"))
                .filter(ResumesOrm.worker_id == WorkersOrm.worker_id)
                .order_by(WorkersOrm.worker_id.desc())
                .limit(2)
                .scalar_subquery()
                .correlate(WorkersOrm)
            )

            query = (
                select(WorkersOrm)
                .join(ResumesOrm, ResumesOrm.resumes_id.in_(subq))
                .options(contains_eager(WorkersOrm.resumes))
            )

            res = session.execute(query)
            result = res.unique().scalars().all()
            print(result)

class AsyncORM:
    @staticmethod
    async def async_insert_data():
        async with async_session_factory() as session:
            worker_bobr = WorkersOrm(username="Bobr")
            worker_volk = WorkersOrm(username="Volk")
            session.add_all([worker_volk, worker_bobr])
            await session.commit()
    @staticmethod
    async def insert_additional_resumes():
        async with async_session_factory() as session:
            workers = [
                    {'username': 'Artem'}, # id 3
                    {'username': 'Roman'}, # id 4
                    {'username': 'Petr'} # id 5
            ]
            resumes = [
                {"title": "Python программист", "compensation": 60000, "workload": "fulltime", "worker_id": 3},
                {"title": "Machine Learning Engineer", "compensation": 70000, "workload": "parttime", "worker_id": 3},
                {"title": "Python Data Scientist", "compensation": 80000, "workload": "parttime", "worker_id": 4},
                {"title": "Python Analyst", "compensation": 90000, "workload": "fulltime", "worker_id": 4},
                {"title": "Python Junior Developer", "compensation": 100000, "workload": "fulltime", "worker_id": 5},
            ]
            insert_workers = insert(WorkersOrm).values(workers)
            insert_resumes = insert(ResumesOrm).values(resumes)
            await session.execute(insert_workers)
            await session.execute(insert_resumes)
            await session.commit()

    @staticmethod
    async def join_cte_subquery_window_func(like_language: str = "Python"):
        """WITH helper2 AS (
            SELECT *, compensation - avg_workload_compensation AS compensation_diff
            FROM
            (SELECT 
                w.worker_id, 
                w.username, 
                r.compensation, 
                r.workload, 
                avg(r.compensation) OVER (PARTITION BY workload)::int AS avg_workload_compensation
            FROM public.resumes r
            join workers w using (worker_id)) helper1
        )
        SELECT * FROM helper2
        ORDER BY compensation_diff DESC
        """
        async with async_session_factory() as session:
            r = aliased(ResumesOrm)
            w = aliased(WorkersOrm)

            subq = (
                select(
                    w, 
                    r,
                    func.avg(r.compensation).over(partition_by=r.workload).cast(Integer).label('avg_workload_compensation')
                )
                # .select_from(r)
                .join(w, w.worker_id==r.worker_id).subquery('helper1') #.join(WorkersOrm, isouter=True) Левый join, правый в Alchemy нет
            )
            cte = (
                select(
                    subq.c.worker_id,
                    subq.c.username,
                    subq.c.compensation,
                    subq.c.avg_workload_compensation,
                    (subq.c.compensation - subq.c.avg_workload_compensation).label('compensation_diff'),
                    subq.c.worker_id,
                    subq.c.worker_id,

                )
                .cte('helper2')
            )
            query = (
                select(cte)
                .order_by(cte.c.compensation_diff.desc())
            )
            # print(query.compile(compile_kwargs={'literal_binds': True}))
            res = await session.execute(query)
            result = res.all()

            # print(f'{result=}')






