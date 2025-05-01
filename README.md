# Green Software Landscape

This is proof of concept of a tool landscape for **Green Software** provided by the German organization [Bundesverband Green Software](https://www.bundesverband-green-software.de/).

The tool [landscape2](https://github.com/cncf/landscape2/) by the CNCF is used to generate the landscape website.

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

Add the tool to `data.yml` in the correct category / subcategory.
Please also provide a logo and place it into the [logos](./logos/) directory.

Possible fields are explained [here](https://github.com/cncf/landscape2/blob/main/docs/config/data.yml).

Note: we use the field `project` not to specify the maturity in the sense of the CNCF, but if we, the Bundesverband Green Software, have successfully field-tested the tool/project. If so, add `project: "proved+tested"`.
