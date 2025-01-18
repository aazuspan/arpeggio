"""Tools for validating parsed songs."""

from pydantic import BaseModel, ConfigDict, ValidationError

from arpeggio.arp_ast import Config
from arpeggio.exceptions import ConfigError


class ValidatedConfig(BaseModel):
    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True)

    @classmethod
    def validate(cls, configs: dict[str, Config], filename: str, **kwargs):
        """
        Instantiate a validated configuration using parsed configuration options.

        On failed validation, the first invalid configuration is reported with
        line/column metadata.
        """
        try:
            return cls(**{k: v.value for k, v in configs.items()}, **kwargs)
        except ValidationError as e:
            error = e.errors()[0]
            err_type = error["type"]
            invalid_config = error["loc"][0]

            if err_type == "extra_forbidden":
                msg = f"Unrecognized configuration @{invalid_config}."
            elif err_type == "missing":
                raise ValueError(
                    f"Missing required configuration {invalid_config}"
                ) from None
            else:
                msg = f"Invalid @{invalid_config} configuration. " + error["msg"]

            configs[invalid_config].meta.filename = filename
            raise ConfigError(msg, meta=configs[invalid_config].meta) from None
