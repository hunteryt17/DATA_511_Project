import warnings

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import loguniform
import pandas as pd

warnings.filterwarnings("ignore")


class Matcher:
    """
    Creates matched dataset based on propensity score.

    Class to create a matched dataset balanced for the control group to be the
    same size as the treatment group based on the variable of interest.
    ------
    Inputs:
    - data = pandas dataframe or csv file (depending on is_csv param)
             with fully cleaned data (see demo or README)
    - treatment_column = string of column corresponding to treatment group,
                         values should be binary with 1 representing
                         minority treatment group
    """

    def __init__(self, data, treatment_column):
        self.data = data
        self.treatment_column = treatment_column
        predictors = list(data.columns)
        predictors.remove(self.treatment_column)
        self.predictors = predictors

    def compute_matched_data(self):
        """
        Creates and returned matched dataset based on data & treatment column.

        This function runs all the logic to create the matched dataset from
        creating an optimal Logistic Regression Model to matching treatment
        data to matching each treatment sample to a control sample.
        ----
        Inputs:
        None
        Outputs:
        - matched_data = pandas dataframe of treatment group and matched
                     control group
        """

        print("Generating Logistic Regression Model...")
        self.__create_logistic_regression()

        print("Model Generated")
        self.__set_scores()

        print("Matching Propesensity Scores...")
        matched_data = self.__match()

        print("Matching Complete")
        return matched_data

    def __create_logistic_regression(self):
        model = LogisticRegression()

        # define search space
        params = {}
        params['solver'] = ['liblinear', 'newton-cg', 'lbfgs', 'saga']
        params['class_weight'] = ['balanced']
        params['penalty'] = ['l1', 'l2', 'elasticnet', 'none']
        params['C'] = loguniform(1e-5, 100)

        search = RandomizedSearchCV(model, params, scoring="roc_auc",
                                    n_iter=100, cv=10, random_state=1)

        X = self.data[self.predictors]
        y = self.data[self.treatment_column]

        result = search.fit(X, y)

        final_model = LogisticRegression(**result.best_params_)
        final_model.fit(X, y)
        self._final_model = final_model

    def __set_scores(self):
        self.data['SCORE'] = [score[1] for score in
                              self._final_model.predict_proba
                              (self.data[self.predictors])]

    def __match(self):
        treatment_scores = self.data[self.data[self.treatment_column]
                                     == 1][['SCORE']]
        control_scores = self.data[self.data[self.treatment_column]
                                   == 0][['SCORE']]
        match_indices = []

        for i in range(len(treatment_scores)):
            score = treatment_scores.iloc[i]
            temp_control = control_scores[~control_scores.index.isin(
                                          match_indices)]

            match = abs(temp_control - score).sort_values(by='SCORE').index[0]

            match_indices.append(match)

        treatment_group = self.data[self.data[self.treatment_column] == 1]
        matched_control_group = self.data[self.data.index.isin(match_indices)]

        matched_data = pd.concat([treatment_group, matched_control_group],
                                 axis=0)

        return matched_data
