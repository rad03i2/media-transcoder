# Media Transcoder

A safe, local-first command-line toolkit for practical video and audio transcoding with FFmpeg. It provides repeatable presets, media inspection, batch conversion, dry runs, overwrite protection, and useful error reporting without uploading media anywhere.

> Author: **Radwan Abdulhadi Ahmed** · **رضوان عبدالهادي أحمد** · GitHub **@rad03i2**

## Why this project?
Raw FFmpeg is powerful but repetitive commands and accidental overwrites are easy mistakes. Media Transcoder adds a small, testable Python layer for common workflows while keeping FFmpeg visible and in control.

## Features
- Convert a single video/audio file with named presets.
- Batch-convert supported media while preserving relative directory structure.
- Inspect streams, codecs and container metadata via FFprobe JSON.
- `web`: H.264 + AAC + fast-start MP4-friendly settings.
- `small`: H.265 + AAC for smaller video output.
- `audio-mp3` and `audio-opus` extraction/transcoding presets.
- `copy`: remux compatible streams without re-encoding.
- Dry-run prints the exact FFmpeg command before doing work.
- Existing outputs are protected unless `--overwrite` is explicit.
- Input and output cannot be the same path.
- Failed conversions remove partial output created by the failed process.
- No cloud service, telemetry, account, token, or API key.

## Requirements
- Python 3.10+
- FFmpeg and FFprobe installed and available on `PATH`

Verify first:
```bash
ffmpeg -version
ffprobe -version
```

## Install
```bash
git clone https://github.com/rad03i2/media-transcoder.git
cd media-transcoder
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -e .
```

## Usage
Inspect media:
```bash
media-transcoder probe movie.mkv
```

Preview a conversion without writing anything:
```bash
media-transcoder convert movie.mkv movie.mp4 --preset web --dry-run
```

Convert:
```bash
media-transcoder convert movie.mkv movie.mp4 --preset web
```

Extract MP3 audio:
```bash
media-transcoder convert interview.mkv interview.mp3 --preset audio-mp3
```

Batch convert, including subdirectories:
```bash
media-transcoder batch ./incoming ./converted --preset web --ext .mp4 --recursive
```

Use `--overwrite` only when replacing an existing destination is intentional.

## Supported discovery inputs
MP4, MKV, MOV, AVI, WebM, M4V, MP3, WAV, FLAC, M4A, OGG and Opus. FFmpeg may support additional individual inputs; the batch scanner intentionally uses a conservative allow-list.

## Project structure
```text
src/media_transcoder/core.py   FFmpeg/FFprobe engine, presets and safety checks
src/media_transcoder/cli.py    CLI and batch workflow
src/media_transcoder/__init__.py
 tests/                         automated behavior tests
.github/workflows/ci.yml       cross-platform Python test matrix
```

## Testing
```bash
pip install -e . pytest
pytest -q
```
CI runs the test suite on Windows, Linux and macOS with Python 3.10, 3.12 and 3.13. Unit tests mock tool discovery where appropriate, so core command-building tests do not require FFmpeg.

## Privacy & security
All processing is local. Filenames are passed to `subprocess` as argument arrays rather than shell command strings. The program does not upload media or collect telemetry. Treat untrusted media as potentially hostile input and keep FFmpeg updated. See `SECURITY.md` for reporting guidance.

## Limitations
- FFmpeg/FFprobe are external requirements and are not bundled.
- Presets intentionally cover common workflows rather than every codec/filter option.
- A container extension does not guarantee codec/container compatibility; FFmpeg remains the authority and returns an error when a combination is invalid.
- The tool does not provide GPU-specific presets because availability differs substantially by machine.

## Contributing
See `CONTRIBUTING.md`. Focus contributions on tested, portable workflows rather than adding opaque FFmpeg flags.

## License
MIT License. See `LICENSE`.

## Author
**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: **@rad03i2**

---

# Media Transcoder — العربية

أداة سطر أوامر محلية وآمنة لتحويل الفيديو والصوت باستخدام FFmpeg. الهدف هو جعل العمليات اليومية واضحة وقابلة للتكرار مع حماية من الاستبدال غير المقصود، ومعاينة الأمر قبل التنفيذ، وتحويل دفعات من الملفات، وفحص معلومات الوسائط دون رفع أي ملف إلى الإنترنت.

## لماذا هذا المشروع؟
FFmpeg قوي جدًا، لكن أوامره الطويلة قد تتكرر ويصبح الخطأ في المسارات أو الاستبدال سهلًا. يضيف هذا المشروع طبقة Python صغيرة ومختبرة للعمليات الشائعة مع إبقاء FFmpeg نفسه محرك التنفيذ.

## الميزات
- تحويل ملف فيديو أو صوت واحد عبر إعدادات جاهزة واضحة.
- تحويل جماعي للمجلدات مع إمكانية البحث داخل المجلدات الفرعية والحفاظ على بنيتها.
- عرض معلومات الحاوية والمسارات والترميزات بصيغة JSON عبر FFprobe.
- إعداد `web` للفيديو H.264 والصوت AAC مع fast-start.
- إعداد `small` باستخدام H.265 لتقليل الحجم في الحالات المناسبة.
- إعدادات لاستخراج/تحويل الصوت إلى MP3 أو Opus.
- إعداد `copy` لإعادة التغليف دون إعادة ترميز عندما تكون الصيغ متوافقة.
- `--dry-run` لعرض أمر FFmpeg دون إنشاء ملفات.
- عدم استبدال الناتج الموجود إلا عند تمرير `--overwrite` صراحةً.
- منع استخدام نفس المسار كمدخل ومخرج.
- حذف الناتج الجزئي عند فشل FFmpeg.
- لا حسابات ولا تتبع ولا مفاتيح API ولا خدمات سحابية.

## المتطلبات والتثبيت
يتطلب Python 3.10 أو أحدث وFFmpeg/FFprobe ضمن `PATH`. بعد تثبيتهما:
```bash
git clone https://github.com/rad03i2/media-transcoder.git
cd media-transcoder
python -m venv .venv
pip install -e .
```

## أمثلة الاستخدام
```bash
media-transcoder probe movie.mkv
media-transcoder convert movie.mkv movie.mp4 --preset web --dry-run
media-transcoder convert movie.mkv movie.mp4 --preset web
media-transcoder convert interview.mkv interview.mp3 --preset audio-mp3
media-transcoder batch ./incoming ./converted --preset web --ext .mp4 --recursive
```

## الاختبارات
```bash
pip install -e . pytest
pytest -q
```
يوجد CI لاختبار المشروع على Windows وLinux وmacOS وإصدارات Python متعددة.

## الخصوصية والأمان
المعالجة محلية بالكامل. تُمرر المسارات إلى `subprocess` كمصفوفة معاملات وليس كسلسلة shell. لا يرفع البرنامج الوسائط ولا يجمع بيانات استخدام. يوصى بإبقاء FFmpeg محدثًا عند التعامل مع ملفات غير موثوقة.

## القيود
FFmpeg وFFprobe غير مدمجين داخل المشروع ويجب تثبيتهما منفصلين. الإعدادات الجاهزة تغطي الاستخدامات الشائعة ولا تحاول إخفاء كل خيارات FFmpeg. كما أن امتداد الملف وحده لا يضمن توافق الحاوية مع الترميز، وفي حالة عدم التوافق يعرض FFmpeg الخطأ الحقيقي.

## المساهمة والترخيص
راجع `CONTRIBUTING.md` للمساهمة و`SECURITY.md` للأمان. المشروع متاح بترخيص MIT الموجود في `LICENSE`.

## المؤلف
**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: **@rad03i2**
