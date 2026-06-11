# linguistics-digest

A small Python app that collects trending young English slang and sends a daily email digest.

## Setup

1. Create a Python environment.
2. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and fill in your SMTP/email settings.

## Run once

```bash
python main.py
```

## Run daily

```bash
python scheduler.py
```

This script uses `schedule` to send the digest at `08:00` local time. You can also use an OS scheduler like Task Scheduler to run `main.py` once per day.

## Windows Task Scheduler

1. Make sure `.env` is filled with your SMTP settings.
2. Open PowerShell and navigate to the project folder.
3. Run:

```powershell
.\setup_task_scheduler.ps1
```

4. Verify the task with:

```powershell
Get-ScheduledTask -TaskName LinguisticsDigestDailySlang
```

If you want a different send time, re-run the script with `-Time "HH:mm"`.

## What it does

- collects a short list of youth slang phrases
- fetches a real classic English quote from an external quote service
- formats a plain-text and HTML email
- sends the email through SMTP

## Notes

If Urban Dictionary is unavailable, the app falls back to a curated list of popular slang terms. The quote is fetched from quotable.io; if that service is unavailable, the email still sends with a note explaining the quote source is temporarily unreachable.
