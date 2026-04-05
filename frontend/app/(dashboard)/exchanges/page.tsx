'use client'

import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { auth } from '@/lib/auth'
import { api } from '@/lib/api'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import DashboardLayout from '@/components/layout/DashboardLayout'
import LoadingSpinner from '@/components/ui/LoadingSpinner'
import EmptyState from '@/components/ui/EmptyState'
import Button from '@/components/ui/Button'
import GlassCard from '@/components/ui/GlassCard'
import ExplainabilityDrawer from '@/components/ExplainabilityDrawer'
import { Activity } from 'lucide-react'
export default function ExchangesPage() {
  const router = useRouter()
  const [loading, setLoading] = useState(true)
  const [exchanges, setExchanges] = useState<any[]>([])
  const [showRating, setShowRating] = useState<string | null>(null)
  const [rating, setRating] = useState(5)
  const [feedback, setFeedback] = useState('')
  const [ratingLoading, setRatingLoading] = useState(false)
  const [error, setError] = useState('')
  const [explainExchangeId, setExplainExchangeId] = useState<string | null>(null)

  const loadExchanges = async () => {
    const userData = auth.getUser()
    try {
      const res = await api.getUserExchanges(userData.id)
      if (res.success) {
        setExchanges(res.exchanges)
      }
    } catch (error) {
      console.error('Failed to load exchanges:', error)
    }
  }

  useEffect(() => {
    const loadData = async () => {
      if (!auth.isAuthenticated()) {
        router.push('/login')
        return
      }
      await loadExchanges()
      setLoading(false)
    }
    loadData()
  }, [router])

  const updateStatus = async (exchangeId: string, status: string) => {
    try {
      await api.updateExchangeStatus(exchangeId, status)
      await loadExchanges()
    } catch (err: any) {
      setError(err.message || 'Failed to update status')
    }
  }

  const submitRating = async (exchangeId: string, partnerId: string) => {
    setRatingLoading(true)
    try {
      await api.rateExchange(exchangeId, partnerId, rating, feedback)
      setShowRating(null)
      setRating(5)
      setFeedback('')
      await loadExchanges()
    } catch (err: any) {
      setError(err.message || 'Failed to submit rating')
    } finally {
      setRatingLoading(false)
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'IN_PROGRESS': return 'bg-blue-100 text-blue-700 border-blue-200'
      case 'SCHEDULED': return 'bg-yellow-100 text-yellow-700 border-yellow-200'
      case 'PENDING': return 'bg-orange-100 text-orange-700 border-orange-200'
      case 'COMPLETED': return 'bg-green-100 text-green-700 border-green-200'
      case 'CANCELLED': return 'bg-red-100 text-red-700 border-red-200'
      case 'NEGOTIATING': return 'bg-purple-100 text-purple-700 border-purple-200'
      default: return 'bg-gray-100 text-gray-700 border-gray-200'
    }
  }

  if (loading) {
    return <LoadingSpinner fullScreen />
  }

  return (
    <DashboardLayout>
      <div className="mb-8">
        <h2 className="text-3xl font-bold gradient-text mb-2">My Exchanges</h2>
        <p className="text-brown-600">Track and manage your skill exchanges</p>
      </div>

      {error && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="mb-6 p-4 glass rounded-2xl border-2 border-pink-300 text-pink-700"
        >
          {error}
          <button onClick={() => setError('')} className="ml-2 font-bold">✕</button>
        </motion.div>
      )}

      {exchanges.length === 0 ? (
        <EmptyState
          icon="🔄"
          title="No exchanges yet"
          description="Start by finding matches for your skills!"
          action={
            <Link href="/matches">
              <Button variant="primary" size="lg">
                🔍 Find Matches
              </Button>
            </Link>
          }
        />
      ) : (
        <div className="space-y-6">
          {exchanges.map((exchange, index) => {
            const partner = exchange.participants?.[0] || { name: 'Unknown', email: '' }
            return (
              <motion.div
                key={exchange.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
              >
                <GlassCard className="p-6">
                  <div className="flex items-start justify-between mb-4">
                    <div>
                      <h3 className="text-2xl font-bold text-brown-900 mb-2">
                        Exchange with {partner.name}
                      </h3>
                      <span className={`px-4 py-2 rounded-full text-sm font-bold border-2 ${getStatusColor(exchange.status)}`}>
                        {exchange.status.replace('_', ' ')}
                      </span>
                    </div>
                    <div className="text-right">
                      <div className="text-sm text-brown-600 mb-1">Fairness Score</div>
                      <div className="text-4xl font-bold gradient-text">
                        {Math.round(exchange.fairness_score || 0)}%
                      </div>
                    </div>
                  </div>

                  <div className="grid md:grid-cols-2 gap-6 mb-6">
                    <div className="glass rounded-2xl p-4">
                      <div className="text-sm text-brown-600 mb-2">Exchange Type</div>
                      <div className="text-xl font-bold text-brown-900">{exchange.type?.replace('_', ' ')}</div>
                    </div>
                    <div className="glass rounded-2xl p-4">
                      <div className="text-sm text-brown-600 mb-2">Created</div>
                      <div className="text-xl font-bold text-brown-900">
                        {new Date(exchange.created_at).toLocaleDateString()}
                      </div>
                    </div>
                  </div>

                    <div className="flex items-center justify-between">
                    <div className="flex items-center gap-4">
                      <div className="text-sm text-brown-600">
                        Partner: {partner.email}
                      </div>
                      <button 
                        onClick={() => setExplainExchangeId(exchange.id)}
                        className="flex items-center gap-1 text-sm text-cyan-600 hover:text-cyan-700 bg-cyan-50 px-2 py-1 rounded-md transition"
                      >
                        <Activity className="w-4 h-4" /> AI Reasoning
                      </button>
                    </div>
                    <div className="flex gap-3">
                      {exchange.status === 'COMPLETED' ? (
                        <Button variant="primary" size="md" onClick={() => setShowRating(exchange.id)}>
                          ⭐ Rate Exchange
                        </Button>
                      ) : exchange.status === 'CANCELLED' ? (
                        <span className="text-sm text-brown-500 italic">Cancelled</span>
                      ) : (
                        <>
                          <Link href={`/chat/${exchange.id}`}>
                            <Button variant="primary" size="md">
                              💬 Chat
                            </Button>
                          </Link>
                          {exchange.status === 'PENDING' && (
                            <>
                              <Button variant="secondary" size="md" onClick={() => updateStatus(exchange.id, 'IN_PROGRESS')}>
                                ▶️ Start
                              </Button>
                              <Button variant="ghost" size="md" onClick={() => updateStatus(exchange.id, 'CANCELLED')}>
                                ✕ Cancel
                              </Button>
                            </>
                          )}
                          {exchange.status === 'IN_PROGRESS' && (
                            <Button variant="primary" size="md" onClick={() => updateStatus(exchange.id, 'COMPLETED')}>
                              ✅ Complete
                            </Button>
                          )}
                        </>
                      )}
                    </div>
                  </div>
                </GlassCard>

                {/* Rating Modal */}
                <AnimatePresence>
                  {showRating === exchange.id && (
                    <motion.div
                      initial={{ opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: 'auto' }}
                      exit={{ opacity: 0, height: 0 }}
                      className="mt-4"
                    >
                      <GlassCard className="p-6">
                        <h4 className="text-xl font-bold text-brown-900 mb-4">Rate this Exchange</h4>
                        
                        <div className="flex gap-2 mb-4">
                          {[1, 2, 3, 4, 5].map(star => (
                            <button
                              key={star}
                              onClick={() => setRating(star)}
                              className={`text-4xl transition-all ${star <= rating ? 'scale-110' : 'opacity-30 hover:opacity-60'}`}
                            >
                              ⭐
                            </button>
                          ))}
                        </div>
                        
                        <textarea
                          value={feedback}
                          onChange={(e) => setFeedback(e.target.value)}
                          placeholder="Share your experience (optional)..."
                          className="w-full px-4 py-3 glass rounded-2xl border-2 border-white/40 focus:border-pink-400 text-brown-900 mb-4 resize-none"
                          rows={3}
                        />
                        
                        <div className="flex gap-3">
                          <Button variant="secondary" size="md" onClick={() => setShowRating(null)}>
                            Cancel
                          </Button>
                          <Button
                            variant="primary"
                            size="md"
                            disabled={ratingLoading}
                            onClick={() => submitRating(exchange.id, partner.id)}
                          >
                            {ratingLoading ? 'Submitting...' : 'Submit Rating'}
                          </Button>
                        </div>
                      </GlassCard>
                    </motion.div>
                  )}
                </AnimatePresence>
              </motion.div>
            )
          })}
        </div>
      )}

      <ExplainabilityDrawer
        isOpen={!!explainExchangeId}
        onClose={() => setExplainExchangeId(null)}
        exchangeId={explainExchangeId}
      />
    </DashboardLayout>
  )
}
