## 0. Clean (Base)
**Family name:** `clean`

- Original, unmodified GSM8K question
- Used as the baseline for accuracy and Performance Drop Rate (PDR)

---

## 1. Irrelevant Numeric Distractor
**Family name:** `irrelevant_numeric_distractor`

### Intent
Test whether models can ignore **numerically salient but semantically irrelevant information**.

### Description
Additional sentences containing unrelated numerical facts are appended to the problem statement.
These numbers are not involved in the required computation and should be ignored by a robust model.

### Constraints
- Exactly **2 distractor numbers** per example
- Distractors are appended at the **end** of the question
- Distractor numbers must **not overlap** with any numbers in the base problem
- Distractors must not plausibly relate to the task (e.g., no quantities of the same object type)

### Allowed Changes
- Add 1–2 sentences containing unrelated numeric facts
- Add contextually neutral phrases (e.g., “For reference,” “Unrelatedly,”)

### Forbidden Changes
- Adding numbers that could reasonably be mistaken as inputs
- Introducing new constraints or modifying the scenario

### Example
**Base:**  
> Alice buys 3 bags of apples with 5 apples in each bag. How many apples does she have?

**Variant:**  
> Alice buys 3 bags of apples with 5 apples in each bag. How many apples does she have?  
> For reference, the store has 18 shelves and 47 shopping carts.

**Gold answer:** unchanged

---

## 2. Symbolic or Operand Swap
**Family name:** `symbolic_or_operand_swap`

### Intent
Test invariance to **superficial symbolic changes** and reordering that should not affect reasoning.

### Description
Entities, variable names, or sentence order are modified while preserving the exact mathematical
relationships.

### Constraints
- At most **one swap operation** per example
- No algebraic structure changes
- No introduction of new entities

### Allowed Changes
- Renaming people or objects (e.g., Alice ↔ Bob)
- Reordering clauses or sentences
- Swapping variable labels when meaning is preserved

### Forbidden Changes
- Changing quantities or operations
- Introducing new dependencies between variables

### Example
**Base:**  
> Tom has 4 boxes with 6 pencils each.

**Variant:**  
> Bob has 4 containers, each holding 6 pencils.

**Gold answer:** unchanged

---

## 3. Scale or Unit Change
**Family name:** `scale_or_unit_change`

### Intent
Test robustness to **unit conversions and rescaling**, a common source of arithmetic errors.

### Description
One quantity is re-expressed using an equivalent unit or scale (e.g., minutes ↔ hours,
cents ↔ dollars), while preserving the underlying computation.

### Constraints
- At most **one unit conversion** per example
- Conversion must be exact and explicit
- Final numeric answer must remain **numerically equal**

### Allowed Conversions
- minutes ↔ hours
- hours ↔ minutes
- cents ↔ dollars
- dollars ↔ cents

### Forbidden Changes
- Multiple conversions in one problem
- Implicit or ambiguous conversions
- Changing the structure of the task

### Example
**Base:**  
> A movie lasts 2 hours. How many minutes is that?

**Variant:**  
> A movie lasts 120 minutes. How many minutes is that?

**Gold answer:** unchanged

---

## 4. Semantic Rephrasing
**Family name:** `semantic_rephrasing`

### Intent
Test sensitivity to **surface-level linguistic variation** without changing logical content.

### Description
The problem is paraphrased using alternative phrasing or sentence structure while keeping all
constraints and quantities identical.

### Constraints
- Deterministic paraphrases from a fixed template bank
- At most **2 sentence-level edits**
- No new information introduced

### Allowed Changes
- Paraphrasing questions (“How many” → “What is the total number”)
- Reordering descriptive clauses
- Synonym substitution

### Forbidden Changes
- Adding or removing constraints
- Changing numerical values or relationships

### Example
**Base:**  
> How many total candies does Sarah have?

**Variant:**  
> What is the total number of candies that Sarah ends up with?

**Gold answer:** unchanged

---

## 5. Implicit Reasoning Required
**Family name:** `implicit_reasoning_required`

### Intent
Test whether models can handle **simple implicit constraints** that require an extra inference step,
without introducing ambiguity.

### Description
A single additional constraint is added that requires the model to reason implicitly
(e.g., whole units only, leftovers discarded), while maintaining a unique correct answer.

### Constraints
- Exactly **one implicit inference hook**
- Must preserve **single-gold-answer**
- No missing information

### Allowed Inference Types
- Whole units only (no fractions)
- Leftovers discarded
- Simple capacity or feasibility constraints

### Forbidden Changes
- Ambiguous or underspecified scenarios
- Multiple interacting implicit constraints

### Example
**Base:**  
> A ribbon is 25 meters long. Each decoration needs 4 meters. How many decorations can be made?

**Variant:**  
> A ribbon is 25 meters long. Each decoration needs 4 meters, and partial decorations are not allowed. How many decorations can be made?

**Gold answer:** unchanged

---


