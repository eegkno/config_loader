"""Module to load configurations from a yaml file """
import yaml


class ConfigLoader:
    def __init__(self):
        self.cfg = {}

    def load(self, filepath: str):
        """
        Load a configuration file.
        Parameters
        ----------
        filepath : str
            Path to the configuration file.

        Returns
        -------
        config : Configuration
        """
        if filepath.lower().endswith(".yaml") or filepath.lower().endswith(".yml"):
            yaml.add_constructor("!join", self._join)  ## register the tag handler
            with open(filepath, "r") as ymlfile:
                self.cfg = yaml.load(ymlfile, Loader=yaml.Loader)


        return self.cfg

    def __repr__(self):
        return self.cfg


    @staticmethod
    def _join(loader, node):
        seq = loader.construct_sequence(node)
        return "".join([str(i) for i in seq])
