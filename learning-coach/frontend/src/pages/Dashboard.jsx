import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { useNavigate } from 'react-router-dom'
import { RadialBarChart, RadialBar, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, Cell } from 'recharts'
import { Brain, Zap, Target, TrendingUp, Award, ArrowRight, Flame, BarChart3 } from 'lucide-react'
import { useApp } from '../context/AppContext'
import { getProgress, getLearningPath } from '../api/client'

const COLORS = ['#6366f1','#a78bfa','#38bdf8','#34d399','#fb923c','#f472b6']

export default function Dashboard() {
  const { userId, setAnalytics } = useApp()
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  useEffect(() => {
    Promise.all([getProgress(userId), getLearningPath(userId)])
      .then(([prog]) => { setData(prog.data); setAnalytics(prog.data) })
      .catch(() => setData({ overall_mastery:0, engagement_score:0, streak:0, xp:0, level:1, total_questions:0, total_correct:0, weak_topics:[], strong_topics:[], topic_performance:[], recommendations:['Start learning to see your progress!'] }))
      .finally(() => setLoading(false))
  }, [userId])

  if (loading) return (
    <div className="pt-24 flex items-center justify-center min-h-screen">
      <div className="w-12 h-12 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin" />
    </div>
  )

  const masteryData = [{ name: 'Mastery', value: data?.overall_mastery || 0, fill: '#6366f1' }]
  const topicData = (data?.topic_performance || []).slice(0, 6).map((t, i) => ({ ...t, fill: COLORS[i % COLORS.length] }))

  return (
    <div className="pt-24 pb-12 px-6 max-w-7xl mx-auto">
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="mb-8">
        <h1 className="text-3xl font-bold text-white mb-1">Learning Dashboard</h1>
        <p className="text-slate-400">Track your progress across all AI topics.</p>
      </motion.div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        {[
          { label:'Overall Mastery', value:`${data?.overall_mastery||0}%`, icon:Brain, color:'from-indigo-500 to-violet-500' },
          { label:'Engagement', value:`${data?.engagement_score||0}%`, icon:Zap, color:'from-violet-500 to-pink-500' },
          { label:'Streak', value:`${data?.streak||0} 🔥`, icon:Flame, color:'from-orange-500 to-amber-500' },
          { label:'Level', value:`Lv. ${data?.level||1}`, icon:Award, color:'from-emerald-500 to-teal-500' },
        ].map((s, i) => (
          <motion.div key={i} initial={{ opacity:0, scale:0.9 }} animate={{ opacity:1, scale:1 }} transition={{ delay:i*0.1 }} className="card">
            <div className={`w-10 h-10 rounded-xl bg-gradient-to-br ${s.color} flex items-center justify-center mb-3`}>
              <s.icon size={18} className="text-white" />
            </div>
            <div className="text-2xl font-bold text-white">{s.value}</div>
            <div className="text-xs text-slate-400 mt-1">{s.label}</div>
          </motion.div>
        ))}
      </div>

      <div className="grid md:grid-cols-2 gap-6 mb-8">
        <motion.div initial={{ opacity:0, x:-20 }} animate={{ opacity:1, x:0 }} transition={{ delay:0.2 }} className="card">
          <h3 className="text-white font-semibold mb-4 flex items-center gap-2"><Target size={18} className="text-indigo-400" /> Mastery Score</h3>
          <div className="relative h-48">
            <ResponsiveContainer width="100%" height="100%">
              <RadialBarChart cx="50%" cy="50%" innerRadius="60%" outerRadius="90%" data={masteryData} startAngle={90} endAngle={-270}>
                <RadialBar dataKey="value" cornerRadius={10} background={{ fill:'rgba(255,255,255,0.05)' }} />
              </RadialBarChart>
            </ResponsiveContainer>
            <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
              <div className="text-3xl font-extrabold gradient-text">{data?.overall_mastery||0}%</div>
              <div className="text-slate-400 text-xs mt-1">Overall Mastery</div>
            </div>
          </div>
        </motion.div>

        <motion.div initial={{ opacity:0, x:20 }} animate={{ opacity:1, x:0 }} transition={{ delay:0.3 }} className="card">
          <h3 className="text-white font-semibold mb-4 flex items-center gap-2"><BarChart3 size={18} className="text-violet-400" /> Topic Performance</h3>
          {topicData.length > 0 ? (
            <div className="h-48">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={topicData} margin={{ top:0, right:0, left:-20, bottom:0 }}>
                  <XAxis dataKey="topic" tick={{ fill:'#94a3b8', fontSize:10 }} />
                  <YAxis tick={{ fill:'#94a3b8', fontSize:10 }} domain={[0,100]} />
                  <Tooltip contentStyle={{ background:'rgba(15,15,30,0.9)', border:'1px solid rgba(255,255,255,0.1)', borderRadius:'12px', color:'#e2e8f0' }} />
                  <Bar dataKey="accuracy" radius={[6,6,0,0]}>
                    {topicData.map((_, i) => <Cell key={i} fill={COLORS[i%COLORS.length]} />)}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          ) : <div className="h-48 flex items-center justify-center text-slate-500 text-sm">Answer questions to see topic performance</div>}
        </motion.div>
      </div>

      <div className="grid md:grid-cols-3 gap-6">
        <motion.div initial={{ opacity:0, y:20 }} animate={{ opacity:1, y:0 }} transition={{ delay:0.4 }} className="card">
          <h3 className="text-white font-semibold mb-4 flex items-center gap-2"><Target size={18} className="text-rose-400" /> Weak Areas</h3>
          {data?.weak_topics?.length > 0 ? data.weak_topics.map((t,i) => (
            <div key={i} className="flex items-center gap-2 py-2 border-b border-white/5 last:border-0">
              <div className="w-2 h-2 rounded-full bg-rose-400" /><span className="text-slate-300 text-sm">{t}</span>
            </div>
          )) : <p className="text-slate-500 text-sm">No weak areas yet — keep learning!</p>}
        </motion.div>

        <motion.div initial={{ opacity:0, y:20 }} animate={{ opacity:1, y:0 }} transition={{ delay:0.5 }} className="card">
          <h3 className="text-white font-semibold mb-4 flex items-center gap-2"><Award size={18} className="text-emerald-400" /> Strong Areas</h3>
          {data?.strong_topics?.length > 0 ? data.strong_topics.map((t,i) => (
            <div key={i} className="flex items-center gap-2 py-2 border-b border-white/5 last:border-0">
              <div className="w-2 h-2 rounded-full bg-emerald-400" /><span className="text-slate-300 text-sm">{t}</span>
            </div>
          )) : <p className="text-slate-500 text-sm">Master topics to see them here!</p>}
        </motion.div>

        <motion.div initial={{ opacity:0, y:20 }} animate={{ opacity:1, y:0 }} transition={{ delay:0.6 }} className="card">
          <h3 className="text-white font-semibold mb-4 flex items-center gap-2"><TrendingUp size={18} className="text-indigo-400" /> Recommendations</h3>
          {data?.recommendations?.map((r,i) => (
            <div key={i} className="flex items-start gap-2 py-2 border-b border-white/5 last:border-0">
              <div className="w-1.5 h-1.5 rounded-full bg-indigo-400 mt-2 flex-shrink-0" />
              <span className="text-slate-300 text-sm">{r}</span>
            </div>
          ))}
          <button onClick={() => navigate('/learn')} className="btn-primary w-full mt-4 flex items-center justify-center gap-2 text-sm py-2.5">
            Continue Learning <ArrowRight size={16} />
          </button>
        </motion.div>
      </div>
    </div>
  )
}
