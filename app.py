from flask import Flask, request
from flask_restx import Resource, Api, fields
from random import randint
from time import sleep


from pathlib import Path
import json

app = Flask(__name__)
api = Api(app)


bmi_category_to_risk = {
    "UNDERWEIGHT": 3,
    "HEALTHY": 1,
    "OVERWEIGHT": 2,
    "OBESE": 3,
    "VERY_OBESE": 4,
}


age_bracket_to_risk = {
    "group_1": 1,
    "group_2": 1,
    "group_3": 2,
    "group_4": 4,
    "group_5": 5,
}

def compute_risk(bmi_category, underlying_health_issues, age_bracket):
    health_factor = 3 if underlying_health_issues else 0

    return (
        bmi_category_to_risk[bmi_category] * age_bracket_to_risk[age_bracket]
        + health_factor
    )


resource_fields = api.model(
    "Resource",
    {
        "bmi_category": fields.String(required=True, enum=["UNDERWEIGHT", "HEALTHY", "OVERWEIGHT", "OBESE", "VERY_OBESE"]),
        "underlying_health_issues": fields.Boolean(required=True),
        "age_group": fields.String(required=True, enum=["group_1", "group_2", "group_3", "group_4", "group_5"]),
    },
)


@api.route("/baseline_risk")
class BaseLine(Resource):
    @api.expect(resource_fields, validate=True)
    def post(self):
        body = request.get_json(force=True)

        bmi_category = body["bmi_category"]
        underlying_health_issues = body["underlying_health_issues"]
        age_group = body["age_group"]

        risk_category = compute_risk(
            bmi_category, underlying_health_issues, age_group
            )

        sleep(randint(0, 3))
        return {"risk_category": min(risk_category, 10)}


if __name__ == "__main__":
    app.run()
