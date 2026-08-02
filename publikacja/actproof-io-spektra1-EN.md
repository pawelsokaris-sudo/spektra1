# SPEKTRA-1 — A preregistered prediction, and why it was wrong

**Status:** completed · **Verdict:** hypothesis not confirmed; opposite effect
observed and technically robust; unstable across language replicas.
**Data, code and full history:** https://github.com/pawelsokaris-sudo/spektra1

## The question

Does a conversation that talks about *itself* leave a different geometric trace
inside a language model than an identically built conversation about something
external?

We measured the correlation spectrum of hidden-layer activations in Gemma 3 4B.
From one shared sentence base we built five variants of the same dialogue,
differing **only in the content of five inserted sentences** — same positions,
same syntax, token lengths matched to within a fraction of a percent.

The analysis rules were frozen and cryptographically sealed **before any
activation was read**: hypothesis hierarchy, significance level, permutation
scheme, endpoint definition and gate criteria.

## The prediction

Self-reference would produce a **stronger** collective signature — a higher
share of variance concentrated in dominant correlation modes.

## What we found

**The opposite, consistently.**

| Replica | Effect (C − C′-G) | Standardised | Scenarios in the same direction |
|---|---:|---:|---|
| English | −0.0058 | −2.65 | **24 / 24** |
| Polish | −0.0036 | −1.49 | **23 / 24** |

The self-referential variant produced the **lowest** integration index of all
five variants, in both languages. Small in absolute terms — about half a percent
of the index — but almost perfectly consistent across independently authored
scenarios.

## Robustness

- **Numeric precision** — recomputed in fp32: effect changed by 3.1% and 3.5%
  (threshold 25%). Per-text tolerance: largest deviation 0.00066 against a
  0.005 limit, zero breaches across 48 texts.
- **Positional component** — removed: effect changed by 7.9% and 8.8%.
- **Language replicas** — same sign, but magnitudes differ by 37.2% against a
  25% threshold. **This criterion fails.** The result is therefore classified
  as *unstable across replicas* and published as such, exactly as the protocol
  requires.

## What we do not claim

We do **not** claim a discovery. The reverse direction was not preregistered,
so the observation is descriptive and becomes a candidate hypothesis for a
follow-up study — not a confirmed finding. Nothing here measures consciousness
or experience; the protocol explicitly forbids that language.

## Limitations, stated plainly

- **No independent timestamp predating the measurement.** The original public
  repository — the only third-party witness — was deleted while removing a
  third party's personal data. Every remaining date is self-attested.
- **Semantic-field confound not eliminated.** Self-referential insertions draw
  on computational vocabulary, external ones on concrete domain nouns. The
  effect may track abstract-versus-concrete rather than self-reference.
- **One model, one scenario family, two languages.** Generalisation is minimal.
- **No container image**, though the protocol promised one.
- Protocol, code, statistics and most reviews passed through language models,
  and one contributor is a system of the class under study. Declared, not hidden.

## Why publish a failed prediction

Because it is the only kind of result that cannot be manufactured afterwards.
The seal exists precisely so that a wrong mapping of a concept onto a measure
surfaces instead of quietly disappearing into the interpretation. It surfaced.
