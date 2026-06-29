import asyncio
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from queries.orm import SyncORM, AsyncORM
from queries.core import SyncCore, AsyncCore


SyncORM.create_tables()
SyncORM.insert_workers()

# SyncCore.create_tables()
# SyncCore.insert_data()

SyncORM.select_workers()
SyncORM.update_workers()

SyncORM.insert_resumes()
# SyncORM.select_resumes_avg_compensation()

# SyncORM.select_workers_with_lazy_relationship()
# SyncORM.select_workers_with_joined_relationship()
# SyncORM.select_workers_with_selectin_relationship()
SyncORM.select_workers_with_condition_relationship()
SyncORM.select_workers_with_condition_relationship_contains_eager()

async def async_main():
    await AsyncORM.insert_additional_resumes()
    await AsyncORM.join_cte_subquery_window_func()

asyncio.run(async_main())


# SyncCore.select_workers()
# SyncCore.update_workers()



# asyncio.run(async_insert_data())