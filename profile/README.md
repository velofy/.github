<picture>
  <source media="(prefers-color-scheme: dark)" srcset="header/top-dark.svg">
  <img src="header/top-light.svg" alt="Velofy, Delhi, India" width="100%" height="20" align="left">
</picture>
<br>
<img src="data:null;," width="100%" height="0" align="left" alt="">
<a href="https://velofy.co/open-source/">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="header/link-open-source-dark.svg">
    <img src="header/link-open-source-light.svg" alt="Browse Velofy's open source projects" width="110" height="18" align="left">
  </picture>
</a>
<img src="data:null;," width="100%" height="0" align="left" alt="">
<a href="https://velofy.co/research/">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="header/link-research-dark.svg">
    <img src="header/link-research-light.svg" alt="Read Velofy's research" width="110" height="18" align="left">
  </picture>
</a>
<img src="data:null;," width="100%" height="0" align="left" alt="">
<a href="https://velofy.co/bulletin/">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="header/link-bulletin-dark.svg">
    <img src="header/link-bulletin-light.svg" alt="Read the Bulletin, plain reviews of the latest AI models" width="110" height="18" align="left">
  </picture>
</a>
<img src="data:null;," width="100%" height="0" align="left" alt="">
<a href="https://www.linkedin.com/company/velofy">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="header/link-linkedin-dark.svg">
    <img src="header/link-linkedin-light.svg" alt="Follow Velofy on LinkedIn" width="110" height="18" align="left">
  </picture>
</a>
<img src="data:null;," width="100%" height="0" align="left" alt="">
<a href="https://cal.com/anishfyi">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="header/link-call-dark.svg">
    <img src="header/link-call-light.svg" alt="Book a call" width="110" height="18" align="left">
  </picture>
</a>
<img src="data:null;," width="100%" height="0" align="left" alt="">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="header/main-dark.svg">
  <img src="header/main-light.svg" alt="An applied AI lab in Delhi. We build the tools, frameworks and harnesses AI agents need to do real work, and publish every one in the open. Below it, a honeycomb of the lab's public commits, one cell per day." width="100%" height="290" align="left">
</picture>
<br clear="left">

Velofy is an open source applied AI lab based in Delhi, India. We build tools, frameworks and harnesses that are AI native from the first commit, designed for a world where AI agents write, read and run code alongside people.

Everything is documented at [velofy.co](https://velofy.co/). Source is on [GitHub](https://github.com/velofy).

## Why an applied AI lab

Velofy began in 2025 as a small studio doing backend work for other companies. Client work taught us speed, but it did not compound. The tools we kept rebuilding for each job did.

Those tools all filled the same kind of gap. Models can now read, plan and act. What has not caught up is everything around them. An agent cannot see the page you are signed into. It starts each session having forgotten the last one. It cannot be trusted near a production database. A spreadsheet or a slide deck comes back half read. A better model alone does not close that gap.

Closing it is nobody's main job. The labs that train models are busy training them, and the companies that ship products are busy shipping. An applied AI lab sits between the two: it takes a model to real work, finds where it breaks, builds the missing piece and publishes it with the evidence. So the studio became a lab, and each project below is our answer to one of those gaps.

The longer version is the founder's note on [velofy.co/about](https://velofy.co/about/).

## Projects

Seven of these are open source. Kestrel, Numera and Whiteboard are products with their own sites.

| Project | What it does | Links |
| --- | --- | --- |
| **Troy** | A free, open source Chromium browser for macOS and Windows. An AI agent attaches over the Chrome DevTools Protocol (CDP) to the session you are already signed into. | [Site](https://troy.velofy.co/) · [Docs](https://velofy.co/troy/) · [Source](https://github.com/velofy/troy) |
| **Kestrel** | An interactive coding command-line interface (CLI) in one static Rust binary for Windows, macOS and Linux. It drives the agent CLIs you already run and works with any model. | [Site](https://kestrel.velofy.co/) |
| **Numera** | The AI accountant for construction and commercial real estate: work-in-progress schedules, job costing, pay applications and retainage, kept current daily. | [Site](https://numera.velofy.co/) |
| **Whiteboard** | A shared workspace for AI agents and their harnesses: clear channels and threads, requests that become tickets, and autonomous work that stops for review. | [Site](https://whiteboard.velofy.co/) |
| **Summit.js** | A rugged, signal-powered framework for composing behavior directly in your HTML. Safe under a strict Content Security Policy (CSP), no build step, about 16KB gzipped. | [Site](https://summitjs.velofy.co/) · [Docs](https://velofy.co/summitjs/) · [Source](https://github.com/velofy/summitjs) |
| **curl_reap** | Reap the web: browser-grade Transport Layer Security (TLS) impersonation, self-healing selectors and a concurrent crawl engine in one library. | [Docs](https://velofy.co/curl_reap/) · [Source](https://github.com/anishfyi/curl_reap) |
| **Terbium** | An algorithmic multi-file parser (PDF, PPTX, XLSX, CSV) that scores its own confidence and only reaches for AI when it is genuinely stuck. | [Docs](https://velofy.co/terbium/) · [Source](https://github.com/velofy/terbium) |
| **Trove** | A Claude Code skill that builds and maintains a personal, file-based semantic layer as you work, and reloads it every session. | [Docs](https://velofy.co/trove/) · [Source](https://github.com/anishfyi/trove) |
| **Querion** | A strictly read-only, natural-language data analyst that plugs into any platform and runs on the Claude Code CLI. | [Docs](https://velofy.co/querion/) · [Source](https://github.com/anishfyi/querion) |
| **glep** | A command-line code search tool for AI coding agents: an indexed grep and glob with ripgrep-compatible output and no daemon. | [Docs](https://velofy.co/glep/) · [Source](https://github.com/velofy/glep) |

Beyond the code, we publish [research](https://velofy.co/research/) teardowns of how agent systems are built, and the [Bulletin](https://velofy.co/bulletin/), plain reviews of the latest AI models.

## Install desktop apps

```sh
brew tap velofy/tap
```

Setup notes are in the [tap's README](https://github.com/velofy/homebrew-tap).

Made with intent in Delhi, India.
