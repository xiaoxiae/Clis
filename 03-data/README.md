# Data

## Specification
The specification of the data format used for the climbing holds and the climbing wall:

```yaml
<sha256sum of the file contents>:
  Color: <blue, yellow,... determined by an enum in the config file>
  Type: <crimp, jug, sloper, pinch, pocket, foothold, structure>
  Manufacturer: <the name of the manufacturer>
  Labels: [<list>, <of>, <custom>, <labels>]
```

## `01-add_models.py`
A script for adding the generated holds into the `holds.yaml` dictionary, automatically inferring their color in the process.
