# Article Reader Rules

## 1. Requirement

Do not generate the final daily digest from titles alone.

Before final digest generation, run a real Article Reader Agent for every candidate item. The reader must be:

- A Codex sub-agent explicitly assigned as `Article Reader Agent`.
- A future LLM summarizer that writes the same fields.

Local extractive scripts are allowed only for development diagnostics. They are not valid official daily digest reader output.

## 2. Required Reader Fields

Every digest candidate must include:

- `reader_status`: `read | partial | blocked`
- `reader_agent`
- `reader_ran_at`
- `article_summary`
- `why_it_matters`
- `action_hint`
- `key_points`
- `evidence_quotes`
- `reading_quality`: `high | medium | low`
- `content_chars`
- `content_hash`
- `summary_source`
- `summary_language`

## 3. Digest Eligibility

Final digest may include only items with:

- `reader_status = read`
- `reader_agent = Article Reader Agent`
- `reading_quality` in `high | medium`
- non-empty `article_summary`
- non-empty `why_it_matters`
- non-empty `action_hint`
- source link
- source time or fetched time

If an item cannot be read, do not silently use the title as the final summary. Either exclude it or keep it in readings/rejected/follow-up data for review.

## 4. Summary Standard

The article summary should answer:

- What is this article mainly about?
- What changed, launched, or was explained?
- What would the user learn by opening it?

The summary should not claim details that are not present in extracted article text.

## 5. Why-It-Matters Standard

`why_it_matters` should explain practical relevance, such as:

- product capability change
- architecture implication
- implementation pattern
- governance or security impact
- market or strategy signal

## 6. Action Hint Standard

`action_hint` should tell the user what to do next:

- read original article
- extract architecture checklist
- compare product capability
- add to topic tracker
- create follow-up research task
