<div align="center">

<img src="composeApp/src/commonMain/composeResources/drawable/app_logo_wordmark.png" alt="Verge" width="320" />

# VERGE

**An open-source media experience built for your screens.**

An independent fork of [Nuvio Mobile](https://github.com/NuvioMedia/NuvioMobile), with original Verge branding and a standalone Android package identity.

[**Android APK downloads**](https://github.com/PedroH0309/Verge-App/releases/tag/android-preview-3) · [**Windows PC installer**](https://github.com/PedroH0309/Verge-App/releases/tag/windows-preview-7) · [**TV builds**](DOWNLOADS.md#televisions) · [**Desktop builds**](DOWNLOADS.md#desktop) · [**Source credits**](docs/UPSTREAM.md)

</div>

---

## About Verge

Verge is an experimental media application based on the GNU GPLv3-licensed Nuvio projects. The Android application retains the upstream Kotlin Multiplatform / Compose Multiplatform player, catalog and library implementation, with distinct Verge application identifiers and brand artwork.

Verge is **not affiliated with or endorsed by NuvioMedia**. This project does not provide films, television channels, copyrighted streams or unauthorized media sources. Connect only services and media you are entitled to access.

> **Project status:** Early preview. Android and Windows packages have passed automated builds, but installation and playback on real devices remain unverified. These previews are not signed, tested production releases.

## Downloads

Different platforms have different packages; an Android APK does not install on iOS, Windows, LG webOS or Samsung Tizen.

| Platform | Package | Status | Download page |
| --- | --- | --- | --- |
| Android phones / tablets | APK | Experimental debug APK built; real-device testing needed | [Download Android APK](https://github.com/PedroH0309/Verge-App/releases/download/android-preview-3/Verge-Android-TEST-debug.apk) |
| Android release distribution | Signed APK | Requires privately configured signing key | [Releases](https://github.com/PedroH0309/Verge-App/releases) |
| Samsung TV (Tizen) | WGT | Upstream source imported; Verge port not built | [TV status](DOWNLOADS.md#televisions) |
| LG TV (webOS) | IPK | Upstream source imported; Verge port not built | [TV status](DOWNLOADS.md#televisions) |
| Windows 10/11 x64 | MSI | Preview installer compiled; real-device testing needed | [Download Windows MSI](https://github.com/PedroH0309/Verge-App/releases/download/windows-preview-7/Verge-Windows-x64-0.1.33-alpha.msi) |
| macOS | DMG | Desktop code imported; packaging and signing not verified | [macOS status](DOWNLOADS.md#linux-and-macos) |
| Linux | AppImage / DEB / RPM | Desktop code imported; package build pending | [Linux status](DOWNLOADS.md#linux-and-macos) |
| iPhone / iPad | iOS app | Not distributed as an Android APK | [Platform status](DOWNLOADS.md#ios) |

For installation steps, build instructions and exact artifact names, see **[DOWNLOADS.md](DOWNLOADS.md)**.

## Features inherited from Nuvio Mobile

- Cross-platform mobile UI using Kotlin and Compose Multiplatform.
- Media catalog, personal library and browsing features.
- Playback, subtitles, stream selection and media controls.
- Optional integrations with external metadata and tracking services.
- Optional user-configured addons and sources, subject to their own terms and access rights.

Some features rely on Nuvio-operated or third-party services, credentials, datasets and media plugins. **These are not owned by Verge**, and are not guaranteed to work with this derivative or to be licensed for commercial use.

## Project structure

This monorepo follows the general organization of the Nuvio projects:

| Directory | Purpose |
| --- | --- |
| `androidApp/` | Android application entry point and APK configuration |
| `composeApp/` | Shared Kotlin Multiplatform UI and application logic |
| `iosApp/` | Upstream iOS sources; not distributed by this release |
| `platforms/tv/` | Nuvio TV Smart source snapshot for future Verge TV porting |
| `platforms/desktop/` | Nuvio Desktop source snapshot for future Verge Desktop porting |
| `verge/scripts/` | Original rebranding and validation tooling |
| `.github/workflows/` | Source import, Android APK, and Windows MSI build workflows |
| `docs/` | Source provenance, licensing, and migration notes |

The TV source is preserved for future porting. The desktop source has a Windows preview packaging workflow that applies Verge branding during the build. The Windows MSI has passed automated packaging, while installation and playback on a real PC remain unverified.

## Build Android from source

Requirements: JDK 17, Android SDK, internet access for Gradle dependencies.

```bash
./gradlew :androidApp:assembleFullDebug \
  -Pnuvio.android.distribution=full \
  -Pnuvio.ios.distribution=appstore
```

The experimental debug APK is generated at:

```text
androidApp/build/outputs/apk/full/debug/androidApp-full-debug.apk
```

For a downloadable Android build without configuring Android Studio on your computer, go to **Actions → Verge Android APK → Run workflow**. The build and its result can be inspected in the workflow logs.

A signed production release requires a **private, persistent Android signing keystore**. Do not commit signing keys, passwords or `local.properties` to this repository.

## Open source license and credits

This repository combines source code derived from three Nuvio projects. Their sources are provided under **GNU GPLv3** (see [LICENSE](LICENSE)). Original copyright notices, third-party credits and applicable license notices must remain intact, including when selling or redistributing the APK.

Read [upstream provenance and attribution](docs/UPSTREAM.md) and review every relevant third-party license before commercial distribution. In particular, the source may reference datasets and APIs with **non-commercial** or independent terms.

Verge is a derivative software distribution, not a claim that upstream authorship or intellectual property has been transferred.

## Security and responsible distribution

- Do not ship bundled unauthorized streaming catalogs or expose someone else's account credentials.
- Do not treat arbitrary third-party addon sources as verified or safe.
- Make corresponding GPLv3 source code available to APK recipients.
- Verify downloaded APK checksums and test installs on real devices before promoting a build.
- No APK has been verified for general public release solely by committing source code.

## Acknowledgments

Original projects: [Nuvio Mobile](https://github.com/NuvioMedia/NuvioMobile) · [Nuvio TV Smart](https://github.com/NuvioMedia/NuvioTVSmart) · [Nuvio Desktop](https://github.com/NuvioMedia/NuvioDesktop).

All original authors retain their respective rights.
