import React, { useState } from 'react';

function App() {
  const [target, setTarget] = useState('');
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);

  const runTask = async (endpoint) => {
    setLoading(true);
    setResult(">> EXECUTING COMMAND ON KALI LINUX... PLEASE WAIT...");
    try {
      const response = await fetch(`http://localhost:8000/${endpoint}?target=${target}`, { method: 'POST' });
      const data = await response.json();
      setResult(`[+] TASK_ID: ${data.task_id}\n[+] STATUS: Queued in Redis\n[+] AI is analyzing the traffic...`);
    } catch (error) {
      setResult("!! ERROR: CONNECTION TO BACKEND FAILED");
    }
    setLoading(false);
  };

  return (
    <div style={{ backgroundColor: '#050505', color: '#00ff41', minHeight: '100vh', padding: '30px', fontFamily: 'Courier New' }}>
      <h1 style={{ textAlign: 'center', borderBottom: '2px solid #00ff41', paddingBottom: '10px' }}>
        CYBER-AI MULTI-TOOL PLATFORM v2.0
      </h1>

      <div style={{ margin: '20px auto', maxWidth: '900px' }}>
        <label>TARGET_URL_OR_IP:</label>
        <input 
          type="text" 
          value={target} 
          onChange={(e) => setTarget(e.target.value)}
          placeholder="e.g., 192.168.1.1 or https://example.com"
          style={{ width: '100%', padding: '12px', background: '#111', border: '1px solid #00ff41', color: '#00ff41', marginBottom: '20px' }}
        />

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px' }}>
          <button onClick={() => runTask('scan/nmap')} style={btnStyle}>[1] NETWORK_SCAN (NMAP)</button>
          <button onClick={() => runTask('scan/nikto')} style={btnStyle}>[2] WEB_VULN_SCAN (NIKTO)</button>
          <button onClick={() => runTask('scan/sqlmap')} style={btnStyle}>[3] DATABASE_EXPLOIT (SQLMAP)</button>
          <button onClick={() => runTask('scan/wifi')} style={btnStyle}>[4] WIFI_AUDIT (WIFITE)</button>
        </div>

        <div style={{ marginTop: '30px', background: '#001100', border: '1px solid #00ff41', padding: '20px', minHeight: '300px' }}>
          <h3 style={{ color: '#fff' }}>>> CONSOLE_OUTPUT:</h3>
          <pre style={{ whiteSpace: 'pre-wrap', color: '#00ff41' }}>{result}</pre>
          {loading && <div className="spinner">SYSTEM PROCESSING...</div>}
        </div>
      </div>
    </div>
  );
}

const btnStyle = {
  padding: '15px',
  background: 'transparent',
  border: '1px solid #00ff41',
  color: '#00ff41',
  cursor: 'pointer',
  fontSize: '14px',
  fontWeight: 'bold',
  textTransform: 'uppercase'
};

export default App;
