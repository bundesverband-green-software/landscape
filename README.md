# Green Software Landscape

This is the tool landscape for **Green Software** provided by the German organization [Bundesverband Green Software](https://www.bundesverband-green-software.de/).

URL: <https://landscape.bundesverband-green-software.de>

The CNCF tool [landscape2](https://github.com/cncf/landscape2/) is used to generate the landscape website.

## Usage

Prerequisites:

- install [landscape2](https://github.com/cncf/landscape2/blob/main/README.md#installation)
- provide a GitHub token with `public_repo` scope in the `GITHUB_TOKENS` environment variable (optional, if not given, GitHub related information are missing)

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

## Add new tool

Add the tool to the correct category/subcategory in `data.yml`. If it belongs to more than one category, you can use the `second_path` field to add it to more than one category.

The possible fields are explained [here](https://github.com/cncf/landscape2/blob/main/docs/config/data.yml).

Note: we use the field `project` not to specify the maturity in the sense of the CNCF, but if we, the Bundesverband Green Software, have successfully field-tested the tool/project. If that is the case, you can add `project: "approved+tested"`.

Please also provide a logo and place it into the [logos](./logos/) directory. If there is no logo available, you may either use the logo of the organization behind the tool (place it in the subfolder [organization](./logos/organization/)) or you may generate a text only image yourself (place it in the [unofficial](./logos/unofficial/)). We used the tool [Text-SVG-Generator](https://text-to-svg.com/) to generate some logos and used the font "Impact".

## Credits

Existing tool lists that we have taken inspiration from when creating this tool landscape:

- Green Web Foundation: <https://github.com/Green-Software-Foundation/awesome-green-software>
- GitHub: <https://github.com/topics/green-software>
- Tim Schade: <https://github.com/schaDev/GreenCoding-measuring-tools>
- Andreas Weber: <https://green-software-big-picture.org>
- Green Coding Solutions: <https://www.green-coding.io/products>
- CNCF Sustainability TAG: <https://tag-env-sustainability.cncf.io/landscape/#observability-tooling>
- Luís Cruz 2021: <https://luiscruz.github.io/2021/07/20/measuring-energy.html>
- Guldner et al. 2024: <https://www.sciencedirect.com/science/article/pii/S0167739X24000384>
