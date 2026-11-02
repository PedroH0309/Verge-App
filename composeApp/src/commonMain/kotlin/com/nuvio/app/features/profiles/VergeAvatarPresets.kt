package com.nuvio.app.features.profiles

import androidx.compose.foundation.Image
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.layout.ContentScale
import nuvio.composeapp.generated.resources.Res
import nuvio.composeapp.generated.resources.verge_avatar_nova
import nuvio.composeapp.generated.resources.verge_avatar_pixel
import nuvio.composeapp.generated.resources.verge_avatar_ember
import nuvio.composeapp.generated.resources.verge_avatar_atlas
import nuvio.composeapp.generated.resources.verge_avatar_luna
import nuvio.composeapp.generated.resources.verge_avatar_orbit
import nuvio.composeapp.generated.resources.verge_avatar_mint
import nuvio.composeapp.generated.resources.verge_avatar_echo
import org.jetbrains.compose.resources.painterResource

/**
 * Original Verge portraits that always work without the Nuvio/Supabase avatar API.
 *
 * The profile backend may restrict avatar_id to its own catalog. To keep profile
 * synchronization compatible, a Verge preset is stored as a unique bg_color
 * value with avatar_id=null. The client reconstructs the illustration from it.
 */
internal val vergeAvatarPresets: List<AvatarCatalogItem> = listOf(
    AvatarCatalogItem("verge-nova", "Nova", category = "verge", sortOrder = -800, bgColor = "#304A85"),
    AvatarCatalogItem("verge-pixel", "Pixel", category = "verge", sortOrder = -799, bgColor = "#6641A7"),
    AvatarCatalogItem("verge-ember", "Ember", category = "verge", sortOrder = -798, bgColor = "#86465F"),
    AvatarCatalogItem("verge-atlas", "Atlas", category = "verge", sortOrder = -797, bgColor = "#246D73"),
    AvatarCatalogItem("verge-luna", "Luna", category = "verge", sortOrder = -796, bgColor = "#62558D"),
    AvatarCatalogItem("verge-orbit", "Orbit", category = "verge", sortOrder = -795, bgColor = "#825B31"),
    AvatarCatalogItem("verge-mint", "Mint", category = "verge", sortOrder = -794, bgColor = "#2E7158"),
    AvatarCatalogItem("verge-echo", "Echo", category = "verge", sortOrder = -793, bgColor = "#395D79"),
)

internal fun isVergeAvatarId(id: String?): Boolean =
    id != null && vergeAvatarPresets.any { it.id == id }

internal fun vergeAvatarFromColor(color: String?): AvatarCatalogItem? =
    color?.let { candidate ->
        vergeAvatarPresets.firstOrNull { it.bgColor.equals(candidate, ignoreCase = true) }
    }

/** Prioritize explicit user URLs and native provider avatars. */
internal fun avatarForProfile(profile: NuvioProfile, catalog: List<AvatarCatalogItem>): AvatarCatalogItem? =
    profile.avatarId?.let { id -> catalog.firstOrNull { it.id == id } }
        ?: if (profile.avatarId == null && normalizedAvatarUrl(profile.avatarUrl) == null)
            vergeAvatarFromColor(profile.avatarColorHex)
        else null

@Composable
internal fun VergeAvatarPortrait(
    id: String,
    modifier: Modifier = Modifier,
    contentDescription: String? = null,
) {
    val resource = when (id) {
        "verge-pixel" -> Res.drawable.verge_avatar_pixel
        "verge-ember" -> Res.drawable.verge_avatar_ember
        "verge-atlas" -> Res.drawable.verge_avatar_atlas
        "verge-luna" -> Res.drawable.verge_avatar_luna
        "verge-orbit" -> Res.drawable.verge_avatar_orbit
        "verge-mint" -> Res.drawable.verge_avatar_mint
        "verge-echo" -> Res.drawable.verge_avatar_echo
        else -> Res.drawable.verge_avatar_nova
    }
    Image(
        painter = painterResource(resource),
        contentDescription = contentDescription,
        modifier = modifier,
        contentScale = ContentScale.Crop,
    )
}
