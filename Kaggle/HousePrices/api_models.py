from pydantic import BaseModel, Field
from typing import Annotated, Optional
from enums import Neighborhood

class SalePriceRequest(BaseModel):
    # Mandatory params - without these, the model will be too error-prone
    quality_score_outof10: Annotated[int, Field(
        strict=True, ge=1, le=10,
        description="Quality score of the house on a scale of 1 to 10.")]

    living_area_sqft: Annotated[float, Field(
        strict=True, ge=0,
        description="Living area in square feet.")]

    basement_sqft: Annotated[float, Field(
        strict=True, ge=0,
        description="Basement area in square feet.")]

    # Optional params
    neighbourhood: Optional[Annotated[Neighborhood, Field(
        None, description="Neighborhood where the house is located.")]]

    rooms: Optional[Annotated[int, Field(
        strict=True, ge=0,
        description="Number of rooms in the house.")]]

    bathrooms: Optional[Annotated[int, Field(
        strict=True, ge=0,
        description="Number of bathrooms in the house.")]]

    fireplaces: Optional[Annotated[int, Field(
        strict=True, ge=0,
        description="Number of fireplaces in the house.")]]

    garage_n_cars: Optional[Annotated[int, Field(
        strict=True, ge=0,
        description="Number of cars the garage can accommodate.")]]

    first_floor_sqft: Optional[Annotated[float, Field(
        strict=True, ge=0,
        description="First floor area in square feet.")]]

    garage_area_sqft: Optional[Annotated[float, Field(
        strict=True, ge=0,
        description="Garage area in square feet.")]]

    lot_area: Optional[Annotated[float, Field(
        strict=True, ge=0,
        description="Lot area in square feet.")]]

    year_built: Optional[Annotated[int, Field(
        strict=True, ge=1800,
        description="Year the house was built.")]]

    year_remodelled: Optional[Annotated[int, Field(
        strict=True, ge=1800,
        description="Year the house was remodeled.")]]

    garage_year_built: Optional[Annotated[int, Field(
        strict=True, ge=1800,
        description="Year the garage was built.")]]

    year_exp_sale: Optional[Annotated[int, Field(
        strict=True, ge=1950,
        description="Year of expected sale.")]]

    model_config = {"json_schema_extra": {"examples": [{
            "summary": "Example house",
            "description": "An example house for sale price prediction based on various parameters.",
            "value": {
                "quality_score_outof10": 7,
                "living_area_sqft": 1710.0,
                "basement_sqft": 856.0,
                "neighbourhood": "NAmes",
                "rooms": 8,
                "bathrooms": 2,
                "fireplaces": 0,
                "garage_n_cars": 2,
                "first_floor_sqft": 856.0,
                "garage_area_sqft": 548.0,
                "lot_area": 8450.0,
                "year_built": 2019,
                "year_remodelled": None,  # We support optional parameters
                "garage_year_built": 2019,
                "year_exp_sale": 2024
            }
        }]}}
