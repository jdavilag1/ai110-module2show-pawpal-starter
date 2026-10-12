from datetime import date

from diagrams.pawpal_system import Pet, Task


def test_task_completion_changes_status() -> None:
    task = Task(description="Feed Mochi", duration_minutes=10)

    assert task.completed is False

    task.mark_completed(on_date=date(2026, 10, 11))

    assert task.completed is True


def test_adding_task_increases_pet_task_count() -> None:
    pet = Pet(name="Mochi", species="dog")
    task = Task(description="Morning walk", duration_minutes=20)

    assert len(pet.tasks) == 0

    pet.add_task(task)

    assert len(pet.tasks) == 1
    assert pet.tasks[0] is task