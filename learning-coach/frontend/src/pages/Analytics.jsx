import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, Legend } from 'recharts'
import { TrendingUp, Target, Zap, Award, BookOpen, Brain } from 'lucide-react'
import { useApp } from '../context/AppContext'
import { getAnalytics } from '../api/client'

const COLORS = ['#6366f1','#a78bfa','#38bdf8','#34d399','#fb923c','#f472b6','#fbbf24']

const Tip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null
  return (
    <div className="glass rounded-xl p-3 text-sm border border-white/10">
      <p className="text-slate-300 mb-1">{label}</p>
      {payload.map((p,i) => <p key={i} style={{ color:p.color }}>{p.name}: {p.value}{p.name==='accuracy'?'%':''}</p>)}
    </div>
  )
}

export default function Analytics() {
  const { userId } = useApp()
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    getAnalytics(userId)
      .then(r => setData(r.data))
      .catch(() => setData({ overall_mastery:0, engagement_score:0, streak:0, xp:0, level:1, total_questions:0, total_correct:0, weak_topics:[], strong_topics:[], topic_performance:[], recommendations:[] }))
      .finally(() => setLoading(false))
  }, [userId])

  if (loading) return (
    <div className="pt-24 flex items-center justify-center min-h-screen">
      <div className="w-12 h-12 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin" />
    </div>
  )

  const topicPerf = data?.topic_performance || []
  const pieData = topicPerf.slice(0,6).map((t,i) => ({ name:t.topic, value:t.attempts, fill:COLORS[i] }))
  const accuracy = data?.total_questions > 0 ? Math.round((data.total_correct/data.total_questions)*100) : 0

  return (
    <div className="pt-24 pb-12 px-6 max-w-7xl mx-auto">
      <motion.div initial={{ opacity:0, y:20 }} animate={{ opacity:1, y:0 }} className="mb-8">
        <h1 className="text-3xl font-bold text-white mb-1">Analytics</h1>
        <p className="text-slate-400">Deep insights into your learning performance.</p>
      </motion.div>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-8">
        {[
          { label:'Mastery', value:`${data?.overall_mastery||0}%`, icon:Brain, color:'text-indigo-400' },
          { label:'Engagement', value:`${data?.engagement_score||0}%`, icon:Zap, color:'text-violet-400' },
          { label:'Accuracy', value:`${accuracy}%`, icon:Target, color:'text-emerald-400' },
          { label:'Questions', value:data?.total_questions||0, icon:BookOpen, color:'text-blue-400' },
          { label:'Streak', value:data?.streak||0, icon:TrendingUp, color:'text-orange-400' },
          { label:'Level', value:data?.level||1, icon:Award, color:'text-amber-400' },
        ].map((s,i) => (
          <motion.div key={i} initial={{ opacity:0, scale:0.9 }} animate={{ opacity:1, scale:1 }} transition={{ delay:i*0.05 }} className="card text-center">
            <s.icon size={20} className={`${s.color} mx-auto mb-2`} />
            <div className="text-xl font-bold text-white">{s.value}</div>
            <div className="text-xs text-slate-500 mt-0.5">{s.label}</div>
          </motion.div>
        ))}
      </div>

      <div className="grid md:grid-cols-2 gap-6 mb-6">
        <motion.div initial={{ opacity:0, x:-20 }} animate={{ opacity:1, x:0 }} transition={{ delay:0.2 }} className="card">
          <h3 className="text-white font-semibold mb-4 flex items-center gap-2"><Target size={18} className="text-indigo-400" /> Topic Accuracy</h3>
          {topicPerf.length > 0 ? (
            <div className="h-56">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={topicPerf.slice(0,8)} margin={{ left:-20 }}>
                  <XAxis dataKey="topic" tick={{ fill:'#64748b', fontSize:10 }} />
                  <YAxis tick={{ fill:'#64748b', fontSize:10 }} domain={[0,100]} />
                  <Tooltip content={<Tip />} />
                  <Bar dataKey="accuracy" name="accuracy" radius={[6,6,0,0]}>
                    {topicPerf.slice(0,8).map((_,i) => <Cell key={i} fill={COLORS[i%COLORS.length]} />)}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          ) : <div className="h-56 flex items-center justify-center text-slate-500 text-sm">No data yet — start answering questions!</div>}
        </motion.div>

        <motion.div initial={{ opacity:0, x:20 }} animate={{ opacity:1, x:0 }} transition={{ delay:0.3 }} className="card">
          <h3 className="text-white font-semibold mb-4 flex items-center gap-2"><BookOpen size={18} className="text-violet-400" /> Topic Distribution</h3>
          {pieData.length > 0 ? (
            <div className="h-56">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie data={pieData} cx="50%" cy="50%" innerRadius={50} outerRadius={90} paddingAngle={3} dataKey="value">
                    {pieData.map((e,i) => <Cell key={i} fill={e.fill} />)}
                  </Pie>
                  <Legend formatter={v => <span style={{ color:'#94a3b8', fontSize:11 }}>{v}</span>} />
                  <Tooltip content={<Tip />} />
                </PieChart>
              </ResponsiveContainer>
            </div>
          ) : <div className="h-56 flex items-center justify-center text-slate-500 text-sm">No data yet</div>}
        </motion.div>
      </div>

      <motion.div initial={{ opacity:0, y:20 }} animate={{ opacity:1, y:0 }} transition={{ delay:0.4 }} className="card">
        <h3 className="text-white font-semibold mb-4 flex items-center gap-2"><TrendingUp size={18} className="text-emerald-400" /> Detailed Topic Performance</h3>
        {topicPerf.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-slate-500 border-b border-white/5">
                  <th className="text-left py-2 pr-4">Topic</th>
                  <th className="text-right py-2 pr-4">Attempts</th>
                  <th className="text-right py-2 pr-4">Correct</th>
                  <th className="text-right py-2 pr-4">Accuracy</th>
                  <th className="text-right py-2">Status</th>
                </tr>
              </thead>
              <tbody>
                {topicPerf.map((t,i) => (
                  <tr key={i} className="border-b border-white/5 last:border-0">
                    <td className="py-3 pr-4 text-slate-300 font-medium">{t.topic}</td>
                    <td className="py-3 pr-4 text-right text-slate-400">{t.attempts}</td>
                    <td className="py-3 pr-4 text-right text-slate-400">{t.correct}</td>
                    <td className="py-3 pr-4 text-right font-semibold" style={{ color: t.accuracy>=80?'#34d399':t.accuracy<50?'#f87171':'#fbbf24' }}>{t.accuracy}%</td>
                    <td className="py-3 text-right">
                      <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${t.status==='strong'?'bg-emerald-500/15 text-emerald-400':t.status==='weak'?'bg-rose-500/15 text-rose-400':'bg-amber-500/15 text-amber-400'}`}>
                        {t.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : <p className="text-slate-500 text-sm text-center py-8">Answer questions to see detailed performance data.</p>}
      </motion.div>
    </div>
  )
}
