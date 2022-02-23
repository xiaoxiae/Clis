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
Contains folders corresponding to each of the scanned sets. Each contains:
- a properly sized model in the `obj` format, centered on the screw hole
- the `mtl` material settings file 
- the `jpg` texture file
- (optionally) a `report.pdf` file that describes the model parameters
