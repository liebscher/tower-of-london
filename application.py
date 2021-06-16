from flask import Flask, request, abort, Response
import boto3
from botocore.exceptions import ClientError
import json
import os

BUCKET = "betterup-labs-prospection-research"

application = Flask(__name__, static_url_path='', static_folder='')

@application.route('/')
def index():
    return application.send_static_file("index.html")

@application.route('/save', methods=["POST"])
def save():
    try:
        response = request.form["data"]
        with open("tmp.json", "w") as f:
            # print(response)
            f.write(response)
    except Exception as e:
        abort(Response(f"Error 102: Please contact the study administrators: {e}"))


    try:
        s3 = boto3.session.Session().client("s3")

        response = json.loads(str(response))
        # print(response)
        # print(response[0])
        # print(response[0]["PID"])
        PID = [_dict["PID"] for _dict in response if "PID" in _dict][0]

        if not PID:
            raise Exception("Invalid PID")

        s3.upload_file("tmp.json", BUCKET, f"{PID}.json")
        print("uploaded")
    except ClientError as e:
        print("error 100")
        abort(Response(f"Error 100: Please contact the study administrators: {e}"))
    except Exception as e:
        print("error 101")
        abort(Response(f"Error 101: Please contact the study administrators: {e}"))
    finally:
        print("delete")
        os.remove("tmp.json")
    
    return Response("You may close this page now.")

@application.route('/next')
def next():
    return "You may now close this page."

if __name__ == "__main__":
    application.debug = True
    application.run()