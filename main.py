from typing import Union

from fastapi import FastAPI, UploadFile
from pydantic import BaseModel


app = FastAPI()

code = """
def print_name(): 
    print('Your code is getting executed ...')

"""
import docker
import os


@app.post("/")
async def execute_code(file: UploadFile):
    print(file.filename)  # pylint: disable=missing-function-docstring

    client = docker.from_env()
    dirname = os.path.split(os.path.abspath(__file__))[0]

    volumes = {
        os.path.join(dirname, "app"): {
            "bind": "/app/",
            "mode": "ro",
        }
    }
    container = client.containers.run(
        "python:3.10-slim",
        command="python /app/test.py",
        volumes=volumes,
        remove=False,  # Remove the container after it exits
        detach=True,
        working_dir="/app/",
    )  # Run container in the background

    # Stream container output
    response = container.wait()
    print(f"response => {response}")
    logs = container.logs().decode("utf-8")
    print(f"In local -- {logs}")
    # result = ""
    # for line in container.logs(stream=False):
    #     print(line)
    #     result += f"{line.decode().strip()}"

    return {"success": True, "result": logs}
