import { useState, useRef, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { MessageCircle, X, Send, Bot, User, BookOpen, HelpCircle, RefreshCw, Zap } from 'lucide-react'
import { useApp } from '../context/AppContext'
import { sendChat } from '../api/client'
import clsx from 'clsx'

const QUICK = [
  { label:'Explain simply', msg:'Explain this concept in simple terms' },
  { label:'Practice question', msg:'Give me a practice question on this topic' },
  { label:'Why wrong?', msg:'Why was my last answer wrong?' },
  { label:'Revise weak areas', msg:'Help me revise my weak topics' },
]

export default function ChatBot() {
  const { userId, currentTopic } = useApp()
  const [open, setOpen] = useState(false)
  const [messages, setMessages] = useState([
    { role:'assistant', content:`Hi! I'm your AI tutor. Ask me anything about ${currentTopic || 'AI & ML'}!` }
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [mode, setMode] = useState('tutor')
  const bottomRef = useRef(null)

  useEffect(() => { bottomRef.current?.scrollIntoView({ behavior:'smooth' }) }, [messages])

  const send = async (text) => {
    const msg = (text || input).trim()
    if (!msg || loading) return
    setInput('')
    setMessages(prev => [...prev, { role:'user', content:msg }])
    setLoading(true)
    try {
      const res = await sendChat(userId, msg, currentTopic, mode)
      const d = res.data
      setMessages(prev => [...prev, { role:'assistant', content:d.response, actions:d.actions }])
    } catch {
      setMessages(prev => [...prev, { role:'assistant', content:"I'm having trouble connecting. Make sure the backend is running on port 8000." }])
    } finally { setLoading(false) }
  }

  return (
    <>
      <motion.button onClick={() => setOpen(true)} whileHover={{ scale:1.1 }} whileTap={{ scale:0.95 }}
        className={clsx('fixed bottom-6 right-6 z-50 w-14 h-14 rounded-2xl bg-gradient-to-br from-indigo-600 to-violet-600 flex items-center justify-center shadow-2xl shadow-indigo-500/40 transition-all', open && 'opacity-0 pointer-events-none')}>
        <MessageCircle size={24} className="text-white" />
        <span className="absolute -top-1 -right-1 w-4 h-4 bg-emerald-400 rounded-full border-2 border-[#0a0a1a]" />
      </motion.button>

      <AnimatePresence>
        {open && (
          <motion.div initial={{ opacity:0, y:20, scale:0.95 }} animate={{ opacity:1, y:0, scale:1 }} exit={{ opacity:0, y:20, scale:0.95 }}
            transition={{ type:'spring', damping:25, stiffness:300 }}
            className="fixed bottom-6 right-6 z-50 w-96 h-[600px] glass-strong rounded-3xl flex flex-col overflow-hidden shadow-2xl shadow-black/50 border border-white/10">

            {/* Header */}
            <div className="flex items-center justify-between p-4 border-b border-white/10 bg-gradient-to-r from-indigo-600/20 to-violet-600/20">
              <div className="flex items-center gap-3">
                <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-indigo-500 to-violet-600 flex items-center justify-center">
                  <Bot size={18} className="text-white" />
                </div>
                <div>
                  <div className="text-white font-semibold text-sm">AI Tutor</div>
                  <div className="text-emerald-400 text-xs flex items-center gap-1">
                    <span className="w-1.5 h-1.5 bg-emerald-400 rounded-full" /> Online · {currentTopic}
                  </div>
                </div>
              </div>
              <div className="flex items-center gap-1">
                {['tutor','quiz','revision'].map(m => (
                  <button key={m} onClick={() => setMode(m)}
                    className={clsx('px-2 py-1 rounded-lg text-xs font-medium transition-all capitalize', mode===m ? 'bg-indigo-600/40 text-indigo-300' : 'text-slate-500 hover:text-slate-300')}>
                    {m}
                  </button>
                ))}
                <button onClick={() => setOpen(false)} className="text-slate-400 hover:text-white ml-1 transition-colors"><X size={18} /></button>
              </div>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-3">
              {messages.map((msg, i) => (
                <motion.div key={i} initial={{ opacity:0, y:10 }} animate={{ opacity:1, y:0 }}
                  className={clsx('flex gap-2', msg.role==='user' ? 'flex-row-reverse' : 'flex-row')}>
                  <div className={clsx('w-7 h-7 rounded-xl flex items-center justify-center flex-shrink-0 mt-0.5', msg.role==='user' ? 'bg-indigo-600/30' : 'bg-violet-600/30')}>
                    {msg.role==='user' ? <User size={13} className="text-indigo-300" /> : <Bot size={13} className="text-violet-300" />}
                  </div>
                  <div className={clsx('max-w-[75%] px-3 py-2.5 rounded-2xl text-sm leading-relaxed', msg.role==='user' ? 'bg-indigo-600/25 text-indigo-100 rounded-tr-sm' : 'glass text-slate-200 rounded-tl-sm')}>
                    {msg.content}
                    {msg.actions?.map((a,j) => a.type==='question' && (
                      <div key={j} className="mt-2 p-2 bg-white/5 rounded-xl border border-white/10 text-xs">
                        <div className="font-medium text-white mb-1">{a.data.question}</div>
                        {a.data.options?.map((o,k) => <div key={k} className="text-slate-400 py-0.5">{['A','B','C','D'][k]}. {o}</div>)}
                      </div>
                    ))}
                  </div>
                </motion.div>
              ))}
              {loading && (
                <motion.div initial={{ opacity:0 }} animate={{ opacity:1 }} className="flex gap-2">
                  <div className="w-7 h-7 rounded-xl bg-violet-600/30 flex items-center justify-center flex-shrink-0">
                    <Bot size={13} className="text-violet-300" />
                  </div>
                  <div className="glass px-4 py-3 rounded-2xl rounded-tl-sm">
                    <div className="flex gap-1">
                      {[0,1,2].map(i => <div key={i} className="w-1.5 h-1.5 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay:`${i*0.15}s` }} />)}
                    </div>
                  </div>
                </motion.div>
              )}
              <div ref={bottomRef} />
            </div>

            {/* Quick actions */}
            <div className="px-4 pb-2 flex gap-2 overflow-x-auto">
              {QUICK.map((a,i) => (
                <button key={i} onClick={() => send(a.msg)}
                  className="flex items-center gap-1.5 px-3 py-1.5 glass rounded-xl text-xs text-slate-400 hover:text-white hover:bg-white/10 transition-all whitespace-nowrap flex-shrink-0">
                  {a.label}
                </button>
              ))}
            </div>

            {/* Input */}
            <div className="p-4 pt-2 border-t border-white/5">
              <div className="flex gap-2">
                <input value={input} onChange={e => setInput(e.target.value)} onKeyDown={e => e.key==='Enter' && send()}
                  placeholder="Ask your AI tutor..." className="input-field text-sm py-2.5 flex-1" />
                <button onClick={() => send()} disabled={!input.trim() || loading}
                  className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-600 to-violet-600 flex items-center justify-center disabled:opacity-40 transition-all hover:scale-105 active:scale-95 flex-shrink-0">
                  <Send size={15} className="text-white" />
                </button>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  )
}
