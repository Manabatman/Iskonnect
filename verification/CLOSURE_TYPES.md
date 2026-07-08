# Closure Types

When verification changes program status, use a **closure type** — not "archived" alone.

| Closure type | Meaning | Recommended ISKONNECT action |
|--------------|---------|------------------------------|
| `permanently_discontinued` | Program no longer offered | `is_active=false`, `data_status` as appropriate |
| `closed_for_this_cycle` | Recurring program between application windows | `application_status=previous_cycle` or expected reopen; **keep active** |
| `temporarily_unavailable` | Page down, portal maintenance, or unclear reopen | `application_status=needs_verification` or `flag_review`; **do not archive** |
| `unknown` | Cannot determine status from official sources | `flag_review`; **do not archive** |

## Rules

1. **Never archive recurring programs** that are merely closed for the season.
2. Use `permanently_discontinued` only with official evidence (announcement, program removal, successor notice).
3. When in doubt, prefer `closed_for_this_cycle` or `temporarily_unavailable` over archiving.
4. Record closure type in `field_changes.csv` whenever changing `is_active`, `application_status`, or `data_status`.

## Examples

| Situation | Closure type |
|-----------|--------------|
| DOST Merit — applications closed until next SY announcement | `closed_for_this_cycle` |
| DepEd voucher program officially terminated | `permanently_discontinued` |
| LGU portal under maintenance, no deadline posted | `temporarily_unavailable` |
| Foundation page removed, no successor found | `permanently_discontinued` (with evidence) |
| Cannot find current cycle info on official site | `unknown` |
