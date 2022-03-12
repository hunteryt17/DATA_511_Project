import unittest
from unittest.mock import MagicMock, patch
import pandas as pd
from pandas.testing import assert_frame_equal, assert_series_equal
from sklearn.linear_model import LogisticRegression

from pypsm import matcher as m
from pypsm import match



def log_reg_proba(df):
    return pd.concat([df['pre_score'], df['pre_score']], axis=1).to_numpy()

test_dict1 = {'treat': [1, 1, 1, 0, 0, 0, 0, 0, 0, 0], \
'pre_score': [0.98, 0.95, 0.97, 0.96, 0.94, 0.91, 0.04, 0.4, 0.3, 0.1]}
test_df1 = pd.DataFrame(data=test_dict1)

model = LogisticRegression()
model.predict_proba = log_reg_proba

m_class = m.Matcher(test_df1, 'treat')
m_class._final_model = model
m_class._Matcher__create_logistic_regression = MagicMock(return_value=model)

test_output = './test_data/test_output.csv'

class TestMatcher(unittest.TestCase):

    
    def test_set_scores(self):
        m_class._Matcher__set_scores()

        temp_df = pd.DataFrame()
        temp_df['SCORE'] = test_df1['pre_score']

        m_class._Matcher__set_scores()

        assert_series_equal(temp_df['SCORE'], m_class.data['SCORE'])

    def test_match(self):

        m_class.data['SCORE'] = test_df1['pre_score']

        tmp_df1 = test_df1
        tmp_df1['SCORE'] = test_df1['pre_score']

        assert_frame_equal(tmp_df1[0:6], m_class._Matcher__match())

    def test_compute_matched(self):
        tmp_df1 = test_df1
        tmp_df1['SCORE'] = test_df1['pre_score']
        assert_frame_equal(tmp_df1[0:6], m_class.compute_matched_data())

class TestMatch(unittest.TestCase):

    def test_match(self):
        with patch('pypsm.matcher.Matcher') as mock:
            tmp_df1 = test_df1
            tmp_df1['SCORE'] = test_df1['pre_score']
            instance = mock.return_value
            instance.compute_matched_data.return_value = tmp_df1[0:6]
            tmp_df_csv = tmp_df1.reset_index()

            output_df = match.match(test_df1, 'treat', output_csv=test_output)

            output_csv = pd.read_csv(test_output)

            assert_frame_equal(tmp_df1[0:6], output_df)
            assert_frame_equal(tmp_df_csv[0:6], output_csv)


suite = unittest.TestLoader().loadTestsFromTestCase(TestMatcher)
_ = unittest.TextTestRunner().run(suite)

suite = unittest.TestLoader().loadTestsFromTestCase(TestMatch)
_ = unittest.TextTestRunner().run(suite)

