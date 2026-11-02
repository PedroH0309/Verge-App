package com.nuvio.app.features.profiles

import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertFalse
import kotlin.test.assertNull
import kotlin.test.assertTrue

class VergeAvatarPresetsTest {
    @Test fun includesOfflineAvatarsWithUniqueKeysAndColors() {
        assertEquals(8, vergeAvatarPresets.size)
        assertEquals(8, vergeAvatarPresets.map { it.id }.toSet().size)
        assertEquals(8, vergeAvatarPresets.map { it.bgColor }.toSet().size)
        assertTrue(vergeAvatarPresets.all { it.storagePath.isBlank() && !it.memberOnly })
        assertTrue(vergeAvatarPresets.all { isVergeAvatarId(it.id) })
        assertFalse(isVergeAvatarId("a-provider-avatar"))
    }

    @Test fun selectedAvatarIsReconstructedFromSyncedColorWithoutServerAvatarId() {
        val sample = NuvioProfile(
            profileIndex = 2, name = "Test",
            avatarColorHex = "#304a85", avatarId = null, avatarUrl = null,
        )
        assertEquals("verge-nova", avatarForProfile(sample, vergeAvatarPresets)?.id)
        assertEquals("verge-nova", vergeAvatarFromColor(sample.avatarColorHex)?.id)
    }

    @Test fun remoteAvatarIdWinsOverOfflineMatchingColor() {
        val remote = AvatarCatalogItem(id = "server-avatar", displayName = "Remote", bgColor = "#304A85")
        val sample = NuvioProfile(profileIndex = 3, avatarId = remote.id, avatarColorHex = "#304A85")
        assertEquals(remote.id, avatarForProfile(sample, vergeAvatarPresets + remote)?.id)
    }

    @Test fun customAvatarUrlIsNotAccidentallyReplacedByOfflineArt() {
        val sample = NuvioProfile(
            avatarUrl = "https://example.org/profile.jpg",
            avatarColorHex = "#304A85",
        )
        assertNull(avatarForProfile(sample, vergeAvatarPresets))
    }

    @Test fun unrelatedColorRetainsExistingLetterAvatarFallback() {
        val sample = NuvioProfile(avatarColorHex = "#1E88E5")
        assertNull(avatarForProfile(sample, vergeAvatarPresets))
    }
}
