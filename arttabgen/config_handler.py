"""Holds the class ConfigHandler which offers functionality to validate and process a config used for the dataset
generation."""
import json
from functools import partial
from pathlib import Path
from typing import Callable, Dict, List, Union

import dacite

from arttabgen import config_validator
from arttabgen.helper import (
    convert_str_to_bool,
    convert_keys_to_int,
    ensure_discrete_style_parameter_value,
    random_value_from_discrete,
    random_value_from_image_manipulation_parameter,
    random_value_from_style_parameter,
)
from arttabgen.transformers import (
    image_manipulator,
    structure_transformer,
    style_transformer,
)
from arttabgen.types_.config_main_keys import ConfigMainKeys
from arttabgen.types_.image_manipulation_parameter import ImageManipulationParameter
from arttabgen.types_.structure_parameter import StructureParameter
from arttabgen.types_.style_parameter import StyleParameter
from arttabgen.types_.transformer_application_strategy import (
    TransformerApplicationStrategy,
)

# Will be initialized by main.py
config_handler: "ConfigHandler" = None


class ConfigHandler:
    def __init__(
            self,
            config_path: Path,
            transformer_application_strategy: TransformerApplicationStrategy,
    ) -> None:
        """Offers functionality to validate and process a config used for the dataset generation.

        Args:
            config_path: The path of the json config file to deserialize.
            transformer_application_strategy: The strategy to use for selecting transformer parameters to apply.
                                            This parameter is used for processing the transformers defined in the
                                            config.

        """
        self.config: Dict = json.loads(config_path.read_text())
        """A deserialized version of the json config file.

            After validating the config, it can be used to access settings.

            Note:
                Because of limitations in the JSON spec,
                certain mappings will have their string keys converted to int keys by
                :func:`validate_config`.

            See also:

                :ref:`Config`
        """
        self.transformer_application_strategy: TransformerApplicationStrategy = (
            transformer_application_strategy
        )
        """The transformer application strategy to use for applying transformers to generated tables.

            This variable is used here, because the list of transformer parameter combinations is built by this class
            and then passed onto the classes, which use the transformer parameter combination.

            See also:

            :ref:`Transformer application strategies`
        """

    def validate_config(self) -> None:
        """Call appropriate validators for all top level keys in the config.

        Note:
            This function calls the following config value converters:
                - :func:`_convert_number_of_columns_odds`: converts it's keys from str to int because JSON can only
                store string keys.
                - :func:`_convert_gen_modes_odds`: converts it's keys from str to int because JSON can only store
                string keys.

        See also:
            :data:`arttabgen.config_validator.TOP_LEVEL_KEY_VALIDATORS`

        Raises:
            RuntimeError: if the validation fails.
        """

        for top_level_key, top_level_value in self.config.items():
            config_validator.TOP_LEVEL_KEY_VALIDATORS[top_level_key](top_level_value)

        self._convert_number_of_columns_odds()
        self._convert_gen_modes_odds()
        self._convert_gt_odds()
        self._convert_do_complex_values()

    def build_image_manipulators(self) -> Dict[str, Callable[[str], None]]:
        """Read the config and build a list of functions making the defined image manipulations.

        Returns:
            A dictionary of effect transformers and functions applying the configured effect transformers.

        See also:
            | :ref:`Config`
            | :ref:`Transformers`
            | :mod:`arttabgen.effect_transformer`

        """

        # Use partial specialization so the DatasetGenerator can call functions
        # without needing to know about any parameters
        image_manipulation_declaration: List[ImageManipulationParameter] = []

        for parameter in self.config[ConfigMainKeys.IMAGE_PARAMETERS]:
            image_manipulation_declaration.append(
                dacite.from_dict(data_class=ImageManipulationParameter, data=parameter)
            )

        effects = {}

        for parameter in image_manipulation_declaration:
            effects[parameter.name] = partial(
                image_manipulator.IMAGE_MANIPULATORS[parameter.name],
                value=random_value_from_image_manipulation_parameter(parameter.value),
            )

        return effects

    def _convert_do_complex_values(self) -> None:
        self.config["do_complex_values"] = convert_str_to_bool(self.config["do_complex_values"])

    def _convert_number_of_columns_odds(self) -> None:
        """
        Convert the keys of the config key ``"number_of_columns_odds"`` from ``str`` to ``int``,
        because JSON can only store string keys.
        """

        self.config[ConfigMainKeys.NUMBER_OF_COLUMNS_ODDS] = convert_keys_to_int(
            self.config[ConfigMainKeys.NUMBER_OF_COLUMNS_ODDS],
        )

    def _convert_gen_modes_odds(self) -> None:
        """
        Convert the keys of the config key "number_of_columns_odds" from str to int,
        because JSON can only store string keys.
        """
        self.config[ConfigMainKeys.GEN_MODES_ODDS] = convert_keys_to_int(
            self.config[ConfigMainKeys.GEN_MODES_ODDS],
        )

    def _convert_gt_odds(self) -> None:
        """
        Convert the keys of the config key "gt_odds_per_mode" from str to int, because JSON can only store string keys.
        """
        self.config[ConfigMainKeys.GT_ODDS_PER_MODE] = convert_keys_to_int(
            self.config[ConfigMainKeys.GT_ODDS_PER_MODE],
        )


def build_style_transformers(
        config: Dict, strategy: TransformerApplicationStrategy
) -> Union[List[Union[int, float, str]], List[List[Union[float, int, str]]]]:
    """
    Read the config and build a list of directives acting as *style transformers*.

    Note:
        At the moment, the exact return type depends on the strategy.

    Args:
        config: A deserialized config containing style transformer configurations.
        strategy: A strategy deciding by what logic to build the style parameters

    Returns:
        A list of direcvties acting ast *style transformers* if strategy is
        :attr:`arttabgen.types_.transformer_application_strategy.TransformerApplicationStrategy.SELECTIVE`.

        A list OF LISTS of direcvties acting as *style transformers* if strategy is
        :attr:`arttabgen.types_.transformer_application_strategy.TransformerApplicationStrategy.COMBINAORICAL`.
        Every outer list item handles a single style parameter, every inner list contains directives including that
        style parameter.

        See also:
            | :ref:`Config`
            | :ref:`Transformers`
            | :ref:`Transformer application strategies`
            | :mod:`arttabgen.types_.transformer_application_strategy`
            | :mod:`arttabgen.style_transformer`

    """
    style_parameter_declarations: List[StyleParameter] = []

    for parameter in config[ConfigMainKeys.STYLE_PARAMETERS]:
        style_parameter_declarations.append(
            dacite.from_dict(data_class=StyleParameter, data=parameter)
        )

    if strategy == TransformerApplicationStrategy.SELECTIVE:
        return [
            style_transformer.STYLE_TRANSFORMERS[parameter.name](
                random_value_from_style_parameter(parameter.value),
                parameter.unit,
            )
            for parameter in style_parameter_declarations
        ]
    elif strategy == TransformerApplicationStrategy.COMBINATORICAL:
        combinations: Dict[str, List[Union[str, int, float]]] = dict()

        for parameter in style_parameter_declarations:
            values: List = ensure_discrete_style_parameter_value(parameter)

            for value in values:
                combinations.setdefault(parameter.name, []).append(
                    style_transformer.STYLE_TRANSFORMERS[parameter.name](
                        value,
                        parameter.unit,
                    )
                )

        return list(combinations.values())


def build_structure_transformers(
        config: Dict, strategy: TransformerApplicationStrategy
) -> Union[Dict[str, Union[str, bool]], List[Dict[str, Union[str, bool]]]]:
    """Read the config and build a list of directives acting as *structure transformers*.

    Note:
        At the moment, the exact return type depends on the strategy.

    Args:
        config: A deserialized config containing style transformer configurations.
        strategy: A strategy deciding by what logic to build the style parameters

    Returns:
        A list of direcvties acting ast *structure transformers* if strategy is
        :attr:`arttabgen.types_.transformer_application_strategy.TransformerApplicationStrategy.SELECTIVE`.

        A list OF LISTS of direcvties acting as *structure transformers* if strategy is
        :attr:`arttabgen.types_.transformer_application_strategy.TransformerApplicationStrategy.COMBINAORICAL`.
        Every outer list item handles a single structure parameter, every inner list contains directives including
        that structure parameter.

        See also:
            | :ref:`Config`
            | :ref:`Transformers`
            | :ref:`Transformer application strategies`
            | :mod:`arttabgen.types_.transformer_application_strategy`
            | :mod:`arttabgen.structure_transformer`

    """
    structure_parameter_declarations: List[StructureParameter] = []

    for parameter in config[ConfigMainKeys.STRUCTURE_PARAMETERS]:
        structure_parameter_declarations.append(
            dacite.from_dict(data_class=StructureParameter, data=parameter)
        )

    if strategy == TransformerApplicationStrategy.SELECTIVE:
        return {
            structure_parameter.name: structure_transformer.STRUCTURE_TRANSFORMERS[
                structure_parameter.name
            ](random_value_from_discrete(structure_parameter.value))
            for structure_parameter in structure_parameter_declarations
        }

    elif strategy == TransformerApplicationStrategy.COMBINATORICAL:
        combinations: List[Dict[str, Union[str, bool]]] = []

        for parameter in structure_parameter_declarations:
            values: List = parameter.value

            combination: List = []

            for value in values:
                combination.append(
                    {
                        parameter.name: structure_transformer.STRUCTURE_TRANSFORMERS[
                            parameter.name
                        ](value)
                    }
                )

            combinations.append(combination)

        return combinations
