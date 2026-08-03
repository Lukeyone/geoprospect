# GeoProspect Stage 0 Issue Index

**Parent gate:** [#1 — Stage 0 feasibility audit and GO/SWITCH/STOP gate](https://github.com/Lukeyone/geoprospect/issues/1)  
**Evidence register:** [`docs/stage0/evidence_register.csv`](evidence_register.csv)  
**Stage 1 status:** BLOCKED

This index maps every decomposed execution step after Step 0.1 to its tracking issue. Issues are execution controls and audit records; routine pull requests do not wait for manual owner review.

| Step | Work unit | Issue | Primary dependency |
|---|---|---:|---|
| 0.2 | Create the evidence register | [#4](https://github.com/Lukeyone/geoprospect/issues/4) | Step 0.1 |
| 0.3 | Confirm repository architecture | [#5](https://github.com/Lukeyone/geoprospect/issues/5) | #4 |
| 0.4 | Bootstrap the Python project | [#6](https://github.com/Lukeyone/geoprospect/issues/6) | #5 |
| 0.5 | Add CI, security and contribution controls | [#7](https://github.com/Lukeyone/geoprospect/issues/7) | #6 |
| 0.6 | Define Stage 0 data contracts | [#8](https://github.com/Lukeyone/geoprospect/issues/8) | #7 |
| 0.7 | Discover current authoritative sources | [#9](https://github.com/Lukeyone/geoprospect/issues/9) | #8 |
| 0.8 | Validate licensing and attribution | [#10](https://github.com/Lukeyone/geoprospect/issues/10) | #9 |
| 0.9 | Design occurrence acquisition | [#11](https://github.com/Lukeyone/geoprospect/issues/11) | #9, #10 |
| 0.10 | Acquire and identify occurrence snapshot | [#12](https://github.com/Lukeyone/geoprospect/issues/12) | #11 |
| 0.11 | Profile occurrence quality | [#13](https://github.com/Lukeyone/geoprospect/issues/13) | #12 |
| 0.12 | Build commodity alias registry | [#14](https://github.com/Lukeyone/geoprospect/issues/14) | #13 |
| 0.13 | Compare candidate commodity definitions | [#15](https://github.com/Lukeyone/geoprospect/issues/15) | #14 |
| 0.14 | Design provisional deduplication rules | [#16](https://github.com/Lukeyone/geoprospect/issues/16) | #15 |
| 0.15 | Run provisional deduplication | [#17](https://github.com/Lukeyone/geoprospect/issues/17) | #16 |
| 0.16 | Define candidate study areas | [#18](https://github.com/Lukeyone/geoprospect/issues/18) | #17 |
| 0.17 | Create provisional cells and blocks | [#19](https://github.com/Lukeyone/geoprospect/issues/19) | #18 |
| 0.18 | Audit geology and structures coverage | [#20](https://github.com/Lukeyone/geoprospect/issues/20) | #19, #9 |
| 0.19 | Audit magnetics and gravity coverage | [#21](https://github.com/Lukeyone/geoprospect/issues/21) | #19, #9 |
| 0.20 | Evaluate spatial spread and fold feasibility | [#22](https://github.com/Lukeyone/geoprospect/issues/22) | #17, #19–#21 |
| 0.21 | Assess exploration-bias risk | [#23](https://github.com/Lukeyone/geoprospect/issues/23) | #20–#22 |
| 0.22 | Build candidate comparison matrix | [#24](https://github.com/Lukeyone/geoprospect/issues/24) | #20–#23 |
| 0.23 | Evaluate formal gate | [#25](https://github.com/Lukeyone/geoprospect/issues/25) | #24 |
| 0.24 | Write feasibility report | [#26](https://github.com/Lukeyone/geoprospect/issues/26) | #25 |
| 0.25 | Record ADR-001 and final decision | [#27](https://github.com/Lukeyone/geoprospect/issues/27) | #25, #26 |
| 0.26 | Produce Stage 1 handover or withhold authorisation | [#28](https://github.com/Lukeyone/geoprospect/issues/28) | #27 |

## Control rule

A step issue may close only when its named evidence exists and its acceptance criteria are satisfied. Closing a step issue does not unblock Stage 1. Only the final Stage 0 decision package can do so.
