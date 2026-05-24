// api/unsplash.js
// Unsplash API 프록시 — API Key를 서버에서 관리

module.exports = async function handler(req, res) {
  // CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'GET') return res.status(405).json({ error: 'Method not allowed' });

  const { query, count = 1, orientation = 'landscape' } = req.query;
  if (!query) return res.status(400).json({ error: 'query 파라미터가 필요합니다.' });

  try {
    const url = `https://api.unsplash.com/photos/random?query=${encodeURIComponent(query)}&count=${count}&orientation=${orientation}`;
    const response = await fetch(url, {
      headers: {
        'Authorization': `Client-ID ${process.env.UNSPLASH_ACCESS_KEY}`
      }
    });

    const data = await response.json();
    return res.status(response.status).json(data);
  } catch (err) {
    console.error('Unsplash API error:', err);
    return res.status(500).json({ error: 'Unsplash API 호출에 실패했습니다.' });
  }
};
