__version__ = "0.01"

import logging
import uvicorn
from typing import Annotated
from fastapi import FastAPI, Body, HTTPException


from api_models import SalePriceRequest
from price_predictor import PricePredictor

log = logging.getLogger(__name__)

app = FastAPI(
    title="Ames House Prices API",
    version=__version__
)

price_predictor = PricePredictor()


@app.post('/sale-price/predict', summary="Predict sale price (USD)")
def sale_price_predict(sale_price_request: SalePriceRequest):
    try:
        prediction_usd = None
        result = {"prediction_usd": prediction_usd}
        return result

    except (KeyError, ValueError, AttributeError) as e:
        raise HTTPException(status_code=500, detail=str(e))


# Allows debugging when running from IDE
if __name__ == "__main__":
    uvicorn.run(app, port=9010)