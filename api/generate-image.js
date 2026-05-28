// api/generate-image.js
// Stability AI — stable-image/generate/core
// Node.js 호환: fetch + FormData (Node 18+) 또는 직접 multipart 구성

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method Not Allowed' });

  const { prompt, aspectRatio = '16:9' } = req.body || {};
  if (!prompt) return res.status(400).json({ error: 'prompt is required' });

  const apiKey = process.env.STABILITY_API_KEY;
  if (!apiKey) return res.status(500).json({ error: 'STABILITY_API_KEY not set' });

  const fullPrompt = `${prompt}, realistic photograph, high quality, clear natural lighting, no text, no watermark`;
  const negPrompt  = 'blurry, distorted, cartoon, anime, text, watermark, low quality, nsfw';

  // multipart/form-data를 직접 Buffer로 구성 (FormData 의존성 제거)
  const boundary = '----StabilityBoundary' + Date.now();
  const parts = [
    { name: 'prompt',          value: fullPrompt },
    { name: 'negative_prompt', value: negPrompt  },
    { name: 'aspect_ratio',    value: aspectRatio },
    { name: 'style_preset',    value: 'photographic' },
    { name: 'output_format',   value: 'jpeg' },
  ];

  const bodyParts = parts.map(p =>
    `--${boundary}\r\nContent-Disposition: form-data; name="${p.name}"\r\n\r\n${p.value}`
  ).join('\r\n');
  const bodyStr = bodyParts + `\r\n--${boundary}--\r\n`;

  try {
    const stabilityRes = await fetch(
      'https://api.stability.ai/v2beta/stable-image/generate/core',
      {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${apiKey}`,
          Accept: 'image/*',
          'Content-Type': `multipart/form-data; boundary=${boundary}`,
        },
        body: bodyStr,
      }
    );

    if (!stabilityRes.ok) {
      const errText = await stabilityRes.text();
      console.error('Stability AI error:', stabilityRes.status, errText);
      return res.status(stabilityRes.status).json({
        error: `Stability AI ${stabilityRes.status}`,
        detail: errText,
      });
    }

    const buf = Buffer.from(await stabilityRes.arrayBuffer());
    const base64 = buf.toString('base64');
    return res.status(200).json({ imageUrl: `data:image/jpeg;base64,${base64}` });

  } catch (err) {
    console.error('generate-image error:', err);
    return res.status(500).json({ error: err.message });
  }
};
