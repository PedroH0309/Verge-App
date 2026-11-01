# Android release signing

The Verge Android build has two modes:

| Build type | Package ID | Use |
| --- | --- | --- |
| Debug | \`com.verge.media.debug\` | Unstable testing package; may require reinstalling on different runner builds |
| Release | \`com.verge.media\` | Signed APK for distribution and upgrade continuity |

## Requirements

Create a unique Android signing keystore in a trusted, private environment. **Do not upload the keystore or passwords to this repository, an issue, a pull request or a chat.** Back up the keystore securely; losing the signing key prevents seamless updates.

Add these GitHub repository Actions secrets:

- \`VERGE_KEYSTORE_BASE64\`: Base64-encoded binary keystore.
- \`VERGE_KEYSTORE_PASSWORD\`: keystore password.
- \`VERGE_KEY_ALIAS\`: alias of your key entry.
- \`VERGE_KEY_PASSWORD\`: key password.

After configuring all four values, run [Verge Android APK](https://github.com/PedroH0309/Verge-App/actions/workflows/verge-android.yml) with \`build_type=release\`. The workflow will fail if a required secret is missing.

Version codes are derived from GitHub Actions run numbers. Keep the same release signing key for every version you distribute.

## Distribution checklist

1. Ensure the build completed successfully and produced signed APKs.
2. Install the APK on a clean Android device and confirm the app opens.
3. Check the license/source-code obligations and licenses of external datasets/services.
4. Verify SHA-256 sums and publish the exact corresponding source commit.
5. Publish compatible, signed packages on [GitHub Releases](https://github.com/PedroH0309/Verge-App/releases), not raw build logs.

A debug APK is not a stable commercial product.
