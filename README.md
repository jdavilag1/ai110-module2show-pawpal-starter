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

============================== 10 passed in 0.03s ==============================
```

**Confidence level:** ★★★★☆ (4/5). The 10 tests cover the main model and scheduling behaviors, including recurring tasks and conflicts. This is good confidence in the tested cases, but not a guarantee against untested edge cases or broader real-world scheduling needs.

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_tasks`, `Scheduler._sort_key` | `sort_tasks` uses a lambda key on zero-padded `HH:MM` due-time strings; daily scheduling then considers priority, owner preference, and stable names. |
| Filtering | `Scheduler.filter_tasks`, `Task.is_due`, `Scheduler.generate_daily_plan` | Filters by completion status or pet name; excludes tasks not due and skips tasks that exceed the shared owner time budget. |
| Conflict detection | `Scheduler.detect_conflicts` | Returns non-fatal warnings for tasks with identical scheduled start times, whether they belong to the same pet or different pets. It does not detect duration overlaps. |
| Recurring tasks | `Owner.mark_task_complete`, `Pet.mark_task_complete`, `Task.mark_completed`, `Task.is_due` | Completing a daily or weekly occurrence adds a new task instance due on the next day or in seven days; once tasks do not recur. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
