from __future__ import annotations


import matplotlib.pyplot as plt
from pandas import DataFrame

from generator import Triplet

from gooddata_pandas import DataFrameFactory
from statsmodels.stats.diagnostic import het_white, normal_ad
from statsmodels.stats.stattools import durbin_watson
import statsmodels.api as sm
import seaborn as sns


class MyLinearRegression:

    def __init__(self, df_factory: DataFrameFactory, triplet: Triplet):
        self.df_factory = df_factory
        self.triplet = triplet
        self.data_frame = df_factory.not_indexed(triplet.as_computable_dictionary)

        self.X = self.data_frame.iloc[:, 1].values.reshape(-1, 1)
        self.Y = self.data_frame.iloc[:, 2].values.reshape(-1, 1)

        self.model = None
        self.assumptions_results = dict()
        self.assumptions = dict()

    def check_assumptions(self,
                          sample_size=10,
                          linearity_threshold=0.7,
                          homoscedasticity_threshold=0.05,
                          independence_interval=None,
                          normality_threshold=0.05):
        if independence_interval is None:
            independence_interval = [1.5, 2.5]
        if not self.data_frame.isnull().values.any() and self.data_frame.shape[0] > sample_size:
            x = sm.add_constant(self.X)
            self.model = sm.OLS(self.Y, x).fit()

            self.assumptions["linearity_assumption"] = self.linearity_assumption()
            self.assumptions["homoscedasticity_assumption"] = self.homoscedasticity_assumption()
            self.assumptions["independence_assumption"] = self.independence_assumption()
            self.assumptions["normality_assumption"] = self.normality_assumption()

            self.assumptions_results["linearity_assumption"] = linearity_threshold < abs(
                self.assumptions["linearity_assumption"].unstack().sort_values(kind="quicksort")[
                    0])
            self.assumptions_results["homoscedasticity_assumption"] = self.assumptions["homoscedasticity_assumption"][
                                                                          "p-value"] > homoscedasticity_threshold
            self.assumptions_results["independence_assumption"] = independence_interval[0] < self.assumptions[
                "independence_assumption"] and self.assumptions["independence_assumption"] < independence_interval[1]

            self.assumptions_results["normality_assumption"] = self.assumptions[
                                                                   "normality_assumption"][1] > normality_threshold

    @property
    def valid_assumptions(self) -> bool:
        if self.assumptions_results:
            return all(self.assumptions_results.values())
        return False

    @property
    def valid_assumptions_count(self) -> int:
        return list(self.assumptions_results.values()).count(True)

    def linearity_assumption(self) -> DataFrame:
        """
        Assumption: The existence of a linear relationship between variables.
        _____________________________________________________________________
        Pearson correlation coefficient is used.
        :return:
        """
        # Explicit say that I want the second and the third columns
        return self.data_frame.iloc[:, 1:3].corr()

    def homoscedasticity_assumption(self) -> dict[str, float]:
        """
        Assumption: The variance of residual is the same for any value of X.
        ________________________________________________________
        Since the p-value is not less than 0.05, we fail to reject the null hypothesis.
        Null (H0): Homoscedasticity is present (residuals are equally scattered)
        :return:
        """
        test_values = het_white(self.model.resid, self.model.model.exog)
        labels = ['Test Statistic', 'p-value', 'F-Statistic', 'F-Test p-value']
        return dict(zip(labels, test_values))

    def independence_assumption(self) -> float:
        """
        Assumption: Residuals are independent of each other.
        ____________________________________________________
        The value should be inside interval 1.5 < x < 2.5
        :return:
        """
        return durbin_watson(self.model.resid)

    def normality_assumption(self) -> float:
        """
        Assumption: Residuals are normally distributed.
        ____________________________________________________
        Residuals are normally distributed if p_value > p_value_threshold. p_value < 0.05 is no go.
        :return:
        """
        return normal_ad(self.model.resid)

    def visualize(self):
        if self.model:
            sns.regplot(x=self.data_frame.columns[1], y=self.data_frame.columns[2], data=self.data_frame).set(
                title=f"Using attribute {self.data_frame.columns[0]}")
            plt.show()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.triplet == other.triplet

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}{self.triplet}"
