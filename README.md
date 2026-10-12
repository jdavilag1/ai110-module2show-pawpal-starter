# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Run the demo from the repository root with `python main.py`. Sample terminal output:

```
Tasks Sorted by Due Time
07:30 - Breakfast
08:15 - Give medication
09:00 - Morning walk

Pending Tasks for Mochi
- Mochi: Morning walk
- Mochi: Breakfast

Completed Breakfast; next daily occurrence is due after 2026-10-11.

Conflict Check
Warning: 08:00 conflict: Morning walk for Mochi, Give medication for Biscuit are scheduled at the same time.

Today's Schedule
08:00 - Give medication for Biscuit (5 min, high priority)
08:05 - Morning walk for Mochi (25 min, high priority)
```

## 🧪 Testing PawPal+

Run the full test suite from the repository root:

```bash
python -m pytest
```

The tests cover task completion and addition, owner-to-pet/task relationships, recurring task creation, sorting and filtering, shared scheduling time limits, due-time constraints, and exact-time conflict warnings for tasks belonging to the same or different pets.

Successful terminal output:

```
============================= test session starts =============================
platform win32 -- Python 3.14.7, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\Davila\OneDrive\ai110-module2show-pawpal-starter
plugins: anyio-4.15.1
collected 10 items

tests\test_pawpal_system.py ..........                                   [100%]

============================== 10 passed in 0.04s ==============================
```

**Confidence level:** ★★★★☆ (4/5). The 10 tests cover the main model and scheduling behaviors, including recurring tasks and conflicts. This is good confidence in the tested cases, but not a guarantee against untested edge cases or broader real-world scheduling needs.

## Features

- **Final class diagram:** [diagrams/uml_final.mmd](diagrams/uml_final.mmd) shows the implemented classes, methods, and relationships. The implementation is in [diagrams/pawpal_system.py](diagrams/pawpal_system.py), and the interactive interface is in [app.py](app.py).
- **Pet and care tracking:** Add multiple pets and assign each one tasks with duration, due time, priority, and frequency.
- **Due-time sorting:** `Scheduler.sort_tasks()` sorts tasks by their zero-padded `HH:MM` due time, with tasks that have no due time last.
- **Task filtering:** `Scheduler.filter_tasks()` filters by pet name, completion status, or both.
- **Daily planning:** `Scheduler.generate_daily_plan()` orders due tasks using due times, priority, owner preferences, and pet/task names while observing one shared owner time budget.
- **Conflict warnings:** `Scheduler.detect_conflicts()` identifies tasks assigned the exact same start time. The Streamlit UI uses a warning message that names the conflicting tasks so the owner can review them. It does not detect duration overlaps.
- **Recurring care:** Completing a daily or weekly task through `Owner.mark_task_complete()` or `Pet.mark_task_complete()` marks that occurrence done and creates a separate next occurrence.
- **Plan explanations:** The scheduler reports planned tasks and why tasks did not fit; the Streamlit interface displays the results and warnings.

## Demo Walkthrough

1. Enter or update the owner's name, daily available minutes, and preferred task categories.
2. Add pets using the pet form. The list updates after submission.
3. Choose a pet and add care tasks with a duration, priority, frequency, category, and optional “complete by” time.
4. Use the All Tasks filters to view tasks for one pet or filter to pending/completed tasks. The table is sorted by due time.
5. Mark tasks complete from a pet's task panel. Daily and weekly tasks create a new occurrence; one-time tasks stay completed.
6. Select **Generate schedule** to see today's plan, skipped-task explanations, and a conflict warning if two tasks share an exact start time.

Run `python main.py` from the repository root for the command-line demonstration. Sample output:

```
Tasks Sorted by Due Time
07:30 - Breakfast
08:15 - Give medication
09:00 - Morning walk

Pending Tasks for Mochi
- Mochi: Morning walk
- Mochi: Breakfast

Completed Breakfast; next daily occurrence is due after 2026-10-11.

Conflict Check
Warning: 08:00 conflict: Morning walk for Mochi, Give medication for Biscuit are scheduled at the same time.

Today's Schedule
08:00 - Give medication for Biscuit (5 min, high priority)
08:05 - Morning walk for Mochi (25 min, high priority)
```
