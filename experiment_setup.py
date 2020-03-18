""" Module to setup experiments """
import getpass
import pathlib

from config_loader import ConfigLoader


class MissingMainKeyError(Exception):
    """Raised when there is a main key missing. """


class WrongUserKeyError(Exception):
    """Raised when user performing experiemnt is different from the one running it. """


class MatchingKeyError(Exception):
    """Raised when keys do not math default keys. """


class ExperimentSetup:
    def __init__(self):
        self.cfg = None

    def setup(
        self, filepath: str, make_outputs: bool = True
    ):
        """
        Load a configuration file and create output directories.

        Parameters
        ----------
        filepath : str
            Path to the configuration file.
        make_outputs: bool
            If true, create output directories, but only when output_dir_key exists.

        Returns
        -------
        config : Configuration
        """
        config_loader = ConfigLoader()
        self.cfg = config_loader.load(filepath)

        self._validate_dic_keys()

        if self.cfg["EXPERIMENT"]["USER"] != getpass.getuser():
            raise WrongUserKeyError("USER value in config file does not match current user ")

        if make_outputs:
            self._create_output_dirs()

        return self.cfg

    def _validate_dic_keys(self):
        main_keys = ["EXPERIMENT", "OUTPUT_DIRS"]
        for element in main_keys:
            if element not in self.cfg:
                raise MissingMainKeyError(
                    "Missing one or more main keys `main_keys`", main_keys
                )

        sub_keys_exp = [
            "SPRINT_NAME",
            "SPRINT_DIR",
            "EXPERIMENT_NAME",
            "MODEL_NAME",
            "USER",
        ]
        for element in sub_keys_exp:
            if element not in self.cfg["EXPERIMENT"]:
                raise MatchingKeyError("Keys do not match `sub_keys_exp`", sub_keys_exp)

        sub_keys_output = ["EXPERIMENT_PATH", "MODEL_PATH"]
        for element in sub_keys_output:
            if element not in self.cfg["OUTPUT_DIRS"]:
                raise MatchingKeyError(
                    "Keys do not match `sub_keys_output`", sub_keys_output,
                )

    def _create_output_dirs(self):

        for _, dir_path in self.cfg["OUTPUT_DIRS"].items():
            pathlib.Path(dir_path).mkdir(parents=True, exist_ok=True)

    def __repr__(self):
        return self.cfg
