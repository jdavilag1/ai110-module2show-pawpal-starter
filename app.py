from datetime import date, time

import streamlit as st

from diagrams.pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")
st.markdown(
    "Plan your pets' care tasks around your available time, priorities, and preferences."
)

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", available_minutes_per_day=90)
if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler()
if "daily_plan" not in st.session_state:
    st.session_state.daily_plan = None

owner: Owner = st.session_state.owner
scheduler: Scheduler = st.session_state.scheduler

st.subheader("Owner")
owner_col, availability_col = st.columns(2)
with owner_col:
    owner.name = st.text_input("Owner name", value=owner.name, key="owner_name")
with availability_col:
    owner.available_minutes_per_day = st.number_input(
        "Available minutes per day",
        min_value=0,
        max_value=1440,
        value=owner.available_minutes_per_day,
        key="owner_available_minutes",
    )
preferences = st.text_input(
    "Preferences (comma-separated task categories)",
    value=", ".join(owner.preferences),
)
owner.update_preferences(preferences.split(","))

st.subheader("Pets")
with st.form("add_pet_form", clear_on_submit=True):
    pet_name = st.text_input("Pet name")
    pet_species = st.selectbox("Species", ["dog", "cat", "other"])
    pet_breed = st.text_input("Breed (optional)")
    pet_age = st.number_input("Age in years", min_value=0, max_value=100, value=0)
    add_pet_submitted = st.form_submit_button("Add pet")

if add_pet_submitted:
    if not pet_name.strip():
        st.error("Enter a name for the pet.")
    elif any(pet.name.casefold() == pet_name.strip().casefold() for pet in owner.pets):
        st.error("A pet with that name is already in the household.")
    else:
        owner.add_pet(
            Pet(
                name=pet_name.strip(),
                species=pet_species,
                breed=pet_breed.strip(),
                age_years=int(pet_age) if pet_age else None,
            )
        )
        st.session_state.daily_plan = None
        st.success(f"Added {pet_name.strip()}.")

if owner.pets:
    st.write("Pets in your household:")
    st.write(", ".join(f"{pet.name} ({pet.species})" for pet in owner.pets))
else:
    st.info("Add a pet before adding care tasks.")

st.subheader("Care Tasks")
if owner.pets:
    selected_pet_index = st.selectbox(
        "Choose a pet",
        options=range(len(owner.pets)),
        format_func=lambda index: owner.pets[index].name,
    )
    selected_pet = owner.pets[selected_pet_index]

    with st.form("add_task_form", clear_on_submit=True):
        task_description = st.text_input("Task description", placeholder="Morning walk")
        task_col1, task_col2 = st.columns(2)
        with task_col1:
            duration = st.number_input(
                "Duration (minutes)", min_value=1, max_value=240, value=20
            )
            frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])
        with task_col2:
            priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
            due_time = st.time_input("Complete by (optional)", value=time(9, 0))
        category = st.text_input("Category", value="general")
        add_task_submitted = st.form_submit_button("Add task")

    if add_task_submitted:
        if not task_description.strip():
            st.error("Enter a description for the task.")
        else:
            selected_pet.add_task(
                Task(
                    description=task_description.strip(),
                    duration_minutes=int(duration),
                    frequency=frequency,
                    priority=priority,
                    due_time=due_time,
                    category=category.strip() or "general",
                )
            )
            st.session_state.daily_plan = None
            st.success(f"Added task for {selected_pet.name}.")

    for pet_index, pet in enumerate(owner.pets):
        with st.expander(f"{pet.name}'s tasks", expanded=True):
            if pet.tasks:
                st.table(
                    [
                        {
                            "Task": task.description,
                            "Duration (min)": task.duration_minutes,
                            "Priority": task.priority,
                            "Frequency": task.frequency,
                            "Status": "Completed" if task.completed else "Pending",
                        }
                        for task in pet.tasks
                    ]
                )
            else:
                st.caption("No care tasks added yet.")

            incomplete_tasks = [task for task in pet.tasks if not task.completed]
            if incomplete_tasks:
                with st.form(f"complete_task_form_{pet_index}"):
                    task_index = st.selectbox(
                        "Task to mark complete",
                        options=range(len(incomplete_tasks)),
                        format_func=lambda index: incomplete_tasks[index].description,
                        key=f"complete_task_selection_{pet_index}",
                    )
                    complete_submitted = st.form_submit_button("Mark task complete")
                if complete_submitted:
                    completed_task = incomplete_tasks[task_index]
                    next_occurrence = owner.mark_task_complete(
                        completed_task,
                        on_date=date.today(),
                    )
                    st.session_state.daily_plan = None
                    if next_occurrence is None:
                        st.success(f"Marked {completed_task.description} complete.")
                    else:
                        st.success(
                            f"Marked {completed_task.description} complete. "
                            f"Added the next {next_occurrence.frequency} occurrence."
                        )

st.divider()
st.subheader("Today's Schedule")
if st.button("Generate schedule", disabled=not owner.pets):
    st.session_state.daily_plan = scheduler.generate_daily_plan(
        owner,
        on_date=date.today(),
    )

if st.session_state.daily_plan is not None:
    st.text(scheduler.explain_plan(st.session_state.daily_plan))
