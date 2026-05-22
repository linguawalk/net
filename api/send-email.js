// api/send-email.js
// Vercel 서버리스 함수 — Hostinger SMTP로 이메일 발송

const nodemailer = require('nodemailer');

module.exports = async function handler(req, res) {
  // CORS 헤더
  res.setHeader('Access-Control-Allow-Origin', 'https://linguawalk.net');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { type, ...data } = req.body;

  // SMTP 설정 (Vercel 환경변수에서 불러옴)
  const transporter = nodemailer.createTransport({
    host: process.env.SMTP_HOST,
    port: parseInt(process.env.SMTP_PORT),
    secure: true, // 465 포트 SSL
    auth: {
      user: process.env.SMTP_USER,
      pass: process.env.SMTP_PASS,
    },
  });

  try {
    // ── 1. 학습자 문의 수신 (마이페이지 → 관리자) ──
    if (type === 'feedback') {
      const { user_name, user_email, feedback_type, rating, subject, message } = data;

      await transporter.sendMail({
        from: `"LinguaWalk" <${process.env.SMTP_USER}>`,
        to: process.env.SMTP_USER, // admin@linguawalk.net
        subject: `[LinguaWalk 문의] ${subject}`,
        html: `
          <div style="font-family:sans-serif;max-width:600px;margin:0 auto;padding:24px;">
            <div style="background:#1C2B45;padding:20px;border-radius:12px 12px 0 0;text-align:center;">
              <h2 style="color:#fff;margin:0;font-size:20px;">📩 새 문의가 도착했습니다</h2>
            </div>
            <div style="background:#f8f7f4;padding:24px;border-radius:0 0 12px 12px;border:1px solid #e0e0e0;">
              <table style="width:100%;border-collapse:collapse;">
                <tr>
                  <td style="padding:8px 0;font-weight:700;color:#5a6a82;width:100px;">보낸 사람</td>
                  <td style="padding:8px 0;">${user_name} (${user_email})</td>
                </tr>
                <tr>
                  <td style="padding:8px 0;font-weight:700;color:#5a6a82;">유형</td>
                  <td style="padding:8px 0;">${feedback_type}</td>
                </tr>
                <tr>
                  <td style="padding:8px 0;font-weight:700;color:#5a6a82;">별점</td>
                  <td style="padding:8px 0;">${rating} / 5 ⭐</td>
                </tr>
                <tr>
                  <td style="padding:8px 0;font-weight:700;color:#5a6a82;">제목</td>
                  <td style="padding:8px 0;">${subject}</td>
                </tr>
              </table>
              <hr style="border:none;border-top:1px solid #ddd;margin:16px 0;">
              <p style="font-weight:700;color:#5a6a82;margin-bottom:8px;">내용</p>
              <p style="background:#fff;padding:16px;border-radius:8px;line-height:1.7;border:1px solid #e0e0e0;">${message.replace(/\n/g, '<br>')}</p>
              <p style="color:#94a3b8;font-size:12px;margin-top:16px;">발송 시각: ${new Date().toLocaleString('ko-KR')}</p>
            </div>
          </div>
        `,
      });

      // 학습자에게 접수 확인 이메일 발송
      await transporter.sendMail({
        from: `"LinguaWalk" <${process.env.SMTP_USER}>`,
        to: user_email,
        subject: '[LinguaWalk] 문의가 접수되었습니다',
        html: `
          <div style="font-family:sans-serif;max-width:600px;margin:0 auto;padding:24px;">
            <div style="background:#2A7F6F;padding:20px;border-radius:12px 12px 0 0;text-align:center;">
              <h2 style="color:#fff;margin:0;">✓ 문의가 접수되었습니다</h2>
            </div>
            <div style="background:#f8f7f4;padding:24px;border-radius:0 0 12px 12px;border:1px solid #e0e0e0;">
              <p>${user_name}님, 안녕하세요.</p>
              <p>문의해 주셔서 감사합니다. 빠른 시일 내에 답변 드리겠습니다.</p>
              <div style="background:#e1f5ee;padding:16px;border-radius:8px;margin:16px 0;">
                <p style="font-weight:700;margin-bottom:4px;">접수된 문의</p>
                <p style="color:#5a6a82;">${subject}</p>
              </div>
              <p style="color:#94a3b8;font-size:12px;">LinguaWalk 운영팀 · admin@linguawalk.net</p>
            </div>
          </div>
        `,
      });

      return res.status(200).json({ success: true, message: '문의가 접수되었습니다.' });
    }

    // ── 2. 관리자 답변 발송 (관리자 → 학습자) ──
    if (type === 'reply') {
      const { to_email, user_name, subject, original_message, reply_message } = data;

      await transporter.sendMail({
        from: `"LinguaWalk 운영팀" <${process.env.SMTP_USER}>`,
        to: to_email,
        subject: `[LinguaWalk] 문의 답변드립니다`,
        html: `
          <div style="font-family:sans-serif;max-width:600px;margin:0 auto;padding:24px;">
            <div style="background:#1C2B45;padding:20px;border-radius:12px 12px 0 0;text-align:center;">
              <h2 style="color:#fff;margin:0;">📩 문의 답변드립니다</h2>
            </div>
            <div style="background:#f8f7f4;padding:24px;border-radius:0 0 12px 12px;border:1px solid #e0e0e0;">
              <p>${user_name}님, 안녕하세요. LinguaWalk 운영팀입니다.</p>
              <div style="background:#f0f0f0;padding:16px;border-radius:8px;margin:16px 0;border-left:3px solid #ccc;">
                <p style="font-size:12px;color:#94a3b8;margin-bottom:8px;">원본 문의</p>
                <p style="color:#5a6a82;">${original_message}</p>
              </div>
              <div style="background:#e1f5ee;padding:16px;border-radius:8px;margin:16px 0;border-left:3px solid #2A7F6F;">
                <p style="font-size:12px;color:#2A7F6F;font-weight:700;margin-bottom:8px;">답변</p>
                <p style="line-height:1.7;">${reply_message.replace(/\n/g, '<br>')}</p>
              </div>
              <p>추가 문의사항이 있으시면 언제든지 연락해 주세요.</p>
              <p style="color:#94a3b8;font-size:12px;margin-top:16px;">LinguaWalk 운영팀 · admin@linguawalk.net</p>
            </div>
          </div>
        `,
      });

      return res.status(200).json({ success: true, message: '답변이 발송되었습니다.' });
    }

    // ── 3. 관리자 대량 이메일 발송 ──
    if (type === 'bulk') {
      const { to_email, subject, message, target } = data;

      await transporter.sendMail({
        from: `"LinguaWalk" <${process.env.SMTP_USER}>`,
        to: to_email,
        subject: subject,
        html: `
          <div style="font-family:sans-serif;max-width:600px;margin:0 auto;padding:24px;">
            <div style="background:#1C2B45;padding:20px;border-radius:12px 12px 0 0;text-align:center;">
              <h2 style="color:#fff;margin:0;">LinguaWalk</h2>
            </div>
            <div style="background:#f8f7f4;padding:24px;border-radius:0 0 12px 12px;border:1px solid #e0e0e0;">
              <p style="line-height:1.7;">${message.replace(/\n/g, '<br>')}</p>
              <hr style="border:none;border-top:1px solid #ddd;margin:16px 0;">
              <p style="color:#94a3b8;font-size:12px;">LinguaWalk 운영팀 · admin@linguawalk.net · linguawalk.net</p>
              <p style="color:#94a3b8;font-size:11px;">수신 거부를 원하시면 admin@linguawalk.net으로 연락해 주세요.</p>
            </div>
          </div>
        `,
      });

      return res.status(200).json({ success: true, message: '이메일이 발송되었습니다.' });
    }

    return res.status(400).json({ error: 'Invalid type' });

  } catch (error) {
    console.error('Email error:', error);
    return res.status(500).json({ error: '이메일 발송에 실패했습니다.', detail: error.message });
  }
};
