from __future__ import annotations
from config import Config

from pathlib import Path

from generator import generate_combinations, Triplet
from linear_regression import MyLinearRegression
from dotenv import load_dotenv
import pickle
from tqdm import tqdm

load_dotenv()

sdk = Config.sdk
pandas = Config.pandas


def set_up() -> None:
    sdk.catalog_data_source.load_and_put_declarative_data_sources(credentials_path=Path("credentials.yaml"),
                                                                  test_data_sources=True)
    sdk.catalog_workspace.load_and_put_declarative_workspaces()


def cache_combinations(workspace_id: str = Config.workspace_id, name: str = "combinations.pickle") -> None:
    combinations = generate_combinations(sdk, workspace_id)
    with open(name, "wb") as f:
        pickle.dump(combinations, f)


def load_combinations(name: str = "combinations.pickle") -> set[Triplet]:
    with open(name, "rb") as f:
        return pickle.load(f)


def run(generate: bool = False, workspace_id: str = Config.workspace_id) -> list[MyLinearRegression]:
    """
    :param generate: Flag to trigger generation. If  it is not defined then cached combinations are used
    :param workspace_id: The id of the workspace we want to explore
    :return: Sorted list of MyLinearRegression objects.
    Assumptions of these objects can be easily re-run with different values.
    """
    pandas_df = pandas.data_frames(workspace_id)

    if generate:
        combinations = generate_combinations(sdk, workspace_id)
    else:
        combinations = load_combinations("combinations.pickle")

    regressions = []

    # create object that perform linear regression
    print("Creating linear regression objects...")
    for combination in tqdm(combinations):
        regression = MyLinearRegression(pandas_df, combination)
        regressions.append(regression)

    # trigger assumptions check
    print("Running linear regression assumptions check...")
    for regression in tqdm(regressions):
        regression.check_assumptions()

    # sort results from the best to the worst
    # sorting can be customized i.e. sum of absolute difference between thresholds
    regressions = [r for r in regressions if r.assumptions_results]
    regressions.sort(key=lambda x: x.valid_assumptions_count, reverse=True)
    return regressions


def main():
    # This will set up whole GoodData CN CE environment for you
    set_up()

    # This will generate or load from cache all combinations and perform linear regression on them. The output is a
    # sorted list of linear regression, where the first object is the best pick for linear regression (passes the
    # most assumptions) and the last is the worst pick for linear regression.
    linear_regressions = run()

    # Have a look at the best linear regression.
    linear_regressions[0].visualize()

    # Have a look at the worst linear regression.
    linear_regressions[-1].visualize()

    # You are more than welcome to further examine these objects and check assumptions.


if __name__ == '__main__':
    main()
