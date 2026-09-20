# Contributing / المساهمة

Thank you for improving Media Transcoder. Keep changes focused, portable and testable.

1. Fork and create a focused branch.
2. Use Python 3.10+ and install with `pip install -e . pytest`.
3. Add or update tests for behavior changes.
4. Run `pytest -q` before opening a pull request.
5. Keep FFmpeg commands as argument lists; do not introduce `shell=True`.
6. Document user-visible behavior in both English and Arabic when practical.
7. Never commit media containing private information, secrets, credentials or copyrighted fixtures without permission.

Bug reports should include OS, Python version, FFmpeg version, command used, and sanitized error output.

---

نرحب بالمساهمات التي تحافظ على بساطة المشروع وقابليته للاختبار والعمل عبر الأنظمة. أضف اختبارات لأي تغيير سلوكي، وشغّل `pytest -q`، ولا تستخدم `shell=True`، ولا ترفع ملفات وسائط خاصة أو أسرارًا أو بيانات اعتماد.

Maintainer / المشرف: **Radwan Abdulhadi Ahmed — رضوان عبدالهادي أحمد — @rad03i2**
