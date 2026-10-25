<a href="https://velofy.co/">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="header/main-dark.svg">
    <img src="header/main-light.svg" alt="Velofy at velofy.co, an applied artificial intelligence (AI) and security lab in Delhi, India: applied AI and security research for real work. Below, a grid of the lab's public commits, one rounded square per day, lit in gold by the number of commits that day." width="100%" height="364" align="left">
  </picture>
</a>
<a href="https://velofy.co/open-source/">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="header/link-open-source-dark.svg">
    <img src="header/link-open-source-light.svg" alt="Browse Velofy's open source projects" width="107" height="48" align="left">
  </picture>
</a>
<a href="https://velofy.co/research/">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="header/link-research-dark.svg">
    <img src="header/link-research-light.svg" alt="Read Velofy's research" width="85" height="48" align="left">
  </picture>
</a>
<a href="https://velofy.co/bulletin/">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="header/link-bulletin-dark.svg">
    <img src="header/link-bulletin-light.svg" alt="Read the Bulletin, plain reviews of the latest AI models" width="70" height="48" align="left">
  </picture>
</a>
<a href="https://www.linkedin.com/company/velofy">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="header/link-linkedin-dark.svg">
    <img src="header/link-linkedin-light.svg" alt="Follow Velofy on LinkedIn" width="77" height="48" align="left">
  </picture>
</a>
<a href="https://cal.com/anishfyi">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="header/link-call-dark.svg">
    <img src="header/link-call-light.svg" alt="Book a call with Velofy" width="92" height="48" align="left">
  </picture>
</a>
<!-- A full-width empty image ends the floats, so Safari starts the text below the links. -->
<img src="data:null;," width="100%" height="0" align="left" alt="">
<br clear="left">

Velofy is an applied artificial intelligence (AI) and security lab in Delhi, India. We study how AI models find and fix vulnerabilities, build the harnesses and tools that agents run on, and publish what we measure.

Everything is documented at [velofy.co](https://velofy.co/). Source is on [GitHub](https://github.com/velofy).

## Why an applied AI and security lab

Start with what models can do now. They read a large codebase, plan work across many steps, call tools and act on what comes back. They also find real security bugs: since 2024, AI systems at Google, OpenAI, Anthropic, Microsoft and others have found hundreds of previously unknown vulnerabilities in software almost everyone runs.

Then look at where they break. An agent cannot see the page you are signed into, forgets the last session, and cannot be trusted near a production database. A model that reports a vulnerability usually cannot prove it on its own, so false alarms and duplicates pile up, and checking and fixing become the slow part. In both cases the model is rarely the limit. The limit is everything around it: the tools, the context it is given and the checks on what it does.

That work has no natural owner. The labs that train models are busy training them, and the companies that ship products are busy shipping. A lab between the two takes models to real work, measures where they fail, builds the missing piece and publishes it with the evidence.

Security belongs in the same lab. An agent that can act can also be misled, and a model that finds bugs can help an attacker as well as a defender. Building the tools and testing how they fail is one job, so we do both, in the open.

The longer version is the founder's note on [velofy.co/about](https://velofy.co/about/).

## Projects

Six of these are open source. Kestrel, Numera and Whiteboard are products with their own sites.

| Project | What it does | Links |
| --- | --- | --- |
| **Troy** | A free, open source Chromium browser for macOS and Windows. An AI agent attaches over the Chrome DevTools Protocol (CDP) to the session you are already signed into. | [Site](https://troy.velofy.co/) · [Docs](https://velofy.co/troy/) · [Source](https://github.com/velofy/troy) |
| **Kestrel** | An interactive coding command-line interface (CLI) in one static Rust binary for Windows, macOS and Linux. It drives the agent CLIs you already run and works with any model. | [Site](https://kestrel.velofy.co/) |
| **Numera** | The AI accountant for construction and commercial real estate: work-in-progress schedules, job costing, pay applications and retainage, kept current daily. | [Site](https://numera.velofy.co/) |
| **Whiteboard** | A shared workspace for AI agents and their harnesses: clear channels and threads, requests that become tickets, and autonomous work that stops for review. | [Site](https://whiteboard.velofy.co/) |
| **curl_reap** | A Python scraping library whose own transport sends a real browser's Transport Layer Security (TLS) handshake byte for byte, with self-healing selectors and a concurrent crawler on top. | [Docs](https://velofy.co/curl_reap/) · [Source](https://github.com/anishfyi/curl_reap) |
| **Terbium** | Rebuilds the tables in a Portable Document Format (PDF) file from the position of every word, reads slides, spreadsheets and images into the same shape, and sends only the tables it cannot resolve to a model. | [Docs](https://velofy.co/terbium/) · [Source](https://github.com/velofy/terbium) |
| **Trove** | Repository index and session memory for coding agents: a Rust engine that returns the context a task needs within a token budget, and a Claude Code plugin that keeps decisions between sessions. | [Docs](https://velofy.co/trove/) · [Source](https://github.com/anishfyi/trove) |
| **Querion** | A read-only analyst that answers plain-English questions about a Postgres database and shows the Structured Query Language (SQL) it ran, so every answer can be checked. It runs on the Claude Code CLI. | [Docs](https://velofy.co/querion/) · [Source](https://github.com/anishfyi/querion) |
| **glep** | Code search for AI coding agents: an indexed grep and glob in Rust, with ripgrep-compatible output and no daemon. | [Docs](https://velofy.co/glep/) · [Source](https://github.com/velofy/glep) |

## Recent research

[Zero-days found by AI systems: what the labs reported and what it costs](https://velofy.co/journal/zero-days-found-by-ai/). A zero-day is a vulnerability its maintainers do not know about yet. This is a sourced review of the ones AI systems at Google, OpenAI, Anthropic, Microsoft and others have found since 2024, the patterns behind them, and what defenders should do now that checking and fixing, not finding, is the slow part.

We also publish [research](https://velofy.co/research/) on how agent systems are built and measured, and the [Bulletin](https://velofy.co/bulletin/), plain reviews of the latest AI models.

## Install Troy

On macOS, Troy installs from the lab's Homebrew tap:

```sh
brew tap velofy/tap
brew trust --cask velofy/tap/troy
brew install --cask troy
```

Homebrew will not load a cask from a third-party tap until you trust it, so the second line is needed once. The app is not notarized by Apple, so you are trusting this source directly. It runs on Apple silicon and Intel with macOS 12 (Monterey) or later. For Windows, see [troy.velofy.co](https://troy.velofy.co/). Setup notes are in the [tap's README](https://github.com/velofy/homebrew-tap).

## Contact

Write to [anish@velofy.co](mailto:anish@velofy.co) or [book a call](https://cal.com/anishfyi).

Made with intent in Delhi, India.
