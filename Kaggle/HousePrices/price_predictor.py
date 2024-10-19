import pandas as pd
import lightgbm as lgb


class PricePredictor:

    def __init__(self):
        self.model = lgb.Booster(model_file="lgbm__15feat.bin")

    def predict(self, query: pd.Series) -> float:
        prediction_usd = self.model.predict(query)
        return prediction_usd

class FeaturePreprocessor:
    pass