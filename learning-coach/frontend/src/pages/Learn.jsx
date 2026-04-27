import { useState, useEffect, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Brain, CheckCircle, XCircle, Zap, ChevronRight, RefreshCw, BookOpen, Lightbulb, MessageCircle, Hash, RotateCcw, AlertTriangle } from 'lucide-react'
import { useApp } from '../context/AppContext'
import { generateQuestion, submitAnswer, getTopics, sendChat } from '../api/client'
import axios from 'axios'
import clsx from 'clsx'

const api = axios.create({ baseURL: 'http://localhost:8000' })

const DIFF_COLORS = { 1:'text-emerald-400', 2:'text-green-400', 3:'text-yellow-400', 4:'text-orange-400', 5:'text-red-400' }
const DIFF_LABELS = { 1:'Easy', 2:'Beginner', 3:'Intermediate', 4:'Hard', 5:'Advanced' }
const DIFF_BG = { 1:'bg-emerald-500/15 border-emerald-500/30', 2:'bg-green-500/15 border-green-500/30', 3:'bg-yellow-500/15 border-yellow-500/30', 4:'bg-orange-500/15 border-orange-500/30', 5:'bg-red-500/15 border-red-500/30' }

export default function Learn() {
  const { userId, currentTopic, setCurrentTopic } = useApp()
  const [topics, setTopics] = useState([])
  const [question, setQuestion] = useState(null)
  const [diffInfo, setDiffInfo] = useState(null)
  const [qNum, setQNum] = useState(1)
  const [selected, setSelected] = useState(null)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [submitting, setSubmitting] = useState(false)
  const [explanation, setExplanation] = useState(null)
  const [xpGained, setXpGained] = useState(0)
  const [showAskAI, setShowAskAI] = useState(false)
  const [aiAnswer, setAiAnswer] = useState(null)
  const [aiLoading, setAiLoading] = useState(false)
  const [revisionMode, setRevisionMode] = useState(false)
  const [revisionInfo, setRevisionInfo] = useState(null)
  const startTime = useRef(Date.now())

  useEffect(() => { getTopics().then(r => setTopics(r.data.topics || [])).catch(() => {}) }, [])
  useEffect(() => { if (currentTopic) fetchQuestion() }, [currentTopic])

  const fetchQuestion = async () => {
    setLoading(true); setSelected(null); setResult(null); setExplanation(null); setXpGained(0); setAiAnswer(null); setShowAskAI(false)
    startTime.current = Date.now()
    try {
      if (revisionMode) {
        const res = await api.get(`/api/revision-mode/${userId}`)
        setQuestion(res.data.question)
        setDiffInfo(res.data.difficulty_info)
        setRevisionInfo(res.data)
        if (res.data.revision_topic) setCurrentTopic(res.data.revision_topic)
      } else {
        const res = await generateQuestion(userId, currentTopic)
        setQuestion(res.data.question)
        setDiffInfo(res.data.difficulty_info)
        setRevisionInfo(null)
      }
    } catch {
      setQuestion({ question: 'What is supervised learning?', options: ['Learning with labels','Learning without labels','Reinforcement','Clustering'], correct_answer: 'Learning with labels', explanation: 'Supervised learning uses labeled training data.', difficulty: 2, topic: currentTopic })
      setDiffInfo({ level: 2, label: 'Beginner' })
    } finally { setLoading(false) }
  }

  const handleAnswer = async (option) => {
    if (selected || submitting) return
    setSelected(option)
    setSubmitting(true)
    const responseTime = (Date.now() - startTime.current) / 1000
    try {
      const res = await submitAnswer({ user_id: userId, topic: currentTopic, question: question.question, user_answer: option, correct_answer: question.correct_answer, difficulty: question.difficulty || 2, response_time: responseTime })
      setResult(res.data)
      if (res.data.explanation) setExplanation(res.data.explanation)
      if (res.data.xp_gained) setXpGained(res.data.xp_gained)
    } catch { setResult({ is_correct: option === question.correct_answer, correct_answer: question.correct_answer }) }
    finally { setSubmitting(false) }
  }

  const handleExplain = async () => {
    setAiLoading(true); setShowAskAI(true)
    try {
      // Send the actual question text so AI explains the specific concept
      const msg = `Explain this concept clearly: "${question?.question}" — The correct answer is "${question?.correct_answer}". Explain why this is correct.`
      const res = await sendChat(userId, msg, currentTopic, 'tutor')
      setAiAnswer(res.data.response)
    } catch { setAiAnswer('Unable to connect to AI. Make sure the backend is running.') }
    finally { setAiLoading(false) }
  }

  const handleAskAI = async () => {
    setAiLoading(true); setShowAskAI(true)
    try {
      const msg = `For the question "${question?.question}" — I answered "${selected}" but the correct answer is "${question?.correct_answer}". Why is my answer wrong and what is the correct explanation?`
      const res = await sendChat(userId, msg, currentTopic, 'tutor')
      setAiAnswer(res.data.response)
    } catch { setAiAnswer('Unable to connect to AI. Make sure the backend is running.') }
    finally { setAiLoading(false) }
  }

  const topicList = topics.length > 0 ? topics : [
    {name:'Machine Learning'},{name:'Deep Learning'},{name:'Neural Networks'},{name:'NLP'},{name:'Computer Vision'},{name:'Reinforcement Learning'},{name:'Data Science'},{name:'Python'},{name:'Algorithms'},{name:'Data Structures'}
  ]

  return (
    <div className="pt-24 pb-12 px-6 max-w-6xl mx-auto">
      <div className="grid lg:grid-cols-4 gap-6">
        {/* Topic sidebar */}
        <div className="lg:col-span-1">
          <div className="card sticky top-28">
            <h3 className="text-white font-semibold mb-4 flex items-center gap-2 text-sm"><BookOpen size={16} className="text-indigo-400" /> Topics</h3>
            <div className="space-y-1 max-h-[60vh] overflow-y-auto pr-1">
              {topicList.map((t) => (
                <button key={t.name} onClick={() => { setCurrentTopic(t.name); setQNum(1) }}
                  className={clsx('w-full text-left px-3 py-2 rounded-xl text-sm transition-all duration-200',
                    currentTopic === t.name ? 'bg-indigo-600/20 text-indigo-300 border border-indigo-500/20' : 'text-slate-400 hover:text-white hover:bg-white/5')}>
                  {t.name}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Main area */}
        <div className="lg:col-span-3 space-y-5">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-white">{revisionMode ? '🔄 Revision Mode' : currentTopic}</h1>
              <div className="flex items-center gap-3 mt-1">
                {diffInfo && (
                  <span className={clsx('text-xs font-semibold px-2.5 py-1 rounded-full border', DIFF_BG[diffInfo.level] || 'bg-slate-500/15 border-slate-500/30', DIFF_COLORS[diffInfo.level])}>
                    {DIFF_LABELS[diffInfo.level] || diffInfo.label}
                  </span>
                )}
                {revisionMode && revisionInfo?.revision_topic && (
                  <span className="text-xs px-2.5 py-1 rounded-full bg-rose-500/15 border border-rose-500/30 text-rose-400 flex items-center gap-1">
                    <AlertTriangle size={11} /> Weak: {revisionInfo.revision_topic}
                  </span>
                )}
                <span className="flex items-center gap-1 text-slate-500 text-xs"><Hash size={12} />Question {qNum}</span>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <button onClick={() => { setRevisionMode(r => !r); setQNum(1) }}
                className={clsx('flex items-center gap-2 text-sm py-2 px-4 rounded-xl border transition-all', revisionMode ? 'bg-rose-500/20 border-rose-500/30 text-rose-300' : 'glass border-white/10 text-slate-400 hover:text-white')}>
                <RotateCcw size={14} /> {revisionMode ? 'Exit Revision' : 'Revision Mode'}
              </button>
              <button onClick={() => { fetchQuestion(); setQNum(n => n + 1) }} disabled={loading}
                className="btn-ghost flex items-center gap-2 text-sm py-2 px-4">
                <RefreshCw size={15} className={loading ? 'animate-spin' : ''} /> New Question
              </button>
            </div>
          </div>

          {/* Question card */}
          <AnimatePresence mode="wait">
            {loading ? (
              <motion.div key="loading" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
                className="card flex items-center justify-center h-64">
                <div className="text-center">
                  <div className="w-10 h-10 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin mx-auto mb-3" />
                  <p className="text-slate-400 text-sm">AI generating question...</p>
                </div>
              </motion.div>
            ) : question ? (
              <motion.div key={question.question} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -20 }}
                className="card">
                <div className="flex items-start gap-3 mb-6">
                  <div className="w-8 h-8 rounded-xl bg-indigo-600/20 flex items-center justify-center flex-shrink-0 mt-0.5">
                    <Brain size={16} className="text-indigo-400" />
                  </div>
                  <p className="text-white text-lg font-medium leading-relaxed">{question.question}</p>
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  {question.options?.map((opt, i) => {
                    const isSelected = selected === opt
                    const isCorrect = result?.correct_answer === opt
                    const isWrong = isSelected && !result?.is_correct
                    return (
                      <motion.button key={i} onClick={() => handleAnswer(opt)} disabled={!!selected}
                        whileHover={!selected ? { scale: 1.02 } : {}} whileTap={!selected ? { scale: 0.98 } : {}}
                        className={clsx('p-4 rounded-2xl text-left text-sm font-medium transition-all duration-300 border',
                          !selected ? 'glass border-white/10 text-slate-300 hover:border-indigo-500/40 hover:text-white hover:bg-indigo-500/10' :
                          isCorrect ? 'bg-emerald-500/15 border-emerald-500/40 text-emerald-300' :
                          isWrong ? 'bg-rose-500/15 border-rose-500/40 text-rose-300' :
                          'glass border-white/5 text-slate-500')}>
                        <div className="flex items-center gap-3">
                          <span className="w-6 h-6 rounded-lg bg-white/5 flex items-center justify-center text-xs font-bold flex-shrink-0">
                            {['A','B','C','D'][i]}
                          </span>
                          <span className="flex-1">{opt}</span>
                          {isCorrect && result && <CheckCircle size={16} className="text-emerald-400 flex-shrink-0" />}
                          {isWrong && <XCircle size={16} className="text-rose-400 flex-shrink-0" />}
                        </div>
                      </motion.button>
                    )
                  })}
                </div>
                {/* Explain + Ask AI buttons */}
                {!selected && (
                  <div className="flex gap-3 mt-4">
                    <button onClick={handleExplain} className="btn-ghost flex items-center gap-2 text-xs py-2 px-4">
                      <Lightbulb size={13} /> Explain Concept
                    </button>
                    <button onClick={handleAskAI} className="btn-ghost flex items-center gap-2 text-xs py-2 px-4">
                      <MessageCircle size={13} /> Ask AI
                    </button>
                  </div>
                )}
              </motion.div>
            ) : null}
          </AnimatePresence>

          {/* AI response panel */}
          <AnimatePresence>
            {showAskAI && (
              <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }}
                className="card border border-indigo-500/20 bg-indigo-500/5">
                <div className="flex items-center gap-2 mb-2">
                  <Brain size={16} className="text-indigo-400" />
                  <span className="text-indigo-300 text-sm font-medium">AI Tutor</span>
                </div>
                {aiLoading ? (
                  <div className="flex gap-1 py-2">
                    {[0,1,2].map(i => <div key={i} className="w-2 h-2 bg-indigo-400 rounded-full animate-bounce" style={{ animationDelay: `${i*0.15}s` }} />)}
                  </div>
                ) : <p className="text-slate-300 text-sm leading-relaxed">{aiAnswer}</p>}
              </motion.div>
            )}
          </AnimatePresence>

          {/* Result feedback */}
          <AnimatePresence>
            {result && (
              <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }}
                className={clsx('card border', result.is_correct ? 'border-emerald-500/20 bg-emerald-500/5' : 'border-rose-500/20 bg-rose-500/5')}>
                <div className="flex items-center gap-3 mb-3">
                  {result.is_correct ? <CheckCircle size={22} className="text-emerald-400" /> : <XCircle size={22} className="text-rose-400" />}
                  <span className={clsx('font-semibold text-lg', result.is_correct ? 'text-emerald-300' : 'text-rose-300')}>
                    {result.is_correct ? 'Correct!' : 'Not quite right'}
                  </span>
                  {xpGained > 0 && (
                    <motion.span initial={{ scale: 0 }} animate={{ scale: 1 }} className="ml-auto flex items-center gap-1 text-amber-400 text-sm font-bold">
                      <Zap size={14} /> +{xpGained} XP
                    </motion.span>
                  )}
                </div>
                {explanation && (
                  <div className="flex items-start gap-2 mb-4">
                    <Lightbulb size={16} className="text-amber-400 mt-0.5 flex-shrink-0" />
                    <p className="text-slate-300 text-sm leading-relaxed">{explanation}</p>
                  </div>
                )}
                <div className="flex gap-3">
                  <button onClick={() => { fetchQuestion(); setQNum(n => n + 1) }} className="btn-primary flex items-center gap-2 text-sm py-2.5 px-5">
                    Next Question <ChevronRight size={16} />
                  </button>
                  {!result.is_correct && (
                    <button onClick={handleAskAI} className="btn-ghost flex items-center gap-2 text-sm py-2.5 px-4">
                      <MessageCircle size={15} /> Why wrong?
                    </button>
                  )}
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </div>
  )
}
