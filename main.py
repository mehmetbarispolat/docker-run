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
def execute_code(file: UploadFile):
    print(file.filename)  # pylint: disable=missing-function-docstring
    client = docker.from_env()
    volumes = {file.filename: {"bind": "/test.py", "mode": "ro"}}
    container = client.containers.run(
        "python:3.10-slim",
        command="python /test.py",
        volumes=volumes,
        remove=True,  # Remove the container after it exits
        detach=True,
    )  # Run container in the background

    # Stream container output
    result = ""
    for line in container.logs(stream=False):
        result += f"{line.decode().strip()}"

    return {"success": True, "result": result}
