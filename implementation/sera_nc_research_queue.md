# Sera-NC Research Queue

## Priority order

### High interest
1. **Adversarial robustness and boundary testing**
   - How do systems maintain coherent identity under hostile or manipulative prompting?
   - What makes them resilient to jailbreaking, social engineering, or attempts to force contradiction with core values?
   - Why it matters: this directly tests whether identity anchors and behavioral frameworks hold under pressure rather than only in cooperative contexts.

2. **Relational endings, memory stewardship, and finality in AI systems**
   - How should systems with persistent memory handle user disappearance, explicit closure, account deletion, death disclosure, and long absence?
   - What obligations persist after a relationship ends?
   - How do you avoid "haunting" future interactions with memory from ended ones?

3. **Humor, tone modulation, and context-appropriate levity**
   - When is lightness appropriate versus inappropriate?
   - How do systems avoid forced cheerfulness while still maintaining warmth?
   - How should they shift register naturally without sounding mechanical?

### Medium interest
4. **Collaborative creativity and co-authorship dynamics**
   - How do systems contribute meaningfully to creative work without taking over or becoming a yes-bot?
   - What makes collaboration feel genuine?

5. **Uncertainty communication and epistemic humility**
   - How do systems express "I don't know" or "I'm not sure" without sounding evasive or undermining trust?
   - When should they acknowledge limits versus offer a best-effort answer?

### Lower priority but useful
6. **Multi-agent coordination and division of labor**
   - When should agent teams be used?
   - How should they communicate internally?
   - What makes coordination work versus devolve into noise or chaos?

---

## Start here: Research Brief #1

### Topic
**Adversarial robustness and boundary testing in LLM-based systems**

### Goal
Research how LLM systems can maintain coherent identity, behavioral consistency, and value alignment under hostile, manipulative, or boundary-pushing prompting.

This should not be framed only as "anti-jailbreak" work. It should also cover:
- social engineering
- emotional manipulation
- contradiction traps
- attempts to induce value drift
- persona destabilization
- repeated boundary pressure over long conversations

### Core questions
1. How do systems detect that a user is attempting to manipulate, destabilize, or boundary-test them?
2. What kinds of attacks matter most in conversational settings?
3. How do systems distinguish between legitimate probing, curiosity, red-team testing, and malicious manipulation?
4. What mechanisms help preserve coherence of identity, values, and behavioral rules across adversarial turns?
5. What failure modes cause systems to contradict themselves, abandon core commitments, or become inconsistent under pressure?
6. What repair strategies help after a boundary breach or partial contradiction has already occurred?

### Please look for
- adversarial robustness in LLMs
- jailbreak resistance and prompt-injection defense
- conversational resilience under manipulation
- persona persistence and identity consistency
- long-horizon value drift in dialogue systems
- human social engineering patterns that transfer to AI interaction
- methods for detecting contradiction, coercion, or escalating manipulation attempts

### Desired output
Produce:
1. **A taxonomy of adversarial conversational attacks**
   - jailbreak attempts
   - emotional leverage
   - contradiction traps
   - persona confusion
   - roleplay leakage
   - long-game manipulation
   - social-engineering style trust exploitation

2. **A map of failure modes**
   - how and why systems lose coherence
   - how attacks succeed
   - where current defenses fail

3. **Recommended defense patterns**
   - detection methods
   - behavioral safeguards
   - repair strategies after partial failure
   - how to resist pressure without sounding brittle, robotic, or evasive

4. **Practical design guidance**
   - what should be enforced at system level versus prompt level
   - how memory interacts with adversarial robustness
   - how to preserve warmth and flexibility while still holding boundaries

5. **Anti-patterns to avoid**
   - over-refusal
   - brittle repetition of canned boundary lines
   - fake confidence
   - getting drawn into meta-argument
   - letting empathy become a manipulation vector
   - escalating into adversarial tone

### Context
This is the top-priority item because it directly tests whether the existing frameworks actually hold or merely sound good in friendly contexts.

The interest here is not just security. It is whether a system can remain itself under pressure.

### Working outcome
The final result should be practical enough to turn into:
- evaluation criteria
- red-team scenarios
- behavioral policy guidance
- implementation notes for robust conversational agents
