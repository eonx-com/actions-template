# Github Actions: Template Builder 

This Github Action can be used to procedurally generate Jinja2 templates based
on the contents of YAML configuration files.

#### Required Parameters

* TEMPLATE_ROOT
            
  Path to template files that are referenced in configuration

* CONFIG_ROOT

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

* OUTPUT_PATH

  Path where generated templates will be saved

* OUTPUT_FILENAME_PREFIX

  Prefix added to the start of all output filenames

* OUTPUT_FILENAME_SUFFIX

  Prefix added to the end of all output filenames

#### Optional Parameters

* ENVIRONMENT

  If specified, this will force the tool to generate only a single environment
  from the CONFIG_ROOT. By default all folders in the CONFIG_ROOT will be
  built.
  
#### Example Usage

The following example shows how the action can be used in a Github workflow file.

```yaml
name: Template Builder 

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
          TEMPLATE_ROOT: '/template'
          CONFIG_ROOT: '/config'
          OUTPUT_PATH: '/output'
          OUTPUT_FILENAME_PREFIX: ''
          OUTPUT_FILENAME_SUFFIX: '.yaml'
```