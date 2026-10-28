---
name: netsupport-nperf-speedtest
description: Test the internet speed of each authorized NetSupport School computer with nPerf through Tech Console, and save per-machine results.
---

# NetSupport nPerf speed tests

Use this for a request to speed-test specified NetSupport School computers, including “each machine” when the open Tech Console clearly supplies the group. Also follow `$netsupport-school-control` for remote access rules. A previous run does not authorize a new group. The desired result is one dated CSV row per target, plus a screenshot of each completed nPerf result.

## Establish the run

1. Inspect the **live** Tech Console. Record the names of connected target Students before acting. The selected row and remote view must identify the same machine before each test. Do not infer the target from a previous screenshot or rely on remembered window coordinates.
2. Make a new `nPerf-YYYY-MM-DD` folder in Documents for this run. Use `nperf-results-YYYY-MM-DD.csv` with `Machine,Download_Mbps,Upload_Mbps,Latency_ms,Jitter_ms,Server,Status`. If a file for today already exists, inspect it and resume missing machines; never duplicate a machine row or overwrite observed results.
3. Process targets **sequentially**. Do not start another test until the current machine is completed or marked unavailable.

## One-machine loop

1. Select exactly one Student in Tech Console; inspect the selected name. Open **View Client** and verify the remote desktop belongs to that Student. Honor any acknowledgment or access prompt.
2. From that remote view, use **Launch Application** to open Chrome at `https://www.nperf.com/en/`. A saved `nPerf speed test in Chrome` entry may exist; inspect its Properties once per run to confirm the command and URL before using it. Wait for the nPerf start screen. Keep the default Mb/s unit unless the user chose another. Close incidental browser prompts if necessary; do not grant location access or sign in.
3. Click **Start** once. Wait through download, upload, and latency until the finished page shows Share/Restart/Compare or an equivalent completed result. Do not use a transient gauge reading as a result and do not click Restart to get a screenshot.
4. On the finished page, read the small labeled **Average** download, **Average** upload, **Average** latency, and jitter values. The large gauge numbers are different. Scroll enough to show all result cards, dismissing only overlays that hide them. Read the selected server. Save the full visible result as `Machine-<name>.png` in the run folder; the prefix avoids Windows reserved names such as `COM1`.
5. Record one CSV row with the observed values and `Status=Completed`. If a value is absent, leave that CSV field blank. Close the remote view; leave Tech Console open and continue to the next selected Student.

If the browser is taken over by an active user, stop interacting with that machine rather than competing for focus. If Chrome or nPerf fails to load, inspect the error and make at most one appropriate reload or launch retry. If no finished result is observed, append one row with blank measurements and a specific `Unavailable - ...` status, then continue. Never claim a test completed because it started.

## Desktop-control fallback on this Windows host

Prefer a working desktop-control tool. If its connection is unavailable, the bundled [desktop.ps1](scripts/desktop.ps1) can operate the **visible interactive session** through PowerShell. First capture and inspect the PNG with an image-view tool; proceed only if it shows the current Tech Console. Each click, wheel, or key action also saves a fresh capture. Examples:

```powershell
$scripts = Join-Path $env:USERPROFILE '.codex\skills\netsupport-nperf-speedtest\scripts'
& (Join-Path $scripts 'desktop.ps1') -Action capture
& (Join-Path $scripts 'desktop.ps1') -Action click -X $x -Y $y
& (Join-Path $scripts 'desktop.ps1') -Action wheel -X $x -Y $y -Delta -240
```

Set `$x` and `$y` from the **latest** capture before each action. Bring Tech Console to the foreground if another window covers it. Check the selected row, dialog, and page after each consequential action. Screen layout, language, prompts, and window position can change. This script captures the primary screen only; if Tech Console is elsewhere or the screenshot is stale/blank, use another available interactive tool or report the blocker. Do not guess at clicks. UI automation does not bypass remote access controls.

Use [record-result.ps1](scripts/record-result.ps1) after each machine. It creates the dated CSV and screenshot, and rejects duplicate machine rows. The screenshot source must show the finished result. For example:

```powershell
& (Join-Path $scripts 'desktop.ps1') -Action capture -Out "$env:TEMP\nperf-$machine.png"
& (Join-Path $scripts 'record-result.ps1') -Machine $machine -Status Completed -DownloadMbps $observedDown -UploadMbps $observedUp -LatencyMs $observedLatency -JitterMs $observedJitter -Server $observedServer -Screenshot "$env:TEMP\nperf-$machine.png"
& (Join-Path $scripts 'record-result.ps1') -Machine $machine -Status 'Unavailable - browser switched during test'
```

Set `$machine` from the selected row and the `observed*` variables from its labeled result cards. Run **only the completed or unavailable command** for each machine. If an earlier capture fails, return to the completed page and capture again without restarting the test.

## Finish

Compare the CSV’s unique machine names with the target list. Confirm every completed row has its own result screenshot. Report completed machines and unavailable machines separately, with the dated CSV path. If desktop interaction is unavailable, state the concrete blocker and next Tech Console action; do not fabricate results.
