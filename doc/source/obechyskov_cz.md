# Hýskov

Support for waste collection schedules provided by [Obec Hýskov](https://www.obechyskov.cz/obec/sluzby/odpady/), Czech Republic.

## Configuration via configuration.yaml

```yaml
waste_collection_schedule:
  sources:
    - name: obechyskov_cz
```

### Configuration Variables

This source has no configuration variables. The municipality publishes a single collection calendar for the whole village (`Hýskov (Beroun)`).

## Example

```yaml
waste_collection_schedule:
  sources:
    - name: obechyskov_cz
```

## How to get the source argument

No arguments are required. The schedule is read from the [waste collection calendar](https://www.obechyskov.cz/obec/sluzby/odpady/) on the municipality website. The municipality publishes the calendar one year at a time, so dates for the next year appear only once the new calendar is published.

## Bin types returned

| Provider description                  | Returned type                          | Icon                      |
|---------------------------------------|----------------------------------------|---------------------------|
| TKO - 1x týdně                        | TKO - 1x týdně                         | `Icons.GENERAL_WASTE`     |
| TKO - 1 x za 14 dní                   | TKO - 1 x za 14 dní                    | `Icons.GENERAL_WASTE`     |
| TKO - 1x měsíčně                      | TKO - 1x měsíčně                       | `Icons.GENERAL_WASTE`     |
| svoz pytlů po obci Hýskov             | svoz pytlů po obci Hýskov              | `Icons.GENERAL_WASTE`     |
| Plasty - kontejnery                   | Plasty - kontejnery                    | `Icons.PLASTIC_PACKAGING` |
| Plast - žluté popelnice svoz od domu  | Plast - žluté popelnice svoz od domu   | `Icons.PLASTIC_PACKAGING` |
| Papír - kontejnery                    | Papír - kontejnery                     | `Icons.PAPER`             |
| Papír - svoz modré popelnice od domu  | Papír - svoz modré popelnice od domu   | `Icons.PAPER`             |
| Sklo - kontejnery                     | Sklo - kontejnery                      | `Icons.GLASS`             |
| Kov - kontejnery                      | Kov - kontejnery                       | `Icons.METAL`             |
| Bio odpad                             | Bio odpad                              | `Icons.ORGANIC`           |
| Nebezpečný odpad                      | Nebezpečný odpad                       | `Icons.HAZARDOUS`         |
