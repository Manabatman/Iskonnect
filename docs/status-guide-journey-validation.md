# Student Journey Validation Matrix

Post-implementation status. **Pass** = behavior matches agreed product policy after `application_status` rollout.

| # | Scenario | Step | Expected | Status | Notes |
|---|----------|------|----------|--------|-------|
| 1 | Grade 11, DOST, future fit | Search | Results visible with lifecycle badge | Pass | Search shows cards; match/eligibility on “Check my match” |
| 1 | | Card | “Future eligibility” + gap_reason when matched | Partial | `gap_reason`/`next_action` shown on match cards |
| 1 | | Bookmark | Saves successfully | Pass | Unchanged |
| 1 | | Notify on reopen | Notification when cycle opens | Fail | Not implemented (stretch) |
| 2 | Deadline passed yesterday | Card label | Single “Closed” / “Past cycle” / “Expected to reopen” | Pass | `LifecycleStatusBadge` replaces Expired/Deadline passed stack |
| 2 | | Searchable | Still in default search | Pass | `is_active` no longer cleared on expiry |
| 2 | | Reopen hint | Shown when `expected_reopen` | Pass | Card shows predicted month + uncertainty copy |
| 3 | Needs verification | Default search | Visible with warning | Pass | Removed `needs_review` from default exclusion |
| 3 | | Not mistaken verified | No “Verified data” when needs_verification | Pass | Card suppresses verified badge |
| 4 | Open + eligible | Apply CTA | Works when `application_status=open` | Pass | |
| 5 | Opening soon | Label | “Opening soon” urgency on open status | Pass | Deadline urgency chip when status open |
| 6 | Prepare ahead | gap_reason | Explains missing requirement | Pass | When API sends `gap_reason` |
| 7 | Bookmarked → closed | Dashboard | Lifecycle badge on saved row | Pass | `LifecycleStatusBadge` on saved list |
| 8 | Archived program | Label | “No longer offered” | Pass | Admin deactivate → `archived` |
| 8 | | Search | Hidden unless `include_archived` | Pass | |
| 9 | Broken link | Warning | “Link issue” separate from lifecycle | Pass | |
| 10 | Guest browse | Status guide | Link from Navbar + search page | Pass | |

## Residual gaps (documented)

- Cycle-open notifications for bookmarked scholarships (Scenario 1 stretch)
- Eligibility states on search cards without running match (by design — “Check my match” required)
