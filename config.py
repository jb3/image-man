import yaml
import attrdict


config = attrdict.AttrDict(yaml.safe_load(open("config.yaml", "r")))
