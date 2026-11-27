# Methodology audit (issue #8)

Total tools: 134, all audited (InfluxData Telegraf was removed from the landscape during the audit)

> Row numbers are stable IDs. Sub-categories were renamed since the audit snapshot (`Infrastructure Provider Level` → `Public Cloud`, `Agent` → `Bare-Metal & Host Level`); CO2 Scope and Carmen were regrouped accordingly, and InfluxData Telegraf (#19) was removed from the landscape (generic metrics collector, verdict N). Tools added later live in the new sub-category `Artificial Intelligence/AI Benchmarks & Leaderboards` and got IDs 130–134.

Verdicts: **V**=explicit methodology page found | **R**=methodology info in README/docs/paper/sensor | **P**=methodology not public (on request only) | **I**=insufficient information (partial, unclear, or nothing found; needs team decision) | **N**=generic tool, no metric methodology

Requirement: for each output metric, the methodology documentation must describe the measurement or calculation approach, including data sources, key formulas and assumptions. Complete formulas are not required, but the basic method must be clear. A link counts only when the page itself describes that approach; naming a standard or a library is not enough.

| # | Tool | Cat | Verdict | Proposed/notes |
|---|------|-----|---------|----------------|
| 0 | Cloud Carbon Footprint | Infrastructure & Cluster Level/Public Cloud | V | https://www.cloudcarbonfootprint.org/docs/methodology |
| 1 | AWS Sustainability Console | Infrastructure & Cluster Level/Public Cloud | V | https://docs.aws.amazon.com/sustainability/latest/userguide/methodology.html existing link points to view-emissions, not methodology |
| 2 | Azure Carbon Optimization | Infrastructure & Cluster Level/Public Cloud | I | Reports emissions from Azure billing/subscription data, but the linked page shows results only: no calculation approach, data sources, or assumptions. |
| 3 | Google Carbon Footprint | Infrastructure & Cluster Level/Public Cloud | V | https://docs.cloud.google.com/carbon-footprint/docs/methodology |
| 4 | Scaleway Environmental Footprint Calculator | Infrastructure & Cluster Level/Public Cloud | V | https://www.scaleway.com/en/docs/environmental-footprint/additional-content/environmental-footprint-calculator/ |
| 5 | OVHcloud Environmental Impact Tracker | Infrastructure & Cluster Level/Public Cloud | V | existing methodology PDF |
| 6 | Li10 for AWS | Infrastructure & Cluster Level/Public Cloud | I | Lists its inputs (AWS Billing data, GSF SCI, Cloud Carbon Footprint library) but not how they produce the emissions number. |
| 7 | Boavizta Cloud-Scanner for AWS | Infrastructure & Cluster Level/Public Cloud | V | https://boavizta.github.io/cloud-scanner/explanations/methodology.html existing link is docs root |
| 8 | Green Cost Explorer for AWS | Infrastructure & Cluster Level/Public Cloud | I | README describes a cost-based green/grey split (AWS sustainable-region list), not a calculation approach for an emissions metric; no data sources or assumptions are given. |
| 9 | Tailpipe | Infrastructure & Cluster Level/Public Cloud | V | https://tailpipe.ai/methodology |
| 10 | Cloud Assess | Infrastructure & Cluster Level/Public Cloud | R | https://github.com/kleis-technology/cloud-assess#how-does-it-work LCA models / PCR; methodology in README + trusted_library |
| 11 | SPRUCE | Infrastructure & Cluster Level/Public Cloud | V | existing methodology.md |
| 14 | Carbon Measurement Engine (Carmen) | Infrastructure & Cluster Level/Public Cloud | V | existing docs/methodology.md |
| 13 | Kepler | Infrastructure & Cluster Level/Kubernetes | V | https://sustainable-computing.io/kepler/usage/power-attribution/ current power attribution docs (archive path is for Kepler <0.10) |
| 15 | KEIT | Infrastructure & Cluster Level/Kubernetes | R | README (repo homepage) documents the composition; no separate doc link |
| 16 | Scaphandre | Infrastructure & Cluster Level/Bare-Metal & Host Level | V | https://hubblo-org.github.io/scaphandre-documentation/index.html methodology spread across several docs pages |
| 17 | CEEMS | Infrastructure & Cluster Level/Bare-Metal & Host Level | V | https://ceems.dev/docs/advanced/power-consumption/ |
| 18 | Dynatrace Cost & Carbon Optimization | Infrastructure & Cluster Level/Bare-Metal & Host Level | R | existing Dynatrace docs; claims SDIA-certified methodology |
| 12 | CO2 Scope® (by EasyVirt) | Infrastructure & Cluster Level/Bare-Metal & Host Level | I | User guide documents the UI and outputs, but not how energy consumption and CO2 emissions are calculated (approach, data sources, assumptions). |
| 20 | Datavizta | Infrastructure & Cluster Level/Planning & Calculation | R | https://doc.api.boavizta.org/ Datavizta exposes Boavizta data/methods (API docs) |
| 21 | EasyVirt Eclyo | Infrastructure & Cluster Level/Planning & Calculation | I | Compares VM prices and carbon emissions across AWS, GCP and Azure, but publishes no calculation approach, data sources, or assumptions. |
| 22 | Cloud Project Carbon Emission Simulator by OxygenIT | Infrastructure & Cluster Level/Planning & Calculation | P | methodology only available on request (not public) |
| 23 | Green Algorithms Calculator | Infrastructure & Cluster Level/Planning & Calculation | R | methodology in publication referenced by README |
| 24 | Data Center Water Consumption Calculator | Infrastructure & Cluster Level/Planning & Calculation | R | existing link is a methodology article |
| 25 | Hardware Replacement Calculator | Infrastructure & Cluster Level/Planning & Calculation | V | https://www.green-coding.io/blog/when-to-replace-a-machine/ blog article documents the replacement-vs-keep calculation |
| 26 | Technology Carbon Estimator | Infrastructure & Cluster Level/Planning & Calculation | R | https://www.techcarbonstandard.org/ LCA-based Technology Carbon Standard; no single methodology page located |
| 27 | Green Metrics Tool | Full-Stack Application/Scenario Measurement | V | https://docs.green-coding.io/docs/prologue/philosophy-methodology/ |
| 28 | GreenFrame | Full-Stack Application/Scenario Measurement | R | https://docs.greenframe.io/ existing docs; methodology page not isolated |
| 29 | Cardamon | Full-Stack Application/Scenario Measurement | V | https://github.com/Root-Branch/cardamon-web-model web emission model repo |
| 30 | OpenTelemetry Java Agent Extension | Full-Stack Application/Monitoring & Tracing | R | README (repo homepage) documents it; no separate doc link |
| 31 | LIMo | Full-Stack Application/Monitoring & Tracing | R | README is the homepage; describes simple linear model; no separate doc link |
| 32 | Power Hog | Desktop & Mobile/Desktop Application | R | existing README#the-power-hog |
| 33 | Watt Wiser | Desktop & Mobile/Desktop Application | R | README lists sensors (RAPL/NVML); no methodology page |
| 34 | Android Power Profiler | Desktop & Mobile/Mobile Application | R | Google profiler docs; sensor-based |
| 35 | Greenspector Studio | Desktop & Mobile/Mobile Application | R | https://greenspector.com/en/studio/environmental-impact-measurement/ |
| 36 | PowDroid | Desktop & Mobile/Mobile Application | R | https://hal.science/hal-03380605v1 paper "PowDroid: Energy Profiling of Android Applications" |
| 37 | Android Runner | Desktop & Mobile/Mobile Application | N | generic experiment framework |
| 38 | JoularJX | Code/Code Level Energy Measurement | R | existing docs; formulas included |
| 39 | jPowerMonitor | Code/Code Level Energy Measurement | R | README (repo homepage) documents it; no separate doc link |
| 40 | DotNet-Counters | Code/Code Level Energy Measurement | N | .NET diagnostics tool; energy metrics |
| 41 | PyRAPL | Code/Code Level Energy Measurement | R | README + paper; RAPL-based |
| 42 | CodeCarbon | Code/Code Level Energy Measurement | V | https://docs.codecarbon.io/latest/explanation/methodology/ |
| 43 | Tracarbon | Code/Code Level Energy Measurement | R | existing docs; emission factors described |
| 44 | oaklean | Code/Code Level Energy Measurement | R | https://github.com/hitabisgmbh/oaklean#readme README; V8 + CPU energy measurement |
| 45 | perun | Code/Code Level Energy Measurement | R | README: samples usage stats from hardware |
| 46 | Coppers | Code/Code Level Energy Measurement | R | README; Intel RAPL based |
| 47 | Creedengo | Code/Static Code Analysis | N | static-analysis rules; no metric methodology required |
| 48 | CAST | Code/Static Code Analysis | I | Static-analysis rules need no methodology; for the energy-efficiency and carbon-footprint metrics it also reports, no calculation approach or data sources are published. |
| 49 | ec0lint | Code/Static Code Analysis | R | README describes rules; no methodology |
| 50 | aDoctor | Code/Static Code Analysis | R | archived; methodology in paper referenced by README |
| 51 | Eco CI | Code/CI Pipeline | V | https://docs.green-coding.io/docs/prologue/philosophy-methodology/ |
| 52 | AI Power Meter | Artificial Intelligence/AI Model Training | R | existing docs site |
| 53 | Carbontracker | Artificial Intelligence/AI Model Training | R | existing docs site |
| 54 | ZEUS | Artificial Intelligence/AI Model Training | R | https://ml.energy/zeus/measure/ measure page + research paper |
| 55 | ML CO2 Impact | Artificial Intelligence/AI Model Training | R | calculator/paper; methodology in README/publication |
| 56 | Green Algorithms Calculator (AI) | Artificial Intelligence/AI Model Training | R | methodology in publication referenced by README |
| 57 | experiment-impact-tracker | Artificial Intelligence/AI Model Training | R | existing docs site |
| 58 | Green Coding AI | Artificial Intelligence/AI Inference | V | https://www.green-coding.io/blog/green-coding-ai/ blog article documents the measurement approach |
| 59 | EcoLogits | Artificial Intelligence/AI Inference | R | https://ecologits.ai/ existing docs; methodology included |
| 60 | claude-carbon | Artificial Intelligence/AI Coding Agents | V | existing METHODOLOGY.md |
| 61 | Token & CO2 Dashboard | Artificial Intelligence/AI Coding Agents | V | https://github.com/neuland/tokendashboard/blob/main/backend/docs/co2-methodology.md |
| 62 | Electricity Maps | Databases/Grid Carbon Intensity API Service | V | https://www.electricitymaps.com/data/methodology |
| 63 | WattTime | Databases/Grid Carbon Intensity API Service | V | https://watttime.org/data-science/methodology-validation/ |
| 64 | Energy-Charts | Databases/Grid Carbon Intensity API Service | N | carbon-intensity data provider; no methodology required |
| 65 | ENTSO-E Transparency Platform | Databases/Grid Carbon Intensity API Service | N | electricity data provider; no methodology required |
| 66 | Carbon-Intensity UK | Databases/Grid Carbon Intensity API Service | V | https://carbonintensity.org.uk/#methodology existing link is API definitions |
| 67 | BoaviztAPI | Databases/IT Emission Inventory | V | https://doc.api.boavizta.org/ multiple methodology pages (embedded/usage/electricity/cloud) |
| 68 | Climatiq | Databases/IT Emission Inventory | V | https://www.climatiq.io/methodology |
| 69 | ResilioDB | Databases/IT Emission Inventory | N | Hardware emission-factor database; website is sufficient. Optional context: https://hotcarbon.org/assets/2026/paper-88.pdf (layered assessment model) |
| 70 | Base Empreinte | Databases/IT Emission Inventory | N | ADEME LCA database; website is sufficient |
| 71 | OxygenIT | Databases/IT Emission Inventory | P | methodology only available on request (not public) |
| 72 | CarbonDB | Data Aggregation/Organizational Level | R | https://docs.green-coding.io/docs/carbondb/overview/ green-coding product docs |
| 73 | fruggr | Data Aggregation/Organizational Level | V | https://www.fruggr.io/en/how-does-fruggr-assess-the-environmental-impacts-of-digital-services/ blog article describing the method |
| 74 | Sopht | Data Aggregation/Organizational Level | I | AI relies on the documented EcoLogits. For cloud it names data sources (cost and usage reports, CloudWatch) but not the calculation approach or assumptions (location-based grid intensity, embodied emissions, PUE). |
| 75 | Resilio Tech | Data Aggregation/Organizational Level | I | LCA software using ResilioDB; product pages describe features but not the calculation approach per metric, data sources, or assumptions. |
| 76 | Verdikt | Data Aggregation/Organizational Level | I | Lists GHG Protocol, ADEME Bilan Carbone (accredited), ISO 14040 and CSRD/ESRS, but does not describe how the metrics are calculated, the data sources, or the assumptions. |
| 77 | Aguaro | Data Aggregation/Organizational Level | I | Applies "prewired environmental profiles" and emission factors (incl. AI/GPU models), but does not describe the calculation approach, data sources, or assumptions. |
| 78 | Antarctica | Data Aggregation/Organizational Level | V | https://antarctica.io/research/one-token-model "Overview of the Methodology" with the energy formula (server + GPUs × utilisation × latency × PUE) and carbon = energy × grid intensity |
| 79 | Impact Framework | Data Aggregation/Modeling | R | https://if.greensoftware.foundation/intro/ existing intro; design-philosophy/major-concepts |
| 80 | Carbon Footprint Modeling Tool | Data Aggregation/Modeling | R | README/model docs |
| 81 | e-footprint model | Data Aggregation/Modeling | V | https://boavizta.github.io/e-footprint/methodology/ |
| 82 | PowerJoular | Device & Process Level/Device Measurement | R | existing docs; power model |
| 83 | Powerstat | Device & Process Level/Device Measurement | R | README/man; reads battery/RAPL |
| 84 | Perf | Device & Process Level/Device Measurement | R | perf wiki; RAPL |
| 85 | Turbostat | Device & Process Level/Device Measurement | R | man page; sensor readings |
| 86 | NVIDIA SMI | Device & Process Level/Device Measurement | R | existing docs; sensor readings |
| 87 | Intel PCM | Device & Process Level/Device Measurement | R | README; sensor readings |
| 88 | PowerTOP | Device & Process Level/Device Measurement | R | README; power diagnosis |
| 89 | Cloud Energy | Device & Process Level/Device Measurement | R | https://github.com/green-coding-solutions/cloud-energy#readme README: XGBoost/linear model from SPECPower |
| 90 | EnergiBridge | Device & Process Level/Device Measurement | R | README; sensor-based |
| 91 | CPU Energy Meter | Device & Process Level/Device Measurement | R | README; Intel RAPL |
| 92 | procpower | Device & Process Level/Process Metrics Exporter | R | existing README |
| 93 | powerletrics | Device & Process Level/Process Metrics Exporter | R | existing README |
| 94 | Energy Monitoring Tool | Device & Process Level/Process Metrics Exporter | V | https://github.com/FairCompute/energy-monitoring-tool#%EF%B8%8F-methodology README methodology section |
| 95 | PowerAPI | Device & Process Level/Process Metrics Exporter | V | https://powerapi.org/reference/formulas/smartwatts/ |
| 96 | EnergAt | Device & Process Level/Process Metrics Exporter | R | archived; methodology in paper |
| 97 | CO2.js | Website/Website Carbon Estimation | R | README + SWDM/Electricity Maps |
| 98 | Website Carbon Calculator | Website/Website Carbon Estimation | V | https://www.websitecarbon.com/how-does-it-work/ |
| 99 | Ecograder | Website/Website Carbon Estimation | V | https://ecograder.com/how-it-works |
| 100 | EcoIndex | Website/Website Carbon Estimation | V | https://www.ecoindex.fr/en/how-it-works/ analysis methodology |
| 101 | Kastor | Website/Website Carbon Estimation | R | Fork of Lighthouse; README/site: CO2 from CO2.js based on the Sustainable Web Design Model, >0.9 g/visit too high, <0.5 g ideal |
| 102 | Klimatest | Website/Website Carbon Estimation | I | States an A+–F "Digital Carbon Rating" relative to the global average, but not how the footprint is calculated, the data sources, or the assumptions. |
| 103 | Website Carbon Meter | Website/Website Carbon Estimation | R | README 'how it works'; CO2.js based |
| 104 | WebNRG | Website/Website Energy Measurement | V | https://website-tester.green-coding.io/methodology.html explicit methodology page (rendering energy, A+–F labels) |
| 105 | GreenIT-Analysis | Website/Website Analysis | N | browser-extension best-practice/recommendation tool; no metric methodology required |
| 106 | Firefox Power Profiler | Website/Website Analysis | R | existing docs; profiler |
| 107 | Safari Web Inspector | Website/Website Analysis | R | existing docs; profiler |
| 108 | Experiment Runner | Measurement Utilities/Automation | N | generic experiment framework |
| 109 | IBM Turbonomic | Optimization/Cloud Infrastructure | N | generic resource-optimisation software; no metric methodology required |
| 110 | Greenpixie GPX | Infrastructure & Cluster Level/Public Cloud | V | https://greenpixie.com/docs/methodology cloud + AI methodology docs; renamed from "Greenpixie GPX Data" |
| 111 | IBM Txture | Optimization/Cloud Infrastructure | R | https://www.ibm.com/docs/en/txture?topic=proposals-carbon-footprint-estimate IBM carbon footprint estimate docs |
| 112 | Cycloid | Optimization/Cloud Infrastructure | R | https://www.cycloid.io/blog/cloud-carbon-footprint-a-greenops-finops-approach-to-cloud-waste/ Blog describes the calculation chain (bottom-up resource usage × energy conversion × PUE × grid intensity) and builds on Cloud Carbon Footprint |
| 113 | EcoInfra | Optimization/Cloud Infrastructure | I | Predicts emissions from Terraform/IaC with an "AI" model; no calculation approach, data sources, or assumptions are published. |
| 114 | Elastic Universal Profiling | Optimization/Application Profiling | N | profiler; existing docs |
| 115 | KEDA | Optimization/Kubernetes | N | autoscaler, no metric methodology |
| 116 | Goldilocks | Optimization/Kubernetes | N | resource requests, no metric methodology |
| 117 | Karpenter | Optimization/Kubernetes | N | autoscaler, no metric methodology |
| 118 | Compute Gardener Scheduler | Optimization/Kubernetes | V | https://github.com/elevated-systems/compute-gardener-scheduler/blob/main/docs/carbon-calculations.md |
| 119 | kube-green | Optimization/Kubernetes | N | no metric methodology |
| 120 | DailyClean | Optimization/Kubernetes | N | no metric methodology |
| 121 | Carbon Aware KEDA Operator | Optimization/Kubernetes | R | README 'how it works' |
| 122 | CLEVER | Optimization/Kubernetes | N | archived; no metric methodology |
| 123 | Carbon Aware SDK | Optimization/Carbon Awareness | R | https://carbon-aware-sdk.greensoftware.foundation/docs/overview docs; data sources / concepts |
| 124 | grid-intensity-go | Optimization/Carbon Awareness | N | carbon-intensity data client (Electricity Maps/WattTime); no own methodology required |
| 125 | Camunda Carbon Reductor | Optimization/Carbon Awareness | N | carbon-intensity data consumer; no own methodology required |
| 126 | Carbon-Aware-Computing.com | Optimization/Carbon Awareness | R | README methodology section |
| 127 | Grid-aware Websites | Optimization/Carbon Awareness | N | carbon-intensity data consumer (Electricity Maps); no own methodology required |
| 128 | VSCarbon | Optimization/Carbon Awareness | N | displays grid carbon intensity; no own methodology required |
| 129 | Pruna AI | Optimization/Artificial Intelligence | N | model optimization framework; existing docs |
| 130 | CLEER | Artificial Intelligence/AI Benchmarks & Leaderboards | V | https://reports.sustainableaigroup.com/CLEER-Tech-Report/ technical report with 4-stage estimation method |
| 131 | AI Energy Score | Artificial Intelligence/AI Benchmarks & Leaderboards | V | https://huggingface.github.io/AIEnergyScore/ methodology section explains energy measurement and star ratings |
| 132 | ML.ENERGY Leaderboard | Artificial Intelligence/AI Benchmarks & Leaderboards | R | https://github.com/ml-energy/benchmark README + NeurIPS paper describe energy measurement |
| 133 | LLM-Perf Leaderboard | Artificial Intelligence/AI Benchmarks & Leaderboards | R | https://github.com/huggingface/optimum-benchmark#readme README covers energy tracking |
| 134 | GoKubeDownscaler | Optimization/Kubernetes | N | autoscaler/downscaler, no metric methodology |

## Decision list (needs discussion)

_Open discussion: should the prerequisite be relaxed so that a methodology accredited by a trustworthy third party (e.g. Base Carbone®, ISO 14040) is sufficient even if the calculation details are not public? (raised for Verdikt)_

### P — methodology not public (on request only) (2)

- 22 Cloud Project Carbon Emission Simulator by OxygenIT
- 71 OxygenIT

### I — insufficient information (12)

- 2 Azure Carbon Optimization
- 6 Li10 for AWS
- 8 Green Cost Explorer for AWS
- 12 CO2 Scope® (by EasyVirt)
- 21 EasyVirt Eclyo
- 48 CAST
- 74 Sopht
- 75 Resilio Tech
- 76 Verdikt
- 77 Aguaro
- 102 Klimatest
- 113 EcoInfra
