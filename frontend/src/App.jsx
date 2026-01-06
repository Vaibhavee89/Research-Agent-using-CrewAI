import React, { useState } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import { Search, Brain, Rocket, AlertCircle, CheckCircle2, Loader2, Link as LinkIcon, Globe } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

function App() {
  const [topic, setTopic] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [status, setStatus] = useState('');

  const handleKickoff = async () => {
    if (!topic) return;
    setLoading(true);
    setResult(null);
    setError(null);
    setStatus('Initializing Agents...');

    try {
      // Simulate status updates for better UX
      setTimeout(() => setStatus('Researching the web...'), 2000);
      setTimeout(() => setStatus('Analyzing findings...'), 5000);
      setTimeout(() => setStatus('Synthesizing professional briefing...'), 8000);

      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      const response = await axios.post(`${apiUrl}/kickoff`, { topic });
      setResult(response.data.result);
      setLoading(false);
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || 'An unexpected error occurred. Is the backend running?');
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen w-full flex flex-col items-center">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="w-full max-w-4xl"
      >
        <header className="text-center mb-12">
          <div className="inline-flex items-center justify-center p-3 mb-4 rounded-2xl bg-blue-500/10 border border-blue-500/20">
            <Brain className="w-8 h-8 text-blue-400" />
          </div>
          <h1 className="text-5xl font-extrabold mb-4">
            <span className="gradient-text">AI Topic Summary Crew</span>
          </h1>
          <p className="text-slate-400 text-lg max-w-2xl mx-auto">
            Orchestrate an autonomous team of AI agents to research and summarize any topic with professional accuracy.
          </p>
        </header>

        <section className="glass-card mb-8">
          <div className="flex flex-col gap-4">
            <div className="relative">
              <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 w-5 h-5" />
              <input
                type="text"
                placeholder="Enter a topic (e.g., Space Exploration Trends 2025)"
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleKickoff()}
                className="pl-12"
                disabled={loading}
              />
            </div>
            <button
              onClick={handleKickoff}
              disabled={loading || !topic}
              className="flex items-center justify-center gap-2"
            >
              {loading ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  Running Crew...
                </>
              ) : (
                <>
                  <Rocket className="w-5 h-5" />
                  Kickoff Crew
                </>
              )}
            </button>
          </div>

          <AnimatePresence>
            {loading && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                exit={{ opacity: 0, height: 0 }}
                className="status-message flex items-center gap-2"
              >
                <div className="loading-spinner"></div>
                {status}
              </motion.div>
            )}
          </AnimatePresence>
        </section>

        <AnimatePresence>
          {error && (
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              className="p-4 bg-red-500/10 border border-red-500/20 rounded-xl flex items-center gap-3 text-red-400"
            >
              <AlertCircle className="w-6 h-6 shrink-0" />
              <p>{error}</p>
            </motion.div>
          )}

          {result && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="glass-card mb-12"
            >
              <div className="flex items-center gap-2 mb-6 text-green-400 border-b border-white/10 pb-4">
                <CheckCircle2 className="w-6 h-6" />
                <h2 className="text-xl font-semibold">Crew Research Report</h2>
              </div>
              <div className="markdown-content">
                <ReactMarkdown>{result}</ReactMarkdown>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        <footer className="mt-auto py-12 text-center text-slate-500 text-sm border-t border-white/5 w-full">
          <div className="flex items-center justify-center gap-6 mb-4">
            <span className="flex items-center gap-1"><Globe className="w-4 h-4" /> Web Research</span>
            <span className="flex items-center gap-1"><LinkIcon className="w-4 h-4" /> Live Citations</span>
            <span className="flex items-center gap-1"><Brain className="w-4 h-4" /> Multi-Agent Logic</span>
          </div>
          Built with CrewAI, React & FastAPI
        </footer>
      </motion.div>
    </div>
  );
}

export default App;
