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
        )
    )
    dog.add_task(
        Task(
            description="Breakfast",
            duration_minutes=10,
            frequency="daily",
            priority="high",
            due_time=time(8, 45),
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
        )
    )

    owner.add_pet(dog)
    owner.add_pet(cat)

    scheduler = Scheduler(start_time=time(8, 0))
    plan = scheduler.generate_daily_plan(owner, on_date=date.today())

    print("Today's Schedule")
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
