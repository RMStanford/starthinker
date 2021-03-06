# Recipe Tests

Recipe tests are integration tests, since StarThinker is mostly an integration platform.  They are recipes
with values hard coded and designed to be ran by anyone with access to the underlying resources.  To help 
test recipes, StarThinker has a [Test Task](../starthinker/task/test/). It is like any other task
in StarThinker except that it doesn't do any work.  It simply compares and asserts endpoints.  

StarThinker also comes with a test helper that loads and runs test recipes for complete integration testing.
Tests are run in parallel and written to individual log files.  The test helper uses StarThinker virtual
environment and shell variables defined in [starthinker_assets/developer.sh](../starthinker_assets/developer.sh)
or [starthinker_assets/production.sh](../starthinker_assets/production.sh).

## Steps
```
source install/deploy.sh
```

1. Option 1) Developer Menu
1. Option 3) Test Tasks
  - You may be asked for a Cloud Project ID ( use the ID, not the Name, not the Number )
  - You may be asked for [Service Credentials](cloud_service.md).
  - You may be asked for [Installed Client Credentials](cloud_client_installed.md).

## Code

  - [tests/helper.py](../tests/helper.py) - Can be run from command line, finds, configures, and executes tests.
  - [tests/config.json](../tests/) - Generated by helper when run, variables required for integration testing.
  - [tests/scripts/[test].json](../tests/scripts/) - Test scripts used by helper.
  - [tests/recipes/[test].json](../tests/) - Generated by helper when run, result of combining scripts and config variables.
  - [tests/logs/[test].log](../tests/) - Generated by helper when run, logs written during test execution.

## Important Testing Setup

StarThinker runs full integration tests, many tests require specific access to testing assets such as account identifiers and emails.
To configure this, the helper will create a config.json file in the [tests/](../tests/) directory. After it is
created edit the file and fill in required fields.

Not all fields need to be filled in, tests missing values will error, if you are not using those components, ignore the errors.
Not all tests require fields, tets not listed in the config file do not require user input.

## Manual Testing

### Initializing the tests to create the configuration file:
```
source starthinker_assets/developer.sh
python tests/helper.py --init
vi tests/config.json
```

### Running all tests from the command line:
```
source starthinker_assets/developer.sh
python tests/helper.py
```

### Running some tests from the command line ( where tests are [tests/scripts/[test].json](../tests/scripts/)):
```
source starthinker_assets/developer.sh
python tests/helper.py --tests dt sheets
```

### Viewing Test Logs

All tests run are logged to **tests/logs/OK_[test].log** and **tests/logs/FAILED_[test].log**.  Running all tests clears the directory.  Running a set of tests does NOT clear the directory but does overwrite the specific log files for each test run.

## Adding Tests

A test is a [script](recipe.md) with additional [test tasks](../task/test/run.py), to create a test:

1. Follow the instructions for creating a script [script](recipe.md).
1. Add [test tasks](../task/test/run.py) to the script to verify execution ( see sample test tasks below ).
1. Save the test script in the [tests/scripts/[test].json](../tests/scripts/) folder.

### Test Task Samples

1. check if sheet matches given values
```
{ "test": {
  "auth":"user",
  "sheets": {
    "url":"https://docs.google.com/spreadsheets/d/1h-Ic-DlCv-Ct8-k-VJnpo_BAkqsS70rNe0KKeXKJNx0/edit?usp=sharing",
    "tab":"Sheet_Clear",
    "range":"A1:C",
    "values":[
      ["Animal", "Age", "Weight ( lbs )"],
      ["dog", 7, 67],
      ["cat", 5, 1.5],
      ["bird", 12, 0.44],
      ["lizard", 22, 1],
      ["dinosaur", 1600, 273.97]
    ]
  }
}}
```
1. check if bigquery table has given values or has data
```
{ "test": {
  "auth":"user",
  "bigquery":{
    "dataset":"Test",
    "table":"Sheet_To_BigQuery",
    "schema":[
      {"name": "Animal", "type": "STRING"},
      {"name": "Age", "type": "INTEGER"},
      {"name": "Weight_lbs", "type": "FLOAT"}
    ],
    "values":[
      ["dog", 7, 67],
      ["cat", 5, 1.5],
      ["bird", 12, 0.44],
      ["lizard", 22, 1],
      ["dinosaur", 1600, 273.97]
    ]
  }
}}
```
1. assert recipe has executed all tasks before this point
```
{ "test": {
  "assert":"Completed all tasks."
}}
``` 
1. check if path exists
```
{ "test": {
  "path":"somefile.txt"
}}
```
1. check if storage file exists
```
{ "test":{
  "auth":"service",
  "storage":{
    "bucket":"bucket_name",
    "file":"file.png",
    "delete":true
   }
}}
```
1. check if storage file exists
```
{ "test":{
  "auth":"service",
  "drive":{
    "file":"Some File Name Or URL",
    "delete":true
   }
}}
```

### Notes

- Ensure the test is re-entrant.
- Ensure any test assets are shared with starthinker-assets@googlegroups.com.
- If test requires a sheet, use the template pattern to copy the master sheet to a user owned test sheet.
- Only use fields for values that absolutely cannot be shared.
- Keeping fields to a minimum is paramount.

---
&copy; 2019 Google Inc. - Apache License, Version 2.0
