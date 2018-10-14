import yaml

mongo_config = None
with open("config/config.yaml", "r") as fdr:
    config = yaml.load(fdr)
mongo_config = config["mongo"]
