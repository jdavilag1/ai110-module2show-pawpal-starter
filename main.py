from datetime import date, time

from diagrams.pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    owner = Owner(
        name="Jordan",
        available_minutes_per_day=90,
        preferences=["feeding"],
    )

    dog = Pet(name="Mochi", species="dog", breed="Shiba Inu", age_years=3)
    cat = Pet(name="Biscuit", species="cat", breed="Domestic Shorthair", age_years=5)

    dog.add_task(
        Task(
            description="Morning walk",
            duration_minutes=25,
            frequency="daily",
            priority="high",
            due_time=time(9, 0),
            category="exercise",
            scheduled_time=time(8, 0),
        )
    )
    dog.add_task(
        Task(
            description="Breakfast",
            duration_minutes=10,
            frequency="daily",
            priority="high",
            due_time=time(7, 30),
            category="feeding",
        )
    )
    cat.add_task(
        Task(
            description="Give medication",
            duration_minutes=5,
            frequency="daily",
            priority="high",
            due_time=time(8, 15),
            category="medication",
            scheduled_time=time(8, 0),
        )
    )

    owner.add_pet(dog)
    owner.add_pet(cat)

    scheduler = Scheduler(start_time=time(8, 0))
    all_tasks = [task for _, task in owner.get_all_tasks()]
    sorted_tasks = scheduler.sort_tasks(all_tasks)
    pending_mochi_tasks = scheduler.filter_tasks(
        owner,
        completed=False,
        pet_name="Mochi",
    )

    print("Tasks Sorted by Due Time")
    for task in sorted_tasks:
        print(f"{task.time or 'No due time'} - {task.description}")

    print("\nPending Tasks for Mochi")
    for pet, task in pending_mochi_tasks:
        print(f"- {pet.name}: {task.description}")

    breakfast = next(task for task in all_tasks if task.description == "Breakfast")
    next_breakfast = owner.mark_task_complete(breakfast, on_date=date.today())
    if next_breakfast is not None:
        print(
            f"\nCompleted Breakfast; next {next_breakfast.frequency} occurrence "
            f"is due after {next_breakfast.last_completed_on:%Y-%m-%d}."
        )

    print("\nConflict Check")
    conflict_warnings = scheduler.detect_conflicts(owner.get_all_tasks())
    if conflict_warnings:
        for warning in conflict_warnings:
            print(warning)
    else:
        print("No exact start-time conflicts found.")

    plan = scheduler.generate_daily_plan(owner, on_date=date.today())

    print("\nToday's Schedule")
    if plan:
        for pet, task in plan:
            start_at = task.scheduled_time.strftime("%H:%M")
            print(
                f"{start_at} - {task.description} for {pet.name} "
                f"({task.duration_minutes} min, {task.priority} priority)"
            )
    else:
        print("No tasks fit the schedule.")

    if scheduler.unscheduled_tasks:
        print("Not scheduled:")
        for pet, task, reason in scheduler.unscheduled_tasks:
            print(f"- {task.description} for {pet.name}: {reason}")


if __name__ == "__main__":
    main()
