from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    path = ROOT / rel
    if not path.exists():
        raise AssertionError(f"missing {rel}")
    return path.read_text(encoding="utf-8")


class NewReferenceModuleTests(unittest.TestCase):
    def test_character_identity_board_contract(self):
        text = read("references/character-identity-board.md")
        for required in [
            "2:1", "RIGHT 25%", "LEFT 10%", "CENTER 65%", "exactly four",
            "top-down", "low-angle", "Acceptance test", "gpt-image-2",
            "execution surface",
        ]:
            self.assertIn(required, text)
        self.assertNotIn("input_fidelity", text)

    def test_creative_dna_contract(self):
        text = read("references/creative-dna-reference-analysis.md")
        for required in ["Extract", "Abstract", "Recombine", "Motion DNA", "DO NOT COPY", "PROOF NEEDED"]:
            self.assertIn(required, text)

    def test_interactive_generated_motion_contract(self):
        text = read("references/interactive-generated-motion.md")
        for required in [
            "scroll", "pointer", "drag", "device orientation", "requestAnimationFrame",
            "prefers-reduced-motion", "Two-dimensional input rule", "Alpha WebP", "chroma MP4",
        ]:
            self.assertIn(required, text)

    def test_minimax_h3_contract_and_kling_separation(self):
        text = read("references/minimax-h3-video.md")
        for required in [
            "MiniMax-H3", "4–15", "2K", "7000", "9 reference images",
            "3 reference videos", "3 reference audios", "12 mixed reference items", "PC Bridge",
        ]:
            self.assertIn(required, text)
        self.assertIn("never alter or substitute the independent Kling route", text)

    def test_pc_bridge_upgrade_contract(self):
        text = read("references/pc-bridge-integration-upgrade.md")
        for required in ["Parallel-change safety", "source hashes", "task ID", "Skill Fabric", "Kling"]:
            self.assertIn(required, text)

    def test_provider_adapters_are_not_bundled_in_portable_core(self):
        self.assertFalse((ROOT / "integrations").exists())

    def test_manifest_routes_new_modules_without_widening_kling(self):
        manifest = json.loads(read("pc-bridge.skill.json"))
        hints = manifest["reference_hints"]
        kling = next(h for h in hints if h.get("terms") == ["Kling"])
        self.assertEqual(kling["terms"], ["Kling"])
        h3 = next(h for h in hints if "MiniMax H3" in h.get("terms", []))
        identity = next(h for h in hints if "character identity board" in h.get("terms", []))
        dna = next(h for h in hints if "Creative DNA" in h.get("terms", []))
        motion = next(h for h in hints if "interactive generated motion" in h.get("terms", []))
        self.assertIn("references/minimax-h3-video.md", h3["paths"])
        self.assertIn("references/character-identity-board.md", identity["paths"])
        self.assertIn("references/creative-dna-reference-analysis.md", dna["paths"])
        self.assertIn("references/interactive-generated-motion.md", motion["paths"])
        generic_video = next(h for h in hints if "generated website video" in h.get("terms", []))
        self.assertNotIn("MiniMax H3", generic_video["terms"])
        self.assertNotIn("Kling", generic_video["terms"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
