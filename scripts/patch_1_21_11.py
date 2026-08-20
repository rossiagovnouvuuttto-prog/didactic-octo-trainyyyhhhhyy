from pathlib import Path
import json

ROOT = Path("ABOBUS123-1.21.11-source")
MIXIN_DIR = ROOT / "src/main/java/platform/inject/mixin"
MIXIN_JSON = ROOT / "src/main/resources/delta.mixins.json"


def write(path: Path, text: str):
    path.write_text(text, encoding="utf-8")
    print(f"patched: {path}")


def remove_mixin(name: str):
    path = MIXIN_DIR / f"{name}.java"
    if path.exists():
        path.unlink()
        print(f"removed obsolete mixin source: {path}")

    data = json.loads(MIXIN_JSON.read_text(encoding="utf-8"))
    key = "client"
    entry = f"mixin.{name}"
    if entry in data.get(key, []):
        data[key].remove(entry)
        MIXIN_JSON.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        print(f"removed {entry} from delta.mixins.json")


# These mixins were tied to removed Misc/Player functionality or rendering APIs
# that no longer exist in 1.21.11. They are intentionally disabled rather than
# left as broken 1.21.4 bytecode hooks.
for obsolete in ("SkinTexturesMixin", "ScreenMixin", "RenderSystemMixin", "BackgroundRendererMixin"):
    remove_mixin(obsolete)

# 1.21.11 WorldRenderer no longer passes the old Fog object to renderWeather.
# Keep the WEATHER removal hook and FreeCamera spectator/culling behavior using
# the current WorldRenderer methods.
write(MIXIN_DIR / "WorldRendererMixin.java", r'''package platform.inject.mixin;

import aethereal.core.Delta;
import aethereal.core.EventManager;
import aethereal.core.Interface;
import aethereal.event.RemovalsEvent;
import com.mojang.blaze3d.buffers.GpuBufferSlice;
import net.minecraft.client.render.Camera;
import net.minecraft.client.render.FrameGraphBuilder;
import net.minecraft.client.render.Frustum;
import net.minecraft.client.render.WorldRenderer;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.ModifyVariable;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

@Mixin(WorldRenderer.class)
public class WorldRendererMixin implements Interface {
    @Inject(method = "renderWeather", at = @At("HEAD"), cancellable = true)
    private void abobus$renderWeather(FrameGraphBuilder frameGraphBuilder, GpuBufferSlice fogBuffer, CallbackInfo ci) {
        RemovalsEvent event = new RemovalsEvent(RemovalsEvent.type.WEATHER);
        EventManager.a(event);
        if (event.a()) {
            ci.cancel();
        }
    }

    @ModifyVariable(method = "updateCamera", at = @At("HEAD"), argsOnly = true, index = 3)
    private boolean abobus$updateCamera(boolean spectator) {
        return Delta.getInstance().getModuleProcessor().t().h().m() || spectator;
    }
}
''')

# DownloadingTerrainScreen was replaced in modern 1.21.x by LevelLoadingScreen.
mc_mixin = MIXIN_DIR / "MinecraftClientMixin.java"
text = mc_mixin.read_text(encoding="utf-8")
text = text.replace("import net.minecraft.client.gui.screen.DownloadingTerrainScreen;", "import net.minecraft.client.gui.screen.LevelLoadingScreen;")
text = text.replace("screen instanceof DownloadingTerrainScreen", "screen instanceof LevelLoadingScreen")
write(mc_mixin, text)

print("ABOBUS123 1.21.11 compatibility patch pass 1 complete")
