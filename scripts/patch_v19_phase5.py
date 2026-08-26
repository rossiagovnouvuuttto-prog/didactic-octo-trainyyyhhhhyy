#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()

def edit(rel, fn):
    p = root / rel
    s = p.read_text(encoding='utf-8')
    n = fn(s)
    if n == s:
        print(f'phase5: no change for {rel}')
    else:
        p.write_text(n, encoding='utf-8')
        print(f'phase5: fixed {rel}')

edit('src/main/java/com/reallyvisuals/module/ChinaHat.java',
     lambda s: s.replace('MathHelper.lerpAngle(', 'MathHelper.lerpAngleDegrees('))

edit('src/main/java/com/reallyvisuals/module/TargetHud.java',
     lambda s: s.replace(
         'livingRenderer.getTexture(livingRenderer.getAndUpdateRenderState(entity, 0.0F))',
         'livingRenderer.getTexture((net.minecraft.client.render.entity.state.LivingEntityRenderState) livingRenderer.getAndUpdateRenderState(entity, 0.0F))'
     ))

def fix_hand(s):
    imp = 'import net.minecraft.client.MinecraftClient;\n'
    if imp not in s:
        idx = s.find('\n', s.find('package ')) + 1
        s = s[:idx] + '\n' + imp + s[idx:]
    return s

edit('src/main/java/com/reallyvisuals/gui/CustomHandEditorScreen.java', fix_hand)
print('phase5 applied')
