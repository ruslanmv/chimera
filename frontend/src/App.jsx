import React, { useEffect, useMemo, useState } from 'react';
import { Terminal, Eye, Play, Activity, Image as ImageIcon, MousePointerClick, Type, Globe, ArrowDown, Clock } from 'lucide-react';

function now() {
  return new Date().toLocaleTimeString();
}

export default function App() {
  const [status, setStatus] = useState({ plugins: [], active_sessions: [], tools: [] });
  const [prompt, setPrompt] = useState("");
  const [selectedFile, setSelectedFile] = useState(null);
  
  const [model, setModel] = useState("ollama");
  const [thoughtLog, setThoughtLog] = useState([
    { t: now(), kind: "system", msg: "Command Center ready." }
  ]);

  // Computer use inputs
  const [gotoUrl, setGotoUrl] = useState("https://example.com");
  const [selector, setSelector] = useState("#prompt-textarea");
  const [typeText, setTypeText] = useState("Hello from Chimera!");
  const [scrollDy, setScrollDy] = useState(800);

  const browserModels = useMemo(() => {
    // heuristic: if a model has an active session screenshot, it’s browser-based
    const active = new Set(status.active_sessions.map(s => s.name));
    return status.plugins.filter(p => active.has(p) || p === "chatgpt"); // include chatgpt as likely browser head
  }, [status]);

  const pushLog = (kind, msg) => {
    setThoughtLog(prev => [{ t: now(), kind, msg }, ...prev].slice(0, 200));
  };

  const fetchStatus = async () => {
    try {
      const res = await fetch('/api/status');
      const data = await res.json();
      setStatus(data);
      
      // set default model smartly
      if (!data.plugins.includes(model)) {
        setModel(data.plugins.includes("ollama") ? "ollama" : (data.plugins[0] || "ollama"));
      }
    } catch (e) { 
      pushLog("error", String(e));
    }
  };

  useEffect(() => {
    fetchStatus();
    const interval = setInterval(fetchStatus, 5000);
    return () => clearInterval(interval);
  }, []);

  const spawn = async (m) => {
    pushLog("action", `Spawning browser session for: ${m}`);
    await fetch(`/api/spawn/${m}`, { method: 'POST' });
    pushLog("system", `${m} spawned. Login in the opened browser window if needed.`);
    fetchStatus();
  };

  const runInference = async () => {
    pushLog("action", `Inference on model=${model} ${selectedFile ? "(vision)" : "(text)"}`);
    
    try {
      if (selectedFile) {
        const formData = new FormData();
        formData.append('model', model);
        formData.append('prompt', prompt || "Describe this image");
        formData.append('file', selectedFile);
        
        const res = await fetch('/api/vision', { method: 'POST', body: formData });
        const data = await res.json();
        pushLog("result", data.response || "No response");
      } else {
        const res = await fetch('/v1/chat/completions', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ model, messages: [{ role: 'user', content: prompt || "Hello" }] })
        });
        const data = await res.json();
        pushLog("result", data?.choices?.[0]?.message?.content || "No response");
      }
    } catch (e) {
      pushLog("error", String(e));
    }
  };

  const runTool = async (tool, args) => {
    pushLog("tool", `${tool} ${JSON.stringify(args)}`);
    try {
      const res = await fetch(`/api/computer/${model}/tool`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ tool, args })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data?.detail || "Tool error");
      pushLog("result", `${tool}: ${data.result.message}`);
      fetchStatus();
    } catch (e) {
      pushLog("error", String(e));
    }
  };

  return (
    <div className="min-h-screen bg-chimera-900 text-gray-200 p-6 font-sans">
      <header className="mb-6 flex flex-col gap-3 md:flex-row md:justify-between md:items-center border-b border-chimera-700 pb-4">
        <div>
          <h1 className="text-3xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-600">
            CHIMERA COMMAND CENTER
          </h1>
          <p className="text-sm text-gray-500">Local Models • Browser Agents • Computer Use</p>
        </div>
        <div className="flex items-center gap-2 text-green-400 text-sm">
          <Activity size={16} /> API Online
        </div>
      </header>

      <div className="grid grid-cols-1 xl:grid-cols-12 gap-6">
        {/* LEFT COLUMN */}
        <div className="xl:col-span-4 space-y-6">
          {/* Models */}
          <div className="bg-chimera-800 p-5 rounded-2xl border border-chimera-700">
            <div className="flex items-center justify-between mb-3">
              <h2 className="text-lg font-semibold flex items-center gap-2"><Terminal size={18}/> Models</h2>
              <select 
                value={model} 
                onChange={e => setModel(e.target.value)}
                className="bg-chimera-900 border border-chimera-700 rounded px-2 py-1 text-sm"
              >
                {status.plugins.map(p => <option key={p} value={p}>{p}</option>)}
              </select>
            </div>

            <div className="space-y-2">
              {status.plugins.map(p => (
                <div key={p} className="flex justify-between items-center bg-chimera-900 p-3 rounded-xl border border-chimera-700">
                  <span className="capitalize font-medium">{p}</span>
                  <div className="flex gap-2">
                    <button 
                      onClick={() => setModel(p)} 
                      className="bg-chimera-700 hover:bg-chimera-600 text-white px-3 py-1 rounded text-xs"
                    >
                      Use
                    </button>
                    <button 
                      onClick={() => spawn(p)} 
                      className="bg-purple-600 hover:bg-purple-500 text-white px-3 py-1 rounded text-xs flex items-center gap-1"
                      title="Spawn browser session (only meaningful for browser heads)"
                    >
                      <Play size={12}/> Spawn
                    </button>
                  </div>
                </div>
              ))}
              <p className="text-xs text-gray-500 pt-2">
                Tip: For OSS virality, default to <b>ollama</b> (local). Use browser heads when needed.
              </p>
            </div>
          </div>

          {/* Playground */}
          <div className="bg-chimera-800 p-5 rounded-2xl border border-chimera-700">
            <h2 className="text-lg font-semibold mb-3">Playground</h2>
            
            <textarea 
               className="w-full bg-chimera-900 border border-chimera-700 rounded-xl p-3 text-sm focus:outline-none focus:border-purple-500"
               rows="5"
               placeholder="Enter prompt..."
               value={prompt}
               onChange={e => setPrompt(e.target.value)}
            />
            
            <div className="mt-3">
               <label className="flex items-center gap-2 cursor-pointer bg-chimera-700 hover:bg-chimera-600 p-2 rounded-xl text-sm justify-center">
                   <ImageIcon size={16} />
                   {selectedFile ? selectedFile.name : "Upload Image (Optional, browser heads)"}
                   <input type="file" className="hidden" onChange={e => setSelectedFile(e.target.files[0])} />
               </label>
            </div>

            <button 
              onClick={runInference} 
              className="w-full mt-3 bg-green-600 hover:bg-green-500 text-white py-2 rounded-xl font-bold"
            >
               Run Inference
            </button>
          </div>

          {/* Computer Use */}
          <div className="bg-chimera-800 p-5 rounded-2xl border border-chimera-700">
            <h2 className="text-lg font-semibold mb-3 flex items-center gap-2">
              <MousePointerClick size={18}/> Computer Use (Playwright Tools)
            </h2>
            <p className="text-xs text-gray-500 mb-3">
              Works only if <b>model</b> is a browser head (spawn it first). These are the primitives you expose as “tools”.
            </p>

            <div className="space-y-3">
              <div className="bg-chimera-900 border border-chimera-700 rounded-xl p-3">
                <div className="flex items-center gap-2 text-sm font-semibold mb-2"><Globe size={14}/> goto</div>
                <input 
                  value={gotoUrl} 
                  onChange={e => setGotoUrl(e.target.value)} 
                  className="w-full bg-chimera-950 border border-chimera-700 rounded px-2 py-1 text-sm"
                />
                <button onClick={() => runTool("goto", { url: gotoUrl })} className="mt-2 w-full bg-purple-600 hover:bg-purple-500 rounded py-2 text-sm font-semibold">
                  Run goto
                </button>
              </div>

              <div className="bg-chimera-900 border border-chimera-700 rounded-xl p-3">
                <div className="flex items-center gap-2 text-sm font-semibold mb-2"><MousePointerClick size={14}/> click</div>
                <input 
                  value={selector} 
                  onChange={e => setSelector(e.target.value)} 
                  className="w-full bg-chimera-950 border border-chimera-700 rounded px-2 py-1 text-sm"
                  placeholder="CSS selector"
                />
                <button onClick={() => runTool("click", { selector })} className="mt-2 w-full bg-purple-600 hover:bg-purple-500 rounded py-2 text-sm font-semibold">
                  Run click
                </button>
              </div>

              <div className="bg-chimera-900 border border-chimera-700 rounded-xl p-3">
                <div className="flex items-center gap-2 text-sm font-semibold mb-2"><Type size={14}/> type</div>
                <input 
                  value={selector} 
                  onChange={e => setSelector(e.target.value)} 
                  className="w-full bg-chimera-950 border border-chimera-700 rounded px-2 py-1 text-sm mb-2"
                  placeholder="CSS selector"
                />
                <textarea 
                  value={typeText} 
                  onChange={e => setTypeText(e.target.value)} 
                  className="w-full bg-chimera-950 border border-chimera-700 rounded px-2 py-1 text-sm"
                  rows="2"
                />
                <button onClick={() => runTool("type", { selector, text: typeText, clear: true })} className="mt-2 w-full bg-purple-600 hover:bg-purple-500 rounded py-2 text-sm font-semibold">
                  Run type
                </button>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div className="bg-chimera-900 border border-chimera-700 rounded-xl p-3">
                  <div className="flex items-center gap-2 text-sm font-semibold mb-2"><ArrowDown size={14}/> scroll</div>
                  <input 
                    value={scrollDy} 
                    onChange={e => setScrollDy(Number(e.target.value))} 
                    className="w-full bg-chimera-950 border border-chimera-700 rounded px-2 py-1 text-sm"
                    type="number"
                  />
                  <button onClick={() => runTool("scroll", { dy: scrollDy })} className="mt-2 w-full bg-purple-600 hover:bg-purple-500 rounded py-2 text-sm font-semibold">
                    Run scroll
                  </button>
                </div>

                <div className="bg-chimera-900 border border-chimera-700 rounded-xl p-3">
                  <div className="flex items-center gap-2 text-sm font-semibold mb-2"><Clock size={14}/> wait</div>
                  <button onClick={() => runTool("wait", { ms: 1000 })} className="w-full bg-purple-600 hover:bg-purple-500 rounded py-2 text-sm font-semibold">
                    Wait 1s
                  </button>
                  <button onClick={() => runTool("wait", { ms: 3000 })} className="mt-2 w-full bg-purple-600 hover:bg-purple-500 rounded py-2 text-sm font-semibold">
                    Wait 3s
                  </button>
                </div>
              </div>
            </div>

          </div>
        </div>

        {/* RIGHT COLUMN */}
        <div className="xl:col-span-8 space-y-6">
          {/* Live Vision */}
          <div className="bg-chimera-800 p-5 rounded-2xl border border-chimera-700">
            <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <Eye size={18}/> Live Browser Vision
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {status.active_sessions.map(s => (
                    <div key={s.name} className="relative group">
                        <img 
                          src={s.screenshot + '?t=' + Date.now()} 
                          alt={s.name} 
                          className="rounded-xl border border-chimera-600 w-full h-56 object-cover opacity-85 group-hover:opacity-100 transition" 
                        />
                        <div className="absolute bottom-0 left-0 bg-black/70 w-full p-2 text-xs font-bold capitalize rounded-b-xl">
                            {s.name} • {s.status}
                        </div>
                    </div>
                ))}
                
                {status.active_sessions.length === 0 && (
                    <div className="text-gray-500 text-sm col-span-2 text-center py-10">
                        No active browser sessions. Spawn a browser head to see live feed.
                    </div>
                )}
            </div>
          </div>

          {/* Thought Log */}
          <div className="bg-black p-4 rounded-2xl font-mono text-xs text-green-300 h-[420px] overflow-y-auto border border-gray-800">
             <div className="text-gray-400 mb-2">Thought Log (most recent first)</div>
             {thoughtLog.map((x, i) => (
               <div key={i} className="mb-2">
                 <span className="text-gray-500">[{x.t}]</span>{" "}
                 <span className="text-purple-300">{x.kind}</span>{" "}
                 <span className="text-green-200">{x.msg}</span>
               </div>
             ))}
          </div>
        </div>
      </div>
    </div>
  );
}
