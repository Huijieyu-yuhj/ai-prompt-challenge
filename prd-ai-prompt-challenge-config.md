# PRD: AI Prompt Challenge - Configurable Meeting Facilitator

## Clarifying Questions (Resolved)

> The following questions have been answered by the user:

| # | Question | Answer |
|---|----------|--------|
| 1 | What is the primary goal? | **A** - Enable facilitators to customize challenges without code changes |
| 2 | Who is the target user? | **D** - Event organizers who pre-configure sessions |
| 3 | What is the scope? | **A** - Full English interface for all UI text and content |
| 4 | What is the minimum number of challenge cards? | **A** - 5 cards (exactly one per group) |
| 5 | Group configuration | **A** - Fixed 5 groups named "Group 1" through "Group 5" |

### Additional Clarifications (Round 2)

| # | Question | Answer |
|---|----------|--------|
| 6 | Support more than 5 groups? | **Yes** - Configurable group count (default 5, but can be increased) |
| 7 | Timer completion sound alert? | **Yes** - Sound alert + popup animation when timer reaches zero |
| 8 | Re-assign for specific groups? | **Yes** - Support re-assignment for individual groups, but not in default view |
| 9 | Form-based config editor (non-JSON)? | **Yes** - Provide visual form editor alongside JSON editor |
| 10 | Copy all tasks button? | **Pending** - User asked for clarification (see notes below) |

### Additional Clarifications (Round 3)

| # | Question | Answer |
|---|----------|--------|
| 11 | Timer completion sound customizable? | **No** - Default sound is sufficient |
| 12 | Drag-and-drop cards between groups? | **Yes** - But must be enabled in config before assignment. Default: Disabled |
| 13 | Import config from URL? | **No** - Not needed |
| 14 | Preview mode before meeting? | **No** - Not needed |

---

## Introduction

The AI Prompt Challenge application is a card-based interactive tool used during the 2026 HR Annual Conference. It presents AI creative challenges to participant groups with a countdown timer. Currently, all card content, timer duration, and group settings are hardcoded in the HTML file, requiring code edits to make any changes.

This feature adds a **parameter configuration system** that allows meeting facilitators to dynamically manage challenge cards, assign tasks to groups in one click, and customize timer settings — all without modifying code.

---

## Goals

- **Primary Goal:** Enable event organizers to customize challenge cards and meeting settings without modifying code
- Allow pre-configuration of sessions before the meeting starts
- Enable one-click batch assignment of unique challenge cards to all configured groups (default 5 groups)
- Support configurable group count (default 5, expandable to more groups)
- Provide configurable countdown timer with manual start control, sound alert, and popup animation on completion
- Provide both JSON and form-based visual editors for configuration
- Support drag-and-drop card reassignment between groups (opt-in via config, disabled by default)
- Persist configuration across page refreshes using localStorage
- Ensure all UI text, system messages, and content are in English for international attendees

---

## User Stories

### US-001: Load External Configuration on Startup
**Description:** As a meeting facilitator, I want the app to automatically read an external `config.json` file on startup, so that I can adjust card content and settings without modifying code.

**Acceptance Criteria:**
- [ ] App attempts to fetch `./config.json` on startup
- [ ] On success, initializes card list, timer, and groups with config data
- [ ] On failure, falls back to built-in default config and shows a warning toast
- [ ] Config loading does not block initial page rendering
- [ ] Uses agent-browser in browser to verify fallback behavior

### US-002: Open and Edit Config Panel
**Description:** As a meeting facilitator, I want to click a Settings button at the bottom-right to open a config panel, so that I can visually modify timer duration, card data, and group info.

**Acceptance Criteria:**
- [ ] Settings button (⚙️) fixed at bottom-right corner (bottom: 20px, right: 20px)
- [ ] Click opens a modal overlay with semi-transparent dark background
- [ ] Panel contains: timer duration input (number field), groups JSON textarea, cards JSON textarea
- [ ] "Apply & Refresh" button re-renders UI immediately and saves to localStorage
- [ ] "Close" button dismisses the panel without saving
- [ ] Panel closes on ESC key press or clicking outside the modal
- [ ] All labels, placeholders, and error messages are in English
- [ ] Uses agent-browser in browser to verify modal open/close interactions

### US-003: Persist Configuration to localStorage
**Description:** As a meeting facilitator, I want my configuration changes to be automatically saved to browser local storage, so that settings are not lost after page refresh or browser close.

**Acceptance Criteria:**
- [ ] On startup, prioritizes reading config from localStorage key `ai_challenge_config`
- [ ] If localStorage is empty, attempts to fetch `./config.json`
- [ ] If both fail, uses built-in default config
- [ ] Every "Apply & Refresh" click updates localStorage
- [ ] Uses agent-browser in browser to verify persistence after page reload

### US-004: Batch Assign Unique Cards to All Groups (CORE)
**Description:** As a meeting facilitator, I want to click one button to randomly assign unique challenge cards to all configured groups, so that all groups receive their challenges simultaneously without manual selection.

**Acceptance Criteria:**
- [ ] Control area includes a prominent "Assign Challenges" button
- [ ] Clicking the button randomly selects unique cards from the card pool (one per group, no duplicates)
- [ ] Each group receives exactly one card
- [ ] Assignment results displayed as a card grid, each card labeled with its group name (Group 1, Group 2, etc.)
- [ ] Each card displays the group's assigned color as a visual border or header accent
- [ ] If card pool has fewer cards than groups, shows error toast: "Not enough cards. Please add at least [X] cards in config."
- [ ] All UI text related to assignment is in English
- [ ] Uses agent-browser in browser to verify assignment results layout

### US-005: Countdown Timer After Assignment (CORE)
**Description:** As a meeting facilitator, I want the countdown timer to start after cards are assigned, so that groups can begin their challenge immediately with a clear time limit.

**Acceptance Criteria:**
- [ ] After batch assignment, countdown timer is ready (manual start by default)
- [ ] Timer duration is configurable via config panel (default: 900 seconds / 15 minutes)
- [ ] Timer display shows `mm:ss` format in a large, prominent font at the top of the page
- [ ] When timer reaches 0, plays a sound alert and shows a popup animation (e.g., modal overlay with celebration effect)
- [ ] Timer supports Pause, Reset, and Restart controls
- [ ] Resetting timer restores to the configured default duration
- [ ] All timer-related text (labels, alerts) is in English
- [ ] Uses agent-browser in browser to verify timer countdown and completion alert

### US-006: Re-assign Card for Specific Group (Optional)
**Description:** As a meeting facilitator, I want to re-assign a new challenge card to a specific group, so that I can replace a card for just one group without re-assigning all groups.

**Acceptance Criteria:**
- [ ] Each assigned card has a "Re-assign" button/icon
- [ ] Clicking re-assign replaces only that group's card with a new random card from the pool
- [ ] The new card is different from the current card and other groups' current cards (if possible)
- [ ] If no unique cards remain, shows a warning message
- [ ] Timer is not affected by re-assignment
- [ ] Uses agent-browser in browser to verify re-assignment flow

### US-007: Drag-and-Drop Cards Between Groups (Optional)
**Description:** As a meeting facilitator, I want to drag and drop challenge cards between groups after assignment, so that I can manually adjust which group gets which challenge.

**Acceptance Criteria:**
- [ ] Drag-and-drop is disabled by default; must be enabled via config (`enableDragAndDrop: true`)
- [ ] When enabled, each assigned card can be dragged and dropped onto another group's card
- [ ] Dropping a card swaps the cards between the two groups
- [ ] Visual feedback during drag (e.g., card opacity change, drop target highlight)
- [ ] Timer is not affected by drag-and-drop
- [ ] Config panel includes a toggle: "Enable drag-and-drop card swapping" (default: Off)
- [ ] Uses agent-browser in browser to verify drag-and-drop interactions

### US-008: Form-Based Configuration Editor
**Description:** As a meeting facilitator who may not be familiar with JSON, I want a visual form-based editor to configure groups, cards, and timer settings, so that I can easily customize the application without writing JSON.

**Acceptance Criteria:**
- [ ] Config panel has two tabs: "Form Editor" (default) and "JSON Editor"
- [ ] Form Editor includes:
  - Timer duration input (number field with +/- buttons)
  - Groups section: Add/Remove/Edit group name and color picker
  - Cards section: Add/Remove/Edit card with fields for type, task, and platforms
- [ ] Changes in Form Editor are reflected in JSON Editor and vice versa (two-way sync)
- [ ] Form validation shows inline error messages (e.g., "Task cannot be empty")
- [ ] "Apply & Refresh" button saves and applies changes from either editor
- [ ] Uses agent-browser in browser to verify form interactions and validation

### US-009: Export and Import Configuration (Optional)
**Description:** As a meeting facilitator, I want to export current config as a JSON file or import from a file, so that I can share config across devices or create backups.

**Acceptance Criteria:**
- [ ] Config panel provides "Export Config" button that downloads current config as `config.json`
- [ ] Provides "Import Config" button that opens a file picker for JSON files
- [ ] Validates JSON format on import; shows friendly error message if invalid
- [ ] Auto-applies and saves to localStorage on successful import
- [ ] Uses agent-browser in browser to verify file download and upload flow

### US-010: Reset to Default Configuration (Optional)
**Description:** As a meeting facilitator, I want to one-click restore the built-in default config, so that I can quickly return to the initial state if my configuration becomes messy.

**Acceptance Criteria:**
- [ ] Config panel provides "Reset to Default" button
- [ ] Click shows a confirmation dialog: "Reset all settings to default? This cannot be undone."
- [ ] On confirmation, clears localStorage and restores default config
- [ ] UI immediately refreshes to show default content
- [ ] Uses agent-browser in browser to verify reset flow

---

## Functional Requirements

- **FR-1:** The system must load configuration from `config.json` on startup, with localStorage as the priority source and built-in defaults as fallback.
- **FR-2:** The system must provide a Settings button (⚙️) at the bottom-right corner that opens a modal config panel.
- **FR-3:** The config panel must contain two tabs: "Form Editor" (visual form) and "JSON Editor" (raw JSON).
- **FR-4:** Form Editor must include: timer duration input, groups management (add/remove/edit with color picker), and cards management (add/remove/edit with type, task, platforms fields).
- **FR-5:** Changes in Form Editor and JSON Editor must be synchronized in real-time (two-way binding).
- **FR-6:** When the user clicks "Apply & Refresh," the system must validate the config, save to localStorage, and re-render the UI.
- **FR-7:** The system must provide an "Assign Challenges" button that randomly selects unique cards and assigns one to each configured group.
- **FR-8:** The system must display assignment results in a responsive grid, with each card showing the group name, card type, task description, recommended platforms, and a color accent matching the group's configured color.
- **FR-9:** Each assigned card must have a "Re-assign" button to replace only that group's card with a new random card.
- **FR-10:** The system must support drag-and-drop card swapping between groups when `enableDragAndDrop` config is set to `true` (default: `false`).
- **FR-11:** The system must start a countdown timer after assignment (manual start by default), with configurable duration.
- **FR-12:** When the timer reaches zero, the system must play a sound alert and display a popup animation (modal overlay with visual effect).
- **FR-13:** The timer must display in `mm:ss` format, support Pause, Reset, and Restart actions.
- **FR-14:** The system must validate that the card pool contains at least as many cards as there are groups before allowing batch assignment.
- **FR-15:** All UI text, system messages, button labels, error messages, and card content must be in English.
- **FR-16:** The system must provide Export and Import buttons in the config panel for saving and loading JSON configuration files.
- **FR-17:** The system must provide a "Reset to Default" button with a confirmation dialog that clears localStorage and restores built-in defaults.

---

## Non-Goals

- No backend server or database integration
- No user authentication or login system
- No real-time collaborative editing of configuration
- No AI-powered automatic generation of challenge cards
- No scoring, ranking, or leaderboard functionality
- No multi-language support (English only for this version)
- No support for assigning more than one card per group in a single round
- Copy all tasks button is NOT included in this version (can be added later if needed)

---

## Design Considerations

### UI/UX Requirements

- **Visual Style:** Maintain the existing gradient background, glassmorphism cards, and rounded corners from the original design.
- **Color Coding:** Each group has a unique color for visual distinction in the assignment results grid (default 5 groups, expandable).
- **Responsive Layout:** On mobile screens (< 700px), the assignment results grid stacks vertically (1 card per row), and the config panel width adjusts to 95%.
- **Config Panel Tabs:** Two tabs - "Form Editor" (default, visual form) and "JSON Editor" (raw JSON view).
- **Timer Completion:** Sound alert + popup animation (modal overlay with celebration effect) when timer reaches zero.

### Mockup: Assignment Results Layout

```
┌─────────────────────────────────────────────────────────────────┐
│                    Challenge Assignment Results                 │
├──────────────┬──────────────┬──────────────┬──────────────┬──────┤
│  Group 1     │  Group 2     │  Group 3     │  Group 4     │ Grp 5│
│  [Music]     │  [Image]     │  [Music]     │  [Image]     │ [Img]│
│  Generate... │  Rewrite...  │  HR team...  │  Depict...   │ Van..│
│  Gemini,Suno │ Gemini,Suno  │ Doubao,...   │ Doubao,...   │ Dou..│
└──────────────┴──────────────┴──────────────┴──────────────┴──────┘
│                                                                     │
│  ⏱️ 15:00    [▶ Start]  [⏸ Pause]  [🔄 Reset]                      │
│                                                                     │
│  [🔄 Re-assign]  [⚙️ Settings]                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### Mockup: Config Panel Layout

```
┌─────────────────────────────────────────────────────────────┐
│  ⚙️ Settings                                          [×]   │
├─────────────────────────────────────────────────────────────┤
│  [Form Editor]  [JSON Editor]                               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ⏱️ Timer Duration: [  900  ] seconds  [-] [+]             │
│                                                             │
│  👥 Groups                                    [+ Add Group] │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ [Group 1    ]  Color: [#FF8C42]  [🗑️]               │   │
│  │ [Group 2    ]  Color: [#2E86AB]  [🗑️]               │   │
│  │ [Group 3    ]  Color: [#A23B72]  [🗑️]               │   │
│  │ [Group 4    ]  Color: [#F18F01]  [🗑️]               │   │
│  │ [Group 5    ]  Color: [#27AE60]  [🗑️]               │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  🃏 Challenge Cards                          [+ Add Card]   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Card #1                                              │   │
│  │ Type:    [Music           ▼]                         │   │
│  │ Task:    [Generate an opening music...]              │   │
│  │ Platforms: [Gemini, Suno/Udio       ]                │   │
│  │                                              [🗑️]    │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │ Card #2                                              │   │
│  │ ...                                                  │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  [Apply & Refresh]  [Export]  [Import]  [Reset to Default] │
│  [Close]                                                    │
└─────────────────────────────────────────────────────────────┘
```

---

## Technical Considerations

### Constraints and Dependencies

- **Pure Frontend:** No backend required. Runs entirely in the browser using HTML5, CSS3, and vanilla JavaScript (ES6+).
- **No External Libraries:** Does not depend on any third-party frameworks or libraries.
- **CORS Limitation:** Fetching `config.json` via the `file://` protocol may be blocked by CORS. Solution: run via a local server (e.g., `npx http-server`) or embed default config as a fallback.

### Integration Points

- Reuses the existing card grid, timer, and navigation logic from the original HTML application.
- localStorage key: `ai_challenge_config`

### Performance Requirements

- Config loading time: < 500ms
- UI re-render time after config change: < 200ms
- localStorage read/write: synchronous, no noticeable delay

### Security Considerations

- JSON parsing must use `try-catch` to prevent crashes from malformed input.
- Must not use `eval()` on user-provided JSON content.
- localStorage data is non-sensitive; no encryption required.

---

## Success Metrics

- Facilitators can assign challenges to all 5 groups in 1 click (target: < 2 seconds)
- Configuration persists across page refreshes with 100% reliability
- Timer completion alert is visible and clear in 100% of test cases
- Page load time remains under 1 second after adding config functionality
- Zero console errors during normal usage flow

---

## Open Questions

> All open questions have been resolved. No further clarifications needed.

---

## Appendix: Default Configuration

```json
{
  "version": "2.0",
  "title": "AI Prompt Challenge",
  "subtitle": "Creative Workshop · Facilitator Assistant",
  "timerDefaultSeconds": 900,
  "autoStartTimer": false,
  "groups": [
    { "name": "Group 1", "color": "#FF8C42" },
    { "name": "Group 2", "color": "#2E86AB" },
    { "name": "Group 3", "color": "#A23B72" },
    { "name": "Group 4", "color": "#F18F01" },
    { "name": "Group 5", "color": "#27AE60" }
  ],
  "cards": [
    { "id": 1, "type": "Music", "task": "Generate an opening music for today's meeting in your favorite movie style", "platforms": "Gemini, Suno/Udio" },
    { "id": 2, "type": "Music", "task": "Rewrite 'Two Tigers' with lyrics covering real workplace pain points", "platforms": "Gemini, Suno/Udio" },
    { "id": 3, "type": "Image", "task": "HR team building — everyone riding lobsters racing through the city", "platforms": "Doubao, Jimeng, Minimax, Gemini" },
    { "id": 4, "type": "Image", "task": "Depict an office scene 10 years from now with humans and AI/robots working together", "platforms": "Doubao, Jimeng, Minimax, Gemini" },
    { "id": 5, "type": "Image", "task": "In Van Gogh's 'Starry Night', every star is a glowing Excel chart", "platforms": "Doubao, Jimeng, Minimax, Gemini" }
  ]
}
```
