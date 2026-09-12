<p align="center">
  <img src="assets/velofy-wordmark.png" alt="Velofy" width="360">
</p>

<p align="center"><strong>AI Native builders out of Delhi, India.</strong></p>

<p align="center">Open Source. by Nature.</p>

---

We build software that is AI native from the first commit: tools, frameworks, and harnesses designed for a world where AI agents write, read, and run code alongside people.

A consistent thesis runs through everything here — **build tools whose primary user is an AI agent, not a human.** Machine-readable contracts, `AGENTS.md` files, `llms.txt` discovery, and formats designed to be read correctly on the first pass.

## Frameworks

### Summit.js

[**Summit.js**](https://github.com/velofy/summitjs) is the open source, AI Agent Native JavaScript framework for composing behavior directly in your HTML. Drop in one script and go. No build step, no virtual DOM, no `eval`.

- **HTML-first and local.** Behavior lives on the element it affects, so an agent edits one place and sees the result.
- **Safe by construction.** Expressions are interpreted, never `eval`ed, so generated markup runs under a strict CSP.
- **Built to be read by machines.** `llms.txt`, full-corpus markdown, and a drop-in `AGENTS.md` brief for your own agent.
- **A UI library, included.** Accessible, token-themed components in about 13KB gzipped.

Docs: [velofy.github.io/summitjs](https://velofy.github.io/summitjs/)

## Agent tooling

| Project | What it does |
| --- | --- |
| [**troy**](https://github.com/velofy/troy) | A headless browser an agent can actually read: DOM for structure, OCR for the pixels the DOM cannot explain. |
| [**querion**](https://github.com/velofy/querion) | A strictly read-only, natural-language data analyst. Connect Postgres, add your API docs, ask in plain English. |
| [**trove**](https://github.com/velofy/trove) | Builds and maintains a personal, file-based semantic layer as you work, and reloads it every session. |
| [**terbium**](https://github.com/velofy/terbium) | Algorithmic multi-file parser (PDF/PPTX/XLSX/CSV) that scores its own confidence and only reaches for AI when genuinely stuck. |
| [**curl_reap**](https://github.com/velofy/curl_reap) | Browser-grade TLS impersonation, self-healing selectors, and a concurrent crawl engine in one library. `pip install curl-reap` |

## Developer tools

| Project | What it does |
| --- | --- |
| [**glep**](https://github.com/velofy/glep) | A faster, more ergonomic take on grep and glob. Written in Rust. |
| [**vaulty**](https://github.com/velofy/vaulty) | Transparent work-in-progress screen lock for macOS. Terminals stay live. |
| [**mac-uninstaller**](https://github.com/velofy/mac-uninstaller) | Fully uninstall macOS apps — bundle plus every leftover — and reclaim the space. |
| [**pawse**](https://github.com/velofy/pawse) | The pomeranian that makes you take breaks. |
| [**classy-fonts**](https://github.com/velofy/classy-fonts) | A cabinet of 324 free typefaces with a live specimen gallery, split by licence. |

Desktop apps install from our tap:

```sh
brew tap velofy/tap
```

---

<p align="center">Made with intent in Delhi, India 🇮🇳</p>
