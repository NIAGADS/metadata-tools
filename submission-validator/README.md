# submission-validator

Scripts in support of automatic validation of meta-data submission files

## Overview

Each type of meta-data sheet has a `config` file (see [configs](configs)) that defines the validation rules (required fields, restricted values, etc) in JSON format.  The format and contents of these config files, in turn, is regulated by a [JSON schema](https://json-schema.org/) defined in `Typescript` for ease of read/write and then converted to JSON format (see [schemas](schemas)).  When modifying an existing `config` JSON file, or creating a new one, the `config` file should be run through validation to make sure it is in compliance with the `config-schema`.

## Modifying the JSON Schema for Config Files

### Dependencies

* [node.js LTS](https://nodejs.org/en); recommend installing using the [Node Version Manager (NVM)](https://github.com/nvm-sh/nvm#installing-and-updating)
* [typescript-json-schema](https://github.com/YousefED/typescript-json-schema) installed globally

```bash
npm install -g typescript-json-schema
```

* Python 3.5+
* [jsonschema](https://pypi.org/project/jsonschema/) python package
