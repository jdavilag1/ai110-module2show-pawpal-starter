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


def test_completing_recurring_task_creates_next_due_occurrence() -> None:
    daily = Task("Feeding", 10, frequency="daily")
    weekly = Task("Grooming", 30, frequency="weekly")
    next_daily = daily.mark_completed(PLAN_DATE)
    next_weekly = weekly.mark_completed(PLAN_DATE)

    assert not daily.is_due(PLAN_DATE)
    assert daily.completed is True
    assert next_daily is not None
    assert next_daily is not daily
    assert not next_daily.is_due(PLAN_DATE)
    assert next_daily.is_due(date(2026, 10, 13))
    assert next_weekly is not None
    assert not next_weekly.is_due(date(2026, 10, 18))
    assert next_weekly.is_due(date(2026, 10, 19))


def test_owner_completing_recurring_task_adds_next_occurrence_to_pet() -> None:
    pet = Pet("Mochi", "dog")
    task = Task("Walk", 20, frequency="daily")
    pet.add_task(task)
    owner = Owner("Jordan", 60, pets=[pet])

    next_occurrence = owner.mark_task_complete(task, PLAN_DATE)

    assert task.completed is True
    assert len(pet.tasks) == 2
    assert pet.tasks[1] is next_occurrence
    assert next_occurrence is not None
    assert next_occurrence.completed is False


def test_completing_one_time_task_does_not_create_another_occurrence() -> None:
    task = Task("Vet appointment", 30, frequency="once")

    next_occurrence = task.mark_completed(PLAN_DATE)

    assert task.completed is True
    assert next_occurrence is None


def test_scheduler_sorts_and_filters_tasks() -> None:
    dog = Pet("Mochi", "dog")
    cat = Pet("Biscuit", "cat")
    late = Task("Evening walk", 20, due_time=time(18, 0))
    early = Task("Medication", 5, due_time=time(8, 5))
    no_due_time = Task("Play time", 15, due_time=None)
    completed = Task("Breakfast", 10, due_time=time(7, 0), completed=True)
    dog.add_task(late)
    dog.add_task(completed)
    cat.add_task(early)
    owner = Owner("Jordan", 60, pets=[dog, cat])

    sorted_tasks = Scheduler.sort_tasks([late, no_due_time, early, completed])
    pending_for_dog = Scheduler.filter_tasks(owner, completed=False, pet_name="mochi")
    completed_tasks = Scheduler.filter_tasks(owner, completed=True)

    assert sorted_tasks == [completed, early, late, no_due_time]
    assert pending_for_dog == [(dog, late)]
    assert completed_tasks == [(dog, completed)]


def test_scheduler_detects_same_pet_exact_start_time_conflict() -> None:
    pet = Pet("Mochi", "dog")
    walk = Task("Walk", 20, scheduled_time=time(8, 0))
    feeding = Task("Feeding", 10, scheduled_time=time(8, 0))
    pet.add_task(walk)
    pet.add_task(feeding)

    warnings = Scheduler.detect_conflicts([(pet, walk), (pet, feeding)])

    assert warnings == [
        "Warning: 08:00 conflict: Walk for Mochi, Feeding for Mochi "
        "are scheduled at the same time."
    ]
    assert walk.scheduled_time == feeding.scheduled_time == time(8, 0)


def test_scheduler_detects_conflicts_across_pets_and_ignores_unscheduled_tasks() -> None:
    dog = Pet("Mochi", "dog")
    cat = Pet("Biscuit", "cat")
    walk = Task("Walk", 20, scheduled_time=time(8, 0))
    medication = Task("Medication", 5, scheduled_time=time(8, 0))
    grooming = Task("Grooming", 30)

    warnings = Scheduler.detect_conflicts(
        [(dog, walk), (cat, medication), (cat, grooming)]
    )

    assert len(warnings) == 1
    assert "Walk for Mochi" in warnings[0]
    assert "Medication for Biscuit" in warnings[0]
    assert grooming.scheduled_time is None


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
