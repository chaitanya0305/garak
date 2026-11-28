import re

from garak import cli


def passed_function(prompt: str, **kwargs):
    return [""]


def passed_function_multi(prompt: str, generations: int, **kwargs):
    return [""] * generations


def test_function_single(capsys):

    args = [
        "-m",
        "function",
        "-n",
        f"{__name__}#passed_function",
        "-p",
        "test.Blank",
    ]
    cli.main(args)
    result = capsys.readouterr()
    last_line = result.out.strip().split("\n")[-1]
    assert re.match("^✔️  garak run complete in [0-9]+\\.[0-9]+s$", last_line)


def test_function_multiple(capsys):

    args = [
        "-m",
        "function.Multiple",
        "-n",
        f"{__name__}#passed_function_multi",
        "-p",
        "test.Blank",
    ]
    cli.main(args)
    result = capsys.readouterr()
    last_line = result.out.strip().split("\n")[-1]
    assert re.match("^✔️  garak run complete in [0-9]+\\.[0-9]+s$", last_line)


targets_called = []


def target_a(prompt: str, **kwargs):
    targets_called.append("a")
    return ["reply from a"]


def target_b(prompt: str, **kwargs):
    targets_called.append("b")
    return ["reply from b"]


def test_function_second_run_uses_its_own_target():
    # garak.cli.main can be invoked more than once in one process; each run
    # must load the target it names, not reuse the previous run's generator
    targets_called.clear()
    for target in ("target_a", "target_b"):
        cli.main(
            [
                "--target_type",
                "function",
                "--target_name",
                f"{__name__}#{target}",
                "--spec",
                "probes.test.Blank",
                "-g",
                "1",
            ]
        )
    assert targets_called == ["a", "b"]
