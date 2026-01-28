import PIL.Image

# --- الحل السحري للمشكلة ---
# بنقول للبايثون: لو ملقتش ANTIALIAS استخدم البديل الجديد (LANCZOS)
if not hasattr(PIL.Image, "ANTIALIAS"):
    PIL.Image.ANTIALIAS = PIL.Image.LANCZOS
# ---------------------------

from moviepy.editor import VideoFileClip

# 1. اسم ملف الفيديو (تأكد إنك غيرت اسم الفيديو لـ game.mp4 زي ما اتفقنا)
video_path = "game.mp4"

try:
    print("🎬 Loading video...")
    clip = VideoFileClip(video_path)

    # 2. قص اللقطة (من الثانية 3 إلى 9)
    # اللقطة دي فيها تغيير ألوان وحركة حلوة
    gif_clip = clip.subclip(t_start=3, t_end=9)

    # 3. تغيير الحجم (600px عرض مثالي للـ Readme)
    gif_clip = gif_clip.resize(width=600)

    # 4. الحفظ
    print("✨ Converting to GIF (This might take a few seconds)...")
    gif_clip.write_gif("gameplay.gif", fps=15)

    print("✅ Done! 'gameplay.gif' is ready.")

except Exception as e:
    print(f"❌ Error: {e}")
