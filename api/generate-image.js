// api/generate-image.js
// Stability AI 이미지 생성 — CommonJS (api/claude.js와 동일 방식)

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method Not Allowed' });

  const { prompt, style = 'photographic', aspectRatio = '16:9' } = req.body || {};
  if (!prompt) return res.status(400).json({ error: 'prompt is required' });

  const apiKey = process.env.STABILITY_API_KEY;
  if (!apiKey) return res.status(500).json({ error: 'STABILITY_API_KEY is not configured' });

  try {
    const formData = new FormData();
    formData.append('prompt', buildPrompt(prompt));
    formData.append('negative_prompt', NEGATIVE_PROMPT);
    formData.append('aspect_ratio', aspectRatio);
    formData.append('style_preset', style);
    formData.append('output_format', 'webp');

    const stabilityRes = await fetch(
      'https://api.stability.ai/v2beta/stable-image/generate/core',
      {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${apiKey}`,
          Accept: 'image/*',
        },
        body: formData,
      }
    );

    if (!stabilityRes.ok) {
      const errText = await stabilityRes.text();
      console.error('Stability AI error:', stabilityRes.status, errText);
      return res.status(stabilityRes.status).json({
        error: `Stability AI error: ${stabilityRes.status}`,
        detail: errText,
      });
    }

    const imageBuffer = await stabilityRes.arrayBuffer();
    const base64 = Buffer.from(imageBuffer).toString('base64');
    const imageUrl = `data:image/webp;base64,${base64}`;
    return res.status(200).json({ imageUrl });

  } catch (err) {
    console.error('generate-image error:', err);
    return res.status(500).json({ error: err.message || 'Internal Server Error' });
  }
};

function buildPrompt(userPrompt) {
  return [
    userPrompt,
    'realistic photograph',
    'high quality',
    'clear natural lighting',
    'everyday scene',
    'no text, no watermark',
  ].join(', ');
}

const NEGATIVE_PROMPT = [
  'blurry', 'distorted', 'cartoon', 'anime', 'painting',
  'text', 'watermark', 'signature', 'low quality', 'nsfw',
].join(', ');
