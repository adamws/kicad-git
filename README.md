# kicad-git

[![CircleCI](https://circleci.com/gh/adamws/kicad-git.svg?style=shield)](https://circleci.com/gh/adamws/kicad-git/tree/master)
:warning: This is work in progress

KiCad plugin for git integration. Commit changes without leaving PCB editor window.

## Features

- [x] Commit changes from `pcbnew` window

## Installation

This plugin is not released yet and it is not available in KiCad's official plugin repository.
Latest `master` build is automatically uploaded to unofficial PCM compatible
[repository](https://adamws.github.io/kicad-git/) hosted on GitHub pages.
In order to install it via `Plugin and Content Manager` add `https://adamws.github.io/kicad-git/repository.json`
to PCM repository list.

Alternatively checkout this repository and copy (or link) content of `source` directory
to one of the KiCad's plugin search paths.
For more details see [this](https://dev-docs.kicad.org/en/apis-and-binding/pcbnew/) guide.

## How to use?

- Click plugin button to open commit window

  ![toolbar-image](resources/toolbar.png)
