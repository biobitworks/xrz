# Antigence clean-room lane — admission / scope / reviewer contract

## Boundaries and source evidence

This is an **isolated software evaluation and mock-lab procedural safety experiment**, not a certified physical cleanroom, biological safety system, biosafety officer, or live BSL-2 approval. The authoritative step policy is a versioned mock SOP plus competent operator approval. Model inference, visual recognition and Antigence anomalies produce proposals to HOLD/REVIEW, never automatic safety clearance.

Source: **private** [biobitworks/antigence](https://github.com/biobitworks/antigence). README blob `35ab30bcbd2e0cae8bdff435fa669d17fd806e4b` declares negative-selection (NK), B-cell pattern matching, T-cell validators, regulatory calibration, offline operation, MCP integration and optional dashboard; repository LICENSE blob `cc8db5128bc8ac7a738c74c57471dfa6bb701f81` contains Apache-2.0. Actual behavior/performance is **NOT independently benchmarked here**. README supplies a BiobitWorks 2026 software citation and claims Zenodo DOI `10.5281/zenodo.18109862`; bibliographic DOI metadata and redistribution of private contents are **NOT VERIFIED**. No source code or private data copied.

## Distinct custody objects

`SourceFCO` (policy/README/license/model/fixture source), `AtomFCO` (protocol clause, synthetic instrument reading, model observation), `OccurrenceFCO` (time/device/operator/context), `TransformFCO` (code and parameter version), `AgentTurnFCO` (Copilot task/known tool output), `DecisionFCO` (HOLD/REVIEW/ACCEPT only by authorized transition), `ClaimFCO` (limited outcomes) and `ArtifactFCO` (notebook, PR, CI). Typed FCG edges include `DERIVED_FROM`, `CHECKED_BY`, `REVIEWED_BY`, `SUPERSEDES`, `CITES`, `CONTAINS_RECEIPT`. These edges are declarations and not causality or truth.

Every experiment has synthetic fixture input identity, hardcoded expected rule output frozen in advance, actual model output (if executed), optional anomaly verdict, FP/FN and latency when measured, disagreement resolution, release rights and negative test receipt. Unknown signing, provenance and reviewer attributes stay UNKNOWN.

## Fail-closed states

`OBSERVED_PPE_SUGGESTION` may only transition to `PPE_REVIEW_PENDING`. Only `AUTHORIZED_HUMAN_CONFIRMATION` plus verified authorization/policy/fixture context can complete a safety gate. Timeouts, camera uncertainty, conflicting identifiers, model-proposed skip, detached headset, prior-event reorder, late-arriving ACK or missing evidence must HOLD. Override requests become new human decision occurrences, not mutation of prior events.

At the IP gate: no mixing of private Antigence source, unpublished models, event-restricted datasets, raw video or voice recordings into upstream public XRZ without an explicit rights + consent receipt. Preserve enough redacted derived atoms for public reproductions.

## Experiments and acceptance

Freeze R0 deterministic SOP-only, R1 rule + uncertain model proposals, R2 rule + Antigence anomaly gate; run exactly the fixtures in `protocols/clean_room_experiment_v1.json`, with train/eval separation and no cherry-picked case deletion. Pair all traces to the same versioned mock input, estimate change in missed unsafe steps, false holds, time/energy/token usage **only if measured**. Avoid claims of net cost savings absent prospective hardware trials.

Production/certification gates: independent site authority, approved SOP, PPE/equipment decontamination, personnel training, accessibility and emergency stop, data-retention/recording consent, privacy rights, validated camera reliability under deployed conditions. A passing synthetic test does **not** satisfy these gates.

## Independent reviewers and NEXT_ACTION

A GitHub Copilot coding agent may implement this lane and open a PR in the fork; its action must be recovered from actual GitHub receipts, not inferred from files. Codex/Copilot review each contribute separate external reviewer occurrences. A named project maintainer approves incorporating reference code into `gj-labs/xrz`, and a local institutional safety authority—not GitHub reviewers—approves actual regulated lab use.

**NEXT_ACTION:** Copilot implements mock adapter from frozen fixtures, runs notebook, compares R0/R1/R2 only when all implementations are available, saves ordered checkpoint+verifier receipts, requests independent review; otherwise ABSTAIN/NOT_TESTED. Never edit source history to make a gate pass.
