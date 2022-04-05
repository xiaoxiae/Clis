# Data

## Specification
The specification of the data format used for the climbing holds and the climbing wall:

```yaml
<sha256sum of the file contents (the first 12 characters)>:
  color: <blue, yellow,... determined by an enum in the config file>
  type: <crimp, jug, sloper, pinch, pocket, foothold, structure>
  date: <the date the hold model was created>
  manufacturer: <the name of the manufacturer>
  labels: [<list>, <of>, <custom>, <labels>]
```

## `01-add_models.py`
A script for adding the generated holds into the `holds.yaml` dictionary, automatically inferring their color from the texture in the process.
