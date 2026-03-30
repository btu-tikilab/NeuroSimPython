<!-- AUTH:DEVNEUROSIM:7A3F9E2B | README.md -->
# NeuroSim (Python Library)

This folder is the non-.NET Python/prototype side of NeuroSim.

Key artifacts:
- `ConceptDiagram.png`: architecture concept image.
- `samples/poc/`: pure-Python toy POCs (no machine-specific deps).
- `workHour/teamBeta_<Member>.csv`: manual work-hour entries.

## Edit WorkHour CSVs

Files:
- `workHour/teamBeta_<Member>.csv`

Required CSV header:

`entry_id,date,start_time,end_time,work_done`

How to edit:
- Add one new row per work block.
- Keep `date` format as `YYYY-MM-DD`.
- Keep `start_time` and `end_time` as `HH:MM` or `HH:MM:SS` (24-hour format).
- If work crosses midnight, keep same `date` and use an `end_time` earlier than `start_time` (example below).

Example:

`8,2026-03-31,09:00:00,11:30:00,Debugged training loop`

`9,2026-03-31,22:00:00,00:30:00,Night run monitoring`


![ConceptDiagram](ConceptDiagram.png)

Note: Please update NeuroSim\scripts\compliance.config.json for compliance checks. Also apply NeuroSim\scripts\apply_devneurosim_signatures.py for signing the work

