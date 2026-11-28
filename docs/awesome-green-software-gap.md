# Gap between the GSF awesome-green-software list and this landscape

Comparison of <https://github.com/Green-Software-Foundation/awesome-green-software> (readme at commit `eac3166`, 2026-11-01) with `data.yml` (134 items), checked 2026-11-28.

The list has 87 entries under Tooling. 41 of them are already in the landscape, 46 are not; those 46 are judged below. "In list since" is the year the entry first appeared in the list's `readme.md`, taken from its git history, so the 2026 column is what the list added this year.

Facts behind the judgements come from the repositories themselves: latest push, archive flag, licence, stars. Age claims are therefore dated, not estimated.

Fit follows the four prerequisites in `README.md`. Methodology documentation is required of a tool that computes a metric; a scheduler, linter or rule pack that outputs no number is judged on user documentation and status instead, and is not held to a measurement method it has no use for.

A `second_path` has to land in a subcategory whose own entries are of that kind: `Artificial Intelligence / AI Inference` holds only measurement tools, and so does `Desktop & Mobile / Mobile Application`. A scheduler, a factor dataset or a rule pack stays in its primary category.

To produce a new snapshot, run the skill `.agents/skills/check-awesome-list/SKILL.md`; it carries the procedure and the judgement categories, this file carries the result.

## Listed there, missing here

### Fit: yes

| Name | In list since | What it is | URLs | Proposed category | Fit |
|---|---|---|---|---|---|
| Tidegap (listed as `ebb-ai`) | 2026 | MCP server and CLI that defer non-urgent LLM tasks to the cleanest grid hour before a deadline from a 72 h forecast across 31 regions, with signed carbon receipts in a local SQLite ledger | <https://www.tidegap.com/> · <https://github.com/tidegap/tidegap> | Optimization / Carbon Awareness | Yes: Apache-2.0, 3 stars, pushed 2026-11-25; `/docs` covers install and both libraries, and the carbon figures rest on a method paper plus a claims audit that names the source of every number. The list's `ebb-ai.com` URL redirects and the repo was renamed, so that entry is stale |
| SOMA AI Emission Factors (SAEF) | 2026 | Open dataset of kg CO2e, energy and water factors per million tokens by model class and 143 cloud regions, plus a standard-library Python calculator | <https://doi.org/10.5281/zenodo.20443585> | Databases / IT Emission Inventory | Yes: Zenodo v3.5 with selftest scripts and the method in Sustainable Production and Consumption 70 (2026). The data licence is non-commercial — a company needs a paid licence — and with no repository the `license` field is set by hand |
| The AI Footprint | 2026 | Leaderboard of electricity and CO2 per answer for about 270 generative models, computed with EcoLogits and a published calibration factor, with per-model pages | <https://theaifootprint.com/> · <https://theaifootprint.com/methodology> | Artificial Intelligence / AI Benchmarks & Leaderboards | Yes: formulas, data sources and error margin stated on the methodology page |
| GreenCalculus | 2026 | Python and JavaScript clients for grid carbon intensity and 16,673 greenhouse-gas emission factors from DEFRA, US EPA, ADEME and IPCC, each returned with its source cell and data version | <https://greencalculus.com/> · <https://github.com/greencalculus/greencalculus-sdk> | Databases / IT Emission Inventory | Yes: every factor returns its source id and spreadsheet cell, and the API echoes the formula; factors answer without a key, `/v1/calculate` needs one |
| GreenScheduled | 2026 | Apache-2.0 Java library adding a `@GreenScheduled` annotation that shifts Spring Boot and Quarkus jobs to the lowest-carbon hour in a window via the carbonintensity.io API | <https://github.com/carbonintensityio/green-scheduler> | Optimization / Carbon Awareness | Yes: Apache-2.0, 18 stars, 0.8.6 on Maven Central, usage docs; it moves work to a greener hour and computes no metric, so no methodology is owed |
| carbon-badge | 2026 | GitHub Action that sums 30 days of CI job runtime, prices each job at its runner's power draw and publishes the result as a Shields.io endpoint badge, each figure flagged measured, declared or guessed | <https://github.com/fabiocicerchia/carbon-badge> · <https://fabiocicerchia.github.io/carbon-badge/> | Code / CI Pipeline | Yes: Apache-2.0, every figure labelled measured, declared or guessed, and the runner wattages and assumptions documented in the repo |
| Greenlint | 2026 | Static linter flagging energy-wasteful patterns in code and CI/Kubernetes configs — busy loops, every-minute crons, `SELECT *`, fat base images, missing resource limits — each finding with a reason and a fix | <https://github.com/fabiocicerchia/greenlint> · <https://fabiocicerchia.github.io/greenlint/> | Code / Static Code Analysis | Yes: Apache-2.0 with a docs site and `/docs`; it emits findings with a fix and no number, so no methodology is owed — 0.x, rule set still growing |
| Joule Profiler | 2026 | Rust CLI and library profiling program energy from RAPL, perf_event and NVML at process and cgroup scope, with per-phase breakdown beacons | <https://joule-profiler.github.io/> · <https://github.com/joule-profiler/joule-profiler> | Device & Process Level / Process Metrics Exporter, `second_path` Code / Code Level Energy Measurement | Yes: MIT, 20 stars, pushed 2026-11-10; the docs site names every source (RAPL, perf_event, NVML) and the CLI usage |
| CometWeb Carbon Badge | 2026 | MIT web component showing a modelled CO2e estimate per page view using a documented Sustainable Web Design Model v4 first-load approximation, with the method visible in the badge | <https://github.com/CometWeb-io/Carbon-Badge> · <https://carbon-badge.cometweb.io/> | Website / Website Carbon Estimation | Yes: MIT, method in `docs/reference.md` as a SWDM v4 first-load lite approximation, and unknown resource sizes show N/D instead of a guess |
| Grammage | 2026 | Commercial French website carbon audit: 100-point score and CO2e per visit from a real visitor load, runnable from CI/CD, with a verifiable attestation | <https://getgrammage.com/en/> · <https://getgrammage.com/en/method/> | Website / Website Carbon Estimation | Yes: five-step method page with a repeatable `grammage-1` protocol, plus a free trial and Docker/CI guides; commercial, but the landscape lists commercial tools already |
| FreeIPMI | 2021 | Reads power consumption of a bare-metal machine through DCMI, the IPMI extension | <https://www.gnu.org/software/freeipmi/> | Device & Process Level / Device Measurement | Yes: GNU package, 1.6.20 on 2026-10-05, manual and FAQ; it reads DCMI power sensors and computes nothing, so no methodology is owed. A per-machine sensor reader, not a monitoring stack, so it stays out of Bare-Metal & Host Level

### Fit: partial

| Name | In list since | What it is | URLs | Proposed category | Fit |
|---|---|---|---|---|---|
| Vessim | 2024 | Co-simulation testbed connecting renewable-generation and energy-storage simulators to real software and hardware, published at HotCarbon'24 | <https://vessim.readthedocs.io/en/latest/> · <https://github.com/dos-group/vessim> | Optimization / Carbon Awareness | Partial: 103 stars, active research testbed; no simulation subcategory exists here, and it measures nothing by itself |
| FedZero | 2024 | Federated learning system targeting zero-carbon distributed AI training, successor to Lowcarb (CarbonHack 2022) | <https://github.com/dos-group/fedzero> | Artificial Intelligence / AI Model Training | Partial: research prototype that needs a cluster, no user workflow that yields a CO2e number; 25 stars |
| CarbonLint | 2026 | Tauri/Rust desktop app plus npm CLI tracking CPU, memory, disk, network and GPU use, converting it to CO2 with regional grid intensity, 0–100 Green Score and CI carbon budgets | <https://github.com/nishal21/CarbonLint> · <https://nishal21.github.io/CarbonLint/> | Desktop & Mobile / Desktop Application, `second_path` Code / Code Level Energy Measurement | Partial: only a three-step description of the model, no methodology page, no LICENSE file, 3 stars |
| Carbon Aware Computing Hangfire Extension | 2024 | Hangfire extension that schedules jobs into the lowest-carbon window of the grid-intensity forecast | <https://github.com/bluehands/Hangfire.Community.CarbonAwareExecution> | Optimization / Carbon Awareness | Partial: maintained (last push 2025-10), 12 stars, but it is a thin .NET wrapper around the same maintainers' service we already list as Carbon-Aware-Computing.com |
| Kernel Tuner | 2023 | Auto-tuner for CUDA and OpenCL kernels that can optimise for energy efficiency through a performance model | <https://github.com/KernelTuner/kernel_tuner> | Optimization / Application Profiling | Partial: 427 stars and very active, but a general performance-tuning tool where energy efficiency is one documented example, not its purpose |
| Globemallow.io | 2022 | Browser extension producing sustainable web development and design reports, plus an analytics and ad blocker that reduces page-load energy | <https://globemallow.io/> · <https://github.com/con-schy1/Globemallow> | Website / Website Analysis | Partial: Apache-2.0 and last pushed 2025-12, but 1 star and no published method for the report figures |
| Perennova Scanner | 2026 | Free server-side scan reporting downloaded bytes by type, request count, third-party hosts and cache headers, scored out of 20 with each point tied to a measured fact | <https://perennova.eu/en/scanner/> | Website / Website Analysis | Partial: it reports downloaded bytes, request count and cache headers, transparent but with no carbon figure at all, so what a green landscape gains is the scan, not a metric; the list's `perennova-eco.github.io` URL redirects |
| ShiftPress Website Carbon Calculator | 2026 | Free estimator: PageSpeed-measured mobile page weight × Sustainable Web Design Model v4 (0.3 kWh/GB) × 494 g CO2e/kWh from Ember, plus claimed waste savings | <https://shiftpress.ai/carbon-check> | Website / Website Carbon Estimation | Partial: the formula is stated on the page, but there is no user documentation beyond a marketing surface, which is the prerequisite it misses |
| CO2_RAPL | 2026 | CC0 bash script reading Intel RAPL counters to monitor a Linux server's CPU energy in real time and estimate the associated CO2 | <https://github.com/Institut-du-Numerique-Responsable/CO2_RAPL> | Device & Process Level / Device Measurement, `second_path` Infrastructure & Cluster Level / Bare-Metal & Host Level | Partial: 1 star and French-only docs; fine as the small RAPL script it is |
| powercfg | 2021 | Built-in Windows CLI whose `/energy`, `/batteryreport` and `/sleepstudy` switches produce reports on energy-efficiency problems and battery wear | <https://learn.microsoft.com/en-us/windows-hardware/design/device-experiences/powercfg-command-line-options> | Desktop & Mobile / Desktop Application | Partial: a general-purpose OS tool with no carbon or energy figure of its own; the entry would document where to look, not what it computes |
| carbon-text | 2025 | Syntax highlighter and snippets for carbon.txt files | <https://github.com/ShayokhShorfuddin/carbon-text> | Website / Website Analysis | Partial: editor snippets for one disclosure file — no analysis, no metric, 2 stars, and it neither measures nor optimises anything |
| Green CodeQL | 2026 | GPL-3.0 CodeQL query packs flagging energy-related sustainability issues, covering Java/Kotlin, Python, C/C++, JavaScript, C# and GitHub Actions | <https://github.com/green-code-initiative/green-codeql-queries> | Code / Static Code Analysis | Partial: GPL-3.0, README how-to and a project page, but the repo labels itself experimental rather than beta, which is the prerequisite it misses; revisit when that changes. Reported here rather than added because Creedengo and creedengo-ios already carry the eco-design rule idea

### Fit: no

| Name | In list since | What it is | URLs | Proposed category | Fit |
|---|---|---|---|---|---|
| 1ClickImpact | 2025 | Commercial API and platform for offsetting carbon emissions from AI workloads with Zapier integration | <https://1clickimpact.com> | — | No: offsetting, not measurement; nothing about the platform's figures is published |
| 1ClickImpact Sustainability API | 2025 | REST API for embedding tree planting, carbon capture and ocean cleanup actions into software | <https://docs.1clickimpact.com/> | — | No: same vendor, offsetting not measurement |
| AXIOMAX ESG Carbon Shield | 2026 | MIT SDK (Python, Node, Bash) signing AI inference calls with ed25519 and SHA-256 hash chains to produce auditable carbon attestations for CSRD/SEC reporting | <https://github.com/axiomaxllc/esg-carbon-shield> | Artificial Intelligence / AI Inference | No: calibration coefficients and keys stay server-side, so how the CO2e is derived is not published; 1 star, patent-pending vendor repo |
| Carbon Service REST API | 2025 | REST API exporting the data behind the Emissions Impact Dashboard and Azure Carbon Optimization | <https://learn.microsoft.com/rest/api/carbon/carbon-service> | — | No: the API of an entry already listed (Azure Carbon Optimization) — it belongs in that entry's `documentation_url`, not as a second entry |
| Well-Architected Framework for Sustainable Workloads | 2025 | Microsoft guidance on designing Azure workloads per Green Software Foundation practice | <https://learn.microsoft.com/azure/well-architected/sustainability/sustainability-get-started> | — | No: a guidance document, not a tool; the landscape holds tools |
| Cloud Jewels | 2021 | Etsy's energy-estimation coefficients and scripts converting GCP billing data into trailing 30-day kWh estimates; unmaintained since 2020 | <https://github.com/etsy/cloud-jewels> | — | No: a coefficient set and method, not a runnable tool; Cloud Carbon Footprint and Boavizta now carry that method, last upstream push 2022-01 |
| Carbonifer | 2023 | CLI to estimate and control the carbon emissions of cloud infrastructure before it is provisioned | <https://github.com/carboniferio/carbonifer> | Infrastructure & Cluster Level / Planning & Calculation | No: unmaintained — last upstream commit 2024-07-13, Apache-2.0, 106 stars; would otherwise fit planning and calculation |
| carbon-budget-action | 2026 | GitHub Action failing a PR when a deployment's estimated carbon exceeds a configured gCO2e budget | <https://github.com/fabiocicerchia/carbon-budget-action> | Code / CI Pipeline | No: repository archived and retired; the gate lives on as the `--budget` flag of <https://github.com/fabiocicerchia/sci-disclose>, which would be the better entry (SCI per command, function, repo or declared deployment) |
| energy-consumption-measuring-toolkit | 2024 | Accenture's RAPL-based toolkit measuring the energy consumption of Python applications | <https://github.com/Accenture/energy-consumption-measuring-toolkit> | Code / Code Level Energy Measurement | No: no licence, 7 stars, last push 2024-05, and it duplicates PyRAPL and CodeCarbon which are listed |
| Carbon AppInsights | 2023 | Azure Functions solution logging Electricity Maps data for Azure regions into Azure Monitor for alerting | <https://github.com/cloudyspells/carbon-appinsights> | — | No: last push 2023-04, thin integration whose data source we already list as Electricity Maps |
| PSElectricityMaps | 2023 | PowerShell module retrieving grid carbon data with an Electricity Maps account | <https://github.com/cloudyspells/PSElectricityMaps> | — | No: last push 2023-09, thin wrapper over a listed data source |
| PSWattTime | 2023 | PowerShell module retrieving grid carbon data with a WattTime account | <https://github.com/cloudyspells/PSWattTime> | — | No: last push 2023-03, thin wrapper over a listed data source |
| SEOCheck-AI | 2026 | Free 60-check SEO and performance audit (payload, DOM complexity, TTFB, caching, AI-crawler readiness) framed as reducing digital emissions | <https://seocheck-ai.com/free-seo-check> | Website / Website Analysis | No: no carbon methodology at all — an SEO tool with a green pitch |
| Energy Rebate Calculator | 2026 | US home energy rebate finder covering HOMES and HEAR programmes, heat pumps and insulation credits | <https://energyrebatecalculator.com/> | — | No: outside green software; the list itself flags this entry as unrelated |
| SunEco BESS Sizer | 2026 | Load-profile modelling and sizing simulation for commercial battery storage and industrial peak shaving | <https://suneco.com.ua/> · <https://github.com/romangrid/suneco-bess-sizing> | — | No: energy hardware sizing, outside the IT scope of this landscape |
| WeDeex | 2021 | Chrome and Edge extension estimating browsing CO2 locally from transferred data volume; unmaintained, last updated 2021 | <https://chromewebstore.google.com/detail/wedeex/ojlagggckhpedblhemgjhecbggnibale> | — | No: unmaintained for five years |
| WedeexApp | 2021 | UWP sample app demonstrating the Wedeex API by showing French grid intensity and Surface power draw | <https://github.com/Wedeex-DevTeam/WedeexApp> | — | No: last push 2021-02, and a sample app rather than a tool |
| ipmitool | 2021 | Reads power consumption of a bare-metal machine through DCMI | <https://github.com/ipmitool/ipmitool> | — | No: the repository is archived (last push 2023-02); FreeIPMI is the maintained alternative and is the better entry |
| turbostress | 2021 | Load generator that reports the machine's power metrics under the generated load | <https://github.com/teads/turbostress> | — | No: last push 2021-03, no licence, 27 stars |
| Beacon | 2022 | Online and bookmarklet report on the environmental impact of a single web page | <https://digitalbeacon.co/> | — | No: another website carbon calculator among the seven already listed, with no distinguishing method |
| Carbonara | 2023 | Custom element from Digital4Better displaying the carbon footprint of web navigation | <https://github.com/digital4better/carbonara> | — | No: unmaintained — last upstream push 2023-03, 11 stars, and it duplicates CO2.js in effect |
| Carbon Footprint of Sending Data | 2021 | Observable notebook estimating network-traffic emissions from The Shift Project's Lean ICT report | <https://observablehq.com/@mrchrisadams/carbon-footprint-of-sending-data-around> | — | No: a one-page notebook with no maintenance and no user documentation |

## In both, under a different name

| In the awesome list | In this landscape |
|---|---|
| CAST Highlight | CAST (`castsoftware.com/highlight`) |
| Customer Carbon Footprint Tool | AWS Sustainability Console (the tool's successor) |
| OVHcloud Carbon Calculator | OVHcloud Environmental Impact Tracker (the list links the same tool's PDF) |
| oaklean.io | oaklean (the list links the `.io` marketing domain) |
| CO2Scope | CO2 Scope® (by EasyVirt) |
| Carbon Aware Computing — Tools and Free Forecast Data | Carbon-Aware-Computing.com |
| Creedengo (formerly ecoCode) | Creedengo |
| PowDroid | PowDroid (the list links the GitHub repo, the landscape the project page) |

Also new in the list this year and already covered here: `claude-carbon`, `Compute Gardener Scheduler`, `webNRG`.

`creedengo-ios` needs no entry of its own: the Creedengo entry links `creedengo-rules-specifications`, the shared rule catalogue, and its description names no platform, so the iOS plugin for that catalogue is already the project the entry stands for. Another platform is not another method — compare `JoularJX` and `PowerJoular`, which are separate because one is a Java agent and the other a host-level CLI.

## In this landscape, not in the list (93)

No judgement needed — these are the entries the list lacks, the five mapping rows above excluded.

- Infrastructure & Cluster Level / Public Cloud: Scaleway Environmental Footprint Calculator, Li10 for AWS, Boavizta Cloud-Scanner for AWS, Tailpipe, Greenpixie GPX, Cloud Assess, SPRUCE, Carbon Measurement Engine (Carmen)
- Infrastructure & Cluster Level / Kubernetes: KEIT
- Infrastructure & Cluster Level / Bare-Metal & Host Level: Dynatrace Cost & Carbon Optimization
- Infrastructure & Cluster Level / Planning & Calculation: Datavizta, EasyVirt Eclyo, Cloud Project Carbon Emission Simulator by OxygenIT, Green Algorithms Calculator, Data Center Water Consumption Calculator, Hardware Replacement Calculator, Technology Carbon Estimator
- Full-Stack Application: Cardamon, OpenTelemetry Java Agent Extension, LIMo
- Desktop & Mobile: Power Hog, Watt Wiser, Android Power Profiler, Greenspector Studio, Android Runner
- Code: jPowerMonitor, DotNet-Counters, PyRAPL, perun, Coppers, aDoctor
- Artificial Intelligence: AI Power Meter, ML CO2 Impact, Green Algorithms Calculator (AI), Green Coding AI, EcoLogits, Token & CO2 Dashboard, CLEER, AI Energy Score, LLM-Perf Leaderboard
- Databases: Energy-Charts, ENTSO-E Transparency Platform, Carbon-Intensity UK, Electricity Maps, WattTime, BoaviztAPI, Climatiq, ResilioDB, Base Empreinte, OxygenIT
- Data Aggregation: CarbonDB, Sopht, Resilio Tech, Verdikt, Aguaro, Antarctica, Impact Framework, Carbon Footprint Modeling Tool, e-footprint model
- Device & Process Level: Powerstat, Perf, Turbostat, NVIDIA SMI, Intel PCM, Cloud Energy, EnergiBridge, CPU Energy Meter, procpower, powerletrics, Energy Monitoring Tool, EnergAt
- Website: Klimatest, Website Carbon Meter, Safari Web Inspector, Firefox Power Profiler
- Measurement Utilities / Automation: Experiment Runner
- Optimization: IBM Turbonomic, IBM Txture, Cycloid, EcoInfra, Elastic Universal Profiling, KEDA, Goldilocks, Karpenter, DailyClean, Carbon Aware KEDA Operator, CLEVER, GoKubeDownscaler, grid-intensity-go, Camunda Carbon Reductor, Grid-aware Websites, VSCarbon, Pruna AI
