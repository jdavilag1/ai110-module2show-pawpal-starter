# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Using the four classes, owner pet, and task, I asked AI to create a mermaid diagram.


**b. Design changes**

My design changed during planning when i made the intial UML better. i added explicit lists so an owner cna have multiplepets and each pet have their own designated care tasks. i also used dataclasses like owner, pet, and task objects. i still need to make sure the scheduler treats the owner's avaialble time as a shared daily limit when planning for multiple pets

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

The conflict check only reports tasks with the exact same scheduled start time; it does not check whether tasks with different start times overlap because of their durations. This keeps conflict detection lightweight and easy to understand, and the daily scheduler already places selected tasks sequentially. A future version could detect interval overlaps if schedules allow fixed or parallel appointments.

The check groups scheduled tasks by start time in one pass, which is easier to follow than comparing every pair and runs in O(n) time. Sorting the small set of conflicting times for predictable warning order adds O(k log k), where k is the number of distinct scheduled times.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
