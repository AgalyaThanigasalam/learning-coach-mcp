import { motion } from 'framer-motion'
import { useNavigate } from 'react-router-dom'
import { Brain, Zap, Target, TrendingUp, MessageCircle, BarChart3, ArrowRight, Sparkles, BookOpen, Award, GitBranch } from 'lucide-react'

const features = [
  { icon: GitBranch, title: 'Knowledge Graph', desc: 'Dynamic topic relationships — ML → DL → Transformers → LLMs.', color: 'from-indigo-500 to-purple-500' },
  { icon: Target, title: 'Adaptive Difficulty', desc: 'Questions get harder when you succeed, easier when you struggle.', color: 'from-violet-500 to-pink-500' },
  { icon: Zap, title: 'LLM Question Generator', desc: 'AI generates fresh questions every session. No repetition.', color: 'from-blue-500 to-cyan-500' },
  { icon: MessageCircle, title: 'Context-Aware Chatbot', desc: 'AI tutor that knows your weak areas and learning history.', color: 'from-emerald-500 to-teal-500' },
  { icon: TrendingUp, title: 'Learner Profiling', desc: 'Tracks accuracy, response time, streaks, and mastery per topic.', color: 'from-orange-500 to-amber-500' },
  { icon: BarChart3, title: 'Progress Analytics', desc: 'Mastery scores, engagement metrics, and smart recommendations.', color: 'from-rose-500 to-pink-500' },
]

export default function Landing() {
  const navigate = useNavigate()
  return (
    <div className="min-h-screen bg-mesh overflow-hidden">
      <nav className="fixed top-0 w-full z-50 glass border-b border-white/5">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-indigo-500 to-violet-600 flex items-center justify-center">
              <Brain size={18} className="text-white" />
            </div>
            <span className="font-bold text-white text-lg">LearnCoach AI</span>
          </div>
          <div className="flex items-center gap-3">
            <button onClick={() => navigate('/dashboard')} className="btn-ghost text-sm py-2 px-4">Dashboard</button>
            <button onClick={() => navigate('/learn')} className="btn-primary text-sm py-2 px-5">Start Learning</button>
          </div>
        </div>
      </nav>

      <section className="pt-36 pb-20 px-6 relative">
        <div className="max-w-5xl mx-auto text-center">
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
            className="inline-flex items-center gap-2 glass px-4 py-2 rounded-full text-sm text-indigo-300 mb-8 border border-indigo-500/20">
            <Sparkles size={14} /> 7 MCP Tools · LLM Powered · Zero Config
          </motion.div>
          <motion.h1 initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}
            className="text-6xl md:text-7xl font-extrabold text-white leading-tight mb-6">
            Your Personal<br /><span className="gradient-text">AI Learning Coach</span>
          </motion.h1>
          <motion.p initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}
            className="text-xl text-slate-400 max-w-2xl mx-auto mb-10 leading-relaxed">
            Adaptive AI tutor for Machine Learning, Deep Learning, NLP, and more. Powered by LLM — no setup required.
          </motion.p>
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }}
            className="flex flex-col sm:flex-row gap-4 justify-center">
            <button onClick={() => navigate('/learn')} className="btn-primary flex items-center gap-2 justify-center text-base py-4 px-8">
              Start Learning Free <ArrowRight size={18} />
            </button>
            <button onClick={() => navigate('/dashboard')} className="btn-ghost flex items-center gap-2 justify-center text-base py-4 px-8">
              <BarChart3 size={18} /> View Dashboard
            </button>
          </motion.div>
        </div>
        <div className="absolute top-40 left-10 w-72 h-72 bg-indigo-600/10 rounded-full blur-3xl pointer-events-none" />
        <div className="absolute top-60 right-10 w-96 h-96 bg-violet-600/8 rounded-full blur-3xl pointer-events-none" />
      </section>

      <section className="py-12 px-6">
        <div className="max-w-4xl mx-auto grid grid-cols-2 md:grid-cols-4 gap-6">
          {[['7','MCP Tools'],['147+','Questions'],['17','AI Topics'],['LLM','Powered']].map(([v,l],i) => (
            <motion.div key={i} initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} transition={{ delay: 0.4 + i * 0.1 }}
              className="card text-center">
              <div className="text-3xl font-extrabold gradient-text mb-1">{v}</div>
              <div className="text-sm text-slate-400">{l}</div>
            </motion.div>
          ))}
        </div>
      </section>

      <section className="py-20 px-6">
        <div className="max-w-6xl mx-auto">
          <motion.div initial={{ opacity: 0 }} whileInView={{ opacity: 1 }} viewport={{ once: true }} className="text-center mb-16">
            <h2 className="text-4xl font-bold text-white mb-4">7 Intelligent MCP Tools</h2>
            <p className="text-slate-400 text-lg">Each tool works independently and in orchestration.</p>
          </motion.div>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((f, i) => (
              <motion.div key={i} initial={{ opacity: 0, y: 30 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ delay: i * 0.1 }}
                whileHover={{ y: -4, scale: 1.02 }} className="card">
                <div className={`w-12 h-12 rounded-2xl bg-gradient-to-br ${f.color} flex items-center justify-center mb-4 shadow-lg`}>
                  <f.icon size={22} className="text-white" />
                </div>
                <h3 className="text-white font-semibold text-lg mb-2">{f.title}</h3>
                <p className="text-slate-400 text-sm leading-relaxed">{f.desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      <section className="py-20 px-6">
        <div className="max-w-3xl mx-auto text-center">
          <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }}
            className="glass-strong rounded-3xl p-12">
            <BookOpen size={48} className="text-indigo-400 mx-auto mb-6" />
            <h2 className="text-4xl font-bold text-white mb-4">Ready to learn smarter?</h2>
            <p className="text-slate-400 mb-8">No API key needed. Just open and start learning.</p>
            <button onClick={() => navigate('/learn')} className="btn-primary text-lg py-4 px-10 flex items-center gap-2 mx-auto">
              <Award size={20} /> Begin Your Journey
            </button>
          </motion.div>
        </div>
      </section>
      <footer className="py-8 text-center text-slate-600 text-sm border-t border-white/5">
        © 2025 LearnCoach AI — Personalized AI Learning Platform
      </footer>
    </div>
  )
}
