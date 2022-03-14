from __future__ import annotations

from gooddata_sdk import GoodDataSdk, CatalogFact, CatalogMetric
import itertools

from typing import Union, Any

Numeric = Union[CatalogFact, CatalogMetric]


class Triplet:

    def __init__(self, values: list):
        assert len(values) == 3
        self.values = values

    @property
    def as_computable_dictionary(self) -> dict[str, Any]:
        return {value.id: value.as_computable() for value in self.values}

    def __hash__(self) -> int:
        return hash([v.id for v in self.values].sort())

    def __str__(self) -> str:
        return self.__repr__()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.values == other.values

    def __repr__(self) -> str:
        ids = ",".join([str(v.id) for v in self.values])
        return f"{self.__class__.__name__}({ids})"


def generate_combinations(sdk: GoodDataSdk, workspace_id: str) -> set[Triplet]:
    """
    This function generates all triplets from workspace catalog.
    :param sdk: GoodDataSdk object to access workspace catalog.
    :param workspace_id: id of workspace where combination are going to be generated.
    :return: Set of all combination stored in Triplet object.
    """
    content_service = sdk.catalog_workspace_content
    catalog = content_service.get_full_catalog(workspace_id)

    # Get attributes
    attributes = []
    for dataset in catalog.datasets:
        attributes.extend(dataset.attributes)

    # Get metrics
    metrics = catalog.metrics

    # Get facts
    facts = []
    for dataset in catalog.datasets:
        facts.extend(dataset.facts)

    numbers: list[Numeric] = metrics + facts

    combinations = itertools.combinations(numbers, 2)
    result = set()
    for combination in combinations:
        valid_objects = content_service.compute_valid_objects(workspace_id, list(combination))
        for a in valid_objects.get("attribute", []):
            attribute = catalog.find_label_attribute(f"label/{a}")
            if attribute:
                result.add(Triplet([attribute] + list(combination)))
    return result
