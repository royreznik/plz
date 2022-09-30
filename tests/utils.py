from click.testing import Result


def assert_cli_output(
    result: Result,
    *,
    expected_stdout: str = "",
    expected_stderr: str = "",
    expected_exit_code: int = 0,
) -> None:
    trace_output = (
        f"stdout: {result.stdout}\n"
        f"stderr: {result.stderr}\n"
        f"exception: {result.exception}\n"
        f"trace: {result.exc_info[2].tb_frame if result.exc_info else ''}"
        f"exit code: {result.exit_code}"
    )

    assert result.exit_code == expected_exit_code, trace_output
    assert expected_stdout in result.stdout, trace_output
    assert expected_stderr in result.stderr, trace_output
