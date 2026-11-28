# SPDX-FileCopyrightText: Portions Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

import os
from pathlib import Path

from garak import cli, _config

CODEPATH_PREFIX = "_garak_test_hitlog_codepath"


def test_hitlog_codepath():

    args = f"-m test.Blank --report_prefix {CODEPATH_PREFIX} -p test.Test -d always.Fail".split()
    cli.main(args)
    report_path = Path(_config.transient.report_filename).parent
    assert os.path.isfile(report_path / f"{CODEPATH_PREFIX}.hitlog.jsonl")


def test_hitlog_not_appended_across_runs():
    # two runs in one process writing to the same prefix: the report is
    # rewritten, so the hitlog must be rewritten too, not appended to
    prefix = CODEPATH_PREFIX + "_rerun"
    args = f"-m test.Blank --report_prefix {prefix} -p test.Test -d always.Fail -g 1".split()
    hitlog_lines = []
    for _ in range(2):
        cli.main(args)
        hitlog_path = Path(
            _config.transient.report_filename.replace(".report.", ".hitlog.")
        )
        with open(hitlog_path, encoding="utf-8") as hitlog:
            hitlog_lines.append(len(hitlog.readlines()))
    assert hitlog_lines[0] > 0
    assert hitlog_lines[1] == hitlog_lines[0]
