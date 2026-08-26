#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()

(root / 'src/main/java/com/reallyvisuals/mixin/InGameOverlayRendererMixin.java').write_text(r'''package com.reallyvisuals.mixin;

import com.reallyvisuals.module.ModuleManager;
import com.reallyvisuals.module.NoFluid;
import com.reallyvisuals.module.RenderTweaks;
import net.minecraft.client.MinecraftClient;
import net.minecraft.client.gui.hud.InGameOverlayRenderer;
import net.minecraft.client.render.VertexConsumerProvider;
import net.minecraft.client.texture.Sprite;
import net.minecraft.client.util.math.MatrixStack;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

@Mixin(InGameOverlayRenderer.class)
public class InGameOverlayRendererMixin {
   @Inject(
      method = "renderFireOverlay(Lnet/minecraft/client/util/math/MatrixStack;Lnet/minecraft/client/render/VertexConsumerProvider;Lnet/minecraft/client/texture/Sprite;)V",
      at = @At("HEAD"), cancellable = true, require = 0
   )
   private static void abobus123$onRenderFireOverlay(MatrixStack matrices, VertexConsumerProvider vertexConsumers, Sprite sprite, CallbackInfo ci) {
      RenderTweaks tweaks = (RenderTweaks)ModuleManager.getInstance().getModule("Render Tweaks");
      if (tweaks != null && tweaks.isEnabled() && tweaks.tweaks.isSelected("Оверлей огня")) {
         ci.cancel();
      }
   }

   @Inject(
      method = "renderUnderwaterOverlay(Lnet/minecraft/client/MinecraftClient;Lnet/minecraft/client/util/math/MatrixStack;Lnet/minecraft/client/render/VertexConsumerProvider;)V",
      at = @At("HEAD"), cancellable = true, require = 0
   )
   private static void abobus123$onRenderUnderwaterOverlay(MinecraftClient client, MatrixStack matrices, VertexConsumerProvider vertexConsumers, CallbackInfo ci) {
      NoFluid noFluid = (NoFluid)ModuleManager.getInstance().getModule("No Fluid");
      if (noFluid != null && noFluid.isEnabled()) {
         ci.cancel();
      }
   }
}
''', encoding='utf-8')

(root / 'src/main/java/com/reallyvisuals/mixin/PlayerPositionDebugHudEntryMixin.java').write_text(r'''package com.reallyvisuals.mixin;

import com.reallyvisuals.module.ModuleManager;
import com.reallyvisuals.module.StreamerMode;
import net.minecraft.client.gui.hud.debug.DebugHudLines;
import net.minecraft.client.gui.hud.debug.PlayerPositionDebugHudEntry;
import net.minecraft.world.World;
import net.minecraft.world.chunk.WorldChunk;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

@Mixin(PlayerPositionDebugHudEntry.class)
public abstract class PlayerPositionDebugHudEntryMixin {
   @Inject(
      method = "render(Lnet/minecraft/client/gui/hud/debug/DebugHudLines;Lnet/minecraft/world/World;Lnet/minecraft/world/chunk/WorldChunk;Lnet/minecraft/world/chunk/WorldChunk;)V",
      at = @At("HEAD"), cancellable = true, require = 0
   )
   private void abobus123$hideCoordinates(DebugHudLines lines, World world, WorldChunk chunk, WorldChunk chunk2, CallbackInfo ci) {
      StreamerMode mode = (StreamerMode)ModuleManager.getInstance().getModule("Streamer Mode");
      if (mode != null && mode.isEnabled() && mode.hideCoords.value) {
         ci.cancel();
      }
   }
}
''', encoding='utf-8')

mixins = root / 'src/main/resources/reallyvisuals.mixins.json'
s = mixins.read_text(encoding='utf-8')
s = s.replace('    "DebugHudMixin",\n', '    "PlayerPositionDebugHudEntryMixin",\n')
mixins.write_text(s, encoding='utf-8')
print('phase7 applied: InGameOverlayRenderer + StreamerMode debug coordinates')
