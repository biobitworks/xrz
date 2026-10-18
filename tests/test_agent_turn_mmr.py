import unittest
from custody.agent_turn_mmr import canonical_bytes, construct_turn_checkpoint, reference_verify

def fixture(n=5):
    return [{"schema": "xrz.agent_turn.v1", "event_id": "fixture-" + str(i),
             "actor": "SYNTHETIC_COPILOT", "turn_id": "fixture-turn", "repo": "biobitworks/xrz",
             "task_ref": "local-synthetic-test", "sequence": i, "status": "SYNTHETIC",
             "input_occurrences": [], "output_occurrences": [], "evidence_refs": []}
            for i in range(n)]

class TestAgentTurnMMR(unittest.TestCase):
    def test_repeatable(self):
        e = fixture()
        self.assertEqual(construct_turn_checkpoint(e), construct_turn_checkpoint(e))

    def test_reference_oracle(self):
        for n in range(1, 23):
            e = fixture(n)
            self.assertTrue(reference_verify(e, construct_turn_checkpoint(e)), n)

    def test_mutation(self):
        e = fixture()
        receipt = construct_turn_checkpoint(e)
        e[1]["status"] = "TAMPERED"
        self.assertFalse(reference_verify(e, receipt))

    def test_reordering(self):
        e = fixture()
        receipt = construct_turn_checkpoint(e)
        e[1], e[2] = e[2], e[1]
        self.assertFalse(reference_verify(e, receipt))

    def test_truncation(self):
        e = fixture()
        self.assertFalse(reference_verify(e[:-1], construct_turn_checkpoint(e)))

    def test_appending(self):
        e = fixture()
        self.assertFalse(reference_verify(e + fixture(1), construct_turn_checkpoint(e)))

    def test_duplicate_event_rejected(self):
        e = fixture()
        e[1]["event_id"] = e[0]["event_id"]
        with self.assertRaises(ValueError):
            construct_turn_checkpoint(e)

    def test_unicode_normalization_rejected(self):
        with self.assertRaises(ValueError):
            canonical_bytes({"x": "e\u0301"})

    def test_float_rejected(self):
        with self.assertRaises(TypeError):
            canonical_bytes({"latency": 0.0001})

    def test_frozen_parent(self):
        e = fixture()
        a = construct_turn_checkpoint(e, parent_checkpoint="ab"*32)
        b = construct_turn_checkpoint(e, parent_checkpoint="cd"*32)
        self.assertNotEqual(a["root"], b["root"])
        self.assertTrue(reference_verify(e, a))
        self.assertTrue(reference_verify(e, b))
        self.assertFalse(reference_verify(e, dict(a, parent_checkpoint="cd"*32)))

    def test_empty_rejected(self):
        with self.assertRaises(ValueError):
            construct_turn_checkpoint([])

    def test_signature_not_claimed(self):
        self.assertEqual(construct_turn_checkpoint(fixture())["signature_state"], "NOT_SIGNED")

    def test_root_tamper(self):
        e = fixture()
        r = construct_turn_checkpoint(e)
        r["root"] = "0"*64
        self.assertFalse(reference_verify(e, r))

    def test_known_synthetic_copilot_vector(self):
        e = []
        for i, kind in enumerate(["synthetic_instructions_read","synthetic_code_proposal","synthetic_test_failure"]):
            e.append({"schema":"xrz.agent_turn.v1","event_id":"SYNTHETIC-"+str(i),
                "actor":"SYNTHETIC_COPILOT","turn_id":"synthetic-turn-001",
                "repo":"biobitworks/xrz","task_ref":"synthetic-local-fixture",
                "sequence":i,"status":"SYNTHETIC",
                "input_occurrences":["source-occurrence-0"],
                "output_occurrences":["fixture-occurrence-"+str(i)],
                "evidence_refs":["synthetic:"+kind]})
        r = construct_turn_checkpoint(e, parent_checkpoint="ab"*32)
        self.assertEqual(r["root"], "0fc4c6332e1c1831036193a6d66b235e7b2fc5893908dd49c880a32fb234166c")
        self.assertEqual([p["height"] for p in r["peaks"]], [1,0])
        self.assertTrue(reference_verify(e, r))


    def test_fake_signed_or_committed_claim_rejected(self):
        e = fixture()
        receipt = construct_turn_checkpoint(e)
        for key, false_claim in (("signature_state", "SIGNED_VERIFIED"), ("state", "MMR_COMMITTED"), ("verification", "PASSED")):
            mutated = dict(receipt, **{key: false_claim})
            self.assertFalse(reference_verify(e, mutated), key)

    def test_json_schema_enforced_on_constructor_and_verifier(self):
        for field, bad in (("actor", "INVALID"), ("status", "INVALID"), ("input_occurrences", "STRING")):
            events = fixture()
            receipt = construct_turn_checkpoint(events)
            events[0][field] = bad
            with self.assertRaises(ValueError):
                construct_turn_checkpoint(events)
            self.assertFalse(reference_verify(events, receipt))
        events = fixture()
        events[0]["unknown_field"] = "not permitted"
        with self.assertRaises(ValueError):
            construct_turn_checkpoint(events)

    def test_hex_parent_validation(self):
        events = fixture()
        for malformed in (" " * 64, "Z" * 64, "abcd", "ab" * 31):
            with self.assertRaises(ValueError):
                construct_turn_checkpoint(events, malformed)
        receipt = construct_turn_checkpoint(events, "ab" * 32)
        self.assertFalse(reference_verify(events, dict(receipt, parent_checkpoint=" " * 64)))

    def test_empty_forged_receipt_rejected(self):
        import hashlib
        events = fixture(1)
        receipt = construct_turn_checkpoint(events)
        empty_root = hashlib.sha256(b"XRZ/MMR/v1/root\x00" + b"\x00" + bytes(8) + bytes(2)).hexdigest()
        forged = dict(receipt, event_count=0, ordered_leaf_hashes=[], peaks=[], root=empty_root)
        self.assertFalse(reference_verify([], forged))

    def test_actual_new_event_appended_after_receipt_rejected(self):
        events = fixture()
        receipt = construct_turn_checkpoint(events)
        new_event = fixture(1)[0].copy()
        new_event["event_id"] = "new-after-checkpoint"
        new_event["sequence"] = len(events)
        self.assertFalse(reference_verify(events + [new_event], receipt))

if __name__ == "__main__":
    unittest.main()
