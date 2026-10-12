"""Core data models and daily scheduling for PawPal+."""

from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta
from typing import Literal

Frequency = Literal["once", "daily", "weekly"]
Priority = Literal["low", "medium", "high"]


@dataclass
class Task:
    """A single pet-care activity, optionally repeated on a schedule."""

    description: str
    duration_minutes: int
    frequency: Frequency = "daily"
    priority: Priority = "medium"
    due_time: time | None = None
    category: str = "general"
    completed: bool = False
    scheduled_time: time | None = None
    last_completed_on: date | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.description, str) or not self.description.strip():
            raise ValueError("Task description cannot be empty.")
        if self.duration_minutes <= 0:
            raise ValueError("Task duration must be greater than zero.")
        if self.frequency not in ("once", "daily", "weekly"):
            raise ValueError("Frequency must be 'once', 'daily', or 'weekly'.")
        if self.priority not in ("low", "medium", "high"):
            raise ValueError("Priority must be 'low', 'medium', or 'high'.")
        if self.completed and self.last_completed_on is None:
            self.last_completed_on = date.today()

    @property
    def title(self) -> str:
        """Compatibility alias for code that refers to a task's title."""
        return self.description

    def mark_completed(self, on_date: date | None = None) -> None:
        """Mark this occurrence complete on the supplied date or today."""
        self.completed = True
        self.last_completed_on = on_date or date.today()

    def is_due(self, on_date: date | None = None) -> bool:
        """Return whether this task has an occurrence due on the given date.

        For recurring tasks, roll the completion flag forward when a new
        occurrence becomes due.
        """
        check_date = on_date or date.today()

        if self.frequency == "once":
            return not self.completed
        if self.last_completed_on is None:
            return True
        if self.frequency == "daily":
            due = self.last_completed_on < check_date
        else:
            due = (check_date - self.last_completed_on).days >= 7
        if due:
            self.completed = False
        return due


@dataclass
class Pet:
    """A pet and the care tasks associated with it."""

    name: str
    species: str
    breed: str = ""
    age_years: int | None = None
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        if any(existing is task for existing in self.tasks):
            raise ValueError(f"Task {task.description!r} is already assigned to {self.name}.")
        self.tasks.append(task)

    def list_pending_tasks(self, on_date: date | None = None) -> list[Task]:
        return [
            task for task in self.tasks
            if task.is_due(on_date)
        ]


@dataclass
class Owner:
    """An owner, their pets, and household-wide scheduling constraints."""

    name: str
    available_minutes_per_day: int
    preferences: list[str] = field(default_factory=list)
    pets: list[Pet] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not 0 <= self.available_minutes_per_day <= 1440:
            raise ValueError("Available minutes per day must be between 0 and 1440.")

    def add_pet(self, pet: Pet) -> None:
        if any(existing is pet for existing in self.pets):
            raise ValueError(f"Pet {pet.name!r} is already registered to {self.name}.")
        self.pets.append(pet)

    def update_preferences(self, preferences: list[str]) -> None:
        self.preferences = [preference.strip() for preference in preferences if preference.strip()]

    def get_all_tasks(self) -> list[tuple[Pet, Task]]:
        """Return every pet/task pair, preserving each task's pet association."""
        assignments: list[tuple[Pet, Task]] = []
        assigned_task_ids: set[int] = set()
        for pet in self.pets:
            for task in pet.tasks:
                if id(task) in assigned_task_ids:
                    raise ValueError(
                        f"Task {task.description!r} is assigned to more than one pet."
                    )
                assigned_task_ids.add(id(task))
                assignments.append((pet, task))
        return assignments


class Scheduler:
    """Builds a prioritized daily plan under one shared owner time budget."""

    _PRIORITY_RANK: dict[str, int] = {"high": 0, "medium": 1, "low": 2}

    def __init__(self, start_time: time = time(8, 0)) -> None:
        self.start_time = start_time
        self.unscheduled_tasks: list[tuple[Pet, Task, str]] = []

    def generate_daily_plan(
        self,
        owner: Owner,
        on_date: date | None = None,
    ) -> list[tuple[Pet, Task]]:
        """Schedule due tasks; return (pet, task) pairs in start-time order."""
        plan_date = on_date or date.today()
        self.unscheduled_tasks = []
        candidates: list[tuple[Pet, Task]] = []
        for pet, task in owner.get_all_tasks():
            task.scheduled_time = None
            if task.is_due(plan_date):
                candidates.append((pet, task))
        candidates.sort(key=lambda item: self._sort_key(item[0], item[1], owner))

        plan: list[tuple[Pet, Task]] = []
        elapsed_minutes = 0
        for pet, task in candidates:
            end_elapsed = elapsed_minutes + task.duration_minutes
            if end_elapsed > owner.available_minutes_per_day:
                self.unscheduled_tasks.append(
                    (pet, task, "Exceeds the owner's remaining daily time.")
                )
                continue

            start_minutes = self.start_time.hour * 60 + self.start_time.minute
            if start_minutes + end_elapsed > 1440:
                self.unscheduled_tasks.append(
                    (pet, task, "Would extend beyond the end of the day.")
                )
                continue

            start_at = self._add_minutes(self.start_time, elapsed_minutes)
            end_at = self._add_minutes(self.start_time, end_elapsed)
            if task.due_time is not None and end_at > task.due_time:
                self.unscheduled_tasks.append(
                    (pet, task, f"Cannot finish by its due time ({task.due_time:%H:%M}).")
                )
                continue

            task.scheduled_time = start_at
            plan.append((pet, task))
            elapsed_minutes = end_elapsed

        return plan

    def explain_plan(self, plan: list[tuple[Pet, Task]]) -> str:
        if not plan:
            message = "No tasks fit the schedule."
        else:
            lines = ["Today's plan:"]
            for pet, task in plan:
                start_at = task.scheduled_time.strftime("%H:%M") if task.scheduled_time else "unscheduled"
                lines.append(
                    f"- {start_at} — {task.description} for {pet.name} "
                    f"({task.duration_minutes} min, {task.priority} priority)"
                )
            message = "\n".join(lines)

        if self.unscheduled_tasks:
            skipped = ["Not scheduled:"]
            skipped.extend(
                f"- {task.description} for {pet.name}: {reason}"
                for pet, task, reason in self.unscheduled_tasks
            )
            message += "\n" + "\n".join(skipped)
        return message

    def _sort_key(
        self,
        pet: Pet,
        task: Task,
        owner: Owner,
    ) -> tuple[int, time, int, int, str, str]:
        preferred_terms = {term.casefold() for term in owner.preferences}
        preference_rank = 0 if (
            task.category.casefold() in preferred_terms
            or any(term in task.description.casefold() for term in preferred_terms)
        ) else 1
        return (
            0 if task.due_time is not None else 1,
            task.due_time or time.max,
            self._PRIORITY_RANK[task.priority],
            preference_rank,
            pet.name.casefold(),
            task.description.casefold(),
        )

    @staticmethod
    def _add_minutes(start: time, minutes: int) -> time:
        start_datetime = datetime.combine(date.min, start)
        return (start_datetime + timedelta(minutes=minutes)).time()
