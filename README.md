# My DIY Static Website Builder

This is a simple static website builder written in Python. I built https://amirkarimi.dev using it.

## Setup

```
npm install
uv sync
uv run playwright install chromium
```

The last command downloads the headless Chromium browser used to render the
resume PDF. On Linux releases newer than Playwright's prebuilt browsers (e.g.
Ubuntu 26.04), the download is rejected with an "unsupported platform" error;
pin a supported platform for the install step:

```
PLAYWRIGHT_HOST_PLATFORM_OVERRIDE=ubuntu24.04-x64 uv run playwright install chromium
```

## Run

To run in development mode run the following after installing the dependencies:

```
uv run python main.py serve --watch
```

## Build

To generate the final website run:

```
uv run python main.py build
```
