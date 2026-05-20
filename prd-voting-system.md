# PRD: AI Prompt Challenge - Awards Voting System

## Clarifying Questions

> The following questions have been answered by the user:

| # | Question                   | Answer                                                                        |
| - | -------------------------- | ----------------------------------------------------------------------------- |
| 1 | What awards are available? | **Two awards**: Best Creative (1 award) and Prompt Master (1 award)           |
| 2 | How does voting work?      | Each person scans QR code to access voting page, votes once per session       |
| 3 | How many votes per award?  | Each person casts **2 votes per award** (cannot vote for the same item twice) |
| 4 | Backend service?           | **Bmob backend cloud** will be used for data storage and voting management    |
| 5 | Deployment target?         | Cloud deployment via Bmob hosting                                             |

***

## Introduction

The AI Prompt Challenge application currently supports challenge card assignment and timer functionality for group activities. This feature adds an **awards voting system** that enables participants to vote for their favorite submissions after the challenge session.

Participants scan a QR code to access a mobile-friendly voting page, where they can cast votes for two awards: **Best Creative** and **Prompt Master**. Each participant votes once, selecting 2 unique items per award. Results are stored in Bmob cloud and displayed in real-time.

***

## Goals

- **Primary Goal:** Enable fair and engaging voting for challenge awards
- Provide a seamless mobile voting experience via QR code access
- Support two awards: Best Creative and Prompt Master
- Each voter casts exactly 2 votes per award (no duplicates allowed)
- Prevent duplicate voting from the same user/session
- Store and manage voting data using Bmob backend cloud
- Display real-time voting results for facilitators
- Deploy the entire application on Bmob cloud hosting

***

## User Stories

### US-001: Access Voting Page via QR Code

**Description:** As a participant, I want to scan a QR code to access the voting page on my phone, so that I can easily participate without typing URLs.

**Acceptance Criteria:**

- [ ] System generates a QR code linking to the voting page URL
- [ ] QR code can be displayed on screen or printed
- [ ] Voting page is mobile-responsive and loads quickly
- [ ] Voting page displays both awards: Best Creative and Prompt Master
- [ ] All UI text is in English

### US-002: Cast Votes for Best Creative Award

**Description:** As a participant, I want to select 2 different submissions for the Best Creative award, so that I can vote for my favorite creative works.

**Acceptance Criteria:**

- [ ] Voting page displays all submitted challenge cards for selection
- [ ] User can select exactly 2 items for Best Creative award
- [ ] Selected items are visually highlighted (e.g., checkmark, color change)
- [ ] User cannot select the same item twice for the same award
- [ ] User cannot submit until exactly 2 items are selected
- [ ] Selection count is displayed (e.g., "Selected: 1/2")

### US-003: Cast Votes for Prompt Master Award

**Description:** As a participant, I want to select 2 different submissions for the Prompt Master award, so that I can vote for the best prompt engineering.

**Acceptance Criteria:**

- [ ] Voting page displays all submitted challenge cards for selection
- [ ] User can select exactly 2 items for Prompt Master award
- [ ] Selected items are visually highlighted
- [ ] User cannot select the same item twice for the same award
- [ ] User cannot submit until exactly 2 items are selected
- [ ] Selection count is displayed (e.g., "Selected: 1/2")

### US-004: Submit Votes

**Description:** As a participant, I want to submit my votes after selecting items for both awards, so that my votes are recorded.

**Acceptance Criteria:**

- [ ] Submit button is disabled until user has selected 2 items for each award
- [ ] Clicking Submit sends votes to Bmob backend
- [ ] On success, shows confirmation message: "Thank you! Your votes have been recorded."
- [ ] On failure, shows error message with retry option
- [ ] After successful submission, user cannot vote again (session locked)
- [ ] Vote submission records: voter session ID, selected items per award, timestamp

### US-005: Prevent Duplicate Voting

**Description:** As a system, I want to ensure each participant can only vote once, so that the voting results are fair.

**Acceptance Criteria:**

- [ ] System generates a unique session ID for each voter (stored in localStorage + cookie)
- [ ] Before allowing vote submission, checks if session ID has already voted
- [ ] If already voted, shows message: "You have already voted. Thank you for participating!"
- [ ] Bmob backend validates duplicate votes server-side
- [ ] Session ID is tied to device/browser (basic anti-duplicate measure)

### US-006: View Voting Results (Facilitator)

**Description:** As a facilitator, I want to view real-time voting results, so that I can announce the winners.

**Acceptance Criteria:**

- [ ] Facilitator can access a results dashboard via a separate URL or button
- [ ] Dashboard displays vote counts for each submission per award
- [ ] Results are sorted by vote count (descending)
- [ ] Top 3 items are highlighted for each award
- [ ] Results auto-refresh every 10 seconds
- [ ] Dashboard shows total number of voters
- [ ] Dashboard is accessible on desktop and mobile

### US-007: Admin Panel for Voting Management

**Description:** As a facilitator, I want to manage the voting session, so that I can control when voting starts and ends.

**Acceptance Criteria:**

- [ ] Admin panel accessible via password or facilitator login
- [ ] Admin can start/stop voting session
- [ ] When voting is stopped, participants see message: "Voting has ended. Thank you!"
- [ ] Admin can view and export voting results as CSV
- [ ] Admin can reset voting session (clears all votes)
- [ ] Admin panel shows real-time voter count

***

## Functional Requirements

- **FR-1:** The system must generate a unique QR code linking to the voting page URL.
- **FR-2:** The voting page must display all submitted challenge cards for both awards.
- **FR-3:** Users must select exactly 2 unique items per award before submitting.
- **FR-4:** The system must prevent users from selecting the same item twice for the same award.
- **FR-5:** The system must generate and store a unique session ID for each voter (localStorage + cookie).
- **FR-6:** The system must validate duplicate votes both client-side and server-side (Bmob).
- **FR-7:** Vote data must be stored in Bmob cloud with fields: voter\_session\_id, best\_creative\_votes (array), prompt\_master\_votes (array), timestamp.
- **FR-8:** The system must display a confirmation message after successful vote submission.
- **FR-9:** The system must lock voting after submission (user cannot vote again).
- **FR-10:** The results dashboard must display vote counts sorted by descending order.
- **FR-11:** The results dashboard must auto-refresh every 10 seconds.
- **FR-12:** The admin panel must allow facilitators to start/stop/reset voting sessions.
- **FR-13:** The system must display voting status (active/ended) to participants.
- **FR-14:** All UI text, messages, and labels must be in English.
- **FR-15:** The voting page must be mobile-responsive (optimized for screens >= 320px).
- **FR-16:** The system must integrate with Bmob SDK for data storage and retrieval.

***

## Non-Goals

- No user registration or account system required
- No social sharing features
- No comment or feedback functionality
- No photo upload capability (uses existing challenge card data)
- No multi-language support (English only)
- No advanced anti-fraud measures beyond session-based duplicate prevention
- No real-time WebSocket updates (polling-based refresh is sufficient)

***

## Design Considerations

### UI/UX Requirements

- **Visual Style:** Consistent with existing AI Prompt Challenge design (gradient background, glassmorphism cards).
- **Mobile-First:** Voting page optimized for mobile screens (primary access via QR code on phone).
- **Card Layout:** Each challenge card displays: group name, card type, task description, and a selectable checkbox/button.
- **Selection Feedback:** Selected cards show visual highlight (e.g., border color change, checkmark icon).
- **Progress Indicator:** Shows selection progress for each award (e.g., "Best Creative: 1/2 selected").

### Voting Page Mockup

```
┌─────────────────────────────────────────┐
│         🏆 AI Prompt Challenge          │
│              Vote for Winners           │
├─────────────────────────────────────────┤
│                                         │
│  🎨 Best Creative Award                 │
│  Select 2 submissions                   │
│  Selected: 1/2                          │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │ ☑ Group 1 - Music               │   │
│  │   Generate opening music...     │   │
│  └─────────────────────────────────┘   │
│  ┌─────────────────────────────────┐   │
│  │ ☐ Group 2 - Music               │   │
│  │   Rewrite Two Tigers...         │   │
│  └─────────────────────────────────┘   │
│  ┌─────────────────────────────────┐   │
│  │ ☐ Group 3 - Image               │   │
│  │   HR team building...           │   │
│  └─────────────────────────────────┘   │
│  ...                                    │
│                                         │
├─────────────────────────────────────────┤
│                                         │
│  ⭐ Prompt Master Award                 │
│  Select 2 submissions                   │
│  Selected: 0/2                          │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │ ☐ Group 1 - Music               │   │
│  │   Generate opening music...     │   │
│  └─────────────────────────────────┘   │
│  ...                                    │
│                                         │
├─────────────────────────────────────────┤
│                                         │
│         [ Submit Votes ]                │
│   (Disabled until 2/2 for each award)   │
│                                         │
└─────────────────────────────────────────┘
```

### Results Dashboard Mockup

```
┌─────────────────────────────────────────────────────────────┐
│              🏆 Voting Results Dashboard                     │
│              Last updated: 10 seconds ago                    │
│              Total Voters: 47                                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  🎨 Best Creative Award                                     │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  🥇 Group 3 - Image              ████████████  32    │  │
│  │  🥈 Group 1 - Music              ██████████    28    │  │
│  │  🥉 Group 4 - Image              ████████      22    │  │
│  │     Group 2 - Music              ██████        18    │  │
│  │     Group 5 - Image              ████          12    │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  ⭐ Prompt Master Award                                     │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  🥇 Group 1 - Music              ████████████  30    │  │
│  │  🥈 Group 4 - Image              ██████████    26    │  │
│  │  🥉 Group 3 - Image              ████████      24    │  │
│  │     Group 2 - Music              ██████        20    │  │
│  │     Group 5 - Image              ████          15    │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  [ Refresh ]  [ Export CSV ]  [ Admin Panel ]               │
└─────────────────────────────────────────────────────────────┘
```

***

## Technical Considerations

### Bmob Backend Integration

#### Data Schema

**Table:** **`Vote`**

| Field               | Type   | Description                 |
| ------------------- | ------ | --------------------------- |
| `objectId`          | String | Auto-generated by Bmob      |
| `voterSessionId`    | String | Unique session ID for voter |
| `bestCreativeVotes` | Array  | Array of 2 card/group IDs   |
| `promptMasterVotes` | Array  | Array of 2 card/group IDs   |
| `createdAt`         | Date   | Vote submission timestamp   |

**Table:** **`VotingSession`**

| Field       | Type    | Description                        |
| ----------- | ------- | ---------------------------------- |
| `objectId`  | String  | Auto-generated by Bmob             |
| `isActive`  | Boolean | Whether voting is currently active |
| `createdAt` | Date    | Session creation timestamp         |
| `updatedAt` | Date    | Last update timestamp              |

#### Bmob SDK Setup

```javascript
// Initialize Bmob SDK
Bmob.initialize("YOUR_APP_ID", "YOUR_REST_API_KEY");

// Submit vote
const Vote = Bmob.Object.extend("Vote");
const vote = new Vote();
vote.set("voterSessionId", sessionId);
vote.set("bestCreativeVotes", bestCreativeSelections);
vote.set("promptMasterVotes", promptMasterSelections);
vote.save();

// Query results
const query = new Bmob.Query("Vote");
query.find().then(results => {
  // Aggregate vote counts
});
```

### Constraints and Dependencies

- **Bmob Backend:** Requires Bmob app setup with appropriate tables and permissions.
- **QR Code Generation:** Use a lightweight JS library (e.g., `qrcode.js`) or Bmob's built-in QR code feature.
- **Pure Frontend:** Voting page runs in browser using HTML5, CSS3, and vanilla JavaScript + Bmob SDK.
- **No Server-Side Code:** All logic runs client-side; Bmob handles data storage and queries.

### Integration Points

- Reuses existing challenge card data from the main application.
- localStorage key for session: `voter_session_id`
- Bmob tables: `Vote`, `VotingSession`

### Performance Requirements

- Voting page load time: < 2 seconds on mobile networks
- Vote submission response time: < 1 second
- Results dashboard refresh: every 10 seconds (polling)
- Bmob query response time: < 500ms

### Security Considerations

- **Bmob ACL:** Set table permissions to allow public read/write for votes, but restrict delete/update to admin.
- **Session Validation:** Validate session ID format before accepting votes.
- **Rate Limiting:** Bmob's built-in rate limiting helps prevent abuse.
- **Data Validation:** Ensure vote arrays contain exactly 2 unique IDs before saving.
- **HTTPS Required:** Bmob requires HTTPS for all API calls.

***

## Deployment Plan

### Bmob Cloud Setup

1. **Create Bmob App:**
   - Register/login to Bmob (<https://www.bmob.cn>)
   - Create a new application
   - Note down `App ID` and `REST API Key`
2. **Create Data Tables:**
   - Create `Vote` table with fields: `voterSessionId`, `bestCreativeVotes`, `promptMasterVotes`
   - Create `VotingSession` table with fields: `isActive`
   - Set ACL permissions appropriately
3. **Deploy Frontend:**
   - Upload HTML/CSS/JS files to Bmob hosting
   - Configure custom domain (optional)
   - Ensure HTTPS is enabled
4. **Generate QR Code:**
   - Use the deployed voting page URL to generate QR code
   - Display QR code on screen or print for participants
5. **Testing:**
   - Test voting flow on multiple devices
   - Verify duplicate vote prevention
   - Test results dashboard and auto-refresh

***

## Success Metrics

- Participants can complete voting in < 2 minutes
- Zero duplicate votes recorded
- Voting page loads in < 2 seconds on mobile
- Results dashboard updates within 10 seconds of vote submission
- 90%+ of participants successfully cast votes without errors
- Facilitators can announce winners within 1 minute of voting close

***

## Bmob Configuration

> The following configuration values are required to integrate with Bmob backend:

| Config Key | Description | Required | Example |
|------------|-------------|----------|---------|
| `BMOB_APP_ID` | Bmob application unique identifier | Yes | `a1b2c3d4e5f6...` |
| `BMOB_REST_API_KEY` | REST API access key | Yes | `f6e5d4c3b2a1...` |
| `BMOB_SECRET_KEY` | Secret key for cloud functions (optional) | No | `xxxxxx...` |
| `VOTING_PAGE_URL` | Deployed voting page full URL (for QR code) | Yes | `https://xxx.bmobapp.com/vote.html` |
| `ADMIN_PASSWORD` | Password for admin panel access | Yes | `your_secure_password` |
| `VOTING_TIME_LIMIT_SECONDS` | Voting session time limit in seconds | Yes | `120` |

### Where to Find Bmob Keys

1. Login to [Bmob Console](https://www.bmob.cn)
2. Select your application
3. Go to **设置** (Settings) → **应用密钥** (Application Keys)
4. Copy `Application ID` and `REST API Key`

---

## Open Questions

| # | Question | Answer |
| - | -------- | ------ |
| 1 | Should voters be able to change their votes after submission? | No (locked after submit) |
| 2 | Should there be a time limit for voting? | Yes, 2 minutes (configurable) |
| 3 | Should results be public or admin-only? | Public dashboard, admin controls session |
| 4 | How to handle tie-breaking for awards? | Both tied winners receive the award |
| 5 | Should we collect voter name/email for verification? | No (anonymous session-based voting) |

***

## Appendix: Bmob Setup Checklist

- [ ] Register Bmob account and create app
- [ ] Obtain App ID and REST API Key
- [ ] Create `Vote` table with required fields
- [ ] Create `VotingSession` table with required fields
- [ ] Configure ACL permissions for tables
- [ ] Upload frontend files to Bmob hosting
- [ ] Test Bmob SDK integration (save/query operations)
- [ ] Generate QR code for voting page URL
- [ ] Test voting flow end-to-end on mobile device
- [ ] Test results dashboard and auto-refresh
- [ ] Test admin panel (start/stop/reset voting)
- [ ] Deploy to production URL
- [ ] Print/display QR code for event

