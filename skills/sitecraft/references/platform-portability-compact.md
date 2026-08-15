# Compact platform and browser portability

Use when a website must work across operating systems, browser engines, input methods, assistive technologies, or capture providers. Load `platform-and-browser-portability.md` for full detail.

## Contract

`implementation.browser_support` is the intended promise. `evidence_contract.environment_matrix` is the proof collected.

Each material row records operating system, architecture, browser, engine, form factor, input, accessibility and motion settings, capture provider, exact build, status, evidence, and limitations. Status is `planned`, `partial`, `passed`, `failed`, `unsupported`, or `not_required`.

One row never passes another. A macOS Safari result does not prove Windows Chromium, Linux Firefox, touch, reduced motion, or another accessibility stack.

## Portable core

- use project-relative paths and language-native path APIs;
- do not hard-code home directories, drive letters, separators, temporary folders, app bundles, or browser binaries;
- do not require one shell, harness, browser, or capture provider;
- expose package scripts or language entry points and let the host choose the safe command form;
- use UTF-8 and tolerate normal line-ending and case-sensitivity differences;
- keep permissions, symlinks, executable bits, firewalls, ports, and browser settings environment-specific;
- never store administrator credentials or bypass a local permission prompt.

## Evidence boundary

Record whether execution was native, visible, headless, remote, emulated, containerised, or virtualised. Structural checks and path simulations are not real platform, browser, touch, screen-reader, screenshot, or recording receipts.

When an environment is unavailable, keep it `planned` and prepare a bounded manual, CI, remote-browser, virtual-machine, or collaborator test. Narrow the support promise or keep release blocked when that row is material.

A broad support claim is verified only when every material row is `passed`, `not_required`, or explicitly accepted by the owner as a bounded exclusion. Use `assets/platform-evidence-matrix.csv`; never generalise one environment’s evidence to another.