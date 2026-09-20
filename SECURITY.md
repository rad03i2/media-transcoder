# Security Policy

Media Transcoder processes untrusted binary media through the locally installed FFmpeg/FFprobe executables. Keep those tools and your operating system patched.

## Design safeguards
- No network calls, telemetry, accounts, API keys, or cloud uploads.
- Subprocesses receive argument arrays; the project does not invoke a shell.
- Existing destinations are protected unless overwrite is explicitly requested.
- Input and output paths must differ.
- Failed transcodes remove partial output produced by that failed attempt.

## Reporting
Please report a suspected vulnerability privately to the maintainer through an appropriate private GitHub contact channel rather than publishing exploit details in a public issue. Do not include private media, credentials, tokens, or personal information in reports.

Maintainer: **Radwan Abdulhadi Ahmed (@rad03i2)**

## سياسة الأمان
تتم معالجة ملفات الوسائط محليًا بواسطة FFmpeg/FFprobe المثبتين على جهاز المستخدم. حافظ على تحديثهما. لا يستخدم المشروع الشبكة أو التتبع أو مفاتيح API، ولا يشغّل الأوامر عبر shell. عند الإبلاغ عن ثغرة لا ترفق ملفات خاصة أو بيانات اعتماد أو رموز وصول.
