import os
import dynaconf  # noqa

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

settings = dynaconf.DjangoDynaconf(
    __name__,
    SETTINGS_FILE_FOR_DYNACONF="../settings.yaml",
    SECRETS_FOR_DYNACONF="../.secrets.yaml",
)  # noqa
