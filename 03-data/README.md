# Data
The specification of the data format used for the climbing holds and the climbing wall:

```yaml
- Id: <sha256sum of the file contents>
  Color: <blue, yellow,...>
  Type: <crimp, jug, sloper, pinch, pocket, foothold>
  Manufacturer: <the name of the manufacturer>
  Labels: [<list>, <of>, <custom>, <labels>]
```

## `holds.yaml`
A dictionary containing the data of all of the holds.

## `models/`
A folder containing the models of the holds in the `obj` format. Each should be:

- properly sized to correspond to the real world
- having correct origin (either in the middle or in some screw hole)
- facing upwards
