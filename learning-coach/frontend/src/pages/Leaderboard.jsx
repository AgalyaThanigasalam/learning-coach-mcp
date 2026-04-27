import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { Trophy, Medal, Star, Zap, Target, TrendingUp, RefreshCw } from 'lucide-react'
import { useApp } from '../context/AppContext'
import axios from 'axios'

const api = axios.create({ baseURL: 'http://localhost:8000' })

export default function Leaderboard() {
  const { userId } = useApp()
  const [board, setBoard] = useState([])
  const [myRank, setMyRank] = useState(null)
  const [loading, setLoading] = useState(true)

  const fetchData = async () => {
    setLoading(true)
    try {
      const [lb, me] = await Promise.all([
        api.get('/api/leaderboard?limit=20'),
        api.get(`/api/leaderboard/user/${userId}`)
      ])
      setBoard(lb.data.leaderboard || [])
      setMyRank(me.data)
    } catch {
      setBoard([])
    } finally { setLoading(false) }
  }

  useEffect(() => { fetchData() }, [userId])

  const topThree = board.slice(0, 3)
  const rest = board.slice(3)

  return (
    <div className="pt-24 pb-12 px-6 max-w-4xl mx-auto">
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="mb-8 flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white mb-1 flex items-center gap-3">
            <Trophy size={32} className="text-amber-400" /> Leaderboard
          </h1>
          <p className="text-slate-400">Ranked by mastery, accuracy, streak and difficulty.</p>
        </div>
        <button onClick={fetchData} className="btn-ghost flex items-center gap-2 text-sm py-2 px-4">
          <RefreshCw size={15} className={loading ? 'animate-spin' : ''} /> Refresh
        </button>
      </motion.div>

      {/* My rank card */}
      {myRank && myRank.total_questions > 0 && (
        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
          className="card border border-indigo-500/30 bg-indigo-500/5 mb-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="text-3xl font-extrabold text-indigo-400">{myRank.rank_badge}</div>
              <div>
                <div className="text-white font-semibold">You</div>
                <div className="text-slate-400 text-sm">{myRank.badge}</div>
              </div>
            </div>
            <div className="flex items-center gap-6 text-sm">
              <div className="text-center"><div className="text-white font-bold text-lg">{myRank.score}</div><div className="text-slate-500">Score</div></div>
              <div className="text-center"><div className="text-emerald-400 font-bold text-lg">{myRank.mastery}%</div><div className="text-slate-500">Mastery</div></div>
              <div className="text-center"><div className="text-amber-400 font-bold text-lg">{myRank.streak}🔥</div><div className="text-slate-500">Streak</div></div>
            </div>
          </div>
        </motion.div>
      )}

      {loading ? (
        <div className="flex items-center justify-center h-48">
          <div className="w-10 h-10 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin" />
        </div>
      ) : board.length === 0 ? (
        <div className="card text-center py-16">
          <Trophy size={48} className="text-slate-600 mx-auto mb-4" />
          <p className="text-slate-400 text-lg">No rankings yet.</p>
          <p className="text-slate-500 text-sm mt-2">Answer questions to appear on the leaderboard!</p>
        </div>
      ) : (
        <>
          {/* Top 3 podium */}
          {topThree.length > 0 && (
            <div className="grid grid-cols-3 gap-4 mb-6">
              {[topThree[1], topThree[0], topThree[2]].filter(Boolean).map((entry, i) => {
                const isFirst = entry.rank === 1
                const colors = { 1: 'from-amber-500 to-yellow-400', 2: 'from-slate-400 to-slate-300', 3: 'from-orange-600 to-amber-500' }
                return (
                  <motion.div key={entry.user_id} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.1 }}
                    className={`card text-center ${isFirst ? 'border border-amber-500/30 bg-amber-500/5' : ''}`}>
                    <div className={`w-12 h-12 rounded-full bg-gradient-to-br ${colors[entry.rank]} flex items-center justify-center mx-auto mb-3 text-white font-bold text-lg`}>
                      {entry.rank === 1 ? '🥇' : entry.rank === 2 ? '🥈' : '🥉'}
                    </div>
                    <div className="text-white font-semibold text-sm truncate">{entry.username}</div>
                    <div className="text-2xl font-extrabold gradient-text mt-1">{entry.score}</div>
                    <div className="text-xs text-slate-400 mt-1">{entry.badge}</div>
                    <div className="flex justify-center gap-3 mt-2 text-xs text-slate-500">
                      <span>{entry.mastery}% mastery</span>
                      <span>{entry.streak}🔥</span>
                    </div>
                  </motion.div>
                )
              })}
            </div>
          )}

          {/* Rest of leaderboard */}
          {rest.length > 0 && (
            <div className="card">
              <table className="w-full text-sm">
                <thead>
                  <tr className="text-slate-500 border-b border-white/5">
                    <th className="text-left py-2 pr-4">Rank</th>
                    <th className="text-left py-2 pr-4">User</th>
                    <th className="text-right py-2 pr-4">Score</th>
                    <th className="text-right py-2 pr-4">Mastery</th>
                    <th className="text-right py-2 pr-4">Accuracy</th>
                    <th className="text-right py-2">Badge</th>
                  </tr>
                </thead>
                <tbody>
                  {rest.map((entry, i) => (
                    <motion.tr key={entry.user_id} initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: i * 0.05 }}
                      className={`border-b border-white/5 last:border-0 ${entry.user_id === userId ? 'bg-indigo-500/5' : ''}`}>
                      <td className="py-3 pr-4 text-slate-400 font-mono">{entry.rank_badge}</td>
                      <td className="py-3 pr-4 text-slate-300 font-medium">{entry.username}{entry.user_id === userId ? ' (You)' : ''}</td>
                      <td className="py-3 pr-4 text-right font-bold text-white">{entry.score}</td>
                      <td className="py-3 pr-4 text-right text-emerald-400">{entry.mastery}%</td>
                      <td className="py-3 pr-4 text-right text-blue-400">{entry.accuracy}%</td>
                      <td className="py-3 text-right text-xs">{entry.badge}</td>
                    </motion.tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </>
      )}

      {/* Score formula */}
      <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.5 }}
        className="mt-6 card border border-white/5">
        <h3 className="text-slate-400 text-xs font-semibold mb-2 uppercase tracking-wider">Score Formula</h3>
        <p className="text-slate-500 text-xs font-mono">
          Score = (0.4 × Mastery%) + (0.3 × Accuracy%) + (0.2 × Streak) + (0.1 × Avg Difficulty)
        </p>
      </motion.div>
    </div>
  )
}
