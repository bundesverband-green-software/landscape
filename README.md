# Green Software Landscape

This is the tool landscape for **Green Software** provided by the German organization [Bundesverband Green Software](https://www.bundesverband-green-software.de/).

URL: <https://landscape.bundesverband-green-software.de>

The CNCF tool [landscape2](https://github.com/cncf/landscape2/) is used to generate the landscape website.

## Propose a new tool

The landscape is open to all Green Software tools. We only require a minimal set of prerequisites:

- The project must be related to Green Software.
- The tool must be usable (the project must have at least beta status).
- Information about how to use the tool is provided.
- Information about the tool's methodology is provided.

If you would like to propose a new tool for the landscape, please create an issue using the template [Tool Proposal](https://github.com/bundesverband-green-software/landscape/issues/new?template=propose_tool_issue_template.yml) and fill in the required information.

## Structure

The file `data.yml` includes all the information about the tools and the categories. To add/edit tools, only this file has to be changed.
Every tool is part of one category. By using the field `second_path`, a tool can be displayed in more than one category.
The available fields are explained [here](https://github.com/cncf/landscape2/blob/main/docs/config/data.yml).

The field `project` is not used to specify the maturity in the sense of the CNCF, but if we, the Bundesverband Green Software, have successfully field-tested the tool/project. If that is the case, the field is set to: `project: "approved+tested"`

Logos are placed in the [logos](./logos/) directory. If there is no logo available, we either use the logo of the organization behind the project (subfolder [organization](./logos/organization/)) or we generate a basic text only image (subfolder [unofficial](./logos/unofficial/)). We used the tool [Text-SVG-Generator](https://text-to-svg.com/) to generate some logos and used the font "Impact".

The definition of how the categories are split into the two groups, measurement and optimization, can be found in the file `settings.yml`.

## Local usage

Prerequisites:

- install [landscape2](https://github.com/cncf/landscape2/blob/main/README.md#installation)
- optional: provide a GitHub token with `public_repo` scope in the `GITHUB_TOKENS` environment variable (if not given, GitHub related information are missing)

Build:

```sh
landscape2 build \
--data-file data.yml \
--settings-file settings.yml \
--guide-file guide.yml \
--logos-path logos \
--cache-dir cache \
--output-dir build
```

Serve:

```sh
landscape2 serve --landscape-dir build
```

## Credits

Existing tool lists that we have taken inspiration from when creating and updating this tool landscape:

- Green Software Foundation's awesome list: <https://github.com/Green-Software-Foundation/awesome-green-software>
- GitHub's Green Software Directory <https://github.com/github/GreenSoftwareDirectory>
- GitHub's Green Software topic list: <https://github.com/topics/green-software>
- ClimateTriage: <https://climatetriage.com/category/consumption>
- Tim Schade: <https://github.com/schaDev/GreenCoding-measuring-tools>
- Andreas Weber: <https://green-software-big-picture.org>
- Green Coding Solutions: <https://www.green-coding.io/products>
- CNCF Sustainability TAG: <https://tag-env-sustainability.cncf.io/landscape/#observability-tooling>
- Luís Cruz 2021: <https://luiscruz.github.io/2021/07/20/measuring-energy.html>
- Guldner et al. 2024: <https://www.sciencedirect.com/science/article/pii/S0167739X24000384>
