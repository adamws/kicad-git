# kicad-git

[![CircleCI](https://circleci.com/gh/adamws/kicad-git.svg?style=shield)](https://circleci.com/gh/adamws/kicad-git/tree/master)
:warning: This is work in progress

KiCad plugin for git integration. Commit changes without leaving PCB editor window.

## Features

- [x] Commit changes from `pcbnew` window

## Installation

This plugin is not released yet and it is not available in KiCad's official plugin repository.
In order to install via `Plugin and Content Manager` grab latest package build from circleci
and use `Install from File...` option or alternatively checkout this repository
and copy (or link) content of `source` directory to on of the KiCad's plugin search paths.
For more details see [this](https://dev-docs.kicad.org/en/python/pcbnew/) guide.

## How to use?

- Click plugin button to open commit window

  ![toolbar-image](resources/toolbar.png)
