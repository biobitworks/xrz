"""XRZ agent-turn MMR reference (test only; not signing or external attestation)."""
from __future__ import annotations
import hashlib
import json
import unicodedata
from typing import Any

LEAF_DOMAIN = b"XRZ/MMR/v1/leaf\x00"
NODE_DOMAIN = b"XRZ/MMR/v1/node\x00"
ROOT_DOMAIN = b"XRZ/MMR/v1/root\x00"
_MAX_INT = 2**53 - 1

def _check(value: Any) -> None:
    if value is None or isinstance(value, bool):
        return
    if isinstance(value, int):
        if not -_MAX_INT <= value <= _MAX_INT:
            raise ValueError("out-of-range integer")
        return
    if isinstance(value, str):
        if unicodedata.normalize("NFC", value) != value:
            raise ValueError("non-NFC unicode")
        return
    if isinstance(value, list):
        for item in value:
            _check(item)
        return
    if isinstance(value, dict):
        for key, item in value.items():
            if not isinstance(key, str):
                raise TypeError("JSON object keys must be strings")
            _check(key)
            _check(item)
        return
    raise TypeError("unsupported canonical type; floats forbidden")

def canonical_bytes(value: Any) -> bytes:
    """xrz-json-v1; UTF-8/NFC, sorted compact JSON, no floats. NOT RFC8785."""
    _check(value)
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")

def leaf_hash(value: dict) -> str:
    payload = canonical_bytes(value)
    return hashlib.sha256(LEAF_DOMAIN + len(payload).to_bytes(8, "big") + payload).hexdigest()

def _node(h: int, left: str, right: str) -> str:
    return hashlib.sha256(NODE_DOMAIN + h.to_bytes(2, "big") + bytes.fromhex(left) + bytes.fromhex(right)).hexdigest()

def _encode_parent(parent_checkpoint: str | None) -> bytes:
    if parent_checkpoint is None:
        return b"\x00"
    if not isinstance(parent_checkpoint, str) or len(parent_checkpoint) != 64:
        raise ValueError("parent checkpoint must be 64 hex chars")
    return b"\x01" + bytes.fromhex(parent_checkpoint)

def _root(count: int, peaks: list[dict], parent_checkpoint: str | None) -> str:
    packed = (_encode_parent(parent_checkpoint) + count.to_bytes(8, "big") +
              len(peaks).to_bytes(2, "big") +
              b"".join(p["height"].to_bytes(2, "big") + bytes.fromhex(p["hash"]) for p in peaks))
    return hashlib.sha256(ROOT_DOMAIN + packed).hexdigest()

def construct_turn_checkpoint(events: list[dict], parent_checkpoint: str | None = None) -> dict:
    if not events:
        raise ValueError("empty checkpoint cannot be committed")
    seen = set()
    for i, event in enumerate(events):
        if not isinstance(event, dict):
            raise ValueError("event object required")
        for field in ("schema", "event_id", "actor", "turn_id", "repo", "task_ref",
                      "sequence", "status", "input_occurrences", "output_occurrences", "evidence_refs"):
            if field not in event:
                raise ValueError("missing " + field)
        if event["schema"] != "xrz.agent_turn.v1":
            raise ValueError("unexpected schema")
        if event["sequence"] != i:
            raise ValueError("unordered sequence")
        if event["event_id"] in seen:
            raise ValueError("duplicate event identity")
        seen.add(event["event_id"])
    leaves = [leaf_hash(x) for x in events]
    peaks = []
    for digest in leaves:
        new_peak = {"height": 0, "hash": digest}
        while peaks and peaks[-1]["height"] == new_peak["height"]:
            left = peaks.pop()
            new_peak = {"height": new_peak["height"] + 1,
                        "hash": _node(new_peak["height"] + 1, left["hash"], new_peak["hash"])}
        peaks.append(new_peak)
    return {"schema": "xrz.agent_turn_mmr_checkpoint.v1",
            "algorithm": "xrz-domain-separated-mmr-v1",
            "canonicalization": "xrz-json-v1",
            "event_count": len(events),
            "ordered_leaf_hashes": leaves,
            "peaks": peaks,
            "root": _root(len(leaves), peaks, parent_checkpoint),
            "parent_checkpoint": parent_checkpoint,
            "signature_state": "NOT_SIGNED",
            "state": "COMPUTED_NOT_EXTERNAL_ATTESTED",
            "verification": "NOT_TESTED"}

def reference_verify(events: list[dict], receipt: dict) -> bool:
    """Second, recursively constructed verification path on one local host."""
    try:
        if receipt["algorithm"] != "xrz-domain-separated-mmr-v1" or receipt["event_count"] != len(events):
            return False
        if receipt["canonicalization"] != "xrz-json-v1":
            return False
        if [e["sequence"] for e in events] != list(range(len(events))):
            return False
        ids = [e["event_id"] for e in events]
        if len(set(ids)) != len(ids):
            return False
        hashes = [leaf_hash(e) for e in events]
        if hashes != receipt["ordered_leaf_hashes"]:
            return False
        def subtree(start: int, length: int):
            if length == 1:
                return (0, hashes[start])
            half = length // 2
            lh, ld = subtree(start, half)
            rh, rd = subtree(start + half, half)
            assert lh == rh
            h = lh + 1
            return (h, hashlib.sha256(NODE_DOMAIN + h.to_bytes(2, "big") + bytes.fromhex(ld) + bytes.fromhex(rd)).hexdigest())
        peaks = []
        index = 0
        while index < len(hashes):
            length = 1 << ((len(hashes) - index).bit_length() - 1)
            height, digest = subtree(index, length)
            peaks.append({"height": height, "hash": digest})
            index += length
        if peaks != receipt["peaks"]:
            return False
        parent = receipt.get("parent_checkpoint")
        if parent is None:
            packed = b"\x00"
        else:
            if not isinstance(parent, str) or len(parent) != 64:
                return False
            packed = b"\x01" + bytes.fromhex(parent)
        packed += len(hashes).to_bytes(8, "big") + len(peaks).to_bytes(2, "big")
        for p in peaks:
            packed += p["height"].to_bytes(2, "big") + bytes.fromhex(p["hash"])
        return hashlib.sha256(ROOT_DOMAIN + packed).hexdigest() == receipt["root"]
    except (KeyError, TypeError, ValueError, OverflowError, AssertionError):
        return False
