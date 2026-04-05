"use client"

import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { api } from '@/lib/api'
import { toast } from 'sonner'
import { X, Activity, Scale, Shield, Calculator } from 'lucide-react'

interface ExplainabilityDrawerProps {
  isOpen: boolean
  onClose: () => void
  exchangeId: string | null
}

export default function ExplainabilityDrawer({ isOpen, onClose, exchangeId }: ExplainabilityDrawerProps) {
  const [traces, setTraces] = useState<any[]>([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    async function fetchTraces() {
      if (!isOpen || !exchangeId) return
      setLoading(true)
      try {
        const data = await api.getTraces(exchangeId)
        setTraces(data.traces || [])
      } catch (err) {
        toast.error('Failed to load AI traces')
      } finally {
        setLoading(false)
      }
    }
    fetchTraces()
  }, [isOpen, exchangeId])

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 0.5 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black z-40"
            onClick={onClose}
          />
          
          {/* Drawer */}
          <motion.div
            initial={{ x: '100%' }}
            animate={{ x: 0 }}
            exit={{ x: '100%' }}
            transition={{ type: 'spring', damping: 20, stiffness: 100 }}
            className="fixed right-0 top-0 h-full w-[400px] bg-[#1a1a1e]/90 backdrop-blur-xl border-l border-white/10 z-50 p-6 overflow-y-auto shadow-2xl flex flex-col"
          >
            <div className="flex justify-between items-center mb-6 border-b border-white/10 pb-4">
              <h2 className="text-xl font-bold bg-gradient-to-r from-cyan-400 to-emerald-400 bg-clip-text text-transparent flex items-center gap-2">
                <Activity className="w-5 h-5 text-cyan-400" />
                AI Explainability
              </h2>
              <button onClick={onClose} className="p-2 hover:bg-white/10 rounded-full transition">
                <X className="w-5 h-5 text-gray-400" />
              </button>
            </div>

            {loading ? (
              <div className="flex justify-center items-center h-48">
                <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-cyan-400"></div>
              </div>
            ) : traces.length === 0 ? (
              <div className="text-center text-gray-400 mt-10">
                <p>No traces found for this exchange.</p>
                <p className="text-sm text-gray-500 mt-2">Traces are generated when an agent interacts with this session.</p>
              </div>
            ) : (
              <div className="flex flex-col gap-6">
                {traces.map((trace, i) => (
                  <div key={trace.id} className="bg-white/5 border border-white/10 rounded-xl p-4 flex flex-col gap-3 relative overflow-hidden group">
                    <div className="absolute top-0 left-0 w-1 h-full bg-cyan-400 opacity-50"></div>
                    
                    <div className="flex items-center justify-between">
                      <h3 className="font-semibold text-white flex items-center gap-2">
                        {trace.agent_name === 'MatchingAgent' && <Calculator className="w-4 h-4 text-cyan-400" />}
                        {trace.agent_name === 'FairnessAgent' && <Scale className="w-4 h-4 text-purple-400" />}
                        {trace.agent_name === 'ReputationAgent' && <Shield className="w-4 h-4 text-emerald-400" />}
                        {trace.agent_name}
                      </h3>
                      <span className="text-xs text-gray-400">{trace.execution_time_ms}ms</span>
                    </div>

                    <p className="text-sm text-gray-300 bg-black/30 p-3 rounded-lg border border-white/5">
                      {trace.decision_reasoning}
                    </p>

                    {trace.metrics && Object.keys(trace.metrics).length > 0 && (
                      <div className="mt-2 grid grid-cols-2 gap-2">
                        {Object.entries(trace.metrics).map(([key, val]) => (
                          <div key={key} className="bg-white/5 p-2 rounded flex flex-col">
                            <span className="text-xs text-gray-500 uppercase tracking-wider">{key.replace(/_/g, ' ')}</span>
                            <span className="text-sm font-medium text-white">
                              {typeof val === 'number' ? (val % 1 !== 0 ? val.toFixed(2) : val) : String(val)}
                            </span>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </motion.div>
        </>
      )}
    </AnimatePresence>
  )
}
