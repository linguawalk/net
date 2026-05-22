// api/set-admin.js
// 관리자 계정 설정 — 최초 1회만 실행

const { initializeApp, cert, getApps } = require('firebase-admin/app');
const { getFirestore } = require('firebase-admin/firestore');
const { getAuth } = require('firebase-admin/auth');

// Firebase Admin 초기화
if(!getApps().length){
  initializeApp({
    credential: cert({
      projectId:   process.env.FIREBASE_PROJECT_ID,
      clientEmail: process.env.FIREBASE_CLIENT_EMAIL,
      privateKey:  process.env.FIREBASE_PRIVATE_KEY?.replace(/\\n/g, '\n'),
    })
  });
}

module.exports = async function handler(req, res){
  // 보안: 비밀 키 확인
  if(req.headers['x-admin-secret'] !== process.env.ADMIN_SECRET){
    return res.status(403).json({ error: 'Forbidden' });
  }

  if(req.method !== 'POST'){
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { email } = req.body;
  if(!email) return res.status(400).json({ error: 'Email required' });

  try {
    const auth = getAuth();
    const db   = getFirestore();

    // Firebase Auth에서 사용자 찾기
    const user = await auth.getUserByEmail(email);

    // Firestore에 admin 역할 설정
    await db.collection('users').doc(user.uid).set({
      uid:   user.uid,
      email: user.email,
      name:  user.displayName || '관리자',
      role:  'admin',
      plan:  'admin'
    }, { merge: true });

    return res.status(200).json({
      success: true,
      message: `${email} 계정이 관리자로 설정되었습니다.`,
      uid: user.uid
    });
  } catch(err){
    return res.status(500).json({ error: err.message });
  }
};
