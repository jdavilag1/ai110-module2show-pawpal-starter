from dataclasses import dataclass, field


@dataclass
class Owner:
    name: str
    available_minutes_per_day: int
    preferences: list[str] = field(default_factory=list)
    pets: list["Pet"] = field(default_factory=list)

    def add_pet(self, pet: "Pet") -> None:
        pass

    def update_preferences(self, preferences: list[str]) -> None:
        pass


@dataclass
class Pet:
    name: str
    species: str
    breed: str
    age_years: int
    tasks: list["Task"] = field(default_factory=list)

    def add_task(self, task: "Task") -> None:
        pass

    def list_pending_tasks(self) -> list["Task"]:
        raise NotImplementedError


@dataclass
class Task:
    title: str
    category: str
    duration_minutes: int
    priority: str
    due_time: str
    completed: bool
    scheduled_time: str

    def mark_completed(self) -> None:
        pass

    def is_due(self) -> bool:
        raise NotImplementedError


class Scheduler:
    def generate_daily_plan(self, owner: Owner) -> list[Task]:
        raise NotImplementedError

    def explain_plan(self, plan: list[Task]) -> str:
        raise NotImplementedError