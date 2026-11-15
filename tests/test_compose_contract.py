#!/usr/bin/env python3
"""Development Compose contract exercised through the public Compose CLI."""

import json
import os
import pathlib
import subprocess
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]


def compose_config(project: str, port: int | None) -> dict:
    environment = os.environ | {"COMPOSE_DISABLE_ENV_FILE": "1"}
    if port is None:
        environment.pop("FRONTEND_PORT", None)
    else:
        environment["FRONTEND_PORT"] = str(port)
    result = subprocess.run(
        [
            "docker",
            "compose",
            "-f",
            "compose.yaml",
            "--project-name",
            project,
            "--profile",
            "ci",
            "config",
            "--format",
            "json",
        ],
        cwd=ROOT,
        env=environment,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


class ComposeDevelopmentContractTest(unittest.TestCase):
    def test_development_mounts_only_source_read_only(self) -> None:
        config = compose_config("frontend-contract-a", 14200)
        frontend = config["services"]["frontend"]

        mounts = frontend["volumes"]
        self.assertEqual(len(mounts), 2)
        self.assertEqual(
            {(mount["source"], mount["target"]) for mount in mounts},
            {
                (str(ROOT / "src"), "/app/src"),
                (str(ROOT / "public"), "/app/public"),
            },
        )
        for mount in mounts:
            self.assertEqual(mount["type"], "bind")
            self.assertTrue(mount["read_only"])

        self.assertNotIn("volumes", config["services"]["frontend-check"])

    def test_ports_and_project_names_allow_isolated_worktrees(self) -> None:
        default = compose_config("frontend-contract-default", None)
        alternate = compose_config("frontend-contract-b", 14200)

        self.assertEqual(default["name"], "frontend-contract-default")
        self.assertEqual(alternate["name"], "frontend-contract-b")
        self.assertEqual(default["services"]["frontend"]["ports"][0]["published"], "4200")
        self.assertEqual(alternate["services"]["frontend"]["ports"][0]["published"], "14200")
        self.assertEqual(alternate["services"]["frontend"]["ports"][0]["host_ip"], "127.0.0.1")


if __name__ == "__main__":
    unittest.main()
