# Github Actions: Template Builder (CloudFormation)

This Github action can be used to automate the update/creation of Pingdom health checks
based on the contents of a YAML file in a Github repository.

#### Required Parameters

* PATH_TEMPLATES
            
  Path to template files that are referenced in configuration

* PATH_CONFIGS

  Path to environment/configuration files. Each environment to be deployed should be 
  defined as a separate directory underneath this folder, for example:
  
  ```text
  + /root
    + /config
      + /dev
        - config.yml
        - xxx.yml
      + /uat
        - config.yml
        - xxx.yml
      + /prod
        - config.yml
        - xxx.yml
    - /templates
  ```

* PATH_OUTPUT

  Path where generated templates will be saved

* OUTPUT_PREFIX

  Prefix added to the start of all output filenames

* OUTPUT_SUFFIX

  Prefix added to the end of all output filenames

#### Example Usage

The following example shows how the action can be used in a Github workflow file.

```yaml
name: Template Builder (CloudFormation)

on:
  push:
    branches:
      - master

jobs:
  build-templates:
    name: Build Templates
    runs-on: ubuntu-latest
    steps:
      - name: Check Out Branch
        uses: actions/checkout@master
      - name: Build Templates
        uses: eonx-com/actions-template@v1.0
        with:
          PATH_TEMPLATES: '/template'
          PATH_CONFIGS: '/config'
          PATH_OUTPUT: '/output'
          OUTPUT_PREFIX: ''
          OUTPUT_SUFFIX: '.yml'
```