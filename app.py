import jsonpickle

from flask import Flask, Response, request, jsonify
from apifuncs import correlation, calculate


check_token = lambda token: True  # Perfection in Protection

api = Flask(__name__)


@api.route("/correlation", methods=['GET'])
def response_correlation():
    api_token = request.args.get("token")
    if check_token(api_token) is False:
        return Response(response=f"Authorization is false. Your api token {api_token} is wrong!",
                        status=403)
    x_data_type = request.args.get("x_data_type")
    y_data_type = request.args.get("y_data_type")
    user_id = request.args.get("user_id")

    corr_data = correlation(user_id, x_data_type, y_data_type)

    if not corr_data:
        return Response(response=f"There is not data about this parameters in database",
                        status=200)

    resp = {"user_id": user_id,
            "x_data_type": x_data_type,
            "y_data_type": y_data_type,
            "correlation": {
                "value": corr_data[0],
                "p_value": corr_data[1],
            }
            }
    json_resp = jsonpickle.encode(resp)

    return Response(response=json_resp, status=200, mimetype="application/json")


@api.route("/calculate", methods=['POST'])
def response_calculate():
    api_token = request.args.get("token")
    if check_token(api_token) is False:
        return Response(response=f"Authorization is false. Your api token {api_token} is wrong!",
                        status=403)
    json_data = request.get_json()

    user_id = json_data['user_id']

    x_data_type = json_data['data']['x_data_type']
    y_data_type = json_data['data']['y_data_type']

    x = json_data['data']['x']
    y = json_data['data']['y']

    corr_value, p_value = calculate(user_id, x_data_type, y_data_type, x, y)

    resp = {"user_id": user_id,
            "x_data_type": x_data_type,
            "y_data_type": y_data_type,
            "correlation": {
                "value": corr_value,
                "p_value": p_value,
                }
            }
    json_resp = jsonpickle.encode(resp)
    return Response(response=json_resp, status=200, mimetype="application/json")


if __name__ == '__main__':
    api.run(host='127.0.0.1')
