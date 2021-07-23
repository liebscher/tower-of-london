from flask import Flask, request, abort, Response
import boto3
from botocore.exceptions import ClientError
import json
import os

BUCKET = "betterup-labs-prospection-research"

application = Flask(__name__, static_url_path='', static_folder='')

@application.route('/training')
def index_training():
    return application.send_static_file("training.html")

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
        print(f"Error 100: Please contact the study administrators: {e}")
        return {"msg": "Error 100: Please contact the study administrators: {e}"}

    try:
        s3 = boto3.session.Session().client("s3")

        response = json.loads(str(response))
        # print(response)
        # print(response[0])
        # print(response[0]["PID"])
        PID = [_dict["PID"] for _dict in response if "PID" in _dict]

        if len(PID) == 0:
            raise ValueError("PROLIFIC_PID not given.")

        PID = PID[0]
        if not PID or PID == "null":
            raise ValueError("Empty PROLIFIC_PID.")

        s3.upload_file("tmp.json", BUCKET, f"{PID}.json")
    except ClientError as e:
        print(f"Error 101: Please contact the study administrators: {e}")
        return {"msg": f"Error 101: Please contact the study administrators: {e}"}
    except ValueError as e:
        print(f"Error 102: Please contact the study administrators: {e}")
        return {"msg": f"Error 102: Please contact the study administrators: {e}"}
    except Exception as e:
        print(f"Error 103: Please contact the study administrators: {e}")
        return {"msg": f"Error 103: Please contact the study administrators: {e}"}
    finally:
        os.remove("tmp.json")
    
    return {"msg": "You may now continue to the next page."}

if __name__ == "__main__":
    application.debug = True
    application.run()