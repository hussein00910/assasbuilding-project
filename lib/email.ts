import nodemailer from 'nodemailer';

const transporter = nodemailer.createTransport({
  host: process.env.SMTP_HOST,
  port: Number(process.env.SMTP_PORT ?? 587),
  secure: false,
  auth: {
    user: process.env.SMTP_USER,
    pass: process.env.SMTP_PASS,
  },
});

export async function sendDownloadEmail({
  to,
  customerName,
  productName,
  downloadUrl,
  expiresAt,
}: {
  to: string;
  customerName: string;
  productName: string;
  downloadUrl: string;
  expiresAt: string;
}) {
  const html = `
    <!DOCTYPE html>
    <html dir="rtl" lang="ar">
    <head><meta charset="utf-8"><title>تأكيد الشراء</title></head>
    <body style="font-family: Arial, sans-serif; background: #f9fafb; padding: 20px;">
      <div style="max-width: 600px; margin: 0 auto; background: white; border-radius: 12px; padding: 32px; box-shadow: 0 4px 6px rgba(0,0,0,0.07);">
        <div style="text-align: center; margin-bottom: 32px;">
          <h1 style="color: #0891b2; font-size: 28px; margin: 0;">أساس بيلدينج</h1>
          <p style="color: #6b7280; margin-top: 8px;">منصة المتاجر الجاهزة والخدمات الرقمية</p>
        </div>
        <h2 style="color: #111827;">مرحباً ${customerName}! 🎉</h2>
        <p style="color: #374151; line-height: 1.6;">شكراً لشرائك <strong>${productName}</strong>. طلبك جاهز للتحميل!</p>
        <div style="background: #f0fdff; border: 1px solid #bae6fd; border-radius: 8px; padding: 20px; margin: 24px 0;">
          <p style="color: #0c4a6e; font-weight: bold; margin: 0 0 12px;">🔗 رابط التحميل المباشر:</p>
          <a href="${downloadUrl}" style="display: block; background: #0891b2; color: white; text-align: center; padding: 12px 24px; border-radius: 8px; text-decoration: none; font-weight: bold;">تحميل الملف الآن</a>
          <p style="color: #64748b; font-size: 13px; margin-top: 12px;">⏰ ينتهي الرابط في: ${new Date(expiresAt).toLocaleString('ar-SA')}</p>
        </div>
        <div style="border-top: 1px solid #e5e7eb; padding-top: 20px; color: #6b7280; font-size: 13px;">
          <p>📧 للدعم الفني: support@assasbuilding.com</p>
          <p>هذا البريد أُرسل تلقائياً، يُرجى عدم الرد عليه مباشرة.</p>
        </div>
      </div>
    </body>
    </html>
  `;

  await transporter.sendMail({
    from: `"أساس بيلدينج" <${process.env.SMTP_FROM}>`,
    to,
    subject: `✅ تأكيد شرائك لـ ${productName} - رابط التحميل جاهز`,
    html,
  });
}
