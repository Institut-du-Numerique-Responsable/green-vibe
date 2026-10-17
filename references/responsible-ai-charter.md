# Responsible AI charter

Load this reference only when a charter assessment is requested, or when an AI
task surfaces a concrete risk in these areas. Related rule: NR-AI-009.
This is guidance for feature work, not an organisational certification.

## The basics an AI feature must answer

1. **Data permissions and provenance.** Where does the training/grounding data
   come from, and does the project have the right to use it that way? Personal
   data reaches prompts only under a stated purpose.
2. **Model oversight.** Who can turn it off, correct it, and review its
   outputs? An AI feature has a named owner and a human path for disputes.
3. **Failure behaviour.** What happens on refusal, uncertainty, or a wrong
   answer? Errors are surfaced, not smoothed over; confidence is not invented.
4. **Scope honesty.** The feature says what it does and does not do. It never
   claims to be impartial, certified or compliant from code alone.
5. **Frugality as respect.** The model is sized to the task (NR-AI-002) - an
   oversized model is both a cost defect and an honesty defect about the
   task's real complexity.

## Sobriety and responsibility are not in tension

Efficiency gains never buy back trust. A service that is frugal but unfair,
opaque or unlawful is not responsible; one that is responsible but wasteful is
not finished. The two floors hold together: secure, correct, accessible,
frugal.

## What this charter does not do

- It does not certify an organisation, a supplier or a compliance framework.
- It does not replace the law or the referentials; it makes the daily questions
  visible in code work.
- Code cannot establish data permissions from reading code; it can surface the
  question and refuse to bury it.
