'use client'

import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { auth } from '@/lib/auth'
import { api } from '@/lib/api'
import { useRouter } from 'next/navigation'
import DashboardLayout from '@/components/layout/DashboardLayout'
import LoadingSpinner from '@/components/ui/LoadingSpinner'
import EmptyState from '@/components/ui/EmptyState'
import Button from '@/components/ui/Button'

const LEVELS = ['BEGINNER', 'INTERMEDIATE', 'ADVANCED', 'EXPERT']

export default function SkillsPage() {
  const router = useRouter()
  const [activeTab, setActiveTab] = useState<'offered' | 'requested'>('offered')
  const [loading, setLoading] = useState(true)
  const [offeredSkills, setOfferedSkills] = useState<any[]>([])
  const [requestedSkills, setRequestedSkills] = useState<any[]>([])
  const [showModal, setShowModal] = useState(false)
  const [catalog, setCatalog] = useState<any[]>([])
  const [selectedSkillId, setSelectedSkillId] = useState('')
  const [selectedLevel, setSelectedLevel] = useState('INTERMEDIATE')
  const [modalLoading, setModalLoading] = useState(false)
  const [error, setError] = useState('')
  const [filterCategory, setFilterCategory] = useState('all')

  const loadSkills = async () => {
    const userData = auth.getUser()
    try {
      const [offeredRes, requestedRes] = await Promise.all([
        api.getUserOfferedSkills(userData.id),
        api.getUserRequestedSkills(userData.id)
      ])
      if (offeredRes.success) setOfferedSkills(offeredRes.skills)
      if (requestedRes.success) setRequestedSkills(requestedRes.skills)
    } catch (error) {
      console.error('Failed to load skills:', error)
    }
  }

  useEffect(() => {
    const loadData = async () => {
      if (!auth.isAuthenticated()) {
        router.push('/login')
        return
      }
      await loadSkills()
      setLoading(false)
    }
    loadData()
  }, [router])

  const openAddModal = async () => {
    setError('')
    setShowModal(true)
    
    if (catalog.length === 0) {
      try {
        const res = await api.getAllSkills()
        if (res.success) {
          setCatalog(res.skills)
          if (res.skills.length > 0) {
            setSelectedSkillId(res.skills[0].id)
          }
        }
      } catch (err) {
        setError('Failed to load skill catalog')
      }
    }
  }

  const addSkill = async () => {
    if (!selectedSkillId) return
    setModalLoading(true)
    setError('')
    
    try {
      const userData = auth.getUser()
      if (activeTab === 'offered') {
        await api.addOfferedSkill(userData.id, selectedSkillId, selectedLevel)
      } else {
        await api.addRequestedSkill(userData.id, selectedSkillId, selectedLevel)
      }
      
      await loadSkills()
      setShowModal(false)
    } catch (err: any) {
      setError(err.message || 'Failed to add skill')
    } finally {
      setModalLoading(false)
    }
  }

  const removeSkill = async (skillRecordId: string) => {
    try {
      if (activeTab === 'offered') {
        await api.removeOfferedSkill(skillRecordId)
      } else {
        await api.removeRequestedSkill(skillRecordId)
      }
      await loadSkills()
    } catch (err: any) {
      console.error('Failed to remove skill:', err)
    }
  }

  if (loading) {
    return <LoadingSpinner fullScreen />
  }

  const currentSkills = activeTab === 'offered' ? offeredSkills : requestedSkills
  const categories = [...new Set(catalog.map(s => s.category))].sort()
  const filteredCatalog = filterCategory === 'all' ? catalog : catalog.filter(s => s.category === filterCategory)

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'Technology': return '💻'
      case 'Business': return '📊'
      case 'Creative': return '🎨'
      case 'Language': return '🌍'
      default: return '📚'
    }
  }

  return (
    <DashboardLayout>
      {/* Header with tabs and add button */}
      <div className="flex items-center justify-between mb-8 flex-wrap gap-4">
        <div className="flex gap-4">
          <Button
            variant={activeTab === 'offered' ? 'primary' : 'secondary'}
            size="md"
            onClick={() => setActiveTab('offered')}
          >
            🎯 Skills I Offer ({offeredSkills.length})
          </Button>
          <Button
            variant={activeTab === 'requested' ? 'primary' : 'secondary'}
            size="md"
            onClick={() => setActiveTab('requested')}
          >
            📚 Skills I Want ({requestedSkills.length})
          </Button>
        </div>
        <Button
          variant="primary"
          size="lg"
          onClick={openAddModal}
        >
          ➕ Add {activeTab === 'offered' ? 'Offered' : 'Requested'} Skill
        </Button>
      </div>

      {/* Skills Grid */}
      {currentSkills.length === 0 ? (
        <EmptyState
          icon={activeTab === 'offered' ? '🎯' : '📚'}
          title={`No ${activeTab === 'offered' ? 'offered' : 'requested'} skills yet`}
          description={`Click "Add ${activeTab === 'offered' ? 'Offered' : 'Requested'} Skill" to get started!`}
        />
      ) : (
        <div className="grid md:grid-cols-3 gap-6">
          {currentSkills.map((item, index) => {
            const skill = item.skills || {}
            return (
              <motion.div
                key={item.id}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: index * 0.1 }}
                whileHover={{ y: -8, scale: 1.02 }}
                className="glass-card p-6 rounded-3xl group relative overflow-hidden"
              >
                <div className="absolute inset-0 shimmer opacity-0 group-hover:opacity-100 transition-opacity" />
                
                <div className="flex items-start justify-between mb-4 relative z-10">
                  <motion.div 
                    className="text-5xl"
                    animate={{ rotate: [0, 10, -10, 0] }}
                    transition={{ duration: 3, repeat: Infinity }}
                  >
                    {getCategoryIcon(skill.category)}
                  </motion.div>
                  <span className="px-3 py-1 glass rounded-full text-sm font-bold text-pink-700">
                    {skill.category || 'General'}
                  </span>
                </div>
                
                <h3 className="text-xl font-bold text-brown-900 mb-2 relative z-10">{skill.name}</h3>
                <p className="text-brown-600 mb-4 relative z-10">
                  Level: <span className="font-semibold text-pink-600">{item.proficiency_level || item.desired_level || 'N/A'}</span>
                </p>
                
                <div className="flex gap-2 relative z-10">
                  {activeTab === 'requested' && (
                    <Button 
                      fullWidth
                      variant="primary"
                      size="sm"
                      onClick={() => router.push('/matches')}
                    >
                      🔍 Find Match
                    </Button>
                  )}
                  <Button 
                    variant="secondary"
                    size="sm"
                    onClick={() => removeSkill(item.id)}
                  >
                    🗑️
                  </Button>
                </div>
              </motion.div>
            )
          })}
        </div>
      )}

      {/* Add Skill Modal */}
      <AnimatePresence>
        {showModal && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/30 backdrop-blur-sm z-50 flex items-center justify-center p-6"
            onClick={() => setShowModal(false)}
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              className="glass-strong rounded-3xl p-8 w-full max-w-lg shadow-glass-xl"
              onClick={(e) => e.stopPropagation()}
            >
              <h2 className="text-2xl font-bold gradient-text mb-6">
                Add {activeTab === 'offered' ? 'Offered' : 'Requested'} Skill
              </h2>

              {error && (
                <div className="mb-4 p-3 glass rounded-2xl border-2 border-pink-300 text-pink-700 text-sm">
                  {error}
                </div>
              )}

              {/* Category filter */}
              <div className="mb-4">
                <label className="block text-sm font-semibold text-brown-800 mb-2">Category</label>
                <select
                  value={filterCategory}
                  onChange={(e) => setFilterCategory(e.target.value)}
                  className="w-full px-4 py-3 glass rounded-2xl border-2 border-white/40 focus:border-pink-400 text-brown-900"
                >
                  <option value="all">All Categories</option>
                  {categories.map(cat => (
                    <option key={cat} value={cat}>{getCategoryIcon(cat)} {cat}</option>
                  ))}
                </select>
              </div>

              {/* Skill selection */}
              <div className="mb-4">
                <label className="block text-sm font-semibold text-brown-800 mb-2">Skill</label>
                <select
                  value={selectedSkillId}
                  onChange={(e) => setSelectedSkillId(e.target.value)}
                  className="w-full px-4 py-3 glass rounded-2xl border-2 border-white/40 focus:border-pink-400 text-brown-900"
                >
                  {filteredCatalog.map(skill => (
                    <option key={skill.id} value={skill.id}>
                      {skill.name} ({skill.level}) — {skill.estimated_hours}h
                    </option>
                  ))}
                </select>
              </div>

              {/* Level selection */}
              <div className="mb-6">
                <label className="block text-sm font-semibold text-brown-800 mb-2">
                  {activeTab === 'offered' ? 'Your Proficiency' : 'Desired Level'}
                </label>
                <div className="flex gap-2">
                  {LEVELS.map(level => (
                    <button
                      key={level}
                      onClick={() => setSelectedLevel(level)}
                      className={`flex-1 py-2 px-3 rounded-xl text-xs font-bold transition-all ${
                        selectedLevel === level
                          ? 'bg-gradient-to-r from-pink-500 to-brown-500 text-white shadow-glass'
                          : 'glass text-brown-700 hover:text-pink-600'
                      }`}
                    >
                      {level.slice(0, 4)}
                    </button>
                  ))}
                </div>
              </div>

              <div className="flex gap-3">
                <Button
                  variant="secondary"
                  size="md"
                  fullWidth
                  onClick={() => setShowModal(false)}
                >
                  Cancel
                </Button>
                <Button
                  variant="primary"
                  size="md"
                  fullWidth
                  disabled={modalLoading || !selectedSkillId}
                  onClick={addSkill}
                >
                  {modalLoading ? 'Adding...' : 'Add Skill'}
                </Button>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </DashboardLayout>
  )
}
