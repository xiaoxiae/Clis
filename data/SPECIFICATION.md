# Specification
The specification of the data format used for the climbing holds and the climbing wall.

## `holds.yaml`
A dictionary containing data of all holds.

```yaml
<TODO: hold name format>:
  color: {blue, yellow, ...}
  type: {crimp, sloper, jug}
  manufacturer: the manufacturer of the hold
  labels: [some, other, custom, labels]
```

## `holds/`
A folder containing the models of the holds (TODO: object format). Each should be:

- properly sized to correspond to the real world
- having correct origin (either in the middle or in some screw hole)
- facing upwards
