# kicad-git

[![CircleCI](https://circleci.com/gh/adamws/kicad-git.svg?style=shield)](https://circleci.com/gh/adamws/kicad-git/tree/master)
[![Coverage Status](https://coveralls.io/repos/github/adamws/kicad-git/badge.svg?branch=master)](https://coveralls.io/github/adamws/kicad-git?branch=master)

KiCad plugin for git integration. Launch [git](https://git-scm.com/docs/git-citool) commit graphical interface without leaving PCB editor window.

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
