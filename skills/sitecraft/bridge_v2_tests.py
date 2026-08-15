from __future__ import annotations

import csv
import importlib.util
import json
import re
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def load_module(name: str, relative_path: str):
    path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


VALIDATOR = load_module("sitecraft_validate_skill", "scripts/validate_skill.py")
ARTIFACT_VALIDATOR = load_module(
    "sitecraft_validate_artifact", "scripts/validate_artifact.py"
)
WORKSPACE = load_module("sitecraft_create_workspace", "scripts/create_workspace.py")


class SitecraftBridgePackageTests(unittest.TestCase):
    def test_portable_package(self) -> None:
        errors = VALIDATOR.validate()
        self.assertEqual(errors, [], "\n".join(errors))
        implementation_text = (ROOT / "references" / "implementation-routing.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("actual resolved versions", implementation_text)
        self.assertIn("`latest` is not a reproducible evidence claim", implementation_text)

    def test_reference_hints_keep_content_and_animated_routes_distinct(self) -> None:
        manifest = json.loads((ROOT / "pc-bridge.skill.json").read_text(encoding="utf-8"))
        hints = manifest["reference_hints"]

        content_hint = next(
            hint for hint in hints if "content-first" in hint.get("terms", [])
        )
        self.assertIn(
            "references/content-and-discoverability.md#people-first-content",
            content_hint["paths"],
        )
        self.assertIn(
            "references/experience-mapping.md#content-hierarchy",
            content_hint["paths"],
        )

        motion_graphics_hint = next(
            hint for hint in hints if "motion graphics" in hint.get("terms", [])
        )
        self.assertIn(
            "references/motion-design-and-graphics-compact.md",
            motion_graphics_hint["paths"],
        )
        self.assertIn(
            "references/motion-design-and-graphics.md#choose-the-lightest-delivery-route",
            motion_graphics_hint["paths"],
        )
        self.assertIn("kinetic typography", motion_graphics_hint["terms"])
        self.assertIn("rive", motion_graphics_hint["terms"])

        image_hint = next(
            hint for hint in hints if "image generation pack" in hint.get("terms", [])
        )
        self.assertIn(
            "references/generated-image-production-compact.md",
            image_hint["paths"],
        )
        self.assertIn(
            "references/generated-image-production.md#construct-a-reference-role-stack",
            image_hint["paths"],
        )
        self.assertIn(
            "references/generated-image-production.md#plan-the-production-graph",
            image_hint["paths"],
        )
        self.assertIn("assets/image-generation-pack.md", image_hint["paths"])
        self.assertIn(
            "references/tutorial-pattern-study.md#image-production-pattern-observed",
            image_hint["paths"],
        )
        self.assertIn("still master", image_hint["terms"])
        self.assertIn("still-to-motion handoff", image_hint["terms"])
        self.assertNotIn("responsive image", image_hint["terms"])
        self.assertNotIn("video asset", image_hint["terms"])

        repair_hint = next(
            hint for hint in hints if "existing-codebase repair" in hint.get("terms", [])
        )
        self.assertIn(
            "references/existing-codebase-repair-compact.md",
            repair_hint["paths"],
        )
        self.assertIn(
            "references/implementation-routing.md#inspect-first",
            repair_hint["paths"],
        )
        self.assertIn(
            "references/evidence-and-qa.md#minimum-visual-matrix",
            repair_hint["paths"],
        )
        self.assertIn("narrow diff", repair_hint["terms"])
        self.assertIn("do not rewrite", repair_hint["terms"])

        content_index = hints.index(content_hint)
        repair_index = hints.index(repair_hint)
        image_index = hints.index(image_hint)
        motion_index = hints.index(motion_graphics_hint)
        self.assertLess(
            repair_index,
            content_index,
            "Specific Repair routing must precede content so preserve-content language inside a repair request does not load new-site guidance.",
        )
        self.assertLess(
            content_index,
            image_index,
            "Content-first routing must precede image routing so responsive or metadata language does not load generated-image guidance.",
        )
        self.assertLess(
            repair_index,
            image_index,
            "Existing-codebase repair routing must precede image routing so protected assets or crop defects cannot displace the primary repair module in constrained contexts.",
        )
        self.assertLess(
            image_index,
            motion_index,
            "Generated-image routing must precede motion routing so a later motion handoff cannot displace the primary image-production module in constrained contexts.",
        )

        portability_hint = next(
            hint for hint in hints if "macOS" in hint.get("terms", [])
        )
        self.assertIn(
            "references/platform-portability-compact.md",
            portability_hint["paths"],
        )
        self.assertIn("Windows", portability_hint["terms"])
        self.assertIn("Linux", portability_hint["terms"])
        self.assertIn("Safari", portability_hint["terms"])
        self.assertIn("WebKit", portability_hint["terms"])
        self.assertNotIn("cross platform website", portability_hint["terms"])
        self.assertNotIn("browser engine", portability_hint["terms"])
        self.assertLess(
            hints.index(portability_hint),
            hints.index(repair_hint),
            "Specific multi-OS routing must precede Repair, content and image routes without using generic website or browser tokens.",
        )

        workflow = manifest["workflows"][0]
        build_observe = next(stage for stage in workflow["stages"] if stage["id"] == "build-observe")
        self.assertIn(
            "references/platform-portability-compact.md",
            build_observe["required_references"],
        )

        animated_hint = next(
            hint for hint in hints if "animated microsite" in hint.get("terms", [])
        )
        overbroad = {"short laptop", "tablet", "mobile", "visual reference", "protected artwork", "AI website builder"}
        self.assertTrue(overbroad.isdisjoint(animated_hint["terms"]))

    def test_capability_palette_routes_and_contract_stay_portable(self) -> None:
        manifest = json.loads((ROOT / "pc-bridge.skill.json").read_text(encoding="utf-8"))
        hints = manifest["reference_hints"]
        capability_hint = next(
            hint for hint in hints if "capability plan" in hint.get("terms", [])
        )
        self.assertIn(
            "references/capability-palette-compact.md",
            capability_hint["paths"],
        )
        self.assertIn(
            "references/capability-palette-and-orchestration.md",
            capability_hint["paths"],
        )
        for term in ["WebGPU", "Three.js", "Rive runtime"]:
            self.assertIn(term, capability_hint["terms"])

        workflow = manifest["workflows"][0]
        build_observe = next(
            stage for stage in workflow["stages"] if stage["id"] == "build-observe"
        )
        self.assertIn(
            "references/capability-palette-compact.md",
            build_observe["required_references"],
        )
        self.assertNotIn(
            "references/capability-palette-and-orchestration.md",
            build_observe["required_references"],
            "The staged workflow should load the compact capability reference by default and reserve the full module for progressive disclosure.",
        )

        schema = json.loads(
            (ROOT / "schemas" / "experience-contract.schema.json").read_text(
                encoding="utf-8"
            )
        )
        implementation = schema["properties"]["implementation"]["properties"]
        plan = implementation["capability_plan"]
        item = plan["items"]
        self.assertEqual(item["properties"]["selected_route"]["type"], "string")
        self.assertIn("gpu-rendering", item["properties"]["capability_class"]["enum"])
        self.assertIn("application-rendering", item["properties"]["capability_class"]["enum"])
        self.assertNotIn("capability_plan", schema["properties"]["implementation"]["required"])
        orchestration = implementation["runtime_orchestration"]
        self.assertIn("coordinated_multi_runtime", orchestration["properties"]["mode"]["enum"])
        ownership_item = orchestration["properties"]["ownership"]["items"]
        self.assertIn("animation-clock", ownership_item["properties"]["concern"]["enum"])
        self.assertIn("render-loop", ownership_item["properties"]["concern"]["enum"])
        self.assertNotIn("runtime_orchestration", schema["properties"]["implementation"]["required"])

        template = json.loads(
            (ROOT / "assets" / "experience-contract-template.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(template["implementation"]["capability_plan"], [])
        self.assertEqual(template["implementation"]["runtime_orchestration"]["mode"], "not_needed")
        self.assertEqual(template["implementation"]["runtime_orchestration"]["ownership"], [])

        example = json.loads(
            (ROOT / "examples" / "experience-contract-example.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertTrue(example["implementation"]["capability_plan"])
        self.assertEqual(
            example["implementation"]["runtime_orchestration"]["mode"],
            "coordinated_multi_runtime",
        )
        self.assertTrue(example["implementation"]["runtime_orchestration"]["ownership"])
        self.assertTrue(example["implementation"]["runtime_orchestration"]["bridges"])

        harness_text = (ROOT / "references" / "harness-integration.md").read_text(
            encoding="utf-8"
        )
        capability_text = (
            ROOT / "references" / "capability-palette-and-orchestration.md"
        ).read_text(encoding="utf-8")
        self.assertIn("Host Capability Profile", harness_text)
        self.assertIn("Runtime Capability Plan", harness_text)
        self.assertIn("Host Capability Profile", capability_text)
        self.assertIn("Technology diversity is not creative diversity", capability_text)
        self.assertIn("implementation.runtime_orchestration", capability_text)
        self.assertNotIn("host_capability_profile", implementation)

    def test_runtime_orchestration_rejects_conflicting_ownership_and_unknown_decisions(self) -> None:
        contract = json.loads(
            (ROOT / "examples" / "experience-contract-example.json").read_text(
                encoding="utf-8"
            )
        )
        orchestration = contract["implementation"]["runtime_orchestration"]
        duplicate = dict(orchestration["ownership"][0])
        duplicate["owner"] = "Competing navigation runtime"
        orchestration["ownership"].append(duplicate)
        orchestration["bridges"][0]["related_decision_ids"].append(
            "missing-capability-decision"
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "experience-contract.json"
            path.write_text(json.dumps(contract), encoding="utf-8")
            errors, _ = ARTIFACT_VALIDATOR.validate(
                path,
                ROOT / "schemas" / "experience-contract.schema.json",
            )

        self.assertTrue(errors)
        joined = "\n".join(errors)
        self.assertIn("conflicts with ownership", joined)
        self.assertIn("missing-capability-decision", joined)
        self.assertIn("unknown capability decision", joined)

    def test_creative_distinction_is_optional_and_rejects_tool_only_or_repeated_mechanisms(self) -> None:
        schema = json.loads(
            (ROOT / "schemas" / "experience-contract.schema.json").read_text(
                encoding="utf-8"
            )
        )
        distinction_schema = schema["properties"]["visual_grammar"]["properties"][
            "creative_distinction"
        ]
        self.assertIn("null", distinction_schema["type"])
        self.assertIn(
            "expressive_flagship",
            distinction_schema["properties"]["intent"]["enum"],
        )

        template = json.loads(
            (ROOT / "assets" / "experience-contract-template.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertIsNone(template["visual_grammar"]["creative_distinction"])

        example = json.loads(
            (ROOT / "examples" / "experience-contract-example.json").read_text(
                encoding="utf-8"
            )
        )
        distinction = example["visual_grammar"]["creative_distinction"]
        self.assertEqual(distinction["intent"], "task_specific")
        self.assertTrue(distinction["project_drivers"])
        self.assertTrue(distinction["mechanisms"])
        self.assertTrue(distinction["familiar_patterns_kept"])
        self.assertTrue(distinction["anti_repetition_rules"])

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "experience-contract.json"
            path.write_text(json.dumps(example), encoding="utf-8")
            valid_errors, _ = ARTIFACT_VALIDATOR.validate(
                path,
                ROOT / "schemas" / "experience-contract.schema.json",
            )
            self.assertEqual(valid_errors, [], "\n".join(valid_errors))

            broken = json.loads(json.dumps(example))
            broken_distinction = broken["visual_grammar"]["creative_distinction"]
            broken_distinction["project_drivers"] = []
            broken_distinction["anti_repetition_rules"] = []
            broken_distinction["mechanisms"][1]["mechanism_id"] = broken_distinction[
                "mechanisms"
            ][0]["mechanism_id"]
            broken_distinction["mechanisms"][0]["mechanism"] = "WebGL"
            broken_distinction["mechanisms"][1]["mechanism"] = "WebGL"
            path.write_text(json.dumps(broken), encoding="utf-8")
            errors, _ = ARTIFACT_VALIDATOR.validate(
                path,
                ROOT / "schemas" / "experience-contract.schema.json",
            )

        self.assertTrue(errors)
        joined = "\n".join(errors)
        self.assertIn("project_drivers", joined)
        self.assertIn("duplicates mechanisms", joined)
        self.assertIn("implementation route or tool name", joined)
        self.assertIn("anti_repetition_rules", joined)

        reference_header = (ROOT / "assets" / "reference-role-map.csv").read_text(
            encoding="utf-8-sig"
        )
        self.assertIn("allowed_transformation,project_synthesis,do_not_copy", reference_header)
        failure_text = (ROOT / "references" / "failure-tests.md").read_text(
            encoding="utf-8"
        )
        visual_text = (ROOT / "references" / "visual-system.md").read_text(
            encoding="utf-8"
        )
        research_text = (
            ROOT / "references" / "research-and-reference-analysis.md"
        ).read_text(encoding="utf-8")
        skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("House-style repetition failure", failure_text)
        self.assertIn("Project-specific distinction chain", visual_text)
        self.assertIn("visual_grammar.creative_distinction", visual_text)
        self.assertIn("project synthesis: what the learned mechanism becomes", research_text)
        self.assertIn("do not invent novelty to fill a form", skill_text)

    def test_generated_video_route_is_bounded_provider_neutral_and_kling_optional(self) -> None:
        manifest = json.loads((ROOT / "pc-bridge.skill.json").read_text(encoding="utf-8"))
        video_hint = next(
            hint for hint in manifest["reference_hints"]
            if "generated website video" in hint.get("terms", [])
        )
        self.assertNotIn("Kling", video_hint["terms"], "Generic generated-video routing must stay provider-neutral")
        self.assertIn("references/generated-video-production-compact.md", video_hint["paths"])
        self.assertIn("assets/video-generation-pack.md", video_hint["paths"])
        kling_hint = next(
            hint for hint in manifest["reference_hints"]
            if "Kling" in hint.get("terms", [])
        )
        self.assertEqual(kling_hint["terms"], ["Kling"])
        self.assertIn("references/generated-video-production-compact.md", kling_hint["paths"])

        schema = json.loads(
            (ROOT / "schemas" / "experience-contract.schema.json").read_text(encoding="utf-8")
        )
        self.assertIn("video_system", schema["properties"])
        self.assertNotIn("video_system", schema["required"])
        schema_text = json.dumps(schema).casefold()
        self.assertNotIn("kling", schema_text, "The portable schema must not require one provider")
        policy = schema["properties"]["video_system"]["properties"]["generation_policy"]["properties"]
        self.assertEqual(policy["max_attempts"]["maximum"], 6)
        self.assertEqual(policy["tool_discovery_required"]["type"], "boolean")
        self.assertEqual(policy["provider_inspection_required"]["type"], "boolean")
        self.assertEqual(policy["separate_generation_authority"]["type"], "boolean")
        self.assertEqual(policy["max_status_polls_per_attempt"]["maximum"], 30)

        template = json.loads(
            (ROOT / "assets" / "experience-contract-template.json").read_text(encoding="utf-8")
        )
        self.assertEqual(template["video_system"]["scope"], "none")
        self.assertFalse(template["video_system"]["generation_policy"]["paid_generation"])
        self.assertFalse(template["video_system"]["generation_policy"]["auto_regenerate"])
        self.assertTrue(template["video_system"]["generation_policy"]["provider_inspection_required"])
        self.assertTrue(template["video_system"]["generation_policy"]["separate_generation_authority"])
        self.assertEqual(template["video_system"]["generation_policy"]["max_status_polls_per_attempt"], 12)

        example = json.loads(
            (ROOT / "examples" / "experience-contract-example.json").read_text(encoding="utf-8")
        )
        example_policy = example["video_system"]["generation_policy"]
        self.assertTrue(example_policy["paid_generation"])
        self.assertEqual(example_policy["max_attempts"], 3)
        self.assertTrue(example_policy["auto_regenerate"])
        self.assertIsNone(example_policy["preferred_provider"])
        self.assertTrue(example_policy["provider_inspection_required"])
        self.assertTrue(example_policy["separate_generation_authority"])
        self.assertEqual(example_policy["max_status_polls_per_attempt"], 12)
        self.assertTrue(example["video_system"]["quality_gate"]["hard_floors"])

        compact = (ROOT / "references" / "generated-video-production-compact.md").read_text(encoding="utf-8")
        deep = (ROOT / "references" / "generated-video-production.md").read_text(encoding="utf-8")
        video_pack = (ROOT / "assets" / "video-generation-pack.md").read_text(encoding="utf-8")
        for required in [
            "Never burn credits indefinitely",
            "inspect the actual video",
            "max_attempts",
            "cheapest sufficient route",
            "image-conditioned",
            "provider inspection",
            "inspection authority separate from generation authority",
            "pre-generation gate",
            "max_status_polls_per_attempt",
        ]:
            self.assertIn(required.casefold(), (compact + deep + video_pack).casefold())

        self.assertFalse(
            (ROOT / "integrations").exists(),
            "The canonical portable skill must not bundle host credentials or provider adapters",
        )
        self.assertFalse(
            (ROOT / ".codex" / "config.toml").exists(),
            "The skill must not install a Codex MCP configuration or grant provider authority",
        )

        negative = json.loads((ROOT / "tests" / "negative-routing-cases.json").read_text(encoding="utf-8"))
        self.assertTrue(any("standalone" in case.get("request", "").casefold() and "video" in case.get("request", "").casefold() for case in negative))

    def test_handoff_packet_is_routable_and_cannot_transfer_authority(self) -> None:
        manifest = json.loads((ROOT / "pc-bridge.skill.json").read_text(encoding="utf-8"))
        handoff_hint = next(
            hint for hint in manifest["reference_hints"] if "handoff packet" in hint.get("terms", [])
        )
        self.assertIn(
            "references/handoff-and-continuity.md#no-authority-transfer",
            handoff_hint["paths"],
        )
        self.assertIn(
            "references/handoff-and-continuity.md#receiving-host-procedure",
            handoff_hint["paths"],
        )
        self.assertIn("assets/handoff-packet-template.json", handoff_hint["paths"])

        schema = json.loads(
            (ROOT / "schemas" / "sitecraft-handoff.schema.json").read_text(
                encoding="utf-8"
            )
        )
        safety = schema["properties"]["safety"]["properties"]
        for key in [
            "contains_hidden_reasoning",
            "contains_private_transcript",
            "contains_secrets",
            "permissions_carried_over",
        ]:
            self.assertIs(safety[key]["const"], False, key)
        self.assertIs(
            schema["properties"]["execution"]["properties"][
                "receiving_host_must_rediscover_capabilities"
            ]["const"],
            True,
        )

        example = json.loads(
            (ROOT / "examples" / "handoff-packet-example.json").read_text(
                encoding="utf-8"
            )
        )
        coordination_schema = schema["properties"]["coordination"]["properties"]
        self.assertIs(
            coordination_schema["receiving_host_must_confirm_checkout_before_write"]["const"],
            True,
        )
        self.assertIn("coordination", schema["required"])

        template = json.loads(
            (ROOT / "assets" / "handoff-packet-template.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(template["coordination"]["workspace_mode"], "unknown")
        self.assertEqual(
            template["coordination"]["checkout_status"], "revalidate_required"
        )
        self.assertEqual(
            template["coordination"]["receiver_write_policy"],
            "read_only_until_handoff",
        )

        self.assertTrue(example["execution"]["receiving_host_must_rediscover_capabilities"])
        self.assertFalse(example["safety"]["permissions_carried_over"])
        self.assertEqual(example["coordination"]["workspace_mode"], "shared")
        self.assertEqual(example["coordination"]["checkout_status"], "free")
        self.assertIsNone(example["coordination"]["current_owner"])
        self.assertEqual(
            example["coordination"]["receiver_write_policy"],
            "allowed_after_revalidation",
        )
        self.assertTrue(example["coordination"]["coordination_receipts"])
        self.assertTrue(example["state"]["next_action"])
        self.assertTrue(example["contract"]["reference"])

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "handoff.json"
            path.write_text(json.dumps(example), encoding="utf-8")
            valid_errors, _ = ARTIFACT_VALIDATOR.validate(
                path,
                ROOT / "schemas" / "sitecraft-handoff.schema.json",
            )
            self.assertEqual(valid_errors, [], "\n".join(valid_errors))

            free_without_receipt = json.loads(json.dumps(example))
            free_without_receipt["coordination"]["coordination_receipts"] = []
            path.write_text(json.dumps(free_without_receipt), encoding="utf-8")
            free_errors, _ = ARTIFACT_VALIDATOR.validate(
                path,
                ROOT / "schemas" / "sitecraft-handoff.schema.json",
            )
            self.assertIn("explicit release/handoff receipt", "\n".join(free_errors))

            reserved_without_owner = json.loads(json.dumps(example))
            reserved_without_owner["coordination"]["checkout_status"] = "reserved"
            reserved_without_owner["coordination"]["current_owner"] = None
            reserved_without_owner["coordination"]["receiver_write_policy"] = (
                "allowed_after_revalidation"
            )
            path.write_text(json.dumps(reserved_without_owner), encoding="utf-8")
            reserved_errors, _ = ARTIFACT_VALIDATOR.validate(
                path,
                ROOT / "schemas" / "sitecraft-handoff.schema.json",
            )
            reserved_joined = "\n".join(reserved_errors)
            self.assertIn("current_owner", reserved_joined)
            self.assertIn("read_only_until_handoff", reserved_joined)

        handoff_text = (ROOT / "references" / "handoff-and-continuity.md").read_text(
            encoding="utf-8"
        )
        harness_text = (ROOT / "references" / "harness-integration.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("clean tree", handoff_text)
        self.assertIn("clean tree", harness_text)
        self.assertIn("receiving_host_must_confirm_checkout_before_write", handoff_text)
        self.assertIn("continuation bundle", handoff_text.casefold())
        self.assertIn("--review", handoff_text)
        self.assertIn("--handoff", handoff_text)

    def test_mutable_forward_test_workspace_is_ignored_and_isolated(self) -> None:
        self.assertFalse((ROOT / "forward-tests").exists())
        temporary_fixture = ROOT / "build" / "validator-isolation-test"
        temporary_fixture.mkdir(parents=True, exist_ok=False)
        try:
            marker = "TO" + "DO: this mutable marker must not enter package validation.\n"
            (temporary_fixture / "intentional-placeholder.md").write_text(
                marker,
                encoding="utf-8",
            )
            self.assertEqual(VALIDATOR.validate(), [])
        finally:
            shutil.rmtree(temporary_fixture, ignore_errors=True)
            try:
                temporary_fixture.parent.rmdir()
            except OSError:
                pass

    def test_distributable_core_has_no_machine_specific_paths_or_implicit_shell(self) -> None:
        machine_patterns = [
            re.compile("/" + "Users" + r"/[A-Za-z0-9._-]+/"),
            re.compile("/" + "home" + r"/[A-Za-z0-9._-]+/"),
            re.compile(r"[A-Za-z]:" + r"\\Users\\" + r"[^\\\s]+\\"),
        ]
        suffixes = {".md", ".json", ".yaml", ".yml", ".py", ".toml", ".csv"}
        for path in ROOT.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in suffixes:
                continue
            relative = path.relative_to(ROOT)
            if any(part.casefold() in {"build", "dist", ".cache"} for part in relative.parts):
                continue
            text = path.read_text(encoding="utf-8-sig")
            for pattern in machine_patterns:
                self.assertIsNone(pattern.search(text), relative.as_posix())

        for relative in [
            "scripts/create_workspace.py",
            "scripts/validate_artifact.py",
            "scripts/validate_skill.py",
        ]:
            text = (ROOT / relative).read_text(encoding="utf-8-sig")
            self.assertNotIn("shell=True", text, relative)
            self.assertNotIn("os.system(", text, relative)

    def test_bundled_examples_validate(self) -> None:
        contract_errors, _ = ARTIFACT_VALIDATOR.validate(
            ROOT / "examples" / "experience-contract-example.json",
            ROOT / "schemas" / "experience-contract.schema.json",
        )
        self.assertEqual(contract_errors, [], "\n".join(contract_errors))

        review_errors, _ = ARTIFACT_VALIDATOR.validate(
            ROOT / "examples" / "sitecraft-review-example.json",
            ROOT / "schemas" / "sitecraft-review.schema.json",
        )
        self.assertEqual(review_errors, [], "\n".join(review_errors))

        handoff_errors, _ = ARTIFACT_VALIDATOR.validate(
            ROOT / "examples" / "handoff-packet-example.json",
            ROOT / "schemas" / "sitecraft-handoff.schema.json",
        )
        self.assertEqual(handoff_errors, [], "\n".join(handoff_errors))

        video_workflow_errors, _ = ARTIFACT_VALIDATOR.validate(
            ROOT / "assets" / "video-generation-workflow-template.json",
            ROOT / "schemas" / "video-generation-workflow.schema.json",
        )
        self.assertEqual(video_workflow_errors, [], "\n".join(video_workflow_errors))
        self.assertIn("video-generation-workflow", ARTIFACT_VALIDATOR.SCHEMAS)

    def test_video_generation_workflow_enforces_readiness_gate(self) -> None:
        workflow = json.loads(
            (ROOT / "assets" / "video-generation-workflow-template.json").read_text(
                encoding="utf-8"
            )
        )
        workflow["route_decision"] = "generated_video"
        workflow["generation_readiness"]["ready"] = True
        workflow["generation_readiness"]["provider_model_frozen"] = True
        workflow["generation_readiness"]["settings_checked_against_contract"] = True

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "video-workflow.json"
            path.write_text(json.dumps(workflow), encoding="utf-8")
            errors, _ = ARTIFACT_VALIDATOR.validate(
                path,
                ROOT / "schemas" / "video-generation-workflow.schema.json",
            )
            self.assertTrue(errors)
            joined = "\n".join(errors)
            self.assertIn("prompt_ready", joined)
            self.assertIn("catalogue_discovered", joined)
            self.assertIn("provider_inspection/provider", joined)
            self.assertIn("settings_summary", joined)

            workflow["asset_plan"]["host_can_inspect_result"] = True
            workflow["asset_plan"]["prompt_ready"] = True
            workflow["asset_plan"]["references_ready"] = True
            workflow["provider_inspection"]["catalogue_discovered"] = True
            workflow["provider_inspection"]["current_source_used"] = True
            workflow["provider_inspection"]["model_requirements_known"] = True
            workflow["provider_inspection"]["provider"] = "example-provider"
            workflow["provider_inspection"]["model"] = "example-image-conditioned-model"
            workflow["provider_inspection"]["settings_summary"] = [
                "Current provider inspection confirmed the required image-conditioned generation arguments."
            ]
            workflow["provider_inspection"]["generation_performed_during_inspection"] = False
            workflow["stage_state"]["asset_plan"] = "passed"
            workflow["stage_state"]["provider_inspection"] = "passed"
            workflow["stage_state"]["generation_readiness"] = "passed"
            path.write_text(json.dumps(workflow), encoding="utf-8")
            ready_errors, _ = ARTIFACT_VALIDATOR.validate(
                path,
                ROOT / "schemas" / "video-generation-workflow.schema.json",
            )
            self.assertEqual(ready_errors, [], "\n".join(ready_errors))

            workflow["review_delivery"]["decision"] = "accepted"
            path.write_text(json.dumps(workflow), encoding="utf-8")
            acceptance_errors, _ = ARTIFACT_VALIDATOR.validate(
                path,
                ROOT / "schemas" / "video-generation-workflow.schema.json",
            )
            self.assertTrue(acceptance_errors)
            acceptance_joined = "\n".join(acceptance_errors)
            self.assertIn("artifact_reference", acceptance_joined)
            self.assertIn("performance_budget_verified", acceptance_joined)
            self.assertIn("media_accessibility_verified", acceptance_joined)
            self.assertIn("evidence_refs", acceptance_joined)

            workflow["review_delivery"]["attempt_count"] = 1
            workflow["review_delivery"]["artifact_reference"] = "accepted-video-attempt-1"
            workflow["review_delivery"]["actual_artifact_inspected"] = True
            workflow["review_delivery"]["hard_floors_passed"] = True
            workflow["review_delivery"]["delivery_verified"] = True
            workflow["review_delivery"]["responsive_delivery_verified"] = True
            workflow["review_delivery"]["performance_budget_verified"] = True
            workflow["review_delivery"]["media_accessibility_verified"] = True
            workflow["review_delivery"]["reduced_motion_verified"] = True
            workflow["review_delivery"]["evidence_refs"] = ["evidence/video-attempt-1-review"]
            workflow["review_delivery"]["owner_approval"] = "approved"
            workflow["stage_state"]["review_delivery"] = "passed"
            path.write_text(json.dumps(workflow), encoding="utf-8")
            accepted_errors, _ = ARTIFACT_VALIDATOR.validate(
                path,
                ROOT / "schemas" / "video-generation-workflow.schema.json",
            )
            self.assertEqual(accepted_errors, [], "\n".join(accepted_errors))

    def test_asset_traceability_bundle_rejects_cross_file_drift(self) -> None:
        contract_source = ROOT / "examples" / "experience-contract-example.json"
        ledger_source = ROOT / "examples" / "asset-ledger-example.csv"
        evidence_source = ROOT / "examples" / "evidence-matrix-example.csv"

        valid_errors = ARTIFACT_VALIDATOR.validate_traceability_bundle(
            contract_source,
            ledger_source,
            evidence_source,
        )
        self.assertEqual(valid_errors, [], "\n".join(valid_errors))

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            contract_path = root / "experience-contract.json"
            ledger_path = root / "asset-ledger.csv"
            evidence_path = root / "evidence-matrix.csv"
            shutil.copyfile(contract_source, contract_path)
            shutil.copyfile(ledger_source, ledger_path)
            shutil.copyfile(evidence_source, evidence_path)

            with ledger_path.open("r", encoding="utf-8-sig", newline="") as handle:
                reader = csv.DictReader(handle)
                ledger_fields = list(reader.fieldnames or [])
                ledger_rows = list(reader)
            for row in ledger_rows:
                if row.get("asset_id") == "programme-mark-ambient-loop-web":
                    row["parent_asset_ids"] = "missing-video-master"
            with ledger_path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=ledger_fields)
                writer.writeheader()
                writer.writerows(ledger_rows)

            parent_errors = ARTIFACT_VALIDATOR.validate_traceability_bundle(
                contract_path,
                ledger_path,
                evidence_path,
            )
            parent_joined = "\n".join(parent_errors)
            self.assertIn("missing-video-master", parent_joined)
            self.assertIn("parent_asset_ids disagree", parent_joined)

            shutil.copyfile(ledger_source, ledger_path)
            with evidence_path.open("r", encoding="utf-8-sig", newline="") as handle:
                reader = csv.DictReader(handle)
                evidence_fields = list(reader.fieldnames or [])
                evidence_rows = list(reader)
            evidence_rows[0]["asset_ids"] = "missing-lineage-asset"
            with evidence_path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=evidence_fields)
                writer.writeheader()
                writer.writerows(evidence_rows)

            evidence_errors = ARTIFACT_VALIDATOR.validate_traceability_bundle(
                contract_path,
                ledger_path,
                evidence_path,
            )
            self.assertIn(
                "missing-lineage-asset",
                "\n".join(evidence_errors),
            )

            evidence_rows[0]["asset_ids"] = "workshop-process-photography"
            evidence_rows[0]["contract_revision"] = "2"
            with evidence_path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=evidence_fields)
                writer.writeheader()
                writer.writerows(evidence_rows)
            revision_errors = ARTIFACT_VALIDATOR.validate_traceability_bundle(
                contract_path,
                ledger_path,
                evidence_path,
            )
            self.assertIn(
                "contract revision disagrees with Experience Contract",
                "\n".join(revision_errors),
            )

            shutil.copyfile(evidence_source, evidence_path)
            contract = json.loads(contract_path.read_text(encoding="utf-8"))
            contract["asset_lineage"]["records"][0]["evidence_refs"].append(
                "missing-evidence"
            )
            contract_path.write_text(json.dumps(contract), encoding="utf-8")
            missing_evidence_errors = ARTIFACT_VALIDATOR.validate_traceability_bundle(
                contract_path,
                ledger_path,
                evidence_path,
            )
            missing_evidence_joined = "\n".join(missing_evidence_errors)
            self.assertIn("missing-evidence", missing_evidence_joined)
            self.assertIn("unknown evidence ID", missing_evidence_joined)

    def test_continuation_bundle_rejects_contract_review_handoff_drift(self) -> None:
        contract_source = ROOT / "examples" / "experience-contract-example.json"
        review_source = ROOT / "examples" / "sitecraft-review-example.json"
        handoff_source = ROOT / "examples" / "handoff-packet-example.json"

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            contract_path = root / "experience-contract.json"
            review_path = root / "sitecraft-review.json"
            handoff_path = root / "sitecraft-handoff.json"
            shutil.copyfile(contract_source, contract_path)
            shutil.copyfile(review_source, review_path)
            shutil.copyfile(handoff_source, handoff_path)

            handoff = json.loads(handoff_path.read_text(encoding="utf-8"))
            handoff["project"]["name"] = "Fieldhouse Workshops"
            handoff_path.write_text(json.dumps(handoff), encoding="utf-8")

            valid_errors = ARTIFACT_VALIDATOR.validate_continuation_bundle(
                contract_path,
                review_path,
                handoff_path,
            )
            self.assertEqual(valid_errors, [], "\n".join(valid_errors))

            review = json.loads(review_path.read_text(encoding="utf-8"))
            review["contract_revision"] = 2
            review_path.write_text(json.dumps(review), encoding="utf-8")
            revision_errors = ARTIFACT_VALIDATOR.validate_continuation_bundle(
                contract_path,
                review_path,
                handoff_path,
            )
            self.assertIn("Review contract_revision disagrees", "\n".join(revision_errors))

            shutil.copyfile(review_source, review_path)
            handoff = json.loads(handoff_path.read_text(encoding="utf-8"))
            handoff["project"]["name"] = "Different Project"
            handoff_path.write_text(json.dumps(handoff), encoding="utf-8")
            identity_errors = ARTIFACT_VALIDATOR.validate_continuation_bundle(
                contract_path,
                review_path,
                handoff_path,
            )
            self.assertIn("Handoff project identity disagrees", "\n".join(identity_errors))

            handoff["project"]["name"] = "Fieldhouse Workshops"
            handoff["contract"]["status"] = "draft"
            handoff_path.write_text(json.dumps(handoff), encoding="utf-8")
            status_errors = ARTIFACT_VALIDATOR.validate_continuation_bundle(
                contract_path,
                review_path,
                handoff_path,
            )
            self.assertIn("Handoff contract status disagrees", "\n".join(status_errors))

            handoff["contract"]["status"] = "buildable"
            handoff_path.write_text(json.dumps(handoff), encoding="utf-8")
            review = json.loads(review_path.read_text(encoding="utf-8"))
            review["capability_scope"]["reviewed_ids"] = ["list-detail-continuity"]
            review["capability_scope"]["unreviewed_ids"] = []
            review_path.write_text(json.dumps(review), encoding="utf-8")
            coverage_errors = ARTIFACT_VALIDATOR.validate_continuation_bundle(
                contract_path,
                review_path,
                handoff_path,
            )
            self.assertIn(
                "does not account for Experience Contract capability decisions",
                "\n".join(coverage_errors),
            )

            shutil.copyfile(review_source, review_path)
            handoff = json.loads(handoff_path.read_text(encoding="utf-8"))
            handoff["contract"]["capability_decision_ids"].append("missing-decision")
            handoff_path.write_text(json.dumps(handoff), encoding="utf-8")
            capability_errors = ARTIFACT_VALIDATOR.validate_continuation_bundle(
                contract_path,
                review_path,
                handoff_path,
            )
            self.assertIn(
                "Handoff references unknown Experience Contract capability decisions",
                "\n".join(capability_errors),
            )

            handoff["contract"]["capability_decision_ids"] = [
                "list-detail-continuity",
                "programme-filter-state",
            ]
            handoff["contract"]["continuity_anchor_ids"].append("missing-anchor")
            handoff["contract"]["continuity_state_dimension_ids"].append(
                "missing-state-dimension"
            )
            handoff_path.write_text(json.dumps(handoff), encoding="utf-8")
            continuity_errors = ARTIFACT_VALIDATOR.validate_continuation_bundle(
                contract_path,
                review_path,
                handoff_path,
            )
            continuity_text = "\n".join(continuity_errors)
            self.assertIn(
                "Handoff references unknown Experience Contract continuity anchors",
                continuity_text,
            )
            self.assertIn(
                "Handoff references unknown Experience Contract continuity state dimensions",
                continuity_text,
            )

    def test_ai_builder_packet_tracks_integrated_contract_without_provider_lock_in(self) -> None:
        packet = (ROOT / "assets" / "ai-builder-work-packet.md").read_text(
            encoding="utf-8"
        )
        translation = (
            ROOT / "references" / "ai-builder-translation.md"
        ).read_text(encoding="utf-8")

        for heading in [
            "## Shared-checkout coordination when applicable",
            "## Runtime orchestration when applicable",
            "## Creative distinction when applicable",
            "## Asset lineage when applicable",
            "## Image-production boundary when applicable",
        ]:
            self.assertIn(heading, packet)

        for required in [
            "Experience Contract reference/revision",
            "Exact project state / build fingerprint",
            "allowed_after_revalidation",
            "read_only_until_handoff",
            "clean tree",
            "Concern + scope + current owner",
            "Explicit bridge between systems",
            "Mechanism ID + what the mechanism actually does",
            "Direct parent asset ID(s)",
            "Reference asset ID(s)",
            "Image Generation Pack reference",
            "Approved image asset ID(s) the builder must consume unchanged",
            "Host reference-loading capability confirmed?",
            "relevant asset IDs and evidence IDs created/updated",
            "shared-checkout coordination state if work is being handed onward",
        ]:
            self.assertIn(required, packet)

        for required in [
            "visual_grammar.creative_distinction",
            "implementation.runtime_orchestration",
            "asset_lineage",
            "image_system.production_jobs",
            "Shared checkout coordination",
            "clean tree does not prove release",
            "exact changed paths",
            "asset IDs and evidence IDs",
        ]:
            self.assertIn(required, translation)

        portable_text = (packet + translation).casefold()
        for forbidden in [
            "kling",
            "bearer_token",
            "api_key",
            "access_token",
            "refresh_token",
        ]:
            self.assertNotIn(forbidden, portable_text)

    def test_generated_image_core_stays_provider_neutral_and_host_portable(self) -> None:
        portable_files = [
            ROOT / "assets" / "image-generation-pack.md",
            ROOT / "references" / "generated-image-production-compact.md",
            ROOT / "references" / "generated-image-production.md",
            ROOT / "references" / "asset-and-media-pipeline.md",
            ROOT / "references" / "harness-integration.md",
        ]
        portable_text = "\n".join(
            path.read_text(encoding="utf-8").casefold() for path in portable_files
        )
        for forbidden in [
            "gpt-image-2",
            "gpt-image-1.5",
            "openai_api_key",
            "$codex_home",
            "view_image",
            "image_gen.py",
        ]:
            self.assertNotIn(forbidden, portable_text)

        pack = (ROOT / "assets" / "image-generation-pack.md").read_text(
            encoding="utf-8"
        )
        for required in [
            "A filesystem path is not automatically an image-model input",
            "execution-context mode",
            "fresh bounded context",
            "Temporary Chat",
            "Do not require API spend",
            "mixed conversation context",
            "CONTEXT CONTAMINATION / CHANGE ROUTE",
            "one distinct output asset = one production job",
            "only independent jobs may run concurrently",
            "every sibling restarts from that same declared master",
            "Do not leave a project-referenced final only",
        ]:
            self.assertIn(required, pack)

        image_route = (ROOT / "references" / "generated-image-production.md").read_text(
            encoding="utf-8"
        )
        for required in [
            "## Gate execution-context isolation",
            "Prompt quality and execution-context isolation are separate requirements.",
            "record **context contamination**",
            "Do not respond by making the prompt longer",
        ]:
            self.assertIn(required, image_route)

    def test_capability_traceability_links_contract_evidence_review_and_handoff(self) -> None:
        contract = json.loads(
            (ROOT / "examples" / "experience-contract-example.json").read_text(
                encoding="utf-8"
            )
        )
        capability_ids = {
            item["id"] for item in contract["implementation"]["capability_plan"]
        }
        self.assertEqual(
            capability_ids,
            {"list-detail-continuity", "programme-filter-state"},
        )

        review = json.loads(
            (ROOT / "examples" / "sitecraft-review-example.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(set(review["capability_scope"]["reviewed_ids"]), capability_ids)
        self.assertEqual(review["capability_scope"]["unreviewed_ids"], [])
        implementation_floor = next(
            item for item in review["blocking_floors"] if item["id"] == "implementation-evidence"
        )
        self.assertEqual(set(implementation_floor["capability_decision_ids"]), capability_ids)

        evidence_header = (ROOT / "assets" / "evidence-matrix.csv").read_text(
            encoding="utf-8-sig"
        ).splitlines()[0].split(",")
        self.assertIn("capability_decision_ids", evidence_header)

        handoff = json.loads(
            (ROOT / "examples" / "handoff-packet-example.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(set(handoff["contract"]["capability_decision_ids"]), capability_ids)

    def test_image_production_graph_enforces_reference_dependent_sequences(self) -> None:
        contract = json.loads(
            (ROOT / "examples" / "experience-contract-example.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(
            ARTIFACT_VALIDATOR.experience_contract_semantic_errors(contract),
            [],
        )

        for asset_id, label in [
            ("programme-mark-shelter", "Shelter"),
            ("programme-mark-release", "Release"),
            ("programme-mark-return", "Return"),
        ]:
            contract["asset_lineage"]["records"].append(
                {
                    "asset_id": asset_id,
                    "kind": "image",
                    "stage": "derivative",
                    "parent_asset_ids": ["programme-mark-key-art"],
                    "reference_asset_ids": [],
                    "external_source_refs": [],
                    "declared_systems": ["image_system", "asset_ledger"],
                    "artifact_ref": None,
                    "capability_decision_ids": [],
                    "evidence_refs": [],
                    "approval_state": "planned",
                    "notes": [f"{label} lighting derivative planned from the same approved master."],
                }
            )
            contract["image_system"]["production_jobs"].append(
                {
                    "job_id": f"edit-{asset_id}",
                    "asset_id": asset_id,
                    "intent": "edit",
                    "depends_on_job_ids": ["generate-programme-mark-master"],
                    "required_approved_asset_ids": ["programme-mark-key-art"],
                    "source_asset_ids": ["programme-mark-key-art"],
                    "reference_ids": [],
                    "parallel_group": "programme-mark-lighting-derivatives",
                    "prompt_path": "prompts/programme-mark-image-pack.md",
                    "output_ref": None,
                    "acceptance_gate": "Preserve the approved master geometry and change only the declared lighting state.",
                    "notes": ["Restart from the master rather than a sibling derivative."],
                }
            )

        self.assertEqual(
            ARTIFACT_VALIDATOR.experience_contract_semantic_errors(contract),
            [],
            "A base master with independent sibling edits should be a valid production graph.",
        )

        missing_source = json.loads(json.dumps(contract))
        missing_source["image_system"]["production_jobs"][1]["source_asset_ids"] = []
        self.assertTrue(
            any(
                "must name at least one edit source" in error
                for error in ARTIFACT_VALIDATOR.experience_contract_semantic_errors(missing_source)
            )
        )

        unknown_reference = json.loads(json.dumps(contract))
        unknown_reference["image_system"]["production_jobs"][0]["reference_ids"].append(
            "reference-that-does-not-exist"
        )
        self.assertTrue(
            any(
                "unknown image reference role" in error
                for error in ARTIFACT_VALIDATOR.experience_contract_semantic_errors(unknown_reference)
            )
        )

        duplicate_output = json.loads(json.dumps(contract))
        duplicate_output["image_system"]["production_jobs"][2]["asset_id"] = (
            duplicate_output["image_system"]["production_jobs"][1]["asset_id"]
        )
        self.assertTrue(
            any(
                "one distinct asset requires one job" in error
                for error in ARTIFACT_VALIDATOR.experience_contract_semantic_errors(duplicate_output)
            )
        )

        dependency_cycle = json.loads(json.dumps(contract))
        dependency_cycle["image_system"]["production_jobs"][0]["depends_on_job_ids"] = [
            "edit-programme-mark-shelter"
        ]
        self.assertTrue(
            any(
                "production_jobs contains a dependency cycle" in error
                for error in ARTIFACT_VALIDATOR.experience_contract_semantic_errors(dependency_cycle)
            )
        )

        broken_lineage = json.loads(json.dumps(contract))
        derivative_id = broken_lineage["image_system"]["production_jobs"][1]["asset_id"]
        derivative_record = next(
            record
            for record in broken_lineage["asset_lineage"]["records"]
            if record["asset_id"] == derivative_id
        )
        derivative_record["parent_asset_ids"] = []
        self.assertTrue(
            any(
                "does not list it as a direct parent" in error
                for error in ARTIFACT_VALIDATOR.experience_contract_semantic_errors(broken_lineage)
            )
        )

    def test_batch11_continuity_direction_review_and_diagnostics_are_optional_but_enforced(self) -> None:
        schema = json.loads(
            (ROOT / "schemas" / "experience-contract.schema.json").read_text(encoding="utf-8")
        )
        self.assertNotIn("continuity_system", schema["required"])
        self.assertNotIn("direction_selection", schema["properties"]["visual_grammar"]["required"])
        self.assertNotIn("diagnostic_escalation", schema["properties"]["evidence_contract"]["required"])

        template = json.loads(
            (ROOT / "assets" / "experience-contract-template.json").read_text(encoding="utf-8")
        )
        self.assertNotIn("continuity_system", template)
        self.assertNotIn("direction_selection", template["visual_grammar"])
        self.assertNotIn("diagnostic_escalation", template["evidence_contract"])

        example = json.loads(
            (ROOT / "examples" / "experience-contract-example.json").read_text(encoding="utf-8")
        )
        self.assertTrue(example["continuity_system"]["anchors"])
        self.assertEqual(example["visual_grammar"]["direction_selection"]["mode"], "not_needed")
        video_role = example["video_system"]["asset_roles"][0]
        self.assertTrue(video_role["first_frame_requirement"])
        self.assertTrue(video_role["last_frame_requirement"])
        self.assertTrue(video_role["continuity_requirements"])

        broken_direction = json.loads(json.dumps(example))
        broken_direction["visual_grammar"]["direction_selection"] = {
            "mode": "exploring",
            "reason": "Testing two possible structures.",
            "directions": [
                {
                    "id": "only-one",
                    "experience_argument": "One route",
                    "structural_difference": "One-column schedule"
                }
            ],
            "selected_id": None,
            "reopen_conditions": []
        }
        direction_errors = ARTIFACT_VALIDATOR.experience_contract_semantic_errors(
            broken_direction
        )
        self.assertTrue(any("at least two structurally different directions" in error for error in direction_errors))

        broken_continuity = json.loads(json.dumps(example))
        duplicate_anchor = json.loads(
            json.dumps(broken_continuity["continuity_system"]["anchors"][0])
        )
        broken_continuity["continuity_system"]["anchors"].append(duplicate_anchor)
        continuity_errors = ARTIFACT_VALIDATOR.experience_contract_semantic_errors(
            broken_continuity
        )
        self.assertTrue(any("duplicates continuity anchor" in error for error in continuity_errors))

        review = json.loads(
            (ROOT / "examples" / "sitecraft-review-example.json").read_text(encoding="utf-8")
        )
        self.assertTrue(review["review_provenance"])
        self.assertEqual(review["review_provenance"][0]["independence"], "not_independent")
        broken_review = json.loads(json.dumps(review))
        broken_review["review_provenance"][0]["independence"] = "independent"
        review_errors = ARTIFACT_VALIDATOR.sitecraft_review_semantic_errors(broken_review)
        self.assertTrue(any("must be 'not_independent'" in error for error in review_errors))

        evidence_text = (ROOT / "references" / "evidence-and-qa.md").read_text(encoding="utf-8")
        self.assertIn("## Review provenance", evidence_text)
        self.assertIn("## Diagnostic escalation", evidence_text)
        self.assertIn("lightest evidence", evidence_text)

    def test_learning_promotion_requires_contrast_and_explicit_approval(self) -> None:
        self.assertIn("learning-candidate", ARTIFACT_VALIDATOR.SCHEMAS)
        candidate = json.loads(
            (ROOT / "assets" / "learning-candidate-template.json").read_text(encoding="utf-8")
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "learning-candidate.json"
            path.write_text(json.dumps(candidate), encoding="utf-8")
            valid_errors, _ = ARTIFACT_VALIDATOR.validate(
                path,
                ROOT / "schemas" / "learning-candidate.schema.json",
            )
            self.assertEqual(valid_errors, [], "\n".join(valid_errors))

            candidate["status"] = "promoted"
            path.write_text(json.dumps(candidate), encoding="utf-8")
            blocked_errors, _ = ARTIFACT_VALIDATOR.validate(
                path,
                ROOT / "schemas" / "learning-candidate.schema.json",
            )
            blocked_text = "\n".join(blocked_errors)
            self.assertIn("contrast_evidence or stronger external_evidence", blocked_text)
            self.assertIn("approved_for_promotion", blocked_text)
            self.assertIn("promotion_target", blocked_text)

            candidate["user_verdict"] = "approved_for_promotion"
            candidate["contrast_evidence"] = [
                "A meaningfully different project reproduced the lesson without inheriting the source design."
            ]
            candidate["promotion_target"] = "references/research-and-reference-analysis.md"
            path.write_text(json.dumps(candidate), encoding="utf-8")
            promoted_errors, _ = ARTIFACT_VALIDATOR.validate(
                path,
                ROOT / "schemas" / "learning-candidate.schema.json",
            )
            self.assertEqual(promoted_errors, [], "\n".join(promoted_errors))

    def test_sitecraft_architecture_maintenance_routing_precedes_provider_adapter_hints(self) -> None:
        manifest = json.loads((ROOT / "pc-bridge.skill.json").read_text(encoding="utf-8"))
        self.assertTrue(
            manifest["intents"][0].startswith("audit evolve or maintain SITECRAFT architecture")
        )
        architecture_hint = manifest["reference_hints"][0]
        self.assertIn("SITECRAFT architecture", architecture_hint["terms"])
        self.assertEqual(
            architecture_hint["paths"],
            ["references/architecture-maintenance-compact.md"],
        )
        compact_text = (ROOT / "references" / "architecture-maintenance-compact.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("## Continuity and direction", compact_text)
        self.assertIn("## Review and evidence", compact_text)
        self.assertIn("## Learning promotion", compact_text)
        self.assertIn("## PC Bridge boundary", compact_text)
        kling_hint = next(
            hint for hint in manifest["reference_hints"]
            if "Kling" in hint.get("terms", [])
        )
        self.assertEqual(kling_hint["terms"], ["Kling"])
        self.assertLess(manifest["reference_hints"].index(architecture_hint), manifest["reference_hints"].index(kling_hint))

    def test_workspace_creation_is_complete_and_non_destructive(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "example SITECRAFT workspace Ω"
            created = WORKSPACE.create_workspace(destination, "Example Website")
            self.assertTrue(created)

            expected = [
                destination / "contracts" / "experience-contract.json",
                destination / "contracts" / "video-generation-workflow-template.json",
                destination / "reviews" / "review-template.json",
                destination / "prompts" / "ai-builder-work-packet.md",
                destination / "prompts" / "image-generation-pack.md",
                destination / "prompts" / "video-generation-pack.md",
                destination / "assets" / "asset-ledger.csv",
                destination / "research" / "reference-role-map.csv",
                destination / "evidence" / "evidence-matrix.csv",
                destination / "evidence" / "platform-evidence-matrix.csv",
                destination / "decisions" / "decision-log.csv",
                destination / "handoffs" / "sitecraft-handoff.json",
            ]
            for path in expected:
                self.assertTrue(path.is_file(), str(path))

            contract = json.loads(
                (destination / "contracts" / "experience-contract.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(contract["project"], "Example Website")
            self.assertEqual(contract["contract_id"], "example-website-experience-v1")
            self.assertEqual(contract["asset_lineage"]["ledger_path"], "assets/asset-ledger.csv")
            self.assertEqual(contract["asset_lineage"]["records"], [])
            self.assertTrue(contract["asset_lineage"]["rules"])
            self.assertEqual(contract["image_system"]["scope"], "none")
            self.assertTrue(contract["image_system"]["production_stages"])
            self.assertEqual(contract["image_system"]["production_jobs"], [])
            image_policy = contract["image_system"]["execution_policy"]
            self.assertEqual(image_policy["production_pack_path"], "prompts/image-generation-pack.md")
            self.assertTrue(image_policy["distinct_asset_per_job"])
            self.assertTrue(image_policy["independent_jobs_may_parallelize"])
            self.assertTrue(image_policy["dependent_jobs_require_approved_inputs"])
            self.assertTrue(image_policy["derivatives_restart_from_declared_parent"])
            self.assertTrue(image_policy["project_bound_persistence"])
            self.assertTrue(image_policy["non_destructive_outputs"])
            self.assertIn("not automatically an image-model input", image_policy["host_reference_rule"])
            self.assertTrue(contract["image_system"]["delivery"])
            self.assertTrue(contract["image_system"]["evidence"])
            self.assertEqual(contract["video_system"]["scope"], "none")
            self.assertFalse(contract["video_system"]["generation_policy"]["paid_generation"])
            self.assertEqual(contract["video_system"]["generation_policy"]["max_attempts"], 1)
            self.assertTrue(contract["video_system"]["generation_policy"]["tool_discovery_required"])
            self.assertTrue(contract["video_system"]["quality_gate"]["hard_floors"])
            self.assertEqual(contract["motion_system"]["scope"], "none")
            self.assertTrue(contract["motion_system"]["accessibility_equivalents"])
            self.assertTrue(contract["motion_system"]["evidence"])
            self.assertNotIn("continuity_system", contract)
            self.assertNotIn("direction_selection", contract["visual_grammar"])
            self.assertNotIn("diagnostic_escalation", contract["evidence_contract"])
            self.assertEqual(contract["evidence_contract"]["environment_matrix"], [])
            self.assertIn("exact environment", contract["evidence_contract"]["support_claim_rule"])

            asset_ledger = (destination / "assets" / "asset-ledger.csv").read_text(encoding="utf-8-sig")
            self.assertTrue(
                asset_ledger.startswith("asset_id,filename,role,routes,source_type,source_or_rights,lineage_stage,parent_asset_ids,reference_asset_ids")
            )
            self.assertIn("capability_decision_ids,evidence_ids", asset_ledger)

            evidence_matrix = (destination / "evidence" / "evidence-matrix.csv").read_text(encoding="utf-8-sig")
            self.assertTrue(
                evidence_matrix.startswith("evidence_id,contract_revision,capability_decision_ids,asset_ids,exact_state")
            )

            platform_matrix = (destination / "evidence" / "platform-evidence-matrix.csv").read_text(encoding="utf-8-sig")
            self.assertTrue(platform_matrix.startswith("environment_id,operating_system,architecture,browser,browser_engine"))

            review = json.loads(
                (destination / "reviews" / "review-template.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(review["capability_scope"]["reviewed_ids"], [])
            self.assertEqual(review["capability_scope"]["unreviewed_ids"], [])
            self.assertEqual(review["review_provenance"], [])

            handoff = json.loads(
                (destination / "handoffs" / "sitecraft-handoff.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(handoff["project"]["name"], "Example Website")
            self.assertEqual(
                handoff["contract"]["reference"], "contracts/experience-contract.json"
            )
            self.assertEqual(handoff["contract"]["continuity_anchor_ids"], [])
            self.assertEqual(handoff["contract"]["continuity_state_dimension_ids"], [])
            self.assertTrue(
                handoff["execution"]["receiving_host_must_rediscover_capabilities"]
            )
            self.assertEqual(handoff["coordination"]["workspace_mode"], "unknown")
            self.assertEqual(
                handoff["coordination"]["checkout_status"], "revalidate_required"
            )
            self.assertEqual(
                handoff["coordination"]["receiver_write_policy"],
                "read_only_until_handoff",
            )
            self.assertTrue(
                handoff["coordination"]["receiving_host_must_confirm_checkout_before_write"]
            )
            self.assertFalse(handoff["safety"]["permissions_carried_over"])
            self.assertFalse(handoff["safety"]["contains_hidden_reasoning"])
            self.assertFalse(handoff["safety"]["contains_private_transcript"])
            self.assertFalse(handoff["safety"]["contains_secrets"])

            with self.assertRaises(FileExistsError):
                WORKSPACE.create_workspace(destination, "Should Not Overwrite")

    def test_creative_control_modules_route_without_widening_kling(self) -> None:
        required = [
            "references/character-identity-board.md",
            "references/creative-dna-reference-analysis.md",
            "references/interactive-generated-motion.md",
            "references/minimax-h3-video.md",
            "references/pc-bridge-integration-upgrade.md",
            "tests/test_new_reference_modules.py",
        ]
        for relative in required:
            self.assertTrue((ROOT / relative).is_file(), relative)

        identity = (ROOT / "references" / "character-identity-board.md").read_text(encoding="utf-8")
        for fragment in ["RIGHT 25%", "LEFT 10%", "CENTER 65%", "exactly four", "top-down", "low-angle"]:
            self.assertIn(fragment, identity)
        self.assertNotIn("input_fidelity", identity)
        self.assertIn("execution surface", identity)

        dna = (ROOT / "references" / "creative-dna-reference-analysis.md").read_text(encoding="utf-8")
        for fragment in ["Extract", "Abstract", "Recombine", "Motion DNA", "DO NOT COPY", "PROOF NEEDED"]:
            self.assertIn(fragment, dna)

        interactive = (ROOT / "references" / "interactive-generated-motion.md").read_text(encoding="utf-8")
        for fragment in ["device orientation", "requestAnimationFrame", "prefers-reduced-motion", "Two-dimensional input rule", "Alpha WebP", "chroma MP4"]:
            self.assertIn(fragment, interactive)

        h3 = (ROOT / "references" / "minimax-h3-video.md").read_text(encoding="utf-8")
        for fragment in ["MiniMax-H3", "4–15", "2K", "7000", "9 reference images", "3 reference videos", "3 reference audios", "12 mixed reference items"]:
            self.assertIn(fragment, h3)
        self.assertIn("never alter or substitute the independent Kling route", h3)

        manifest = json.loads((ROOT / "pc-bridge.skill.json").read_text(encoding="utf-8"))
        hints = manifest["reference_hints"]
        kling_hint = next(hint for hint in hints if hint.get("terms") == ["Kling"])
        self.assertEqual(kling_hint["terms"], ["Kling"])
        h3_hint = next(hint for hint in hints if "MiniMax H3" in hint.get("terms", []))
        identity_hint = next(hint for hint in hints if "character identity board" in hint.get("terms", []))
        dna_hint = next(hint for hint in hints if "Creative DNA" in hint.get("terms", []))
        interactive_hint = next(hint for hint in hints if "interactive generated motion" in hint.get("terms", []))
        self.assertIn("references/minimax-h3-video.md", h3_hint["paths"])
        self.assertIn("references/character-identity-board.md", identity_hint["paths"])
        self.assertIn("references/creative-dna-reference-analysis.md", dna_hint["paths"])
        self.assertIn("references/interactive-generated-motion.md", interactive_hint["paths"])
        generic_video = next(hint for hint in hints if "generated website video" in hint.get("terms", []))
        self.assertNotIn("MiniMax H3", generic_video["terms"])
        self.assertNotIn("Kling", generic_video["terms"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
