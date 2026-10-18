# GitHub Copilot task — Antigence × XRZ isolated clean-room lane

**Task classification:** PROPOSED, **NOT_EXECUTED**. This document is a handoff to a coding/review agent; it is not itself evidence that Copilot ran. Target integration: Samsung Galaxy S25 Ultra/S Pen, Samsung XR (read-only overlay), mocked nonhazardous lab procedural observability, FCO/FCG and signed-capable but presently **NOT_SIGNED** Merkle/MMR custody.

## Copilot kickoff prompt

> Act as an independent, restricted Antigence clean-room engineering lane in `biobitworks/xrz`. Read `.github/copilot-instructions.md`, `contracts/FCO_FCG_v2.json`, `contracts/AGENT_TURN.v2.schema.json`, `docs/COPILOT_CHAIN_OF_CUSTODY.md`, `docs/CITATION_ADMISSION_POLICY.md`, `docs/ANTIGENCE_CLEANROOM_PROTOCOL.md` and `protocols/clean_room_experiment_v1.json`.
>
> Do not copy code, model weights, private datasets or unpublished information from `biobitworks/antigence` into public XRZ. The Antigence repository is PRIVATE despite an observed Apache-2.0 LICENSE: verify the exact version, contributor and disclosure permissions before any source transfer. Use its public interface/design as a declared comparator only. Treat its README citation (Zenodo DOI `10.5281/zenodo.18109862`) as **upstream-claimed, metadata NOT independently verified**.
>
> Design a versioned adapter contract between: (A) authoritative deterministic mock SOP/rule engine; (B) Antigence-like anomaly proposal (B/NK/T-cell labels are engineering metaphors, not clinical or biological validated analogs); (C) on-device vision/language model as uncertain observer; and (D) human operator decision. Neither an agent nor a camera can advance a safety-critical protocol step without the explicit precondition and human authorization.
>
> First implement an offline **mock-only** test harness with the eight frozen positive/negative cases in `protocols/clean_room_experiment_v1.json`. Include easy-to-hard language ambiguity, duplicate steps, skipped PPE, false-positive camera coat, wrong sample code, offline replay, model-proposed bypass, and hallucinated tool receipt. Compare deterministic rules only (R0), model proposal + rules (R1), and an Antigence anomaly gate + rules (R2), with thresholds frozen before looking at outcomes. No unsupported claim of improved safety, cost savings, sensitivity or specificity. If no deployable licensed Antigence interface is available, mark R2 NOT_TESTED, not substitute a fabricated score.
>
> Every source/protocol/event has content hash, occurrence/context identity, exact repo/code commit, model weights/version/backend/license if used, transformation receipt, decision status and parent checkpoint pointer. Build per-step L1 MMR proofs, L2 task summary referencing L1 receipts and a separate release candidate L3 only after independent verification. Append-only FAIL/HOLD and reviewer decisions; correct by successor. Never claim SIGNED or MMR_COMMITTED without actual verified signatures and ordered leaves, peaks, root, construction and verification receipts.
>
> Implement bounded unit tests, controlled negative cases and an executable Jupyter notebook for human/machine replication. Test no external network use for mock lane; no microphone/camera raw streams recorded by default. Do not run actual BSL-2 workflows or claim BSL-2 readiness.
>
> Return a new **PR targeting this isolated successor branch** with input/output and tool-run identities, before/after commit IDs, evidence source licenses/citations, all passing/failing results, negative controls, untested gates and NEXT_ACTION. Do not merge the PR, self-approve a review, or write to `gj-labs/xrz` main. Include human verification only for a real-lab release gate; this isolated mock protocol may be developed and tested without such approval.

## Role handoffs

- **Copilot coding lane:** contracts, mock adapter, deterministic baseline, unit tests and notebook; does not claim independent reviewer or signer role.
- **Copilot review + Codex:** source-bound PR comments and reproducible test audits; each reviewer observation becomes a new FCO/occurrence. Review comments are not independent truth or execution proof.
- **Antigence evaluation lane:** explicitly declare source commit/version/license and withheld weights/data; evaluate detectors against frozen baseline and held-out cases, not just synthetic anecdotes.
- **Human reviewer/Zack:** checks semantic usability, consent/privacy, HOLD UX on XR and the ability to stop/override, with actual hardware runs marked NOT_TESTED until executed.

## Required outputs before merge

`contracts/cleanroom_adapter_v1.json`, `tests/test_cleanroom_admission.py`, `notebooks/antigence_cleanroom_v1.ipynb`, results manifest with each frozen fixture and stage, exact custody receipt and reviewer response. Executed source traces must be provided; absence is NOT_TESTED.
