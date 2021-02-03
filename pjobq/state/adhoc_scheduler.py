"""
A slice of state living on the parent State object.

Keeping a cache of adhoc-scheduled jobs.
We try to keep the cache small, because if this process were to die,
we would lose all the cached jobs.
However, we must query the adhoc_jobs table at the same interval as our cache,
so it cannot be arbitrarily small.
"""

from asyncio import Task

from pjobq.models import AdhocJobModel


class AdhocSchedulerState:
    """
    Cache of jobs to run in the future.
    This is maintained as a dict of asyncio tasks, indexed by job id.
    When updating the job cache, if a job has been rescheduled, we cancel
    the existing task and create a new one.

    We refer to the current time range as the 'window'.
    """

    scheduled: dict[str, Task]
    adhoc_job_model: AdhocJobModel
    start_time: float
    end_time: float

    async def init(
        self,
        adhoc_job_model: AdhocJobModel,
    ):
        self.scheduled = {}
        self.adhoc_job_model = adhoc_job_model
        return self
