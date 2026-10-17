# Measurement guide

Read this before making any resource comparison, carbon claim or optimisation
statement. Related rules: NR-MEASURE-001 to NR-MEASURE-004, NR-STRAT-005, NR-STRAT-006.

## Before comparing

1. Define the functional unit: one completed search, one rendered page, one
   export. Comparisons without a unit compare different things.
2. State the boundary: client CPU, transferred bytes, server CPU, embodied
   hardware. A gain on one boundary can be a transfer to another.
3. Record the context: hardware or cloud instance, workload profile, date.
   Numbers from another context are not your numbers.
4. Baseline first: measure the current alternative the same way, then the
   candidate, then compare on equal terms.

## What a measurement must carry

- workload and functional unit
- method and tool (with version)
- sample size and variance/uncertainty when relevant
- hardware or cloud context
- the boundary it was measured on

## Honest claims

- A technical gain (fewer bytes, less CPU, fewer tokens) is a technical claim.
  Report it as such, with its measurement.
- An environmental claim (energy, CO2, water) requires its own measurement on
  the stated boundary. Never derive it from a technical proxy, and never copy
  a percentage from a vendor, benchmark or case study.
- Tool scores (EcoIndex, Lighthouse, sonar) are indicators of what they measure,
  not compliance with any referential. Never convert a score into "RGESN/RGAA
  compliant" (NR-MEASURE-002).
- Missing measurement means unknown gains, not zero impact (NR-MEASURE-004).
  Say "unknown" and name the next measurement.

## Direction vs ratio

Fewer resources processed means less computation, and less computation means
less energy: the direction holds qualitatively and is worth acting on. The
quantitative ratio (tokens to watts, requests to grams) depends on caching,
model, batching, hardware and grid mix - each moves the result more than the
count. Measure before putting a number on it (NR-USAGE-016).
