import React, { useState } from 'react';

function App() {
  const [target, setTarget] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const startScan = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/scan/nmap?target=' + target, { method: 'POST' });
      const data = await response.json();
      setResult("جاري الفحص... Task ID: " + data.task_id);
    } catch (error) {
      setResult("خطأ في الاتصال بالخادم");
    }
    setLoading(false);
  };

  return (
    <div style={{ backgroundColor: '#0a0a0a', color: '#00ff41', minHeight: '100vh', padding: '20px', fontFamily: 'monospace' }}>
      <header style={{ borderBottom: '1px solid #00ff41', paddingBottom: '10px', marginBottom: '30px' }}>
        <h1>TERMINAL: CYBER-AI-SCANNER v1.0</h1>
      </header>
      
      <div style={{ maxWidth: '800px', margin: '0 auto' }}>
        <p>> ENTER TARGET IP/DOMAIN:</p>
        <input 
          type="text" 
          value={target} 
          onChange={(e) => setTarget(e.target.value)}
          placeholder="e.g. scanme.nmap.org"
          style={{ width: '100%', padding: '10px', background: '#1a1a1a', border: '1px solid #00ff41', color: '#00ff41', outline: 'none' }}
        />
        <button 
          onClick={startScan}
          style={{ marginTop: '20px', padding: '10px 20px', background: '#00ff41', color: '#000', border: 'none', cursor: 'pointer', fontWeight: 'bold' }}
        >
          {loading ? 'EXECUTING...' : 'EXECUTE ATTACK / SCAN'}
        </button>

        {result && (
          <div style={{ marginTop: '40px', padding: '15px', border: '1px dashed #00ff41', background: '#050505' }}>
            <h3>[+] ANALYSIS_REPORT:</h3>
            <pre style={{ whiteSpace: 'pre-wrap' }}>{result}</pre>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
