import unittest
from custody.agent_turn_mmr import canonical_bytes, construct_turn_checkpoint, reference_verify

def fixture(n=5):
    return [{"schema": "xrz.agent_turn.v2", "event_kind": "OBSERVATION", "event_id": "fixture-" + str(i),
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
        kinds = ["INSTRUCTION_READ", "CODE_EDIT", "TEST_EXECUTION"]
        labels = ["synthetic_instructions_read", "synthetic_code_proposal", "synthetic_test_failure"]
        for i, (kind, label) in enumerate(zip(kinds, labels)):
            e.append({"schema": "xrz.agent_turn.v2", "event_kind": kind,
                "event_id": "SYNTHETIC-V2-" + str(i),
                "actor": "SYNTHETIC_COPILOT", "turn_id": "synthetic-turn-002",
                "repo": "biobitworks/xrz", "task_ref": "synthetic-local-successor-fixture",
                "sequence": i, "status": "SYNTHETIC",
                "input_occurrences": ["source-occurrence-0"],
                "output_occurrences": ["fixture-v2-occurrence-" + str(i)],
                "evidence_refs": ["synthetic:" + label]})
        parent = "0fc4c6332e1c1831036193a6d66b235e7b2fc5893908dd49c880a32fb234166c"
        r = construct_turn_checkpoint(e, parent_checkpoint=parent)
        self.assertEqual(r["root"], "d459eb5b1c36a67b8637a4897e6201ae5e8dff7ccd47e03434a792b1968e0049")
        self.assertEqual([p["height"] for p in r["peaks"]], [1, 0])
        self.assertTrue(reference_verify(e, r))

    def test_event_kind_required(self):
        e = fixture()
        del e[0]["event_kind"]
        with self.assertRaises(ValueError):
            construct_turn_checkpoint(e)

    def test_event_kind_enum_invalid(self):
        e = fixture()
        e[0]["event_kind"] = "MADE_UP_ACTION"
        with self.assertRaises(ValueError):
            construct_turn_checkpoint(e)


if __name__ == "__main__":
    unittest.main()
