# Upstream provenance and legal notices

Verge is an **independent derivative** of the following projects. These source bases are provided under the GNU General Public License, version 3 (GPL-3.0).

| Component | Original source | Imported revision | Main directory |
| --- | --- | --- | --- |
| Mobile app | [Nuvio Mobile](https://github.com/NuvioMedia/NuvioMobile) | `46febb568348aa5e135bff0d4d5c914933aff5a0` on `cmp-rewrite` | Repository root |
| Television | [Nuvio TV Smart](https://github.com/NuvioMedia/NuvioTVSmart) | `c96671616acf35600675f732b378d0e428439b09` on `main` | `platforms/tv` |
| Desktop | [Nuvio Desktop](https://github.com/NuvioMedia/NuvioDesktop) | `3e876f699e59e38b66ccc738331fa8071cbf29cc` on `Dev` | `platforms/desktop` |

The revisions above identify the intended pinned imports. After bootstrap, check `docs/SOURCE_REVISIONS.txt` and the GitHub Actions logs to verify that the source snapshots were actually copied. This document alone does not prove that the import ran.

## Copyright and permitted use

- Original authors retain their copyright. Changing UI artwork, application identifiers or branding does **not** transfer ownership of the upstream code.
- When distributing this fork, preserve copyright notices and GPLv3 notices, provide the corresponding source, and meet the GPL's distribution requirements.
- Do not remove third-party license attributions from product settings or bundled code.
- The Android branding transformation keeps internal Kotlin namespace names, since renaming them throughout the codebase would be a separate migration.
- Verge does not claim ownership of `nuvio.tv` or Nuvio's API services.
- Assets and trademarks belonging to the original projects must not be presented as official Verge branding in distributed builds.

## Commercial distribution considerations

GPLv3 permits selling copies of software, but separate **third-party content/data licenses** must be considered. This codebase may refer to IMDb noncommercial datasets, TMDB, user-configured addons and proprietary APIs. Their terms are not overridden by the source-code license.

No movies, series, sports streams, or commercial broadcasts are licensed or supplied through this repository.

## Build / snapshot limitations

The mobile project has an upstream `MPVKit` Git submodule for iOS. The bootstrap imports the mobile code without copying a nested Git object database or treating the iOS submodule as a release-ready Verge component. The Android build does not require the iOS distribution to be published.

TV and desktop source trees are retained for future independent porting. They are not automatically rebranded, certified, or production-ready.

## Changes introduced by Verge

- English-first project documentation and separated per-platform downloads.
- Original Verge Android icons, splash art and wordmark.
- Android package identifiers `com.verge.media` and `com.verge.media.debug`.
- Android-facing deep-link scheme `verge://`; Nuvio domain verification is removed from the Android manifest.
- User-facing brand string changes where legal/service attribution is not involved.
- Automated Android APK build workflow and source-import provenance.
