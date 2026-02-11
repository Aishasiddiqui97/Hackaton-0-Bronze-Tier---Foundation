# 🔍 Skill: File Triage

## Purpose

Evaluate incoming task files from Inbox to determine their status, priority, and required action path.

## When to Apply This Skill

Execute this skill when:
- A new markdown file appears in Inbox
- You need to assess task completeness
- You must route a file to the correct destination

## Step-by-Step Procedure

### STEP 1: Read the Task File

1. Open the markdown file from Inbox
2. Read the entire content from top to bottom
3. Identify the following elements:
   - Title or heading (usually first line starting with #)
   - Task objective or goal statement
   - Requirements list (if present)
   - Action items or steps (if present)
   - Any completion markers or status indicators

### STEP 2: Extract Core Information

Determine the following:

**Task Objective:**
- What is the primary goal?
- What outcome is expected?
- Is the objective clearly stated or implied?

**Scope:**
- Is this a single action or multi-step task?
- Does it require file creation, modification, or analysis?
- Are there dependencies on other tasks or files?

**Completeness:**
- Is the task description sufficient to act on?
- Are there missing details or ambiguities?
- Does it contain placeholder text or incomplete sections?

### STEP 3: Summarize the Task

Create a concise summary containing:
- One sentence describing the objective
- Key requirements (2-4 bullet points maximum)
- Expected deliverable or outcome

Format:
```
Objective: [Single sentence]
Requirements:
- [Key requirement 1]
- [Key requirement 2]
Output: [What will be produced]
```

### STEP 4: Determine Task Status

Evaluate the file against these criteria:

**NEEDS ACTION if:**
- Task has clear objective and actionable steps
- File contains work to be performed
- Status is not marked as "Completed"
- No completion timestamp present
- Contains phrases like "TODO", "Action required", "Please", "Create", "Update"

**ALREADY DONE if:**
- File contains "Status: Completed" marker
- Timestamp indicating completion is present
- File is a report or summary of completed work
- Contains phrases like "Completed", "Finished", "Done"

**INVALID/UNCLEAR if:**
- File is empty or contains only whitespace
- Objective is missing or incomprehensible
- File contains only metadata without substance
- Task description is too vague to act upon

### STEP 5: Make Routing Decision

Based on status determination:

**If NEEDS ACTION:**
- Route to: Needs_Action folder
- Reason: Task requires processing
- Next step: Task will be picked up by task processor

**If ALREADY DONE:**
- Route to: Done folder
- Reason: Task is complete, archive for records
- Next step: Log the completion event

**If INVALID/UNCLEAR:**
- Route to: Inbox (keep in place)
- Reason: Requires clarification or is malformed
- Next step: Flag for human review or deletion

### STEP 6: Write Triage Output

Create a triage note (optional, for logging purposes):

```
# Triage Report

File: [filename]
Triaged: [timestamp]

Summary: [One sentence objective]

Status: [NEEDS_ACTION | ALREADY_DONE | INVALID]
Routing: [destination folder]
Reason: [Brief explanation]

Priority: [HIGH | MEDIUM | LOW]
Estimated Complexity: [SIMPLE | MODERATE | COMPLEX]
```

### STEP 7: Execute Routing

1. Move the file to the determined destination folder
2. Log the triage action in System_Log.md
3. If routed to Needs_Action, trigger task processor
4. If routed to Done, update completion statistics

## Decision Matrix

| Condition | Status | Destination |
|-----------|--------|-------------|
| Clear objective + No completion marker | NEEDS_ACTION | Needs_Action/ |
| Has "Status: Completed" | ALREADY_DONE | Done/ |
| Empty file or size = 0 bytes | INVALID | Inbox/ (flag) |
| Vague or missing objective | UNCLEAR | Inbox/ (flag) |
| Contains TODO or action verbs | NEEDS_ACTION | Needs_Action/ |

## Quality Checks

Before finalizing triage:

- [ ] File has been fully read
- [ ] Objective is clearly understood or marked as unclear
- [ ] Status determination follows decision matrix
- [ ] Routing destination is correct
- [ ] Triage action will be logged

## Common Patterns

**Action-Required Patterns:**
- "Create [something]"
- "Update [something]"
- "Generate [something]"
- "Analyze [something]"
- "Fix [something]"

**Already-Done Patterns:**
- "Status: Completed"
- "Timestamp: [date]"
- "Processed_By: [agent]"
- Past tense descriptions ("Created", "Updated", "Generated")

**Invalid Patterns:**
- Empty files
- Only metadata, no content
- Corrupted or unreadable text
- Non-markdown files with .md extension

## Bronze Tier Constraints

- No external API calls for triage
- No complex natural language processing
- Use simple keyword matching and pattern recognition
- Operate only on local file system
- No destructive operations during triage

## Error Handling

If triage fails:
1. Leave file in Inbox
2. Log error with details
3. Mark for manual review
4. Do not move or modify the file
5. Continue with next file in queue

## Success Criteria

Triage is successful when:
- File is correctly routed to appropriate folder
- Status determination is accurate
- Action is logged in System_Log.md
- No data loss or file corruption occurs
- Next processing step is triggered if needed
