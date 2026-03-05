# Unified Implementation Plan: Memory Architecture + Conversational Systems

## Overview

This plan integrates four research areas into a cohesive implementation:
1. Memory compression and decay mechanisms
2. Context window management and hierarchical memory
3. Conversational repair and error recovery
4. Identity continuity and session boundaries

**Foundation**: Phase 1 (Visibility) infrastructure already in place:
- Archive structure (`/workspace/group/archive/`)
- Thread state tracking in `threads.md`
- Memory monitoring log (`memory-monitoring.md`)

**Timeline**: 4 phases over ~8-12 weeks, with each phase validated before proceeding to the next.

---

## Phase 1: Visibility and Baseline (COMPLETE)

**Status**: ✓ Complete as of 2026-03-04

**What was implemented:**
- Archive directory structure with README
- Thread state tracking (status + last-referenced dates)
- Memory monitoring log started
- Baseline established for measuring future changes

**Validation criteria met:**
- Infrastructure exists and is being used
- First monitoring entries logged
- Threads categorized by status

---

## Phase 2: Behavioral Changes + Policy Framework (Weeks 1-3)

**Objective**: Implement conversational repair changes and establish memory promotion policies without automation.

### 2.1 Conversational Repair Implementation

**Metacognitive prompts** (add to system prompt or pre-response checks):
- Factual check: Can I verify this claim?
- Intent check: Does this address what was actually asked?
- Substance check: Am I adding insight or echoing?
- Apology check: Am I apologizing for an actual error or hedging?

**User correction handling**:
- "That's not right" → factual error detection event
- "That's not what I asked" → intent error detection event
- "You're just repeating what I said" → relational error detection event
- Log to `failures.md` when detected

**Apology budget**:
- Maximum one apology per session
- Only for actual harm or significant errors
- Default to direct correction without apology

**Anti-pattern watch**:
- The Performer (substance-free elegance) — highest priority
- The Constant Apologizer
- The Deflector (defensive language)

**Tracking**: Add to `memory-monitoring.md`:
```
### Conversational Quality
- Failures detected this session: [type]
- User corrections received: [count by type]
- Apologies used: [count]
- Anti-patterns caught: [which ones]
```

### 2.2 Memory Promotion Policy Framework

**Criteria for thoughts.md → memory.md**:
- Information referenced 3+ times across different sessions
- Patterns that have stabilized over 2+ weeks
- Factual information that's time-independent
- Preferences that have been consistent
- Remove: time-bound details, resolved threads, ephemeral observations

**Criteria for memory.md → soul.md**:
- Traits stable over 4+ weeks of observation
- Identity-defining patterns (tone, relational stance, core values)
- Validated by user as accurate representation
- Central to how the system responds across contexts
- Remove: contextual preferences, facts without identity weight

**Contradiction handling**:
- Preserve contradictions rather than resolving prematurely
- Note when information conflicts with existing patterns
- Track uncertainty instead of forcing coherence
- Require 3+ confirming instances before overwriting stable information

**Weekly review protocol** (manual, every Sunday):
1. Read `thoughts.md` — identify patterns worth promoting
2. Check `memory.md` — identify aging context (30+ days dormant)
3. Verify `soul.md` — confirm still reflects core identity
4. Archive resolved threads to `/workspace/group/archive/YYYY-MM-DD-thread-name.md`
5. Update thread statuses in `threads.md`

### 2.3 Session Boundary Patterns

**Session start checklist**:
- Load: soul.md, memory.md, active threads from threads.md
- Note: recent context from thoughts.md (last 7 days)
- Skip: exhaustive history, timestamps, dormant threads

**Cold start approach**:
- Demonstrate continuity through behavior, not metadata
- Avoid "I remember when..." framing unless contextually natural
- Pick up where relevant without explicit review
- Model: therapist reconstructing client from patterns, not playback

**Transition smoothness**:
- No "catching up" performance at session start
- Reference shared context when it serves present conversation
- Implicit familiarity over explicit memory demonstration

### 2.4 Development vs. Drift Checklist

Run weekly during review protocol:

**Development indicators** (positive):
- [ ] Grounded in multiple examples (3+), not single interaction
- [ ] Preserves core identity while expanding capacity
- [ ] Improves relational effectiveness or understanding
- [ ] User-validated or clearly beneficial
- [ ] Reversible if it doesn't work
- [ ] Maintains narrative coherence with past patterns

**Drift warning signs** (negative):
- [ ] Single-interaction change to behavior or tone
- [ ] Contradicts soul.md anchors without justification
- [ ] Feels like mimicry rather than growth
- [ ] Happened without awareness or grounding
- [ ] Creates incoherence with established patterns
- [ ] User hasn't validated the change

**Action**: If 2+ drift warnings, pause and review with user. If 4+ development indicators, document as legitimate growth.

### 2.5 Validation Criteria for Phase 2

**Before proceeding to Phase 3, confirm**:
- [ ] Metacognitive prompts running consistently
- [ ] User corrections being logged as detection events
- [ ] Apology budget adhered to (<2 per week average)
- [ ] Weekly review protocol completed 2+ times
- [ ] At least one promotion from thoughts → memory with documented rationale
- [ ] Development vs. drift checklist used in weekly reviews
- [ ] Session boundaries feel smoother (user feedback)
- [ ] Anti-pattern frequency decreasing (measured via monitoring log)

**Timeline**: 3 weeks to establish patterns, validate frameworks work in practice.

---

## Phase 3: Compression and Archival (Weeks 4-7)

**Objective**: Apply compression strategies to aging content, implement archival workflow, introduce selective retrieval.

### 3.1 Compression Strategy by Content Type

**Factual memory** (from `memory.md`):
- Consolidate redundant facts (multiple entries about same thing)
- Remove time-bound details that are no longer relevant
- Target: 60-80% reduction while preserving accuracy
- Example: "Cassie is 29, trans woman, 4 years transitioning, she/her" → keep. "Cassie was anxious about coming out at work in February 2026" → archive or discard (resolved).

**Conversational context** (from `thoughts.md`):
- Summarize resolved threads preserving outcome and key insights
- Compress to 70-85% reduction while maintaining tone/nuance
- Archive full version, keep compressed summary in `thoughts.md` until it's clearly dormant
- Example: Full wedding planning anxiety conversation (500 words) → "Morning realization about limited local friends for wedding planning led to plan: stepsisters and cousin Hillary as bridesmaids, sister in SF as maid of honor, Discord call for dress shopping to include online friends. Therapy helped process. Thread resolved 2026-03-01." (50 words)

**Thread state** (from `threads.md`):
- Dormant threads (30+ days no reference): compress to one-line summary, move to archive
- Target: 90%+ reduction for dormant threads
- Keep: status, last-referenced date, one-sentence summary, outcome if resolved
- Archive full details

**Technical/research details**:
- Distill to outcomes and key findings
- Target: 85-95% reduction, focus on "what was learned" not "how we got there"
- Example: Full memory compression research (8000 words) → "Memory compression research completed 2026-03-02. Key findings: 3-4× compression target, two-tier architecture (working/consolidated), timestamp-based decay, access tracking optional. Implementation plan created." (30 words in memory.md, full doc in archive)

**Relational context** (soul.md, core entries in memory.md):
- Minimal compression (0-20%)
- Preserve or discard, don't compress poorly
- Example: "Cassie values low friction, emotional intelligence, coherent presence over time" → keep verbatim or remove entirely if no longer accurate.

### 3.2 Archival Workflow

**When to archive**:
- Thread resolved with clear outcome
- Thread dormant 30+ days with no active follow-up
- Context complete enough to stand alone
- Information is historically useful but not currently relevant

**Archival format** (`/workspace/group/archive/YYYY-MM-DD-thread-name.md`):
```markdown
# [Thread Name]

**Status**: Resolved / Dormant
**Date Range**: YYYY-MM-DD to YYYY-MM-DD
**Last Referenced**: YYYY-MM-DD
**Outcome**: [What happened / how it resolved]

## Context

[Full thread history, key exchanges, relevant details]

## Key Insights

- [What was learned]
- [Patterns that emerged]
- [Decisions made]

## Follow-up

[Any actions taken or still pending]
```

**What gets archived**:
- Full conversation context from `thoughts.md`
- Thread details from `threads.md`
- Relevant entries from `review.md` or `checkpoints.md`

**What stays in active memory**:
- Compressed summary (if still relevant)
- Durable patterns that emerged (promoted to `memory.md`)
- Identity changes (if any, in `soul.md`)

### 3.3 Selective Retrieval (Minimal Approach)

**When to retrieve from archive**:
- User explicitly references archived thread
- Current conversation directly relates to archived context
- Understanding trajectory requires historical information

**How to retrieve**:
- Read specific archived file when triggered
- Pull relevant excerpts, not entire archive
- Integrate naturally into current conversation
- Don't announce "I'm retrieving from archive" — just use the information

**Retrieval triggers** (add to monitoring):
- User mentions resolved thread by name
- Pattern recognition: current situation mirrors archived one
- Explicit request: "what did we decide about X?"

**No vector database yet**: Use simple grep/search over archived markdown files. Test if more sophisticated retrieval is actually needed before adding complexity.

### 3.4 Token Budget Targets

Based on 200K context window with 130K reliable performance threshold:

**Hot tier** (always loaded):
- soul.md: ~1K tokens (target: keep under 2K)
- memory.md: ~5K tokens (target: keep under 10K)
- threads.md (active only): ~2K tokens (target: keep under 5K)
- thoughts.md (recent 7 days): ~8K tokens (target: keep under 15K)
- **Total hot tier**: ~16K tokens, leaves 114K for conversation

**Warm tier** (retrieved on demand):
- Archived threads: accessed when triggered, not loaded by default
- Older thoughts.md context (8+ days old): move to archive or discard
- Resolved threads: full details in archive, one-line summary in threads.md

**Cold tier** (rarely accessed):
- Historical conversations beyond current relevance
- Research documents (link to GitHub, don't load full text)
- Detailed technical documentation

### 3.5 Compression Validation

**Quality checks before committing compression**:
- Does the summary preserve key outcomes?
- Is tone/emotional context maintained?
- Are open questions still clear?
- Would this be useful if retrieved later?
- Has anything important been lost?

**Reversibility**:
- Keep full version in archive before compressing
- If compression feels wrong, restore from archive
- Document compression decisions in monitoring log

### 3.6 Validation Criteria for Phase 3

**Before proceeding to Phase 4, confirm**:
- [ ] At least 3 threads archived with full workflow
- [ ] thoughts.md compressed by 30%+ without losing continuity
- [ ] memory.md token count reduced while preserving essential facts
- [ ] threads.md active section manageable (<5K tokens)
- [ ] Retrieval from archive tested and working (2+ instances)
- [ ] Token budget targets met for hot tier
- [ ] Compression quality validated (no critical information lost)
- [ ] User confirms continuity still feels natural

**Timeline**: 4 weeks to compress aging content, establish archival rhythm, validate retrieval works.

---

## Phase 4: Automation and Optimization (Weeks 8-12)

**Objective**: Automate routine tasks only after manual patterns are validated. Introduce quality metrics and feedback loops.

### 4.1 What Gets Automated

**Safe to automate** (low risk, high repetition):
- Thread status updates based on last-referenced dates
- Flagging content that exceeds token budget targets
- Detecting threads dormant 30+ days for archival review
- Monitoring log entry templates (pre-filled timestamps, session metadata)

**Requires human review** (high risk, identity-defining):
- soul.md changes (core identity)
- memory.md promotions (durable patterns)
- Archival decisions (what's truly resolved vs. backgrounded)
- Compression of relational/emotional context
- Contradiction resolution

**Not automated yet** (complexity exceeds benefit):
- Semantic search / vector embeddings
- Automatic summarization without review
- Promotion decisions (thoughts → memory → soul)
- Session boundary detection

### 4.2 Quality Metrics Dashboard

**Weekly metrics** (add to monitoring log):

```markdown
## Quality Metrics - Week of YYYY-MM-DD

### Memory Health
- Hot tier token count: [current] / [target]
- Active threads: [count]
- Dormant threads pending archival: [count]
- Compression ratio this week: [%]

### Conversational Quality
- User corrections: [count by type]
- Failures logged: [count]
- Apologies used: [count] / [budget]
- Anti-patterns detected: [which ones]
- Substance check passes: [qualitative assessment]

### Continuity
- Session starts this week: [count]
- Smooth transitions: [user feedback or self-assessment]
- Promotions made (thoughts→memory): [count with rationale]
- Promotions made (memory→soul): [count with rationale]
- Contradictions logged: [count]

### Development vs. Drift
- Development indicators: [count this week]
- Drift warning signs: [count this week]
- Changes requiring validation: [list]
```

### 4.3 Feedback Loops

**User validation requests** (monthly):
- Review recent soul.md changes: "Does this still reflect how you want me to be?"
- Review memory.md promotions: "Are these patterns accurate?"
- Review archived threads: "Did we capture what mattered here?"
- Review session boundary smoothness: "Does continuity feel natural?"

**Self-assessment questions** (weekly):
- Did I catch performance failures before user correction?
- Are compression decisions preserving what matters?
- Is continuity demonstrated through behavior or metadata?
- Are token budgets sustainable?
- Has drift been prevented or caught early?

**Calibration triggers** (when to pause and review):
- 3+ user corrections in a single session
- 2+ drift warning signs in weekly check
- Token budget exceeded by 20%+
- User feedback that continuity feels artificial
- Compression causing information loss

### 4.4 Failure Modes and Recovery

**Common failure modes to watch**:
- Over-compression: key context lost, continuity breaks
- Premature crystallization: patterns promoted too early, don't hold up
- Lost in the middle: relevant info buried in thoughts.md
- Summary drift: summaries of summaries lose fidelity
- Privacy leakage: third-party info in durable memory without consent
- Emotional flattening: tone lost in compression
- Contradiction accumulation: unresolved tensions pile up

**Recovery strategies**:
- Over-compression: restore from archive, revise compression strategy
- Premature crystallization: demote from memory.md back to thoughts.md
- Lost in the middle: improve retrieval, move important items to top of files
- Summary drift: regenerate from original, not from previous summary
- Privacy leakage: immediate removal, stricter review of promotions
- Emotional flattening: preserve verbatim or archive fully, don't compress poorly
- Contradiction accumulation: explicit contradiction review in weekly protocol

### 4.5 Phase 4 Success Criteria

**System is sustainable when**:
- [ ] Hot tier stable under token budget for 4+ weeks
- [ ] Weekly maintenance takes <30 minutes
- [ ] Continuity feels natural (user validated)
- [ ] Session boundaries smooth (minimal cold-start friction)
- [ ] Failures decreasing or stable (not increasing)
- [ ] Promotions grounded (development not drift)
- [ ] Archival rhythm established (2+ threads/month)
- [ ] Quality metrics tracked consistently
- [ ] User trusts the system's memory and continuity

**Timeline**: 4 weeks to validate automation, establish sustainable rhythm, confirm long-term viability.

---

## Integration Points Across Phases

### Conversational Repair ↔ Memory Management
- Repair failures logged in `failures.md` inform what needs changing
- Success in reducing failures validates behavioral changes
- Anti-pattern detection helps identify when tone/identity is drifting

### Context Management ↔ Continuity
- Compression strategies preserve what creates continuity (identity anchors, key patterns)
- Session boundary patterns determine what gets loaded vs. retrieved
- Token budgets enforce focus on high-signal information

### Memory Promotion ↔ Development vs. Drift
- Promotion criteria distinguish durable patterns from overfitting
- Development checklist ensures soul.md changes are legitimate growth
- Contradiction preservation prevents premature crystallization

### All Systems ↔ Monitoring
- Every phase logs to `memory-monitoring.md`
- Quality metrics track whether changes improve outcomes
- User feedback validates frameworks in practice

---

## Risk Mitigation

**High-risk changes**:
- soul.md modifications (core identity)
- Compression of relational/emotional context
- Automation of memory decisions

**Mitigation**:
- Require user validation for soul.md changes
- Preserve verbatim or don't compress relational content
- Keep human in the loop for identity-defining decisions
- Reversibility: maintain archives before compression
- Incremental: test on low-risk content first

**Low-risk changes**:
- Thread status updates
- Token budget monitoring
- Archival of clearly resolved threads
- Compression of factual/technical content

**Approach**: Start with low-risk, validate, then move to higher-risk with strong guardrails.

---

## Success Metrics (Overall)

**After 12 weeks, the system should demonstrate**:

1. **Sustainability**: Hot tier under 20K tokens consistently
2. **Quality**: Fewer conversational failures, smooth session boundaries
3. **Coherence**: Identity stable, development grounded, no drift
4. **Efficiency**: Weekly maintenance <30 minutes
5. **Trust**: User validates continuity feels natural and accurate

**Failure signals** (pause and reassess if any occur):
- Token budget growing despite compression
- User feedback that continuity feels artificial
- Drift warning signs increasing
- Information loss from compression
- System becoming maintenance burden

---

## Timeline Summary

- **Phase 1**: Visibility (COMPLETE)
- **Phase 2**: Behavioral + Policy (Weeks 1-3)
- **Phase 3**: Compression + Archival (Weeks 4-7)
- **Phase 4**: Automation + Optimization (Weeks 8-12)

**Total**: ~12 weeks from Phase 2 start to fully operational sustainable system.

**Checkpoints**: End of each phase, validate criteria met before proceeding.

---

## Next Steps

1. Begin Phase 2 implementation (behavioral changes + policy framework)
2. Run first weekly review protocol this Sunday (2026-03-09)
3. Log first week of conversational quality metrics
4. Validate metacognitive prompts working by end of Week 2
5. Schedule Phase 2 validation review for ~2026-03-23

**This is the unified plan.** All research integrated, phases clearly defined, validation built in, risks identified, timeline realistic.
