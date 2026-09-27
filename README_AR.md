<div dir="rtl">

# Media Transcoder — الدليل العربي

**Media Transcoder** أداة سطر أوامر مكتوبة بلغة Python لتنفيذ عمليات تحويل الفيديو والصوت محليًا بواسطة FFmpeg وFFprobe. تركّز على وضوح الأوامر، الإعدادات الجاهزة، فحص المسارات، المعاينة قبل التنفيذ، التحويل الجماعي، وحماية الملفات الناتجة من الاستبدال غير المقصود.

## ماذا يفعل المشروع؟

- تحويل ملف فيديو أو صوت واحد باستخدام إعداد جاهز.
- فحص معلومات الحاوية والمسارات والترميزات عبر FFprobe وإخراج JSON.
- تحويل ملفات مدعومة داخل مجلد كامل.
- الحفاظ على البنية النسبية للمجلدات أثناء التحويل الجماعي.
- البحث داخل المجلدات الفرعية عند استخدام الخيار المخصص لذلك.
- عرض أمر FFmpeg الفعلي عند استخدام `--dry-run` من دون إنشاء ناتج.
- حماية الملف الناتج الموجود مسبقًا ما لم يُستخدم `--overwrite` صراحةً.
- منع استخدام المسار نفسه كمدخل ومخرج.
- إنشاء ملف مؤقت بجوار الوجهة أثناء التحويل الحقيقي.
- حذف الملف المؤقت إذا فشل التحويل.

## المتطلبات

- Python 3.10 أو أحدث.
- FFmpeg.
- FFprobe.
- يجب أن يكون `ffmpeg` و`ffprobe` متاحين ضمن `PATH`.

```bash
ffmpeg -version
ffprobe -version
```

## التثبيت

```bash
git clone https://github.com/rad03i2/media-transcoder.git
cd media-transcoder
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
python -m pip install -e .
```

بعد التثبيت يصبح الأمر التالي متاحًا:

```text
media-transcoder
```

## الأوامر

### فحص ملف وسائط

```bash
media-transcoder probe movie.mkv
```

يعرض معلومات FFprobe عن التنسيق والمسارات بصيغة JSON.

### تحويل ملف

```bash
media-transcoder convert movie.mkv movie.mp4 --preset web
```

للمعاينة قبل التنفيذ:

```bash
media-transcoder convert movie.mkv movie.mp4 --preset web --dry-run
```

للسماح باستبدال ملف موجود بشكل مقصود:

```bash
media-transcoder convert movie.mkv movie.mp4 --preset web --overwrite
```

### التحويل الجماعي

```bash
media-transcoder batch ./incoming ./converted --preset web --ext .mp4 --recursive
```

يعيد أمر التحويل الجماعي رمز خروج غير صفري إذا فشل تحويل ملف واحد أو أكثر من الملفات المكتشفة.

## الإعدادات الجاهزة الموجودة حاليًا

| الإعداد | الوظيفة الحالية |
|---|---|
| `web` | فيديو H.264 وصوت AAC، بقيمة CRF 23 وإعداد medium مع `+faststart` |
| `small` | فيديو H.265 وصوت AAC، بقيمة CRF 28 وإعداد medium |
| `audio-mp3` | تحويل/استخراج الصوت إلى MP3 باستخدام `libmp3lame` |
| `audio-opus` | تحويل/استخراج الصوت إلى Opus باستخدام `libopus` بمعدل 128 kb/s |
| `copy` | نسخ المسارات وإعادة التغليف دون إعادة ترميز عندما تكون الحاوية متوافقة |

## صيغ البحث الجماعي

```text
.mp4 .mkv .mov .avi .webm .m4v
.mp3 .wav .flac .m4a .ogg .opus
```

هذه القائمة تخص اكتشاف الملفات في أمر `batch`. قد يقبل FFmpeg صيغًا إضافية عند تمرير ملف بشكل مباشر إلى `convert`.

## الخصوصية والأمان

المشروع نفسه لا يرفع الملفات إلى الإنترنت ولا يستخدم تتبعًا أو حسابات أو مفاتيح API. يتم تشغيل FFmpeg وFFprobe المثبتين محليًا، وتُمرر المعاملات إلى `subprocess` على شكل مصفوفة وليس عبر `shell=True`.

عند تنفيذ تحويل حقيقي يُكتب الناتج أولًا إلى ملف مؤقت فريد بجوار الوجهة، ثم تُستبدل الوجهة بعد نجاح FFmpeg والتأكد من وجود ملف ناتج غير فارغ. وفي مسار الفشل يُحذف الملف المؤقت.

عند التعامل مع ملفات وسائط غير موثوقة، حافظ على تحديث FFmpeg ونظام التشغيل. راجع [SECURITY.md](SECURITY.md).

## الاختبارات

```bash
python -m pip install -e . pytest
pytest -q
```

يشغّل CI الاختبارات على Ubuntu وWindows وmacOS مع Python 3.10 و3.12 و3.13.

## المعمارية

راجع [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) لفهم توزيع المسؤوليات ومسار التنفيذ.

## المساهمة

راجع [CONTRIBUTING.md](CONTRIBUTING.md). يفضّل أن تكون التغييرات قابلة للاختبار، ومتوافقة عبر الأنظمة، وواضحة في تأثيرها على أوامر FFmpeg.

## الترخيص

المشروع متاح بترخيص MIT. راجع [LICENSE](LICENSE).

## المطور

**رضوان عبدالهادي**  
**Radwan Abd alhady Ahmed**  
GitHub: [@rad03i2](https://github.com/rad03i2)

</div>
