import os
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
START_TIME = time.time()

app = Flask(__name__)

JENKINS_URL = os.getenv("JENKINS_URL", "").rstrip("/")
JENKINS_USER = os.getenv("JENKINS_USER", "")
JENKINS_TOKEN = os.getenv("JENKINS_TOKEN", "")
JENKINS_JOB = os.getenv("JENKINS_JOB", "NEXUS-CI-CD")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")


def jenkins_configured():
    return bool(JENKINS_URL and JENKINS_USER and JENKINS_TOKEN)


def jenkins_get(path, params=None):
    if not jenkins_configured():
        return None, "Jenkins credentials are not configured."

    try:
        response = requests.get(
            f"{JENKINS_URL}{path}",
            params=params,
            auth=(JENKINS_USER, JENKINS_TOKEN),
            timeout=6,
        )
        response.raise_for_status()
        return response, None
    except requests.RequestException as exc:
        return None, str(exc)


def job_path():
    return f"/job/{quote(JENKINS_JOB, safe='')}"


@app.get("/")
def index():
    return render_template(
        "index.html",
        job=JENKINS_JOB,
        jenkins_url=JENKINS_URL,
        app_version=APP_VERSION,
    )


@app.get("/health")
def health():
    return jsonify({
        "status": "healthy",
        "service": "nexus-devops-dashboard",
        "version": APP_VERSION,
        "uptime_seconds": int(time.time() - START_TIME),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })


@app.get("/api/jenkins/overview")
def jenkins_overview():
    response, error = jenkins_get(
        f"{job_path()}/api/json",
        {"tree": "name,url,color,lastBuild[number,result,duration,timestamp,building,url,displayName],lastSuccessfulBuild[number,result,duration,timestamp,url],lastFailedBuild[number,result,duration,timestamp,url]"},
    )
    if error:
        return jsonify({
            "connected": False,
            "configured": jenkins_configured(),
            "error": error,
            "job": JENKINS_JOB,
            "jenkins_url": JENKINS_URL,
        })

    return jsonify({
        "connected": True,
        "configured": True,
        "job": response.json(),
        "job_name": JENKINS_JOB,
        "jenkins_url": JENKINS_URL,
    })


@app.get("/api/jenkins/builds")
def jenkins_builds():
    response, error = jenkins_get(
        f"{job_path()}/api/json",
        {"tree": "builds[number,result,duration,timestamp,building,url,displayName]"},
    )
    if error:
        return jsonify({"connected": False, "configured": jenkins_configured(), "error": error, "builds": []})

    builds = response.json().get("builds", [])[:15]
    for build in builds:
        if build.get("duration") is not None:
            build["duration_seconds"] = round(build["duration"] / 1000, 1)
        if build.get("timestamp"):
            build["timestamp_iso"] = datetime.fromtimestamp(
                build["timestamp"] / 1000, tz=timezone.utc
            ).isoformat()

    return jsonify({"connected": True, "builds": builds, "job_name": JENKINS_JOB})


@app.get("/api/jenkins/console/latest")
def latest_console():
    response, error = jenkins_get(
        f"{job_path()}/api/json",
        {"tree": "lastBuild[number,result,building]"},
    )
    if error:
        return jsonify({"connected": False, "error": error}), 503

    build = response.json().get("lastBuild")
    if not build:
        return jsonify({"connected": True, "message": "No Jenkins builds exist yet.", "console": ""})

    console_response, error = jenkins_get(f"{job_path()}/{build['number']}/consoleText")
    if error:
        return jsonify({"connected": False, "error": error}), 503

    return jsonify({
        "connected": True,
        "build_number": build["number"],
        "result": build.get("result"),
        "building": build.get("building", False),
        "console": console_response.text,
    })


@app.get("/api/jenkins/stages/<int:build_number>")
def jenkins_stages(build_number):
    response, error = jenkins_get(f"{job_path()}/{build_number}/wfapi/describe")
    if error:
        return jsonify({
            "available": False,
            "build_number": build_number,
            "error": error,
            "stages": [],
        })

    data = response.json()
    return jsonify({
        "available": True,
        "build_number": build_number,
        "status": data.get("status"),
        "stages": data.get("stages", []),
    })


@app.get("/api/pipeline-source")
def pipeline_source():
    try:
        return jsonify({"source": (BASE_DIR / "Jenkinsfile").read_text(encoding="utf-8")})
    except OSError as exc:
        return jsonify({"error": str(exc)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=False)
