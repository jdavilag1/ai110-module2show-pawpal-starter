# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- My first diagram had four classes: Owner, Pet, Task, and Scheduler. Owner keeps the pets, each pet keeps its tasks, and Scheduler makes a daily plan.

**b. Design changes**

I added methods for filtering and sorting tasks, checking time conflicts, and creating the next occurrence of a recurring task. I also made the available time one shared limit for all the owner's pets.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- The scheduler checks due times, priority, owner preferences, and the owner's available minutes. Tasks that do not fit are listed as skipped.
- I put due times and high priority tasks first because they are the most important to finish on time.

**b. Tradeoffs**

The conflict check only reports tasks with the exact same scheduled start time. It does not check whether tasks with different start times overlap because of their durations. This keeps the check simple. A future version could check for overlapping time ranges.

The check groups tasks by start time in one pass instead of comparing every pair. This is easier to read and works efficiently for a small schedule.

---

## 3. AI Collaboration

**a. How you used AI**

- I used the AI coding assistant to brainstorm the UML, write class code, add tests, connect the Streamlit UI, and update the documentation.
- Asking it to explain a specific feature and then run tests was most helpful.

**b. Judgment and verification**

- I changed the first conflict-check idea so it only gives a warning and does not stop the program. I ran the tests and the command-line demo to check it.

---

## 4. Testing and Verification

**a. What you tested**

- I tested adding pets and tasks, completion, recurring tasks, sorting, filtering, schedule limits, due times, and conflict warnings.
- These tests help catch mistakes in the main behaviors.

**b. Confidence**

- I am fairly confident in the tested cases because all 10 tests pass.
- I would next test overlapping task durations and unusual time limits.

---

## 5. Reflection

**a. What went well**

- I am most satisfied that the scheduler works for more than one pet and explains tasks it could not schedule.

**b. What you would improve**

- I would improve conflict detection so it checks overlapping durations, not just exact start times.

**c. Key takeaway**

- Separate chat sessions for the diagram, implementation, tests, and UI helped me focus on one phase at a time.
- I learned that I need to guide and check the AI's work. I am still responsible for deciding what fits my design and testing that it works.
