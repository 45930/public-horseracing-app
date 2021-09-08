import code
import pandas as pd
import tensorflow as tf
import numpy as np

from main import live_odds_model


class TensorFlowPredictor(object):
    def __init__(self, data, use_odds=False):
        self.data = data
        self.use_odds = use_odds

    def call(self):
        dummy_race = pd.DataFrame([
            [0, 1, 'dmr', 'gstk', 'f', 'd', 's', 1.0, 2],
            [0, 2, 'bel', 'alw', 'm', 't', '', 2.0, 3],
            [0, 3, 'pid', 'aoc', 'h', 'x', '', 3.0, 4],
            [0, 4, 'pid', 'aoc', 'c', 'd', '', 4.0, 5],
            [0, 5, 'pid', 'aoc', 'c', 'd', '', 4.0, 2],
            [0, 6, 'pid', 'aoc', 'c', 'd', '', 4.0, 2],
            [0, 7, 'pid', 'aoc', 'c', 'd', '', 4.0, 2],
            [0, 8, 'pid', 'aoc', 'c', 'd', '', 4.0, 2],
            [0, 9, 'pid', 'aoc', 'c', 'd', '', 4.0, 2],
            [0, 10, 'pid', 'aoc', 'c', 'd', '', 4.0, 2],
            [0, 11, 'pid', 'aoc', 'c', 'd', '', 4.0, 2],
            [0, 12, 'pid', 'aoc', 'c', 'd', '', 4.0, 2],
            [0, 13, 'pid', 'aoc', 'c', 'd', '', 4.0, 2],
            [0, 14, 'pid', 'aoc', 'c', 'd', '', 4.0, 2],
            [0, 15, 'pid', 'aoc', 'c', 'd', '', 4.0, 2],
            [0, 16, 'pid', 'aoc', 'c', 'd', '', 4.0, 2],
            [0, 17, 'pid', 'aoc', 'c', 'd', '', 4.0, 2],
            [0, 18, 'pid', 'aoc', 'c', 'd', '', 4.0, 2],
            [0, 19, 'pid', 'aoc', 'c', 'd', '', 4.0, 2],
            [0, 20, 'pid', 'aoc', 'c', 'd', '', 4.0, 2]
        ], columns=['race_id', 'post_position', 'race_track_code', 'race_classification', 'horse_sex', 'race_surface', 'race_state_bred', 'quarter', 'age'])

        df = pd.concat([self.data, dummy_race]).fillna(0).reset_index()
        df['track_tier'] = self.track_tiers(df['race_track_code'])
        df['class_tier'] = self.class_tiers(df['race_classification'])
        df = self.create_categorical(df, 'race_surface')
        df = self.create_categorical(df, 'horse_sex')
        df = self.create_categorical(df, 'race_state_bred')
        df = self.create_categorical(df, 'track_tier')
        df = self.create_categorical(df, 'class_tier')
        df = self.create_categorical(df, 'quarter')
        df = self.create_categorical(df, 'age')
        df['sprint'] = (df.race_distance < 7).astype(int)
        df['route'] = (df.race_distance >= 9).astype(int)

        race_filter = df.groupby('race_id')[
            'race_id'].agg(['count'])

        df = df.join(race_filter, on='race_id', how='inner')

        if self.use_odds:
            race_features = df[df.post_position == 1][['race_id',
                                                       'post_position',
                                                       'track_tier_TIER1',
                                                       'track_tier_TIER2',
                                                       'race_surface_d',
                                                       'race_surface_t',
                                                       'race_state_bred_s',
                                                       'class_tier_TIER1',
                                                       'class_tier_TIER2',
                                                       'class_tier_TIER3',
                                                       'quarter_1.0',
                                                       'quarter_2.0',
                                                       'quarter_3.0',
                                                       'quarter_4.0',
                                                       'field_size',
                                                       'sprint',
                                                       'route'
                                                       ]]

            model_data = df[[
                'race_id',
                'post_position',
                'horse_sex_f',
                'horse_sex_m',
                'horse_sex_c',
                'horse_sex_h',
                'age_2.0',
                'age_3.0',
                'lifetime_eps',
                'turf_eps',
                'pp_count',
                'total_perf',
                'total_beyer',
                'total_first_call',
                'total_second_call',
                'similar_perf',
                'similar_beyer',
                'similar_first_pos',
                'similar_second_pos',
                'dslr',
                'jock',
                'trainer',
                'count120',
                'track_itm',
                'implied_proba'
            ]]

            model_data = model_data.pivot(
                index='race_id', columns='post_position', values=model_data.columns[2:])

            model_data = race_features.join(
                model_data, on='race_id', how='inner')

            model_data = model_data.fillna(0)

            X = model_data[model_data.columns[2:]]

            from datetime import datetime

            model = live_odds_model

            pred_win_probability = model.predict(X)
            probabilities_vector = []
            for arr in pred_win_probability:
                probabilities = {}
                for i, probability in enumerate(arr):
                    probabilities[i+1] = round(float(probability), 3)
                probabilities_vector.append(probabilities)

            model_data['pred_win_probability_live'] = probabilities_vector
            return model_data[['race_id', 'pred_win_probability_live']]
        else:
            race_features = df[df.post_position == 1][['race_id',
                                                       'post_position',
                                                       'track_tier_TIER1',
                                                       'track_tier_TIER2',
                                                       'race_surface_d',
                                                       'race_surface_t',
                                                       'race_state_bred_s',
                                                       'class_tier_TIER1',
                                                       'class_tier_TIER2',
                                                       'class_tier_TIER3',
                                                       'quarter_1.0',
                                                       'quarter_2.0',
                                                       'quarter_3.0',
                                                       'quarter_4.0',
                                                       'field_size',
                                                       'sprint',
                                                       'route'
                                                       ]]

            df['implied_proba'] = df.morning_line_odds.apply(
                lambda x: self.convert_ml_odds(x))
            model_data = df[[
                'race_id',
                'post_position',
                'horse_sex_f',
                'horse_sex_m',
                'horse_sex_c',
                'horse_sex_h',
                'age_2.0',
                'age_3.0',
                'lifetime_eps',
                'turf_eps',
                'pp_count',
                'total_perf',
                'total_beyer',
                'total_first_call',
                'total_second_call',
                'similar_perf',
                'similar_beyer',
                'similar_first_pos',
                'similar_second_pos',
                'dslr',
                'jock',
                'trainer',
                'count120',
                'track_itm',
                'implied_proba'
            ]]

            model_data = model_data.pivot(
                index='race_id', columns='post_position', values=model_data.columns[2:])

            model_data = race_features.join(
                model_data, on='race_id', how='inner')

            model_data = model_data.fillna(0)

            X = model_data[model_data.columns[2:]]

            pred_win_probability = live_odds_model.predict(X)
            probabilities_vector = []
            for arr in pred_win_probability:
                probabilities = {}
                for i, probability in enumerate(arr):
                    probabilities[i+1] = round(float(probability), 3)
                probabilities_vector.append(probabilities)

            model_data['pred_win_probability'] = probabilities_vector
            return model_data[['race_id', 'pred_win_probability']]

    def create_categorical(self, df, col_name):
        df2 = df.groupby(col_name)[col_name].agg(['count'])
        df[col_name] = pd.Categorical(
            df[col_name], categories=df2.index, ordered=False)
        df[col_name] = df[col_name].cat.add_categories(
            "OTHER").fillna("OTHER")
        df = df.join(pd.get_dummies(
            df[col_name], prefix=col_name).astype(np.int))
        df = df.drop(col_name, axis=1)
        del df2
        return df

    def track_tiers(self, track_codes):
        tiers = {
            'dmr': 'TIER1',
            'kee': 'TIER1',
            'sa': 'TIER1',
            'sar': 'TIER1',
            'ap': 'TIER2',
            'aqu': 'TIER2',
            'bel': 'TIER2',
            'cd': 'TIER2',
            'gg': 'TIER2',
            'gp': 'TIER2',
            'mth': 'TIER2',
            'op': 'TIER2',
            'tam': 'TIER2',
            'wo': 'TIER2'
        }

        ret = []
        for tc in track_codes:
            if tc not in tiers.keys():
                ret.append('TIER3')
            else:
                ret.append(tiers[tc])
        return pd.Series(ret)

    def convert_ml_odds(self, string_odds):
        if '-' in str(string_odds):
            elements = string_odds.split('-')
            num = float(elements[0])
            den = int(elements[1])
            return 1.18 / (100*num/den)
        else:
            return 0.00001

    def class_tiers(self, race_class):
        tiers = {
            'gstk': 'TIER1',
            'stk': 'TIER2',
            'msw': 'TIER2',
            'alw': 'TIER2',
            'an1x': 'TIER3',
            'an2l': 'TIER3',
            'aoc': 'TIER3',
            'ocln': 'TIER3',
            'soc': 'TIER3',
            'str': 'TIER3',
            'shp': 'TIER3'
        }

        ret = []
        for rc in race_class:
            if rc not in tiers.keys():
                ret.append('TIER4')
            else:
                ret.append(tiers[rc])
        return pd.Series(ret)
