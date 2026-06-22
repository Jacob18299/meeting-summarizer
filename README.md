# Meeting Summarizer

Turn a messy meeting transcript into a clean summary — a short overview, the
decisions that were made, and a list of action items with who's responsible
for each.

The thing that makes it different: it runs **entirely on your own computer**.
It uses a free, local AI model (through a tool called
[Ollama](https://ollama.com)) instead of sending anything to the internet. No
accounts, no API keys, no costs, and your meeting notes never leave your
machine. That makes it safe to use even when the meeting content is private or
sensitive.

## What it does

You paste in a transcript, click one button, and get back three things:

- **Overview** — a couple of sentences capturing what the meeting was about.
- **Decisions** — the concrete things that were agreed on.
- **Action items** — the tasks, each tagged with who owns it.

## How it's built

The project has three simple parts that each do one job:

- **The AI part** (`summarizer.py`) — sends the transcript to the local AI and
  asks it to reply in a fixed, tidy format so the results always come back
  clean and ready to show on screen.
- **The server** (`app.py`) — a small program (built with Flask, a popular
  Python web tool) that loads the web page and passes your transcript to the
  AI part when you hit the button.
- **The web page** (`index.html`) — the screen you actually see and type into.

In other words: the page sends your text to the server, the server hands it to
the AI, and the summary comes back to the page. That same back-and-forth is how
most websites work.

```
web page  ──►  server  ──►  local AI (via Ollama)
   ▲                              │
   └───────  summary  ◄───────────┘
```

## Getting started

**You'll need** [Ollama](https://ollama.com) installed, with the AI model
downloaded once:

```bash
ollama pull llama3:8b
```

Then install the project's requirements:

```bash
pip3 install -r requirements.txt
```

## How to use it

1. Make sure Ollama is running.
2. Start the app:
   ```bash
   python3 app.py
   ```
3. Open `http://127.0.0.1:5001` in your browser.
4. Paste a transcript (there's a sample in `sample-transcript.txt` you can try
   first) and click **Summarize meeting**.

## Good to know

- A summary takes a few seconds, since the AI is running on your own machine
  rather than a powerful server — that's the trade-off for keeping everything
  private.
- Easy things to add next: let people upload a file instead of pasting, add a
  button to save the summary, or offer different summary styles.

## License

MIT
