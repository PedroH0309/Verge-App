# Verge downloads

Verge is distributed as **separate packages per platform**. Do not attempt to install an APK on a TV running webOS/Tizen or on an iPhone.

## Android

### Preview APK — testing only

1. Download the publicly available [Verge Android preview APK](https://github.com/PedroH0309/Verge-App/releases/download/android-preview-3/Verge-Android-TEST-debug.apk).
2. For build details, visit the [successful Android workflow](https://github.com/PedroH0309/Verge-App/actions/runs/41357217932).
3. If you prefer the CI artifact, download `Verge-Android-debug-3` from the workflow's **Artifacts** section.
4. Check the APK against [SHA256SUMS.txt](https://github.com/PedroH0309/Verge-App/releases/download/android-preview-3/SHA256SUMS.txt) before installation.
5. Install the APK on a supported Android phone or tablet. Android may ask for permission to install apps from this source.

Debug builds are for testing and may use an ephemeral signing key. Reinstalling or upgrading across runs may require uninstalling the older build, which can erase app data.

### Signed release APK

After a successful Android device test, configure a persistent, private keystore in GitHub Actions secrets (see [release signing](docs/RELEASE_SIGNING.md)). Only signed and tested release packages should be shared as stable download links.

- [Verge Android releases](https://github.com/PedroH0309/Verge-App/releases)
- [Verge Android build workflow](https://github.com/PedroH0309/Verge-App/actions/workflows/verge-android.yml)

**No signed production APK is claimed to exist until a successful release build is published.**

## Televisions

| TV platform | Required file | Current Verge status |
| --- | --- | --- |
| Samsung Tizen | `.wgt` | Source snapshot in `platforms/tv/`; Verge build **not available yet** |
| LG webOS | `.ipk` | Source snapshot in `platforms/tv/`; Verge build **not available yet** |
| Android TV / Google TV | Android APK, TV-optimized | No certified Verge TV layout or remote-control testing yet |

The original Nuvio TV Smart source and its build steps are documented at https://github.com/NuvioMedia/NuvioTVSmart . Existing Nuvio releases are **not Verge packages**.

## Desktop (PC)

### Windows 10/11 x64 — MSI installer preview

The Windows desktop build uses the original Nuvio Desktop source with a separate **Verge** installer name and upgrade identity. It includes the required Windows media-player runtime in the build, retrieved from a pinned upstream Git LFS revision.

**[Download Windows x64 preview installer (.msi)](https://github.com/PedroH0309/Verge-App/releases/download/windows-preview-7/Verge-Windows-x64-0.1.33-alpha.msi)**

**[Windows MSI build history](https://github.com/PedroH0309/Verge-App/actions/workflows/verge-desktop.yml)**

1. Open the [Windows preview release](https://github.com/PedroH0309/Verge-App/releases/tag/windows-preview-7) and download the MSI directly.
2. Alternatively, download the archive named `Verge-Windows-x64-MSI-7` from the [successful workflow run](https://github.com/PedroH0309/Verge-App/actions/runs/41358335252).
3. Extract the artifact ZIP to obtain `Verge-Windows-x64-*.msi` and `SHA256SUMS.txt`.
4. Check the installer hash, then run the MSI on your Windows PC.
5. Treat this as an **untested preview** until a real Windows installation and playback test succeeds. The installer is not code-signed with a commercial Windows certificate, so Windows SmartScreen may warn.

If the workflow is red or no artifact is listed, **no verified Windows installer is available yet**. Do not use a renamed upstream Nuvio MSI as a Verge release.

### Linux and macOS

| Operating system | Target package | Status |
| --- | --- | --- |
| Linux | `.deb`, `.rpm`, or `.AppImage` | Imported upstream source; Verge build and native runtime verification pending |
| macOS | `.dmg` | Imported upstream source; Verge signing, runtime and notarization pending |

Windows MSI generation is intentionally separated from Android APK builds and from the future Linux/macOS packages.

Original desktop source: https://github.com/NuvioMedia/NuvioDesktop . The GPLv3 applies to this derivative, and third-party data and runtime licenses must be respected.

## iOS

Android APKs cannot be installed on iPhone or iPad. The original Nuvio Mobile iOS source is included in `iosApp/` for development, but a Verge IPA has not been signed, approved or distributed.

## License

All three source snapshots are derivatives of projects licensed under GNU GPLv3. A distribution must provide the corresponding source code and preserve upstream credit notices. Third-party metadata, API and streaming-content permissions are not granted by the GPL.
