import pytest
from pytest import CaptureFixture, Pytester


@pytest.mark.attr(id="FN-DL-01")
async def test_download_existing_dataset(
  pytester: Pytester,
  capsys: CaptureFixture,
) -> None:
  """Check that 'chromie dl' downloads a given existing dataset."""

  # (1) act
  out = pytester.run("chromie", "dl", "eurostat/prc_hicp_manr")
  capsys.readouterr()

  # (2) assessment
  assert out.ret == 0
  out.stdout.re_match_lines_random("Downloading 'eurostat/prc_hicp_manr'")


@pytest.mark.attr(id="FN-DL-02")
async def test_download_existing_dataset_and_check(
  pytester: Pytester,
  capsys: CaptureFixture,
) -> None:
  """Check that 'chromie dl -c' downloads and checks a given existing dataset."""

  # (1) act
  out = pytester.run("chromie", "dl", "-c", "eurostat/prc_hicp_manr")
  capsys.readouterr()

  # (2) assessment
  assert out.ret == 0
  out.stdout.re_match_lines_random(
    (
      "Downloading 'eurostat/prc_hicp_manr'",
      "Checking",
    )
  )


@pytest.mark.attr(id="FN-DL-03")
async def test_download_nonexisting_dataset(
  pytester: Pytester,
  capsys: CaptureFixture,
) -> None:
  """Check that 'chromie dl' raises error if non-existing dataset."""

  # (1) act
  out = pytester.run("chromie", "dl", "eurostat/unknown")
  capsys.readouterr()

  # (3) assessment
  assert out.ret == 1
  out.stderr.re_match_lines_random((".*not found.*",))
