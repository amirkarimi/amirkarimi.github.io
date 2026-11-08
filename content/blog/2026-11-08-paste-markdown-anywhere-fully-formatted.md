---
date: 2026-11-08
title: Paste Markdown Anywhere, Fully Formatted
slug: paste-markdown-anywhere-fully-formatted
keywords: linux, markdown, productivity, cli
template: post.html
---

I write almost everything in Markdown: notes, docs, PR descriptions, even drafts of emails. The trouble starts when I paste that Markdown into Outlook, Gmail or Google Docs and end up with a wall of `**asterisks**` and `## hashes`. Not a great look.

What I wanted was dead simple. I copy some Markdown, press a key, and paste nicely formatted text into whatever app I'm using.

Turns out it's a one-liner on Linux.

<!--more-->

## The trick

Two tools do all the work:

- **pandoc** converts the Markdown into HTML.
- **xclip** (on X11) or **wl-clipboard** (on Wayland) reads from and writes to the clipboard.

The secret sauce is putting the result back on the clipboard as `text/html`. Pretty much every rich text editor checks for that type when you paste, so it renders the formatting instead of showing raw text. That covers:

- **Email:** Outlook (desktop and web), Gmail, Thunderbird
- **Docs:** Google Docs, Microsoft Word, LibreOffice Writer
- **Wikis and chat:** Confluence, Microsoft Teams, and most web apps with a "rich" editor

Install the bits:

```bash
sudo apt install pandoc xclip        # X11
sudo apt install pandoc wl-clipboard # Wayland
```

## The one-liner

On **X11**:

```bash
xclip -selection clipboard -o | pandoc -f gfm -t html | xclip -selection clipboard -t text/html
```

On **Wayland**:

```bash
wl-paste | pandoc -f gfm -t html | wl-copy --type text/html
```

That's it. Copy your Markdown, run the command, then paste into your email or doc. Headings, bold, lists, links and tables all show up properly.

## Make it a script

I don't want to remember which display server I'm on, so I wrapped both versions in a tiny script at `~/bin/md2clip`:

```bash
#!/usr/bin/env bash
set -euo pipefail
if [ -n "${WAYLAND_DISPLAY:-}" ]; then
  wl-paste | pandoc -f gfm -t html | wl-copy --type text/html
else
  xclip -selection clipboard -o | pandoc -f gfm -t html | xclip -selection clipboard -t text/html
fi
```

```bash
chmod +x ~/bin/md2clip
```

## Bind it to a key

This is where it gets really nice. Open your desktop's keyboard shortcut settings and bind `md2clip` to something like **Super+M**. Now the whole flow is:

1. Copy the Markdown
2. Hit Super+M
3. Paste into Gmail, Outlook, Docs, wherever

No browser extension, no online converter, no fiddling.

## A few gotchas

- **Plain-text paste goes blank.** After you run the script, the clipboard only holds HTML. If you paste into a terminal you'll get nothing, so just copy the source again.
- **Every app is picky in its own way.** Each editor decides which bits of HTML it keeps. Outlook's desktop app is the strictest, and Gmail drops some styling too. Code blocks usually keep their monospace font but lose the grey background. Headings, lists, links and tables come through almost everywhere.
- **`xclip` hangs around on purpose.** It stays running to serve the clipboard. If the paste comes up empty when you trigger it from a shortcut, add `-loops 1` to the last `xclip` call or launch the script with `setsid`.
- **Pick your flavour.** `-f gfm` is GitHub-flavoured Markdown, which handles tables and fenced code. Swap in `-f markdown` if you prefer pandoc's own dialect.
