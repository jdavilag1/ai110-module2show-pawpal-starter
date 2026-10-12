from datetime import date, time

import pytest

from diagrams.pawpal_system import Owner, Pet, Scheduler, Task


PLAN_DATE = date(2026, 10, 12)


def test_owner_get_all_tasks_preserves_pet_association() -> None:
    dog = Pet("Mochi", "dog")
    cat = Pet("Biscuit", "cat")
    walk = Task("Walk", 20)
    feeding = Task("Feeding", 10)
    dog.add_task(walk)
    cat.add_task(feeding)
    owner = Owner("Jordan", 60)
    owner.add_pet(dog)
    owner.add_pet(cat)

    assert owner.get_all_tasks() == [(dog, walk), (cat, feeding)]


def test_owner_rejects_one_task_object_assigned_to_multiple_pets() -> None:
    shared_task = Task("Feeding", 10)
    dog = Pet("Mochi", "dog", tasks=[shared_task])
    cat = Pet("Biscuit", "cat", tasks=[shared_task])
    owner = Owner("Jordan", 60, pets=[dog, cat])

    with pytest.raises(ValueError, match="more than one pet"):
        owner.get_all_tasks()


def test_recurring_task_becomes_due_again_after_frequency_interval() -> None:
    daily = Task("Feeding", 10, frequency="daily")
    weekly = Task("Grooming", 30, frequency="weekly")
    daily.mark_completed(PLAN_DATE)
    weekly.mark_completed(PLAN_DATE)

    assert not daily.is_due(PLAN_DATE)
    assert daily.is_due(date(2026, 10, 13))
    assert daily.completed is False
    assert not weekly.is_due(date(2026, 10, 18))
    assert weekly.is_due(date(2026, 10, 19))


def test_scheduler_orders_tasks_and_uses_one_household_time_budget() -> None:
    dog = Pet("Mochi", "dog")
    cat = Pet("Biscuit", "cat")
    dog.add_task(Task("Walk", 20, priority="high"))
    dog.add_task(Task("Feeding", 10, category="feeding", priority="medium"))
    cat.add_task(Task("Grooming", 15, priority="medium"))
    owner = Owner("Jordan", 35, preferences=["feeding"])
    owner.add_pet(dog)
    owner.add_pet(cat)
    scheduler = Scheduler(start_time=time(8, 0))

    plan = scheduler.generate_daily_plan(owner, PLAN_DATE)

    assert [(pet.name, task.description) for pet, task in plan] == [
        ("Mochi", "Walk"),
        ("Mochi", "Feeding"),
    ]
    assert [task.scheduled_time for _, task in plan] == [time(8, 0), time(8, 20)]
    assert [(pet.name, task.description) for pet, task, _ in scheduler.unscheduled_tasks] == [
        ("Biscuit", "Grooming")
    ]
    assert "remaining daily time" in scheduler.explain_plan(plan)


def test_scheduler_skips_task_that_cannot_finish_by_due_time() -> None:
    pet = Pet("Mochi", "dog")
    pet.add_task(Task("Medication", 15, due_time=time(8, 10)))
    owner = Owner("Jordan", 60, pets=[pet])
    scheduler = Scheduler(start_time=time(8, 0))

    plan = scheduler.generate_daily_plan(owner, PLAN_DATE)

    assert plan == []
    assert "Cannot finish by its due time" in scheduler.unscheduled_tasks[0][2]
