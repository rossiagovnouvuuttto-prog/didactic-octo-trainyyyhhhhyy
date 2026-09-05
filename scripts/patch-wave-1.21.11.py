from pathlib import Path
import json
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "work")
SRC = ROOT / "src/client/java"

replacements = {
    "import net.minecraft.client.render.VertexFormat;": "import com.mojang.blaze3d.vertex.VertexFormat;",
    "import net.minecraft.client.render.VertexFormat.DrawMode;": "import com.mojang.blaze3d.vertex.VertexFormat.DrawMode;",
    "net.minecraft.client.render.VertexFormat.DrawMode": "com.mojang.blaze3d.vertex.VertexFormat.DrawMode",
    "import com.mojang.blaze3d.platform.GlStateManager;": "import com.mojang.blaze3d.opengl.GlStateManager;",
    "com.mojang.blaze3d.platform.GlStateManager": "com.mojang.blaze3d.opengl.GlStateManager",
    "import net.minecraft.item.ModelTransformationMode;": "import net.minecraft.item.ItemDisplayContext;",
    "ModelTransformationMode": "ItemDisplayContext",
}

changed = 0
for path in SRC.rglob("*.java"):
    text = path.read_text(encoding="utf-8", errors="ignore")
    new = text
    for old, repl in replacements.items():
        new = new.replace(old, repl)
    if new != text:
        path.write_text(new, encoding="utf-8")
        changed += 1

# 1.21.11 replaced the old BackgroundRenderer/Fog hook with FogRenderer.
# Disable this single obsolete mixin for the first compatibility pass; the
# visual Removals module itself remains present.
old_mixin = SRC / "moscow/rockstar/mixin/minecraft/client/gui/overlay/BackgroundRendererMixin.java"
if old_mixin.exists():
    old_mixin.unlink()

mixin_json = ROOT / "src/main/resources/rockstar.mixins.json"
if mixin_json.exists():
    data = json.loads(mixin_json.read_text(encoding="utf-8"))
    for key in ("mixins", "client"):
        vals = data.get(key)
        if isinstance(vals, list):
            data[key] = [v for v in vals if "BackgroundRendererMixin" not in v]
    mixin_json.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

# Show all compile errors instead of javac's default first 100.
build = ROOT / "build.gradle"
if build.exists():
    text = build.read_text(encoding="utf-8")
    marker = "// CHATGPT_12111_MAXERRS"
    if marker not in text:
        text += "\n" + marker + "\ntasks.withType(JavaCompile).configureEach { options.compilerArgs += ['-Xmaxerrs', '5000'] }\n"
        build.write_text(text, encoding="utf-8")

print(f"1.21.11 compatibility pass 1: patched {changed} Java files")
