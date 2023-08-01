from dataclasses import dataclass, field
from z3 import Int
from z3 import Optimize
from z3 import And
from z3 import Solver

# 1 Ten jobs numbered from 1 to 10 have to be executed without interrupt, and satisfying the following requirements:
#  • The running time of job i is i + 10, for i = 1, 2, . . . , 10.
#  • Job 3 may only start if jobs 1 and 2 have been finished.
#  • Job 6 may only start if jobs 2 and 4 have been finished.
#  • Job 7 may only start if jobs 1, 4 and 5 have been finished.
#  • Job 8 may only start if jobs 3 and 6 have been finished.
#  • Job 9 may only start if jobs 6 and 7 have been finished.
#  • Job 10 may only start if jobs 8 and 9 have been finished.
# What is the minimal total running time?


def main():
    s = Solver()
    optimize = Optimize()
    total_running_time_var = Int("tot_run_time")
    jobs = {}
    for i in range(1, 11):
        jobs[i] = JobTask(s, total_running_time_var, i)

    set_job_to_start_after_other_jobs(s, jobs[3], jobs[1])
    set_job_to_start_after_other_jobs(s, jobs[3], jobs[2])

    set_job_to_start_after_other_jobs(s, jobs[6], jobs[2])
    set_job_to_start_after_other_jobs(s, jobs[6], jobs[4])

    set_job_to_start_after_other_jobs(s, jobs[7], jobs[1])
    set_job_to_start_after_other_jobs(s, jobs[7], jobs[4])
    set_job_to_start_after_other_jobs(s, jobs[7], jobs[5])

    set_job_to_start_after_other_jobs(s, jobs[8], jobs[3])
    set_job_to_start_after_other_jobs(s, jobs[8], jobs[6])

    set_job_to_start_after_other_jobs(s, jobs[9], jobs[6])
    set_job_to_start_after_other_jobs(s, jobs[9], jobs[7])

    set_job_to_start_after_other_jobs(s, jobs[10], jobs[8])
    set_job_to_start_after_other_jobs(s, jobs[10], jobs[9])

    optimize.minimize(total_running_time_var)

    print(s.check())
    print(s.model())


@dataclass(frozen=False, order=True)  # frozen = false as this needs to be mutable
class JobTask:
    solver: Solver
    total_time: Int
    job_number: int

    def __post_init__(self):
        self.running_time = 10 + self.job_number
        self.instantiate_z3_vars()
        self.set_requirements_for_time_vars()
        self.set_job_length_to_start_end_diff()

    def instantiate_z3_vars(self):
        self.start_time_var = Int(f"start{self.job_number}")
        self.end_time_var = Int(f"end{self.job_number}")
        self.running_time_var = Int(f"job_{self.job_number}_duration")

    def set_requirements_for_time_vars(self):
        self.solver.add(self.running_time_var == self.running_time)
        self.solver.add(self.start_time_var >= 0)
        self.solver.add(self.end_time_var > 0)
        self.solver.add(self.running_time_var > 0)
        self.solver.add(self.start_time_var < self.end_time_var)
        self.solver.add(
            self.end_time_var <= self.total_time,
        )

    def set_job_length_to_start_end_diff(self):
        self.solver.add(
            self.running_time_var == self.end_time_var - self.start_time_var
        )


def set_job_to_start_after_other_jobs(
    solver: Solver, job_to_start: JobTask, jobs_to_finish_first: JobTask
):
    solver.add(job_to_start.start_time_var >= jobs_to_finish_first.end_time_var)


if __name__ == "__main__":
    main()
