# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.0](https://github.com/KristjanESPERANTO/LoneWatcher/compare/v0.3.0...v0.4.0) - 2015-06-17

### Added

- feat: add translations for author, license, and repository in info popup
- feat: log startup and shutdown events for LoneWatcher
- feat: log status change when a previously failed check now succeeds

### Changed

- feat: enhance action popup with detailed target information

## [0.3.0](https://github.com/KristjanESPERANTO/LoneWatcher/compare/v0.2.0...v0.3.0) - 2015-06-16

### Added

- ci: add linter workflow and requirements.txt
- feat: add info button to GUI
- docs: add `Windows Executable` section to README

### Changed

- ci: update build script for Windows
- feat: ping check fails only after the third fail and not after a single one
- l10n: update description
- refactor: handle linter issues

## [0.2.0](https://github.com/KristjanESPERANTO/LoneWatcher/compare/v0.1.1...v0.2.0) - 2015-06-02

### Changed

- chore: update screenshot
- refactor: rename config files
- feat: move timers to `config.toml`
- feat: move font_size to `config.toml`

### Added

- feat: add translations support
- refactor: add width setting to `config.toml`

## [0.1.1](https://github.com/KristjanESPERANTO/LoneWatcher/compare/v0.1.0...v0.1.1) - 2015-05-31

### Changed

- chore: add a `CHANGELOG.md` file
- gui: improve row highlighting (until next action instead of a timeout)
- gui: remove GUI focus stealing on error occurrence
- gui: reorder columns, replace button with symbol and vertical center row content

## [0.1.0](https://github.com/KristjanESPERANTO/LoneWatcher/tag/v0.1.0) - 2015-05-31

Initial release