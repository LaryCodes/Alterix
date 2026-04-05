'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { api } from '@/lib/api'
import { auth } from '@/lib/auth'
import { useRouter } from 'next/navigation'
import DashboardLayout from '@/components/layout/DashboardLayout'
import EmptyState from '@/components/ui/EmptyState'
import Button from '@/components/ui/Button'
import GlassCard from '@/components/ui/GlassCard'
import ExplainabilityDrawer from '@/components/ExplainabilityDrawer'
import { Activity } from 'lucide-react'

export default function MatchesPage() {
  const router = useRouter()
  const [matches, setMatches] = useState<any[]>([])
  const [loading, setLoading] = useState(false)
  const [requestedSkills, setRequestedSkills] = useState<any[]>([])
  const [selectedSkill, setSelectedSkill] = useState<any>(null)
  const [error, setError] = useState('')
  const [traceId, setTraceId] = useState<string | null>(null)
  const [isDrawerOpen, setIsDrawerOpen] = useState(false)

  useEffect(() => {
    if (!auth.isAuthenticated()) {
      router.push('/login')
      return
    }

    // Load user's requested skills so they can choose which to match
    const loadSkills = async () => {
      try {
        const userData = auth.getUser()
        const res = await api.getUserRequestedSkills(userData.id)
        if (res.success && res.skills.length > 0) {
          setRequestedSkills(res.skills)
          setSelectedSkill(res.skills[0])
        }
      } catch (err) {
        console.error('Failed to load requested skills:', err)
      }
    }
    loadSkills()
  }, [router])

  const findMatches = async () => {
    if (!selectedSkill) {
      setError('Please add a requested skill first from the Skills page')
      return
    }

    setLoading(true)
    setError('')
    try {
      const userData = auth.getUser()
      const skill = selectedSkill.skills || selectedSkill
      const response = await api.findMatches(userData.id, {
        name: skill.name,
        category: skill.category,
        level: selectedSkill.desired_level || skill.level,
        estimated_hours: skill.estimated_hours || 10
      })
      
      const directMatches = response.data?.direct_matches || []
      setMatches(directMatches)
      if (response.data?.trace_id) {
        setTraceId(response.data.trace_id)
      }
      
      if (directMatches.length === 0) {
        setError('No matches found yet. As more users join and add skills, matches will appear!')
      }
    } catch (err: any) {
      setError(err.message || 'Failed to find matches')
      console.error('Failed to find matches:', err)
    } finally {
      setLoading(false)
    }
  }

  const initiateExchange = async (match: any) => {
    try {
      const userData = auth.getUser()
      // Get user's first offered skill for the exchange
      const offeredRes = await api.getUserOfferedSkills(userData.id)
      if (!offeredRes.success || offeredRes.skills.length === 0) {
        setError('You need to add an offered skill before you can exchange')
        return
      }

      const offeredSkill = offeredRes.skills[0]
      const skill = selectedSkill.skills || selectedSkill

      await api.createExchange({
        type: 'DIRECT_SWAP',
        partner_id: match.user_id,
        offered_skill_id: offeredSkill.skill_id,
        requested_skill_id: skill.id || selectedSkill.skill_id
      })

      router.push('/exchanges')
    } catch (err: any) {
      setError(err.message || 'Failed to create exchange')
    }
  }

  return (
    <DashboardLayout>
      <div className="flex items-center justify-between mb-8">
        <div>
          <h2 className="text-3xl font-bold bg-gradient-to-r from-pink-400 to-brown-400 bg-clip-text text-transparent mb-2">AI-Powered Matches</h2>
          <div className="flex items-center gap-4">
            <p className="text-brown-600">Find the perfect skill exchange partners using AI</p>
            {traceId && (
              <button 
                onClick={() => setIsDrawerOpen(true)}
                className="flex items-center gap-1 text-sm text-cyan-600 hover:text-cyan-700 bg-cyan-50 px-3 py-1 rounded-full transition"
              >
                <Activity className="w-4 h-4" /> View AI Reasoning Pipeline
              </button>
            )}
          </div>
        </div>
        <div className="flex items-center gap-4">
          {requestedSkills.length > 0 && (
            <select
              value={selectedSkill ? JSON.stringify(selectedSkill) : ''}
              onChange={(e) => setSelectedSkill(JSON.parse(e.target.value))}
              className="px-4 py-3 glass rounded-2xl border-2 border-white/40 focus:border-pink-400 text-brown-900 font-medium"
            >
              {requestedSkills.map((s: any) => (
                <option key={s.id} value={JSON.stringify(s)}>
                  {s.skills?.name || 'Unknown'} ({s.desired_level})
                </option>
              ))}
            </select>
          )}
          <Button
            onClick={findMatches}
            disabled={loading}
            variant="primary"
            size="lg"
          >
            {loading ? (
              <span className="flex items-center gap-2">
                <motion.span
                  animate={{ rotate: 360 }}
                  transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                  className="inline-block w-5 h-5 border-2 border-white border-t-transparent rounded-full"
                />
                Finding...
              </span>
            ) : (
              '🤖 Find Matches'
            )}
          </Button>
        </div>
      </div>

      {error && (
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-6 p-4 glass rounded-2xl border-2 border-pink-300"
        >
          <div className="flex items-center gap-2 text-pink-700">
            <span className="text-xl">💡</span>
            <span>{error}</span>
          </div>
        </motion.div>
      )}

      <div className="space-y-6">
        {matches.length === 0 && !error ? (
          <EmptyState
            icon="🔍"
            title="No matches yet"
            description={requestedSkills.length === 0
              ? "Add skills you want to learn on the Skills page first, then come back to find matches!"
              : "Select a skill and click 'Find Matches' to discover partners!"
            }
          />
        ) : (
          matches.map((match: any, index: number) => (
            <motion.div
              key={match.user_id || index}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
            >
              <GlassCard className="p-6">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-4 mb-4">
                      <div className="w-16 h-16 bg-gradient-to-br from-pink-400 to-brown-400 rounded-full flex items-center justify-center text-white text-2xl font-bold shadow-glass">
                        {(match.name || match.user_id || 'U').charAt(0).toUpperCase()}
                      </div>
                      <div>
                        <h3 className="text-2xl font-bold text-brown-900">{match.name || 'Skill Partner'}</h3>
                        <p className="text-brown-600">
                          {match.match_type === 'direct' ? '✅ Direct Match' : '🔄 Potential Match'}
                        </p>
                      </div>
                    </div>

                    {match.offered_skills && match.offered_skills.length > 0 && (
                      <div className="mb-4">
                        <div className="text-sm text-brown-600 mb-2">Skills they offer:</div>
                        <div className="flex flex-wrap gap-2">
                          {match.offered_skills.map((s: any, i: number) => (
                            <span key={i} className="px-3 py-1 glass rounded-full text-sm font-medium text-pink-700">
                              {s.name} • {s.level}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}

                    <div className="grid md:grid-cols-3 gap-4 mb-4">
                      <div className="glass rounded-2xl p-4">
                        <div className="text-sm text-brown-600 mb-1">Match Score</div>
                        <div className="text-2xl font-bold text-pink-600">{Math.round((match.score || 0) * 100)}%</div>
                      </div>
                      <div className="glass rounded-2xl p-4">
                        <div className="text-sm text-brown-600 mb-1">Trust Score</div>
                        <div className="text-2xl font-bold text-brown-600">{Math.round(match.trust_score || 50)}</div>
                      </div>
                      {match.fairness && (
                        <div className="glass rounded-2xl p-4">
                          <div className="text-sm text-brown-600 mb-1">Fairness</div>
                          <div className={`text-2xl font-bold ${match.fairness.is_fair ? 'text-green-600' : 'text-orange-600'}`}>
                            {match.fairness.is_fair ? '✅ Fair' : '⚠️ Review'}
                          </div>
                        </div>
                      )}
                    </div>

                    {match.ai_insight && (
                      <div className="glass rounded-2xl p-4 mb-4 border-l-4 border-pink-400">
                        <div className="text-sm text-brown-600 mb-1">🤖 AI Insight</div>
                        <div className="text-brown-800">{match.ai_insight}</div>
                      </div>
                    )}

                    <div className="flex gap-3">
                      <Button variant="primary" size="md" className="flex-1" onClick={() => initiateExchange(match)}>
                        🤝 Start Exchange
                      </Button>
                    </div>
                  </div>
                </div>
              </GlassCard>
            </motion.div>
          ))
        )}
      </div>

      <ExplainabilityDrawer
        isOpen={isDrawerOpen}
        onClose={() => setIsDrawerOpen(false)}
        exchangeId={traceId}
      />
    </DashboardLayout>
  )
}
