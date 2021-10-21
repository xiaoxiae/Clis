# Data
The specification of the data format used for the climbing holds and the climbing wall.

## `holds.yaml`
A dictionary containing data of all holds.

```yaml
- Name: <hold name - sha256sum of the file>
  Color: <blue, yellow,...]>
  Type: <crimp, jug, sloper, pinch, pocket, foothold>
  Manufacturer: <the name of the manufacturer>
  Labels: [<a list of custom labels>]
```

## `holds/`
A folder containing the models of the holds in the `obj` format. Each should be:

- properly sized to correspond to the real world
- having correct origin (either in the middle or in some screw hole)
- facing upwards
