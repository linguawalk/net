// api/claude.js
// Claude API 프록시 — JSON 정제 포함

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  try {
    const response = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': process.env.ANTHROPIC_API_KEY,
        'anthropic-version': '2023-06-01'
      },
      body: JSON.stringify(req.body)
    });

    const data = await response.json();

    // JSON 생성 요청인 경우 서버에서 정제
    const rawText = data.content?.[0]?.text || '';
    if (rawText && req.body?.messages?.[0]?.content?.includes('Return ONLY')) {
      const cleaned = sanitizeJSON(rawText);
      // 정제된 텍스트로 교체해서 반환
      if (data.content?.[0]) data.content[0].text = cleaned;
    }

    return res.status(response.status).json(data);
  } catch (err) {
    console.error('Claude API error:', err);
    return res.status(500).json({ error: 'Claude API 호출에 실패했습니다.' });
  }
};

function sanitizeJSON(raw) {
  // 1. 마크다운 코드블록 제거
  let s = raw.replace(/```json\s*/gi, '').replace(/```\s*/g, '').trim();

  // 2. { } 범위만 추출
  const start = s.indexOf('{');
  const end   = s.lastIndexOf('}');
  if (start !== -1 && end !== -1 && end > start) {
    s = s.slice(start, end + 1);
  }

  // 3. JSON 문자열 내부의 제어문자·줄바꿈 정리
  // JSON 파서가 읽을 수 있도록 문자열 값 내부의 raw 줄바꿈을 \\n으로 치환
  s = fixStringNewlines(s);

  return s;
}

function fixStringNewlines(jsonStr) {
  // 문자열 토큰 내부의 raw 줄바꿈(\n, \r)을 이스케이프된 \\n으로 교체
  // JSON 파서는 문자열 밖의 공백은 허용하지만 문자열 안의 raw 줄바꿈은 허용하지 않음
  let result = '';
  let inString = false;
  let escape = false;

  for (let i = 0; i < jsonStr.length; i++) {
    const ch = jsonStr[i];

    if (escape) {
      result += ch;
      escape = false;
      continue;
    }

    if (ch === '\\') {
      escape = true;
      result += ch;
      continue;
    }

    if (ch === '"') {
      inString = !inString;
      result += ch;
      continue;
    }

    if (inString) {
      if (ch === '\n') { result += '\\n'; continue; }
      if (ch === '\r') { result += '\\r'; continue; }
      if (ch === '\t') { result += '\\t'; continue; }
    }

    result += ch;
  }

  return result;
}
