# Dynamic Toll Charging System

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white) ![Django](https://img.shields.io/badge/Django-092E20?style=flat-square&logo=django&logoColor=white) ![Computer vision](https://img.shields.io/badge/Computer%20vision-YOLO%20%2B%20OCR-6D28D9?style=flat-square) ![Status](https://img.shields.io/badge/Status-Research%20prototype-64748B?style=flat-square)

A university research prototype for distance-based toll collection. It combines automatic number plate recognition (ANPR), RFID-based vehicle identification, entry/exit tracking and simulated toll payments to explore an alternative to fixed-price toll booths.

## Engineering highlights

- Computer vision for vehicle and number plate recognition using YOLO and OCR.
- RFID-based identification and an exit-point API.
- Django data models for vehicles, cameras, exit points, entry events and toll records.
- Distance-based charging logic and a simulated payment workflow.
- Web-based management interface for monitoring and administration.

## System workflow

```mermaid
flowchart TD
    A[Vehicle entry] --> B[Camera / plate recognition]
    B --> C[Vehicle entry record]
    C --> D[Exit point / RFID]
    D --> E[Match vehicle journey]
    E --> F[Calculate distance-based charge]
    F --> G[Simulated payment and toll record]
```

## Repository structure

| Path | Responsibility |
| --- | --- |
| `Core/` | Vehicle, entry, exit and toll models; core application workflows |
| `API/` | API endpoints for exit-point processing |
| `CoreApp/` | Django application configuration and URL routing |
| `Templates/` | Web interface templates |
| `Utils/` | Supporting utilities |
| `static/` | Frontend static assets |
| `requirements.txt` | Python dependencies |

## Local development

The project uses Django, Django REST Framework, OpenCV, OCR and ML tooling. Some vision dependencies are hardware- or platform-specific; review the pinned requirements before installation.

From the repository root:

```bash
python -m venv .venv
# Activate .venv using the command for your operating system.
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Configure test cameras, recognition model assets, exit points and RFID inputs for your local environment before running a complete vehicle journey. These are source-derived setup steps, not a verified deployment procedure.

## Publication

[Dynamic Toll Charging System — IJIRT (2026)](https://ijirt.org/article?manuscript=191077)

## Scope and limitations

The repository represents an academic research prototype. Payment and FASTag-style workflows are simulated; no live payment-network or highway integration is claimed. Real deployment would require validated recognition performance, secure secret management, privacy safeguards, production configuration, reliable hardware integration and regulatory review. Use synthetic or authorized test vehicle data.

For related engineering work and case studies, visit [andrewneil.dev](https://andrewneil.dev).
