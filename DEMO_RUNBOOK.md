# NEXUS IA-1 — LIVE DEMO RUNBOOK

## Before the demo

Start Jenkins, Docker and NEXUS. Confirm the Jenkins API is connected on the dashboard, the NEXUS container is running, and the GitHub webhook works.

## Demo sequence

### 1 — Application
Open `http://localhost:5000`.

Say:

> This is the live NEXUS control center. The values shown here are pulled from my running application and Jenkins. There are no simulated build values.

### 2 — CI
Make a small real application change:

```powershell
git add .
git commit -m "Update application"
git push
```

Show Jenkins receiving the change.

### 3 — Automated testing
Show the Test stage and JUnit report.

Say:

> The pipeline runs real pytest tests and publishes the results to Jenkins using JUnit.

### 4 — Docker
Show Docker Build, then:

```bash
docker ps
```

Say:

> After the quality gate passes, Jenkins creates the Docker image and replaces the previous running container.

### 5 — Deployment verification
Open:

```text
http://localhost:5000/health
```

Say:

> The deployment is not considered successful until the health check returns a healthy response.

### 6 — AI root-cause analysis
Temporarily change:

```python
assert payload["status"] == "healthy"
```

to:

```python
assert payload["status"] == "broken"
```

Push it. Show the real Jenkins failure. Fetch the console in NEXUS. Copy the RCA prompt and paste it into ChatGPT.

Say:

> ChatGPT is receiving the actual Jenkins evidence and is being used as a DevOps root-cause analysis assistant.

Fix the assertion and push again.

### 7 — AI optimization
Use the NEXUS optimization prompt, paste it into ChatGPT, and request an improved Jenkinsfile.

Say:

> AI is being used both for incident analysis and for optimization of the actual CI/CD pipeline.
