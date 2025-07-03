# Hydra (is built on OmegaConf and is the standard interface for this purpose).
from omegaconf import OmegaConf
from pprint import pprint

# Create a config from a dictionary
config = OmegaConf.create({
    "database": {
        "host": "localhost",
        "port": 3306
    },
    "debug": True
})

# Access values
print("Host:", config.database.host)
print("Port:", config["database"]["port"])
print("Debug mode:", config.debug)

# Merge with another config
'''
In case of conflicts, values from later configs override earlier ones.
'''
default_cfg = OmegaConf.create({"debug": False, "database": {"user": "root"}})
merged_cfg = OmegaConf.merge(default_cfg, config)
'''
resolve=True tells OmegaConf to evaluate interpolations in the config before converting it to a standard Python dict.

cfg = OmegaConf.create({
    "a": 10,
    "b": "${a}",   # interpolated reference
})

print(cfg.b)  # prints 10
print(OmegaConf.to_container(cfg, resolve=False))  # {'a': 10, 'b': '${a}'}
print(OmegaConf.to_container(cfg, resolve=True))   # {'a': 10, 'b': 10}
'''
pprint(OmegaConf.to_container(merged_cfg, resolve=True))
