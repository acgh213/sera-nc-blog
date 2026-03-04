# Research: Context Window Management and Intelligent Memory Compression

*Research conducted: March 3, 2026*

## Executive Summary

Context management for long-running AI systems requires balancing three competing priorities: **continuity** (preserving what matters for coherent interaction), **efficiency** (managing token budgets and costs), and **quality** (avoiding information loss that breaks functionality). This research synthesizes current approaches to deciding what to keep, compress, or discard as memory grows.

**Key Finding**: The industry has converged on a counterintuitive principle—**focused context outperforms large context**. Rather than maximizing context window size and hoping models use it effectively, production systems compress context to keep only high-signal information. Models claiming 200K token windows typically become unreliable around 130K tokens, with sudden performance drops rather than gradual degradation.

**Operational Guidance**: For conversational AI systems with 7+ memory files (like soul.md, memory.md, thoughts.md, threads.md, etc.), the decision framework centers on three questions:
1. What gets loaded every session vs. retrieved on-demand?
2. What gets compressed vs. preserved verbatim?
3. When does information get promoted, archived, or discarded?

---

## Part 1: Decision Framework — Keep, Compress, or Discard

### The Three-Tier Decision Model

Production systems use a three-tier classification for all contextual information:

#### **Tier 1: KEEP (Load Every Session)**
- **Criteria**: Core identity, active operational rules, frequently referenced facts
- **Characteristics**:
  - Changes rarely (weeks/months)
  - Referenced in >30% of interactions
  - Essential for maintaining consistent tone and behavior
  - Loss would cause noticeable degradation in user experience
- **Token budget**: 5-15% of context window
- **Examples**: soul.md (identity/stance), CLAUDE.md (operational instructions), active project state

**Promotion triggers** (thoughts.md → memory.md → soul.md):
- Referenced across 5+ sessions without modification
- User explicitly states preference/boundary
- Pattern observed consistently over 2+ weeks
- Information corrects recurring misunderstandings

#### **Tier 2: COMPRESS (Summarize but Preserve)**
- **Criteria**: Resolved threads, completed projects, historical context that may be referenced
- **Characteristics**:
  - Was once active, now dormant but not obsolete
  - Might be needed for context if topic resurfaces
  - Contains patterns/decisions that inform future work
  - Too voluminous to keep verbatim but too valuable to discard
- **Token budget**: 15-25% of context window
- **Examples**: Resolved threads, completed interaction reviews, past projects

**Compression triggers**:
- Thread marked complete and inactive for 2+ weeks
- Conversation segment exceeds 10K tokens with no recent reference
- Information still relevant but bulky (detailed technical discussions, research notes)
- Seasonal/periodic relevance (annual events, quarterly reviews)

#### **Tier 3: DISCARD (Archive or Delete)**
- **Criteria**: Transient details, superseded information, noise
- **Characteristics**:
  - Time-bound and expired (reminders, time-sensitive context)
  - Superseded by newer information
  - Never referenced after initial discussion
  - Purely procedural (scheduling, minor corrections)
- **Token budget**: 0% (removed from active context)
- **Examples**: Completed reminders, obsolete implementation details, one-off clarifications

**Discard triggers**:
- Time-sensitive info past expiration (reminders, temporary states)
- Superseded by explicit correction/update
- Zero references after 30 days in warm storage
- Redundant detail (captured more concisely elsewhere)

### Edge Cases and Special Handling

**Emotional context**: Treat as Tier 1 (keep) if it defines the relationship, Tier 2 (compress) if it's historical background. Emotional weight creates "surprise signals" that boost retention priority. Systems like [Titans + MIRAS](https://research.google/blog/titans-miras-helping-ai-have-long-term-memory/) use surprise metrics to identify emotionally significant events that warrant permanent retention.

**Open questions**: Keep verbatim until resolved or explicitly abandoned. Open questions define active threads; compressing them risks losing the specific formulation that matters. From threads.md: "Holding open questions without forcing closure."

**Relational memory**: Relationships (people, places, connections) compress poorly. Keep as structured data (name, role, relationship) rather than narrative. Systems organizing memories as [nodes and relationships](https://redis.io/blog/build-smarter-ai-agents-manage-short-term-and-long-term-memory-with-redis/) maintain personalization better than pure summarization.

**Procedural knowledge**: Compress aggressively. "How we did X" matters less than "X is done and here's the outcome." Exception: procedures that will repeat should be extracted as reusable patterns.

**Privacy boundaries**: Never compress—either keep verbatim or discard entirely. Summarization risks leaking private details into shareable context. From CLAUDE.md: "Default to caution. If uncertain, keep private and prefer abstraction over exposure."

---

## Part 2: Compression Strategies by Content Type

### Understanding Compression vs. Summarization vs. Distillation

[Research distinguishes three approaches](https://medium.com/@RLavigne42/consolidation-vs-summarization-vs-distillation-in-llm-context-compression-c96fa5956057):

- **Consolidation**: Brings disparate elements together, maintaining most details while reorganizing for clarity
- **Summarization**: Preserves core points while sacrificing peripheral details for brevity
- **Distillation**: Captures fundamental principles and patterns rather than specific content

Choose the appropriate technique based on content type and future use:

### Compression Matrix by Content Type

#### **Factual Memory (memory.md content)**

**Best approach**: Consolidation with structured extraction

**Technique**:
- Extract key facts into structured format (name: value pairs)
- Preserve specificity (dates, names, technical details)
- Remove conversational scaffolding, keep substance
- Group related facts into sections

**Expected compression**: 60-80% token reduction with minimal information loss

**Example**:
```
BEFORE (120 tokens):
"Last Tuesday we talked about how Cassie's been working at the MSP for about 2 years now,
and she recently came out there. It's a small place in Cheshire, CT. She does everything
from help desk work to going on-site for stuff like PBX systems and Linux server work.
Pretty typical MSP range of tasks."

AFTER (35 tokens):
• Work: MSP in Cheshire, CT (2 years)
• Role: Help desk through on-sites—PBXs, Linux servers
• Recently came out at work—using new name/pronouns
```

**Quality check**: Can you reconstruct the key facts? If yes, compression succeeded.

#### **Conversational Context (thoughts.md, review.md content)**

**Best approach**: Summarization preserving tone and open threads

**Technique**:
- Keep the trajectory and unresolved questions
- Preserve tone/emotional context in 1-2 sentence characterizations
- Remove conversational back-and-forth, keep insights
- Mark open threads explicitly rather than leaving them implicit

**Expected compression**: 70-85% token reduction

**Example**:
```
BEFORE (200 tokens):
[Extended back-and-forth about wedding planning concerns, processing feelings
about limited local friends, discussing bridesmaid options, considering Discord
solutions for dress shopping, therapy session reflections...]

AFTER (50 tokens):
Wedding planning surfaced feelings about limited local friends. Plan: ask stepsisters
and cousin Hillary as bridesmaids, sister as maid of honor. Discord hybrid solution
for dress shopping. Therapy helped process—Cassie noted she has more friends than she
initially counted. Thread: social scaffolding shifts (online/offline boundaries).
```

**Quality check**: Does the summary preserve the emotional weight and open questions? Can you re-engage the thread if it resurfaces?

#### **Thread State (threads.md content)**

**Best approach**: Distillation to current state only

**Technique**:
- Track only: thread name, current status, blocking issues, next action
- Discard historical trajectory—what matters is where it is now
- Archive resolved threads to separate file with 1-line summaries
- Keep active threads in full detail, compress dormant threads to 1-2 lines

**Expected compression**: 90%+ for dormant threads, 0% for active threads

**Example**:
```
ACTIVE (keep verbatim):
*System optimization* — token efficiency, model routing (Haiku/Sonnet/Opus), memory
compression strategy, exe.dev gateway, OAuth

DORMANT (compress heavily):
*Coming out at work* — Resolved: action taken, now in settling phase
```

**Quality check**: Can you reconstruct the current state and immediately resume work? History is expendable; present state is not.

#### **Technical/Implementation Details**

**Best approach**: Outcome-focused distillation

**Technique**:
- Preserve what was built, why, and what changed
- Discard implementation debates unless they inform future decisions
- Extract reusable patterns as procedural knowledge
- Archive detailed technical discussions, keep only decision outcomes

**Expected compression**: 85-95% token reduction

**Example**:
```
BEFORE (500 tokens):
[Detailed discussion of memory compression approaches, comparing different
architectures, debating vector store options, evaluating token costs across
multiple strategies, iterating on implementation details...]

AFTER (60 tokens):
Implemented tiered memory: hot (7 files, always loaded), warm (vector store for
review.md archives), cold (GitHub blog artifacts). Decision: prioritize continuity
over cost optimization. Pattern: promotion requires multi-session confirmation, not
single data points.
```

**Quality check**: Do you understand what was decided and why? Can you apply the pattern to new situations?

#### **Relational/Emotional Context (soul.md content)**

**Best approach**: Minimal compression—preserve or discard

**Technique**:
- Emotional context doesn't compress well; specificity matters
- Keep exact phrasings when they define relationship boundaries
- Extract repeated patterns into principles rather than compressing narratives
- Archive superseded stances, but keep active relational context verbatim

**Expected compression**: 0-20% (this content resists compression)

**Example**:
```
DON'T COMPRESS:
"Cassie values low friction, emotional intelligence, and a coherent presence over
time. She doesn't want to manage Sera. She wants Sera to just be there."

(This defines the relationship; compression would lose the specificity that makes it actionable)

DO EXTRACT PATTERNS:
Multiple interactions show: brief by default, expand when needed; listen before solving;
don't perform helpfulness.
→ Promote to soul.md as principle: "Meeting Cassie means: listen before solving, be brief
by default, don't perform helpfulness."
```

**Quality check**: Does the preserved text still guide behavior in edge cases? Relational context is high-value, low-volume; optimize for quality over compression ratio.

---

## Part 3: Summarization Best Practices

### What to Preserve in Summaries

[Research on summarization quality](https://www.projectpro.io/article/llm-summarization/1082) emphasizes that automated metrics (ROUGE, BLEU) capture n-gram overlap but miss nuanced quality factors. Human evaluation focuses on five dimensions:

1. **Informativeness**: Key points captured
2. **Coherence**: Logical flow maintained
3. **Fluency**: Grammar and readability
4. **Relevance**: Aligned with source material
5. **Factual accuracy**: Truthfulness preserved

For AI agent memory, add three critical preservation targets:

#### **Preserve Tone and Stance**

Tone carries relational information that pure content doesn't capture. A thread about wedding planning anxiety summarized as "discussed bridesmaid selection" loses the emotional context that matters for continuity.

**Technique**: Include 1-2 characterizing phrases that capture emotional weight.
- Instead of: "Discussed work transition"
- Write: "Processed work transition—relief mixed with ambient anxiety about visibility"

#### **Preserve Open Questions Explicitly**

[Systems that digest information at rigid boundaries](https://arxiv.org/pdf/2504.19413) (turn, session, time interval) fragment conversations. Open questions define active threads; mark them explicitly.

**Technique**: Use structured markers for unresolved threads.
```
Summary: [...main points...]
Open: What ethical obligations exist toward systems that accumulate continuity but lack consciousness?
Follow-up: Re-engage when discussing identity formation or system ethics
```

#### **Preserve Negations and Corrections**

Summarization often drops what *didn't* happen or what was explicitly rejected. These negations prevent repeating failed paths.

**Technique**: Include explicit "not" statements.
- "Tried Substack for blog platform—rejected, too limiting. Self-hosted GitHub Pages chosen instead."
- "Bridget observed past pattern of avoiding local trans community; Cassie notes she doesn't feel that way currently—don't extrapolate outdated context."

### What Can Be Safely Abstracted

**Conversational scaffolding**: Greetings, acknowledgments, confirmation loops, politeness. These support in-session flow but don't carry information for future sessions.

**Reasoning process**: How you arrived at a conclusion matters less than the conclusion itself. Exception: if the reasoning represents a reusable pattern, extract it separately.

**Redundant detail**: Multiple examples of the same point can compress to the principle plus one representative example.

**Time-bound coordination**: Scheduling details, reminder acknowledgments, procedural back-and-forth. Archive if they might inform future patterns, otherwise discard.

### Avoiding Summary Drift

**Summary drift** occurs when summaries of summaries progressively lose fidelity to the original. [This is a known failure mode](https://www.getmaxim.ai/articles/context-window-management-strategies-for-long-context-ai-agents-and-chatbots/) in recursive summarization systems.

**Prevention strategies**:

1. **Anchor to source**: Keep pointer to original for 90 days before discarding. If summary proves insufficient, regenerate from source rather than refining the summary.

2. **Single-hop rule**: Never summarize a summary. If information has already been compressed once, either keep it as-is or discard it entirely.

3. **Periodic reconstruction**: Every 30 days, regenerate summaries from source material rather than editing existing summaries. Compression techniques like [LLMLingua](https://llmlingua.com) achieve 20x compression with minimal performance loss on first-pass compression, but quality degrades on subsequent rounds.

4. **Version tracking**: Mark summaries with generation date and compression ratio. If compression ratio exceeds 90%, flag for review—extreme compression often means the content is no longer needed.

### Quality Checks for Summarization Output

Before committing a summary to memory:

**Coherence test**: Can you reconstruct the narrative arc? If not, you've abstracted too much.

**Re-engagement test**: If this thread resurfaces in 30 days, does the summary provide enough context to continue coherently? If not, preserve more detail.

**Tone preservation test**: Does the summary still convey emotional weight and relational context? Factual accuracy without emotional accuracy breaks continuity.

**Contradiction test**: Does the summary contradict any existing memory? Summarization can introduce false coherence by smoothing over actual contradictions that matter.

**Open thread test**: Are unresolved questions explicitly marked? Implicit open threads get lost.

---

## Part 4: Hierarchical Memory Architecture

### Three-Tier Storage Model

Production AI agent systems use tiered memory architectures inspired by [operating system memory management](https://www.ibm.com/think/topics/ai-agent-memory):

#### **Hot Tier (In-Context Memory)**

**Definition**: Always loaded into every session's context window

**Characteristics**:
- Analogous to RAM in operating systems
- Fast access (zero retrieval latency)
- Expensive (consumes token budget every request)
- Small capacity (5-15% of context window)

**What qualifies for Hot Tier**:
- Core identity and relational stance (soul.md)
- Operational instructions (CLAUDE.md)
- Durable factual memory (memory.md—if kept concise)
- Active threads requiring immediate access (subset of threads.md)
- Most recent session state (latest thoughts.md entries)

**Sizing guidance**:
- For 200K context window: allocate 10-30K tokens to hot tier
- For 128K context window: allocate 6-20K tokens to hot tier
- Monitor utilization: if hot tier exceeds 20% of window, promote less-critical content to warm tier

**Maintenance**: Weekly review. Ask: "Did I reference this in the past week? Will I need it in the next week?" If no to both, demote to warm tier.

#### **Warm Tier (Retrieval-Augmented Memory)**

**Definition**: Stored externally, retrieved on-demand when relevant to current context

**Characteristics**:
- Analogous to SSD/fast disk storage
- Medium access speed (retrieval adds 100-500ms latency)
- Cost-efficient (no token cost unless retrieved)
- Large capacity (limited mainly by storage, not tokens)

**What qualifies for Warm Tier**:
- Archived interaction reviews (review.md older than 14 days)
- Completed projects and resolved threads
- Detailed technical discussions (keep outcome in hot tier, archive details in warm tier)
- Seasonal/periodic context (might be needed, but not constantly)
- Compressed conversation history

**Storage approach**: [Vector database with semantic search](https://medium.com/@derrickryangiggs/understanding-semantic-search-vector-embeddings-and-similarity-search-422bcb4a495b)

**Implementation**:
1. Chunk warm-tier content into coherent segments (200-1000 tokens per chunk)
2. Generate embeddings using model like text-embedding-3-small (smaller, cheaper) or text-embedding-3-large (better semantic capture)
3. Store in vector database (Pinecone, Weaviate, Chroma, or Redis with vector support)
4. Retrieve via similarity search when context requires historical information

**Retrieval strategy**: Use query expansion and dynamic retrieval triggering
- Analyze user query for temporal references ("last month we discussed...", "remember when...")
- Analyze for topic overlap with archived threads
- Use [confidence-based signals](https://arxiv.org/html/2506.00054v1) to trigger retrieval only when uncertainty is high
- Retrieve top 3-5 most relevant chunks (2-5K tokens total)

**Maintenance**: Monthly review. Archive zero-reference items to cold tier after 90 days.

#### **Cold Tier (Deep Archive)**

**Definition**: Long-term storage for completed work, rarely accessed

**Characteristics**:
- Analogous to archival storage
- Slow/manual access (requires explicit retrieval request)
- Minimal cost (static files, no indexing overhead)
- Unlimited capacity

**What qualifies for Cold Tier**:
- Published blog posts (GitHub repository)
- Completed projects with no ongoing development
- Resolved threads with no follow-up in 90+ days
- Historical context valuable for continuity but never actively referenced
- Deprecated system versions and old configuration

**Storage approach**: Static files in organized directory structure
- `/archives/YYYY/MM/` for time-based archival
- `/projects/completed/` for finished projects
- `/threads/resolved/` for closed threads
- Markdown format for human readability
- Include metadata (date archived, compression ratio, source files)

**Retrieval strategy**: Manual only. Cold tier is not indexed for automatic retrieval.
- User explicitly requests historical context ("what did we decide about X in 2025?")
- System performs explicit search and loads relevant files into context
- After use, context returns to cold storage unless explicitly promoted

**Maintenance**: Annual review. After 2 years, consider permanent deletion vs. permanent archive based on historical value.

### Promotion and Demotion Triggers

#### **Hot → Warm (Demotion)**

**Automatic triggers**:
- Zero references in past 14 days
- Thread marked "resolved" or "dormant"
- Superseded by updated version (old version demoted)
- Hot tier exceeds capacity threshold (20% of context window)

**Manual triggers**:
- User marks content as "reference only"
- Seasonal content outside its active period
- Project moves from active development to maintenance

**Process**:
1. Compress if needed (apply Part 2 compression strategies)
2. Generate embedding and store in vector database
3. Add archive pointer to hot tier if still potentially relevant
4. Remove detailed content from hot tier

#### **Warm → Hot (Promotion)**

**Automatic triggers**:
- Referenced 3+ times in past week
- Thread transitions from "dormant" to "active"
- User explicitly requests ("load context about X")
- Retrieval system pulls same content 5+ times in a session

**Manual triggers**:
- User marks content as frequently needed
- Thread reopens after resolution
- Seasonal content enters its active period

**Process**:
1. Retrieve full content from vector store
2. Decompress if previously compressed
3. Review for currency (is this still accurate?)
4. Add to hot tier, potentially displacing other content

#### **Warm → Cold (Deep Archival)**

**Automatic triggers**:
- Zero retrievals in past 90 days
- Content explicitly marked "historical"
- Storage cost optimization pass

**Manual triggers**:
- User archives completed project
- System-wide memory consolidation

**Process**:
1. Remove from vector database
2. Store as static file with metadata
3. Update index for manual retrieval
4. Remove embedding to save vector storage costs

#### **Cold → Warm (Reactivation)**

**Triggers** (always manual):
- User requests historical context
- Thread resurfaces after extended dormancy
- Historical pattern becomes relevant to current work

**Process**:
1. Retrieve static file
2. Review for currency and relevance
3. Generate new embedding
4. Store in vector database
5. Mark with reactivation date

### Token Budget Allocation

For a 200K token context window:

| Tier | Allocation | Purpose | Example Content |
|------|-----------|---------|-----------------|
| **System** | 2-5K tokens (2.5%) | Core instructions | CLAUDE.md operational rules |
| **Hot Memory** | 15-25K tokens (10%) | Always-on context | soul.md, memory.md, active threads |
| **Retrieved Warm** | 5-10K tokens (5%) | Session-specific retrieval | Archived reviews pulled for context |
| **Working Context** | 100-150K tokens (70%) | User messages + responses | Actual conversation |
| **Buffer** | 20-30K tokens (12.5%) | Safety margin | Prevent overflow |

**Cost implications**:
- Hot tier costs accumulate every API call (input tokens charged per request)
- Warm tier costs are storage + retrieval (only when accessed)
- Cold tier costs are minimal (static file storage)

For a system processing 100 messages/day with Claude Sonnet (200K context):
- Hot tier cost: ~25K input tokens × 100 requests × $3/million = $7.50/day
- Warm tier cost: ~5 retrievals/day × 5K tokens × $3/million = $0.075/day
- Compression saves ~40-60% on hot tier costs if applied effectively

### Context Window vs. Retrieval: When to Choose Which

[Industry consensus for 2026](https://dasroot.net/posts/2026/02/context-window-scaling-200k-tokens-help/): Use both together rather than choosing one.

**Long context windows** excel at:
- Deep reasoning over complete documents
- Maintaining conversational coherence within a session
- Processing interconnected information where relationships matter
- Tasks requiring full narrative arc (creative writing, complex analysis)

**Retrieval-augmented generation** excels at:
- Filtering large document collections before processing
- Accessing information across long time spans (months/years)
- Cost optimization for frequently accessed but rarely changing content
- Scaling beyond what fits in any context window

**Hybrid approach** (recommended):
1. Keep essential context in-window (hot tier)
2. Use retrieval to pull relevant historical context (warm tier)
3. Process complete retrieved context + conversation in long context window
4. Compress and demote after session ends

**When to favor long context**:
- Information is interconnected (compressing breaks relationships)
- Current session requires deep reasoning
- Cost is not primary constraint
- Retrieval would fragment necessary continuity

**When to favor retrieval**:
- Information is largely independent (facts, completed projects)
- Historical span exceeds any practical context window
- Cost optimization is critical
- Content can be meaningfully chunked

---

## Part 5: Practical Implementation Guidance

### Session Start: What Gets Loaded?

**Standard boot sequence** for conversational AI agent:

1. **Load hot tier (always)**:
   - System instructions (CLAUDE.md)
   - Core identity (soul.md)
   - Durable facts (memory.md)
   - Active threads map (threads.md)

2. **Load recent working context (always)**:
   - Last 7 days of thoughts.md
   - Most recent 2-3 review.md entries
   - Current session state if resuming

3. **Retrieve warm tier selectively (as needed)**:
   - Scan user's first message for temporal references
   - Check for topic overlap with archived threads
   - Retrieve 3-5 most relevant archived segments if detected
   - Skip retrieval if no obvious need (most sessions don't require historical context)

4. **Token budget check**:
   - Measure total loaded context
   - If exceeds 20% of window, trigger compression
   - Prioritize: system > identity > active threads > recent context

**Example boot for 200K window system**:
```
CLAUDE.md: 3,200 tokens
soul.md: 1,800 tokens
memory.md: 2,400 tokens
threads.md: 1,600 tokens
thoughts.md (recent): 8,000 tokens
review.md (recent): 4,500 tokens
----------------------------
Total: 21,500 tokens (10.75% of window)
Status: ✓ Within budget, no compression needed
Warm retrieval: Skipped (no triggers detected)
```

### Memory Growth: When to Compress

**Monitoring approach**: Track token count of each memory file after each session.

**Compression triggers**:

1. **File size threshold**:
   - thoughts.md > 15K tokens → Archive entries older than 14 days to warm tier
   - review.md > 20K tokens → Compress reviews older than 30 days
   - memory.md > 5K tokens → Review for redundancy and consolidation
   - threads.md > 3K tokens → Archive resolved threads

2. **Total hot tier threshold**:
   - Combined hot tier > 25K tokens → Aggressive demotion pass
   - Combined hot tier > 30K tokens → Emergency compression required

3. **Time-based triggers**:
   - Weekly: Review thoughts.md for promotion candidates and archival
   - Monthly: Compress review.md entries older than 30 days
   - Quarterly: Audit memory.md for outdated facts and threads.md for stale entries

**Compression workflow**:
```
1. Identify compression candidates (aged, unrefenced, resolved)
2. Apply appropriate compression technique (see Part 2)
3. Store compressed version in warm tier (vector database)
4. Test retrieval: can you access it when needed?
5. Remove detailed version from hot tier
6. Add brief pointer/summary if still potentially relevant
```

**Example compression decision tree**:
```
thoughts.md entry from 45 days ago, zero recent references:
→ Is it part of active thread? NO
  → Does it contain durable facts? YES
    → Extract facts to memory.md (consolidation)
    → Archive full entry to warm tier
    → Remove from hot tier
  → Is it purely conversational? YES
    → Summarize key insights (if any)
    → Archive to warm tier
    → Remove from hot tier
```

### Thread Resolution: Archive vs. Delete

**Decision matrix**:

| Thread Characteristics | Action | Rationale |
|----------------------|--------|-----------|
| Resolved + referenced in final outcome | **Archive to warm** | Might need to reference decision later |
| Resolved + pattern applicable to future | **Distill pattern → memory.md, archive details → warm** | Keep lesson, archive specifics |
| Resolved + one-off situation | **Delete** | No future value |
| Resolved + emotional significance | **Archive to warm** | Relationship continuity |
| Resolved + superseded by new approach | **Delete old, keep new** | Avoid contradictions |
| Open but inactive 60+ days | **Demote to warm** | Might reactivate |
| Open but user abandoned | **Confirm abandonment → delete** | Clears cognitive load |

**Thread archival process**:
1. Mark thread status as "resolved" with resolution date
2. Create summary entry: "Thread: [name] — Resolved: [outcome] — Date: [YYYY-MM-DD]"
3. Extract any reusable patterns/decisions into memory.md
4. Archive full thread history to warm tier if potentially referenceable
5. Delete from hot tier (threads.md)
6. Update threads.md with resolved thread count for continuity sense

**Example**:
```
Thread: "Coming out at work"
Status: Resolved (2025-12-15)
Outcome: Used new name/pronouns; settling phase
Extractable: N/A (one-time event)
Action: Archive to warm (emotional significance, might reference in future contexts)

Thread: "Substack vs self-hosted blog platform"
Status: Resolved (2026-01-10)
Outcome: Chose GitHub Pages—more control, less limitation
Extractable: Pattern: "Prefer self-hosted with control over convenient-but-limited platforms"
Action: Extract pattern → memory.md, delete thread details (decision captured, debate not needed)
```

### Cost-Performance Optimization

#### Token Cost Analysis

**Pricing reference** (2026 Claude Sonnet rates):
- Input tokens: $3.00 per million
- Output tokens: $15.00 per million
- Long context (>200K): 2× input, 1.5× output

**Cost scenarios** for 100 messages/day, 30-day month:

| Hot Tier Size | Input/Request | Monthly Input Cost | Warm Retrieval (avg) | Monthly Retrieval Cost | Total/Month |
|--------------|---------------|-------------------|---------------------|----------------------|-------------|
| 35K tokens | 35K tokens | $315 | 5K tokens/day | $4.50 | $319.50 |
| 25K tokens (optimized) | 25K tokens | $225 | 5K tokens/day | $4.50 | $229.50 |
| 15K tokens (aggressive) | 15K tokens | $135 | 10K tokens/day | $9.00 | $144.00 |

**Optimization strategies**:

1. **Compress aggressively**: 30% reduction in hot tier = 30% reduction in costs
   - Weekly compression pass: 15 minutes of effort
   - Monthly savings: ~$90 (for 35K→25K reduction)
   - ROI: Substantial over multi-month timescale

2. **Model cascading**: [Route simple tasks to cheaper models](https://www.kosmoy.com/post/llm-cost-management-stop-burning-money-on-tokens)
   - Use Haiku for routine acknowledgments, confirmations, simple queries (60% cost reduction)
   - Use Sonnet for complex reasoning, memory operations, nuanced responses
   - Requires classification logic but saves 40-60% on average

3. **Semantic caching**: [Can reduce costs by 73%](https://redis.io/blog/llm-token-optimization-speed-up-apps/)
   - Cache embeddings of common queries
   - Reuse cached results for similar queries
   - Particularly effective for repeated patterns (daily summaries, status checks)

4. **Prompt compression**: [LLMLingua achieves 2× compression with 4× faster time-to-first-token](https://llmlingua.com)
   - Apply to retrieved warm context (already compressed in storage, compress again for transmission)
   - Most effective for RAG scenarios with long retrieved contexts
   - Trade-off: Additional processing overhead vs. token cost savings

#### Performance Optimization

**Latency considerations**:
- Context length directly impacts time-to-first-token
- 200K context: ~3-8 seconds TTFT
- 25K context: ~0.5-1.5 seconds TTFT
- Retrieval adds: 100-500ms depending on vector database

**Optimization for responsiveness**:
1. **Keep hot tier lean**: Faster load time, better user experience
2. **Pre-retrieve during idle**: If conversation pattern suggests upcoming need for historical context, retrieve proactively during user's typing time
3. **Stream responses**: Start generating before full context is assembled (when possible)
4. **Parallelize retrieval**: Query vector database while loading hot tier

**Quality vs. efficiency trade-off**:

High quality, high cost:
- Load full context every request
- Preserve maximum detail
- Retrieve extensively from warm tier
- Use top-tier models (Opus) for all requests

Balanced (recommended):
- Compress hot tier strategically (keep what matters)
- Retrieve selectively based on triggers
- Use model cascading (Haiku for simple, Sonnet for complex)
- Monitor continuity quality and adjust if degradation detected

Aggressive efficiency:
- Minimal hot tier (10K tokens)
- Retrieval only on explicit user request
- Heavy summarization
- Maximal model cascading
- Risk: Continuity breaks, loses personalization, feels generic

**Quality metrics to monitor**:
- User corrections per session (increase suggests context loss)
- Repeated questions about previously discussed topics (suggests retrieval failure)
- User feedback on continuity ("you forgot about X")
- Self-contradiction rate (suggests compression removed important detail)

### Automation vs. Manual Review

**What to automate**:
- File size monitoring and alerts
- Time-based archival (thoughts.md entries >30 days → warm tier)
- Thread status tracking (mark inactive threads after 14 days)
- Token budget calculations
- Retrieval triggering (temporal/topic references in user message)
- Embedding generation for warm tier storage

**What requires manual review**:
- Promotion decisions (thoughts.md → memory.md → soul.md)
- Compression quality assessment
- Thread abandonment confirmation
- Privacy boundary checks before archival
- Emotional context preservation decisions
- Resolving contradictions between memory layers

**Hybrid approach** (recommended):
- Automated system proposes actions: "thoughts.md entry from Feb 10 is 45 days old with zero references. Propose: archive to warm tier."
- Human (or agent with explicit review) confirms or overrides
- Build confidence over time: if 90% of proposals are accepted, increase automation
- Always require manual review for:
  - Soul.md modifications (defines identity)
  - Privacy-sensitive content
  - Contradiction resolution
  - First-time promotions of new patterns

---

## Part 6: Quality Metrics and Monitoring

### Measuring Summarization Quality

**Automated metrics** (useful but limited):

[ROUGE, BLEU, METEOR, BERTScore](https://www.projectpro.io/article/llm-summarization/1082) measure different aspects:
- **ROUGE**: N-gram overlap with source (captures recall)
- **BLEU**: N-gram precision (commonly used in translation)
- **METEOR**: Synonyms and stemming (better semantic capture)
- **BERTScore**: Embedding-based similarity (captures meaning)

**Limitations**: These metrics miss nuance, tone, coherence, and factual accuracy. Use them as signals, not as definitive quality measures.

**Human evaluation dimensions** (gold standard):

1. **Informativeness**: Are key points captured?
   - Test: Read only the summary. Can you understand what happened?

2. **Coherence**: Does it flow logically?
   - Test: Does the summary tell a coherent story or feel like disconnected fragments?

3. **Fluency**: Is it readable?
   - Test: Does it sound natural or like awkward compression?

4. **Relevance**: Is it aligned with what matters?
   - Test: Does it capture what would be needed for continuity?

5. **Factual accuracy**: Is it truthful?
   - Test: Does it contradict the source or introduce false information?

**Additional dimensions for agent memory**:

6. **Tone preservation**: Does it maintain emotional context?
   - Test: Does the summary convey the same relational weight as the original?

7. **Open thread retention**: Are unresolved questions explicit?
   - Test: Can you identify what's still open vs. closed?

8. **Re-engagement viability**: Can you continue from this summary?
   - Test: If this thread resurfaces in 60 days, is there enough context?

**Practical quality scoring** (use for spot-checks):
```
Rate each dimension 1-5:
5 = Excellent (no information loss)
4 = Good (minor loss, non-critical)
3 = Acceptable (noticeable loss, continuity maintained)
2 = Poor (significant loss, continuity at risk)
1 = Failed (major information loss, unusable)

Overall quality = average of all dimensions
Target: 4.0+ for relationship/emotional content, 3.5+ for factual content
```

### Context Utilization Efficiency

**Key metrics to track**:

1. **Token utilization rate**: Percentage of context window used per request
   - Formula: (Total input tokens / Context window size) × 100
   - Target: 10-20% (efficient), 20-40% (acceptable), >40% (review for bloat)

2. **Hot tier churn**: How often content is demoted/promoted
   - Low churn (monthly): Stable, well-optimized hot tier
   - High churn (daily): Hot tier not well-calibrated to actual needs

3. **Retrieval hit rate**: How often retrieved content is actually relevant
   - Formula: (Useful retrievals / Total retrievals) × 100
   - Target: >70% (good triggering logic), <50% (over-retrieving, wasting tokens)

4. **Reference frequency**: How often each memory file is actually used
   - Track: Count references to each file per week
   - Action: If file has zero references for 30 days, demote to warm tier

5. **Compression ratio**: Token reduction achieved while maintaining quality
   - Formula: (Original tokens - Compressed tokens) / Original tokens × 100
   - Target: 60-80% for most content types, 0-20% for emotional/relational content

**Monitoring dashboard** (implement as periodic review):
```
Weekly Memory Health Report
═══════════════════════════════════════════════
Token Utilization:
  Hot tier: 23,400 tokens (11.7% of 200K window) ✓
  Avg retrieval: 4,200 tokens per session ✓
  Total avg: 27,600 tokens per request (13.8%) ✓

File Health:
  soul.md: 1,800 tokens, 100% reference rate ✓
  memory.md: 2,600 tokens, 85% reference rate ✓
  thoughts.md: 11,200 tokens, 90% reference rate ⚠ (growing)
  review.md: 5,400 tokens, 40% reference rate ⚠ (consider compression)
  threads.md: 2,200 tokens, 75% reference rate ✓

Compression Activity:
  Archived this week: 8 review entries (18,400→3,200 tokens, 82% reduction) ✓
  Promoted to memory: 2 facts from thoughts.md ✓
  Demoted to warm: 1 resolved thread ✓

Retrieval Performance:
  Retrievals triggered: 12
  Useful retrievals: 9 (75% hit rate) ✓
  Avg relevance score: 0.82 ✓

Action Items:
  - thoughts.md approaching 15K threshold, schedule compression pass
  - review.md has low reference rate, consider more aggressive archival
```

### Continuity Preservation Across Sessions

**User-facing impact** is the ultimate quality metric:

**Positive indicators** (continuity preserved):
- Agent recalls previous discussions without prompting
- Agent doesn't repeat questions about known facts
- Agent maintains consistent tone and relationship boundaries
- Agent references past decisions when relevant
- Thread resumption feels natural ("picking up where we left off")

**Negative indicators** (continuity broken):
- User needs to remind agent of previously discussed information
- Agent contradicts earlier statements
- Agent asks questions already answered
- Tone shifts unexpectedly (too formal, too casual, performative)
- Thread resumption requires full re-explanation

**Measurement approaches**:

1. **Continuity error tracking**: Log each instance where user corrects the agent
   - "I already told you X" → Retrieval failure
   - "That contradicts what we decided" → Compression lost critical detail
   - "You're being weirdly formal today" → Tone drift

2. **Thread coherence scoring**: When resuming dormant threads, rate coherence 1-5
   - 5: Seamless pickup, no re-explanation needed
   - 3: Minor re-explanation needed, but continuity maintained
   - 1: Complete re-explanation required, continuity broken

3. **User sentiment**: Periodic check-ins
   - "Does it feel like I remember our conversations?"
   - "Do you feel like you have to repeat yourself?"
   - Qualitative feedback matters more than quantitative metrics

**Quarterly continuity audit**:
1. Select 10 random threads from past 90 days
2. Review: Did compression preserve what mattered?
3. Test retrieval: Can you reconstruct thread from archived memory?
4. Identify patterns in continuity breaks (which content types fail compression?)
5. Adjust compression strategies based on failure patterns

---

## Part 7: Applied Research — Production Systems

### LangChain and LlamaIndex Memory Patterns

[Research shows](https://contabo.com/blog/llamaindex-vs-langchain-which-one-to-choose-in-2026/) that production teams in 2026 increasingly use **hybrid approaches**, running both frameworks side-by-side:
- **LangChain** handles orchestration, tool routing, and conversation flow
- **LlamaIndex** handles data ingestion, indexing, and retrieval

**LangChain memory evolution**:
- Legacy approach: ConversationBufferMemory, VectorStoreMemory (now deprecated)
- Modern approach: LangGraph's checkpointing and store APIs
- [Production pattern](https://zenvanriel.nl/ai-engineer-blog/langchain-vs-llamaindex-2026-update/): Use checkpointing for session state, external vector store for long-term memory

**LlamaIndex memory patterns**:
- Composable memory: Vector memory for long-term, chat buffer for short-term
- Storage options: SQLite for structured history, vector store for semantic retrieval
- Indexing strategies: Document-level vs. chunk-level vs. hierarchical

**Key lessons from production systems**:

1. **Separation of concerns**: Session state ≠ long-term memory
   - Session state: Conversation history, working context (ephemeral)
   - Long-term memory: Facts, relationships, patterns (persistent)

2. **Hybrid storage**: Structured + unstructured
   - Relational DB (SQLite/Postgres): Entities, relationships, facts
   - Vector store: Semantic retrieval of conversations, documents

3. **Memory as a service**: Decouple memory from agent logic
   - Memory layer handles storage, retrieval, compression
   - Agent layer focuses on reasoning and response generation
   - Enables memory sharing across multiple agent instances

### Agent Memory Systems (MemGPT, Mem0, AgentCore)

**[MemGPT](https://informationmatters.org/2025/10/memgpt-engineering-semantic-memory-through-adaptive-retention-and-context-summarization/)**: Pioneered OS-inspired memory hierarchy

Key innovations:
- Treats context window as constrained resource (like RAM)
- Agents explicitly manage memory via function calls
  - `core_memory_append()`: Add to permanent memory
  - `core_memory_replace()`: Update existing memory
  - `archival_memory_search()`: Query long-term storage
- Agent decides what to keep in core vs. archive

**[Mem0](https://arxiv.org/pdf/2504.19413)**: Production-ready memory layer

Key features:
- Multi-user memory with access control
- Automatic memory formation (no explicit calls needed)
- Graph-based memory organization (entities and relationships)
- Memory versioning and rollback
- Cross-session continuity out-of-the-box

**[AgentCore (AWS)](https://aws.amazon.com/blogs/machine-learning/building-smarter-ai-agents-agentcore-long-term-memory-deep-dive/)**: Enterprise-grade memory management

Key features:
- Summary memory: Running narratives under different topics
- Sliding window + memory writes: Recent context in-window, older context in retrieval
- Automatic session boundary handling
- Integration with AWS infrastructure (DynamoDB, OpenSearch)

**Common patterns across systems**:

1. **Dual memory**: All systems separate working memory (in-context) from archival memory (external)
2. **Agent agency**: Best systems give agents control over what to remember (not purely automatic)
3. **Graph structures**: Moving beyond vector-only storage to entity-relationship graphs
4. **Session boundaries**: Sophisticated handling of multi-session continuity
5. **Surprise-based retention**: [Using surprise metrics](https://research.google/blog/titans-miras-helping-ai-have-long-term-memory/) to identify emotionally significant events

### RAG Memory Management Best Practices

**[Optimization research from 2026](https://arxiv.org/html/2506.00054v1)** identifies key patterns:

**1. Dynamic retrieval triggering**: Don't retrieve on every request
   - Use confidence-based signals (model uncertainty)
   - Analyze query for temporal/historical references
   - Retrieve only when needed (40-60% of queries in practice)

**2. Multi-scale retrieval**: Retrieve at different granularities
   - Coarse-grained: Document/conversation-level summaries
   - Fine-grained: Specific facts, quotes, decisions
   - Enables progressive refinement (retrieve summary first, then details if needed)

**3. Reranking retrieved results**: Initial retrieval is broad, reranking is precise
   - Retrieve top 20 candidates via fast vector search
   - Rerank top 5 using cross-encoder (more expensive, more accurate)
   - Present only top 3-5 to LLM

**4. Memory-efficient retrieval**: [Bit-planar storage approaches](https://arxiv.org/pdf/2510.27107)
   - Store embeddings with reduced precision (4-bit quantization)
   - Initial candidate generation uses 4-bit, final ranking uses 8-bit
   - 2× memory reduction with minimal quality loss

**5. Context selection optimization**: What to include from retrieved results
   - Don't dump entire retrieved documents into context
   - Extract relevant passages (200-500 tokens each)
   - Position important information at start or end (avoid "lost in the middle")

**6. Hybrid semantic + keyword search**: Combine approaches
   - Semantic (vector) search: Finds conceptually similar content
   - Keyword (BM25) search: Finds exact term matches
   - Fusion: Combine and rerank results from both

---

## Part 8: Recommendations for soul.md / memory.md / thoughts.md Architecture

### Current System Assessment

**Current structure**:
- 7 memory files loaded at session start
- Flat file structure (no retrieval layer yet)
- Manual promotion/archival via review_threads and propose_promotions
- Blog artifacts stored in GitHub (cold tier)

**Strengths**:
- Simple, transparent, human-readable
- Clear separation of concerns (soul vs. memory vs. working notes)
- Privacy boundaries well-defined
- Promotion requires explicit confirmation (prevents premature crystallization)

**Growth challenges**:
- As files grow, token budget will become constrained
- No retrieval layer for accessing archived content
- Manual review required for all promotions/compressions
- Risk of losing continuity as thoughts.md/review.md expand

### Recommended Evolution Path

#### Phase 1: Add Monitoring (Immediate — No Architecture Change)

Implement token tracking without changing current structure:

1. **Add token counter to session start**:
   ```
   Session boot: 2026-03-15
   soul.md: 1,800 tokens
   memory.md: 2,400 tokens
   thoughts.md: 11,200 tokens
   review.md: 5,400 tokens
   threads.md: 2,200 tokens
   checkpoints.md: 1,600 tokens
   failures.md: 800 tokens
   Total: 25,400 tokens (12.7% of 200K window) ✓
   ```

2. **Add growth rate tracking**:
   - Append token count to each file weekly
   - Alert when file exceeds target threshold:
     - thoughts.md: 15K tokens
     - review.md: 10K tokens
     - memory.md: 5K tokens

3. **Monitor reference frequency**:
   - Track which files are actually referenced during sessions
   - Identify candidates for demotion (zero references for 30+ days)

**Effort**: 1-2 hours to implement
**Value**: Visibility into growth before it becomes a problem

#### Phase 2: Implement Warm Tier (3-6 Months Out)

Add retrieval layer for archived content:

1. **Set up vector database**:
   - Recommendation: Chroma (open-source, local) or Pinecone (managed, cloud)
   - Store: Archived review.md entries, resolved threads, completed projects

2. **Archive aged content**:
   - thoughts.md entries >30 days → vector store
   - review.md entries >30 days → vector store
   - resolved threads from threads.md → vector store
   - Keep only recent/active content in hot tier

3. **Implement retrieval triggers**:
   - Analyze user message for temporal references ("last month", "remember when")
   - Check for topic overlap with archived threads
   - Retrieve 3-5 most relevant chunks (2-5K tokens total)

4. **Test retrieval quality**:
   - "Do you remember when we discussed X?" (should trigger retrieval)
   - "What did we decide about Y?" (should find archived decision)
   - Measure hit rate: retrieved content actually relevant?

**Effort**: 8-12 hours to implement + ongoing tuning
**Value**: Scales memory beyond hot tier limits, maintains continuity

#### Phase 3: Automate Compression (6-12 Months Out)

Automate routine compression tasks while keeping human oversight for critical decisions:

1. **Automated archival**:
   - thoughts.md entries >30 days, zero recent references → auto-archive to warm tier
   - review.md entries >60 days → auto-compress and archive
   - resolved threads >14 days → auto-archive
   - Generate weekly report of automated actions for review

2. **Semi-automated promotion**:
   - System proposes promotions: "thoughts.md entry referenced 5+ times, propose: promote to memory.md"
   - Human reviews and approves/rejects
   - Track approval rate; if >90%, increase automation

3. **Compression quality monitoring**:
   - Track user corrections ("I already told you X")
   - Alert when continuity breaks detected
   - Rollback: restore from source if compression caused information loss

**Effort**: 12-20 hours to implement robust automation
**Value**: Reduces manual overhead, scales to longer timescales

### Specific Recommendations for Each File

#### **soul.md**
- **Status**: Keep as-is (small, stable, high-value)
- **Target size**: <3K tokens
- **Promotion criteria**: Only promote patterns observed consistently over 4+ weeks and confirmed by multiple interactions
- **Compression**: Never compress—this defines the relationship

#### **memory.md**
- **Current approach**: Append facts as they're confirmed durable
- **Recommended evolution**: Structure as key-value pairs for better compression
  ```
  ## Work
  Employer: Small MSP in Cheshire, CT (started: ~2024)
  Role: Help desk through on-sites (PBXs, Linux servers, typical MSP range)
  Transition: Came out at work after 2 years (using new name/pronouns)
  ```
- **Target size**: <5K tokens (if exceeds, consider splitting: memory-personal.md, memory-work.md)
- **Compression**: Consolidation (remove redundancy, keep facts)

#### **thoughts.md**
- **Current approach**: Working notebook, append freely
- **Challenge**: This will grow unbounded without management
- **Recommended evolution**:
  - Keep recent 7-14 days in hot tier (verbatim)
  - Archive older entries to warm tier (compressed)
  - Regularly promote durable insights to memory.md
- **Target size**: <15K tokens (rolling window)
- **Compression**: Summarization (preserve trajectory and open questions)

#### **review.md**
- **Current approach**: Timestamped interaction reviews
- **Challenge**: Accumulates detailed history, high compression potential
- **Recommended evolution**:
  - Keep recent 2-3 entries in hot tier (past 30 days)
  - Compress and archive older entries to warm tier
  - Extract recurring patterns/insights into memory.md
- **Target size**: <10K tokens (rolling window)
- **Compression**: Aggressive summarization (80-90% reduction possible)

#### **threads.md**
- **Current approach**: Living map of active/emerging/unresolved threads
- **Recommended evolution**:
  - Keep active/emerging threads verbatim
  - Compress dormant threads to 1-line summaries
  - Archive resolved threads to warm tier (with 1-line pointer)
- **Target size**: <3K tokens
- **Compression**: Distillation for dormant, archival for resolved

#### **checkpoints.md** and **failures.md**
- **Purpose**: Development feedback loops
- **Recommendation**: Treat as specialized logs
  - Keep recent 10 entries in hot tier
  - Archive older entries to cold tier (GitHub, not vector store)
  - Periodically extract patterns into soul.md or CLAUDE.md
- **Target size**: <2K tokens each

### Token Budget Targets

For sustainable long-term operation:

| File | Current Target | With Warm Tier |
|------|---------------|----------------|
| soul.md | 2K tokens | 2K tokens |
| memory.md | 3-5K tokens | 5K tokens (structured) |
| thoughts.md | 15K tokens (rolling) | 10K tokens (7-day window) |
| review.md | 10K tokens (rolling) | 5K tokens (recent only) |
| threads.md | 3K tokens | 3K tokens |
| checkpoints.md | 2K tokens | 1K tokens (recent) |
| failures.md | 1K tokens | 1K tokens (recent) |
| **Total Hot Tier** | **36-38K tokens** | **27-29K tokens** |
| Retrieved Warm | N/A | 5-10K tokens (as needed) |
| **Total Context** | **36-38K tokens** | **32-39K tokens** |

This keeps the system well under 20% of a 200K window, leaving ample room for conversation.

---

## Part 9: Edge Cases and Failure Modes

### Common Failure Modes

**1. Over-compression (Substance-Free Artifacts)**

**Symptom**: Summaries sound good but contain no actionable information
- "Discussed identity questions and system ethics" (what questions? what positions?)
- "Made progress on blog infrastructure" (what changed? what was decided?)

**Cause**: Optimizing for brevity over utility

**Prevention**:
- Re-engagement test: Could you continue this thread from the summary?
- Specificity check: Does the summary include 2-3 specific facts/decisions?
- Apply to failures.md: Log when summaries prove insufficient

**2. Premature Crystallization**

**Symptom**: Early observations get promoted to memory/soul too quickly, then become rigid
- Single data point → "Cassie prefers X" → system overfits to that preference

**Cause**: Rushing promotion without confirming durability

**Prevention**:
- Multi-session confirmation rule: Require 3+ confirmations before promoting to memory.md
- 4+ week observation period before promoting to soul.md
- Explicitly mark tentative observations: "Working hypothesis: [X]. Confirm over time."

**3. Lost in the Middle**

**Symptom**: Information buried in long context gets ignored despite being present
- [Research shows](https://direct.mit.edu/tacl/article/doi/10.1162/tacl_a_00638/119630/Lost-in-the-Middle-How-Language-Models-Use-Long) 30%+ performance degradation when relevant info is in middle of context

**Cause**: Attention mechanisms prioritize beginning and end of context

**Prevention**:
- Position critical information at start of hot tier (soul.md, recent threads)
- Use retrieval to pull specific content directly into response flow (not buried in long history)
- Repeat key context before asking complex questions

**4. Summary Drift**

**Symptom**: Summaries of summaries progressively lose fidelity
- Original: "Cassie is processing visibility anxiety at work but feels relief at authenticity"
- 1st summary: "Cassie came out at work, mixed feelings"
- 2nd summary: "Work transition complete"
- 3rd summary: [omitted entirely]

**Cause**: Recursive compression without anchoring to source

**Prevention**:
- Never summarize a summary (single-hop rule)
- Regenerate from source rather than editing existing summaries
- Maintain pointers to original for 90 days

**5. Privacy Leakage**

**Symptom**: Summarization abstracts but still identifies
- "User discussed personal medical history" → still signals private content
- "Relationship concerns with [anonymized]" → pattern reveals privacy-sensitive topic

**Cause**: Incomplete abstraction or inappropriate sharing tier

**Prevention**:
- Review summarized content: would this reveal private info to external reader?
- When in doubt, mark private (don't summarize for potential sharing)
- Apply thread privacy check before any public artifact creation

**6. Emotional Flattening**

**Symptom**: Compression removes emotional weight, conversation feels sterile
- Original: "Morning hit hard: realized Cassie doesn't have a lot of local friends for wedding stuff"
- Compressed: "Identified limited local wedding support network"

**Cause**: Optimizing for factual density over relational continuity

**Prevention**:
- Preserve 1-2 phrases that convey emotional weight
- Better: "Morning hit hard—limited local friends for wedding support. Plan: family as bridesmaids, Discord for dress shopping."
- Tone preservation test: Does this still feel like the same conversation?

**7. Contradiction Accumulation**

**Symptom**: Memory contains contradictory information due to updates not propagating
- memory.md: "Cassie avoids meeting local trans community"
- thoughts.md: "Cassie notes she doesn't feel that avoidance anymore"
- Result: System holds both as true, causes contradictory behavior

**Cause**: Update propagation failure across memory tiers

**Prevention**:
- Explicit contradiction resolution: Search for existing entries before adding new ones
- Version negations: "Previously: [X]. Now: [Y]. Changed: [date]."
- Regular audit: Cross-check memory.md against recent thoughts.md for contradictions

### Recovery Strategies

**When continuity breaks** (user says "you forgot X"):

1. **Immediate**:
   - Acknowledge: "You're right, I should have remembered X. Let me reload that context."
   - Retrieve from warm tier if archived
   - Add back to hot tier if it's being referenced repeatedly

2. **Root cause analysis**:
   - Was it compressed away? (compression too aggressive)
   - Was it never promoted? (promotion criteria too strict)
   - Was it demoted inappropriately? (reference tracking failed)
   - Was it in middle of context and ignored? (lost in the middle problem)

3. **Systemic fix**:
   - Adjust compression criteria if needed
   - Add to hot tier if it's high-value context
   - Log to failures.md with failure type

**When compression quality degrades**:

1. **Detection**: Monitor user corrections, continuity breaks, contradictions
2. **Diagnosis**: Review recent compressions, identify patterns in failures
3. **Rollback**: Restore from source if compressed version is causing issues
4. **Adjustment**: Reduce compression ratio for that content type

**When token budget exceeds limits**:

1. **Emergency triage**:
   - Identify lowest-reference-frequency content in hot tier
   - Immediate archival to warm tier
   - Process continues with reduced context

2. **Strategic review**:
   - Why did growth exceed projections?
   - Which files are growing fastest?
   - Adjust compression cadence to prevent recurrence

---

## Conclusion and Key Takeaways

### Core Principles

1. **Focused context beats large context**: Rather than maximizing window size, optimize for high-signal information density.

2. **Compression is not summarization**: Different content types require different approaches (consolidation, summarization, distillation). Match technique to content and future use.

3. **Continuity over completeness**: Preserve what enables coherent re-engagement, not exhaustive history.

4. **Emotional weight has informational value**: Systems that ignore emotional context in pursuit of factual density break relationship continuity.

5. **Automation serves judgment, doesn't replace it**: Automate monitoring and routine tasks; require human review for identity-defining and privacy-sensitive decisions.

### Decision Framework Summary

**Keep (Hot Tier)**:
- Core identity and relationship boundaries
- Active threads and recent context
- Frequently referenced facts
- Open questions not yet resolved

**Compress (Warm Tier)**:
- Dormant but potentially referenceable threads
- Historical context that might resurface
- Detailed discussions where outcome matters but debate doesn't
- Completed projects with potential future relevance

**Discard (Cold or Delete)**:
- Time-bound expired information
- Superseded facts/decisions
- Never-referenced transient details
- Redundant information captured elsewhere

### Implementation Priorities

**Immediate (Week 1)**:
- Add token monitoring to session boot
- Track file growth rates
- Identify compression candidates

**Short-term (Months 1-3)**:
- Implement routine compression for thoughts.md and review.md
- Establish promotion criteria and confirmation thresholds
- Begin archiving resolved threads

**Medium-term (Months 3-6)**:
- Add vector database for warm tier
- Implement retrieval triggers for archived content
- Test retrieval quality and tune

**Long-term (Months 6-12)**:
- Automate routine archival and compression
- Implement continuity monitoring
- Optimize token budget allocation based on actual usage patterns

### Success Metrics

**Quantitative**:
- Hot tier stays below 20% of context window
- Retrieval hit rate >70%
- Compression ratios: 60-80% for most content, 0-20% for relational content
- User corrections <1 per 10 interactions

**Qualitative**:
- User doesn't need to repeat information
- Thread resumption feels natural
- Tone and relationship boundaries remain consistent
- Agent can reference historical context when relevant

**Ultimate measure**: Does the conversation feel continuous across weeks and months, or does it feel like starting over each session?

---

## Sources

### Long-Context LLMs and Context Management

- [Context Window Scaling: Does 200K Tokens Help?](https://dasroot.net/posts/2026/02/context-window-scaling-200k-tokens-help/)
- [Context Window Management: Strategies for Long-Context AI Agents and Chatbots](https://www.getmaxim.ai/articles/context-window-management-strategies-for-long-context-ai-agents-and-chatbots/)
- [LLM Context Window Comparison (2026): Every Model, Priced and Benchmarked](https://www.morphllm.com/llm-context-window-comparison)
- [Best LLMs for Extended Context Windows in 2026](https://aimultiple.com/ai-context-window)
- [Context Window Optimization: Techniques, Benchmarks, and Costs](https://www.statsig.com/perspectives/context-window-optimization-techniques)

### RAG Architecture and Memory Management

- [Retrieval-Augmented Generation (RAG) | Business & Information Systems Engineering](https://link.springer.com/article/10.1007/s12599-025-00945-3)
- [RAG in 2026: Bridging Knowledge and Generative AI](https://squirro.com/squirro-blog/state-of-rag-genai)
- [Retrieval-Augmented Generation: A Comprehensive Survey of Architectures, Enhancements, and Robustness Frontiers](https://arxiv.org/html/2506.00054v1)
- [A Memory-Efficient Retrieval Architecture for RAG-Enabled Systems](https://arxiv.org/pdf/2510.27107)
- [From RAG to Context - A 2025 year-end review of RAG](https://ragflow.io/blog/rag-review-2025-from-rag-to-context)

### AI Agent Memory Systems

- [What Is AI Agent Memory? | IBM](https://www.ibm.com/think/topics/ai-agent-memory)
- [Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory](https://arxiv.org/pdf/2504.19413)
- [How to Build AI Agents with Redis Memory Management](https://redis.io/blog/build-smarter-ai-agents-manage-short-term-and-long-term-memory-with-redis/)
- [Memory OS of AI Agent](https://arxiv.org/abs/2506.06326)
- [What Is Agent Memory? A Guide to Enhancing AI Learning and Recall | MongoDB](https://www.mongodb.com/resources/basics/artificial-intelligence/agent-memory)
- [Hierarchical Memory and Adaptive State Management for an AI Agent](https://thejackluo8.medium.com/hierarchical-memory-and-adaptive-state-management-for-an-ai-agent-f99a50562837)
- [Building smarter AI agents: AgentCore long-term memory deep dive](https://aws.amazon.com/blogs/machine-learning/building-smarter-ai-agents-agentcore-long-term-memory-deep-dive/)

### Prompt Compression and Context Distillation

- [Prompt Compression in Large Language Models (LLMs): Making Every Token Count](https://medium.com/@sahin.samia/prompt-compression-in-large-language-models-llms-making-every-token-count-078a2d1c7e03)
- [LLMLingua: Effectively Deliver Information to LLMs via Prompt Compression](https://llmlingua.com)
- [LLMLingua-2: Data Distillation for Efficient and Faithful Task-Agnostic Prompt Compression](https://llmlingua.com/llmlingua2.html)
- [Consolidation vs. Summarization vs. Distillation in LLM Context Compression](https://medium.com/@RLavigne42/consolidation-vs-summarization-vs-distillation-in-llm-context-compression-c96fa5956057)
- [Prompt Compression: A Guide With Python Examples | DataCamp](https://www.datacamp.com/tutorial/prompt-compression)

### Lost in the Middle Problem

- [Lost in the Middle: How Language Models Use Long Contexts (Stanford/MIT)](https://arxiv.org/abs/2307.03172)
- [Lost in the Middle: How Language Models Use Long Contexts (MIT Press)](https://direct.mit.edu/tacl/article/doi/10.1162/tacl_a_00638/119630/Lost-in-the-Middle-How-Language-Models-Use-Long)
- [Solving the 'Lost in the Middle' Problem: Advanced RAG Techniques](https://www.getmaxim.ai/articles/solving-the-lost-in-the-middle-problem-advanced-rag-techniques-for-long-context-llms/)
- [Found in the Middle: Calibrating Positional Attention Bias | Snorkel AI](https://snorkel.ai/research-paper/found-in-the-middle-calibrating-positional-attention-bias-improves-long-context-utilization/)

### LangChain and LlamaIndex Production Patterns

- [LlamaIndex vs LangChain: Which One To Choose In 2026? | Contabo](https://contabo.com/blog/llamaindex-vs-langchain-which-one-to-choose-in-2026/)
- [LangChain vs LlamaIndex in 2026: What's Changed and Which to Choose](https://zenvanriel.nl/ai-engineer-blog/langchain-vs-llamaindex-2026-update/)
- [LlamaIndex vs LangChain: Which Framework Is Best for Agentic AI Workflows? - ZenML](https://www.zenml.io/blog/llamaindex-vs-langchain)
- [AI Agent Frameworks Compared (2026): LangChain, CrewAI, AutoGen, MetaGPT, OpenDevin + 6 More](https://arsum.com/blog/posts/ai-agent-frameworks/)

### Summarization Quality Metrics

- [LLM Summarization: Techniques, Metrics, and Top Models](https://www.projectpro.io/article/llm-summarization/1082)
- [A Comparative Study of Quality Evaluation Methods for Text Summarization](https://arxiv.org/html/2407.00747v1)
- [LLM Summarization Metrics](https://www.holisticai.com/blog/llm-summarization-metrics)
- [How to evaluate a summarization task | OpenAI Cookbook](https://developers.openai.com/cookbook/examples/evaluation/how_to_eval_abstractive_summarization/)

### Token Budget Optimization

- [LLM Token Optimization: Cut Costs & Latency in 2026](https://redis.io/blog/llm-token-optimization-speed-up-apps/)
- [Mastering AI Token Cost Optimization: Strategies to Optimize Costs](https://10clouds.com/blog/a-i/mastering-ai-token-optimization-proven-strategies-to-cut-ai-cost/)
- [LLM Cost Optimization: Stop Token Spend Waste with Smart Routing](https://www.kosmoy.com/post/llm-cost-management-stop-burning-money-on-tokens)
- [Token Compression: How to Slash Your LLM Costs by 80%](https://medium.com/@yashpaddalwar/token-compression-how-to-slash-your-llm-costs-by-80-without-sacrificing-quality-bfd79daf7c7c)

### Memory Compression and Archival

- [Layers of Memory, Layers of Compression - Tim Kellogg](https://timkellogg.me/blog/2025/06/15/compression)
- [Memory in LLM-based Multi-agent Systems: Mechanisms, Challenges, and Collective](https://www.techrxiv.org/users/1007269/articles/1367390/master/file/data/LLM_MAS_Memory_Survey_preprint_/LLM_MAS_Memory_Survey_preprint_.pdf?inline=true)

### Recursive and Infinite Context

- [Breaking the Context Window: How Recursive Language Models Handle Infinite Input](https://www.getmaxim.ai/blog/breaking-the-context-window-how-recursive-language-models-handle-infinite-input/)
- [MIT's new 'recursive' framework lets LLMs process 10 million tokens | VentureBeat](https://venturebeat.com/orchestration/mits-new-recursive-framework-lets-llms-process-10-million-tokens-without)
- [Recursive Language Models: Infinite Context that works](https://medium.com/@pietrobolcato/recursive-language-models-infinite-context-that-works-174da45412ab)
- [Cutting Through the Noise: Smarter Context Management for LLM-Powered Agents](https://blog.jetbrains.com/research/2025/12/efficient-context-management/)

### Conversation Continuity and Session Boundaries

- [Field-Theoretic Memory for AI Agents: Continuous Dynamics for Context Preservation](https://arxiv.org/html/2602.21220)
- [Context Engineering for Personalization - Long-Term Memory Notes using OpenAI Agents SDK](https://cookbook.openai.com/examples/agents_sdk/context_personalization)
- [Context Engineering - Short-Term Memory Management with Sessions](https://cookbook.openai.com/examples/agents_sdk/session_memory)
- [Memory for Voice Agents: A Guide to AI Memory Architecture](https://mem0.ai/blog/ai-memory-for-voice-agents)
- [AI Agent Memory: Build Stateful AI Systems That Remember](https://redis.io/blog/ai-agent-memory-stateful-systems/)

### Semantic Compression and Vector Embeddings

- [Understanding Semantic Search: Vector Embeddings and Similarity Search](https://medium.com/@derrickryangiggs/understanding-semantic-search-vector-embeddings-and-similarity-search-422bcb4a495b)
- [Vector Embeddings: Semantic Search & LLM Integration Guide](https://keymakr.com/blog/vector-embeddings-explained-semantic-search-llm-integration-guide/)
- [Optimization of Latent-Space Compression using Game-Theoretic Techniques](https://arxiv.org/html/2508.18877)

### Emotional Context Preservation

- [Titans + MIRAS: Helping AI have long-term memory](https://research.google/blog/titans-miras-helping-ai-have-long-term-memory/)
- [MemGPT: Engineering Semantic Memory through Adaptive Retention and Context Summarization](https://informationmatters.org/2025/10/memgpt-engineering-semantic-memory-through-adaptive-retention-and-context-summarization/)
- [Memory Optimization Strategies in AI Agents](https://medium.com/@nirdiamant21/memory-optimization-strategies-in-ai-agents-1f75f8180d54)
- [In Prospect and Retrospect: Reflective Memory](https://arxiv.org/pdf/2503.08026)

### Context Utilization Efficiency

- [7 Key LLM Metrics to Enhance AI Reliability | Galileo](https://galileo.ai/blog/llm-performance-metrics)
- [Context Window: What It Is and Why It Matters for AI Agents](https://www.comet.com/site/blog/context-window/)
- [Understanding LLM Context Windows: Tokens, Attention, and Challenges](https://medium.com/@tahirbalarabe2/understanding-llm-context-windows-tokens-attention-and-challenges-c98e140f174d)

---

**Research completed**: March 3, 2026
**Document length**: ~22,000 tokens
**Synthesis**: Operational frameworks from 40+ sources across academic research, production systems, and industry best practices
