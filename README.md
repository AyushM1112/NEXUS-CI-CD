# NEXUS — Real CI/CD + Jenkins + Docker + AI DevOps Workspace

NEXUS is a practical DevOps project designed to run as a real application, not a simulation.

## Real delivery path

Git/GitHub → Jenkins → Install → pytest → Docker build → Docker deployment → HTTP health check → NEXUS reads real Jenkins data → ChatGPT analyzes real evidence.

## What is genuinely connected

- Git/GitHub — source control and push-based delivery.
- Jenkins — pipeline execution through `Jenkinsfile`.
- pytest — real automated quality gate.
- JUnit — Jenkins test reporting.
- Docker — real image build and container deployment.
- Flask/Gunicorn — real application running inside the container.
- `/health` — real deployment verification endpoint.
- Jenkins REST API — dashboard pulls real job/build/console information.
- ChatGPT — external AI tool used on real Jenkins logs and the real Jenkinsfile.

There are no hardcoded build numbers, success rates, deployment results, or fake incident buttons.

## 1. Run locally

PowerShell:

```powershell
cd NEXUS_Real_CICD_AI
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
.\.venv\Scripts\python.exe apppp.py
```

Open `http://localhost:5000`.

Run tests:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

## 2. Run with Docker

```powershell
docker build -t nexus-devops:local .
docker run --rm -p 5000:5000 --name nexus-devops nexus-devops:local
```

## 3. GitHub

```powershell
git init
git add .
git commit -m "Initial NEXUS DevOps project"
git branch -M main
git remote add origin <YOUR_GITHUB_REPOSITORY_URL>
git push -u origin main
```

## 4. Jenkins

Create a Pipeline job named:

```text
NEXUS-CI-CD
```

Use **Pipeline script from SCM → Git**, point it at your GitHub repository, use branch `*/main`, and set Script Path to `Jenkinsfile`.

The Jenkins agent must have Git, Python 3, Docker and curl. A Linux/WSL agent is the simplest choice for the supplied Jenkinsfile.

Useful Jenkins plugins:

- Pipeline
- Git
- JUnit
- GitHub integration if using webhooks

## 5. Connect the dashboard to Jenkins

Copy `.env.example` to `.env` and set:

```text
JENKINS_URL=http://localhost:8080
JENKINS_USER=your-jenkins-username
JENKINS_TOKEN=your-api-token
JENKINS_JOB=NEXUS-CI-CD
```

Restart NEXUS.

The dashboard then reads actual Jenkins REST API data: latest build, build history, durations, console output and optional Workflow API stages.

The token remains server-side.

## 6. Real CI/CD trigger

For an automatic GitHub trigger, enable the GitHub webhook trigger in the Jenkins job. Jenkins must be reachable by GitHub.

If Jenkins is local, you can use your existing Cloudflare Tunnel setup to expose Jenkins temporarily. The GitHub webhook endpoint is:

```text
/github-webhook/
```

Then:

```powershell
git add .
git commit -m "Update application"
git push
```

Jenkins should execute:

Checkout → Install → Test → Docker Build → Deploy → Health Check.

## 7. Real failure + AI RCA demonstration

Do not use a simulation button.

Temporarily change this real test:

```python
assert payload["status"] == "healthy"
```

to:

```python
assert payload["status"] == "broken"
```

Push the change.

Jenkins will genuinely fail the Test stage. Fetch the real console output in NEXUS and copy the RCA prompt. Paste it into ChatGPT.

Ask ChatGPT to identify:

1. failed stage
2. evidence
3. root cause
4. corrective action
5. prevention
6. failure category

Then restore the assertion and push again. Jenkins should pass and redeploy.

## 8. AI pipeline optimization

NEXUS can copy a prompt containing the actual Jenkinsfile. Paste it into ChatGPT and ask it to optimize:

- parallel execution
- dependency caching
- timeouts
- JUnit reporting
- cleanup
- Docker build efficiency
- failure diagnostics

The AI result is not hardcoded into NEXUS. ChatGPT is operating on the real project artifacts.

## 9. Recommended live IA sequence

1. Open NEXUS.
2. Show Jenkins connected.
3. Open the Jenkins job.
4. Show the Jenkinsfile.
5. Make a real code change.
6. `git add`, `git commit`, `git push`.
7. Show Jenkins executing.
8. Show pytest.
9. Show Docker build.
10. Show `docker ps`.
11. Show `/health`.
12. Refresh NEXUS and show the new real build.
13. Create the temporary test regression.
14. Show the real Jenkins failure.
15. Feed the real console log to ChatGPT.
16. Show the root-cause analysis.
17. Fix the issue and push again.
18. Show successful deployment.
19. Ask ChatGPT to optimize the Jenkinsfile.
