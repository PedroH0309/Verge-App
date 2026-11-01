# Verge downloads

Verge is distributed as **separate packages per platform**. Do not attempt to install an APK on a TV running webOS/Tizen or on an iPhone.

## Android

### Preview APK — testing only

1. Open [Verge Android APK workflow](https://github.com/PedroH0309/Verge-App/actions/workflows/verge-android.yml).
2. Open the latest **successful** run (or use **Run workflow** if Actions are enabled).
3. Under **Artifacts**, download the archive named **Verge-Android-debug-...**.
4. Extract the archive and check its \`SHA256SUMS.txt\` before installing \`Verge-Android-TEST-debug.apk\`.
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
| Samsung Tizen | \`.wgt\` | Source snapshot in \`platforms/tv/\`; Verge build **not available yet** |
| LG webOS | \`.ipk\` | Source snapshot in \`platforms/tv/\`; Verge build **not available yet** |
| Android TV / Google TV | Android APK, TV-optimized | No certified Verge TV layout or remote-control testing yet |

The original Nuvio TV Smart source and its build steps are documented at https://github.com/NuvioMedia/NuvioTVSmart . Existing Nuvio releases are **not Verge packages**.

## Desktop

| Operating system | Typical package | Current Verge status |
| --- | --- | --- |
| Windows | \`.msi\` | Desktop source snapshot imported; Verge build not yet compiled |
| macOS | \`.dmg\` | Desktop source snapshot imported; Verge build not yet compiled |
| Linux | \`.deb\`, \`.rpm\`, \`.AppImage\` | Desktop source snapshot imported; Verge build not yet compiled |

Original desktop project: https://github.com/NuvioMedia/NuvioDesktop .

## iOS

Android APKs cannot be installed on iPhone or iPad. The original Nuvio Mobile iOS source is included in \`iosApp/\` for development, but a Verge IPA has not been signed, approved or distributed.

## License

All three source snapshots are derivatives of projects licensed under GNU GPLv3. A distribution must provide the corresponding source code and preserve upstream credit notices. Third-party metadata, API and streaming-content permissions are not granted by the GPL.
