'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import Link from 'next/link'
import { auth } from '@/lib/auth'
import { api } from '@/lib/api'
import { useRouter } from 'next/navigation'
import DashboardLayout from '@/components/layout/DashboardLayout'
import StatCard from '@/components/ui/StatCard'
import LoadingSpinner from '@/components/ui/LoadingSpinner'
import GlassCard from '@/components/ui/GlassCard'

export default function DashboardPage() {
  const router = useRouter()
  const [loading, setLoading] = useState(true)
  const [stats, setStats] = useState({
    skills_offered: 0,
    skills_requested: 0,
    active_exchanges: 0,
    completed_exchanges: 0,
    trust_score: 0,
    total_exchanges: 0
  })
  const [notifications, setNotifications] = useState<any[]>([])

  useEffect(() => {
    const loadData = async () => {
      if (!auth.isAuthenticated()) {
        router.push('/login')
        return
      }

      const userData = auth.getUser()

      try {
        // Load stats and notifications in parallel
        const [statsRes, notifRes] = await Promise.allSettled([
          api.getUserStats(userData.id),
          api.getNotifications(userData.id)
        ])

        if (statsRes.status === 'fulfilled' && statsRes.value.success) {
          setStats(statsRes.value.stats)
        }

        if (notifRes.status === 'fulfilled' && notifRes.value.success) {
          setNotifications(notifRes.value.notifications || [])
        }
      } catch (error) {
        console.error('Failed to load data:', error)
      } finally {
        setLoading(false)
      }
    }

    loadData()
  }, [router])

  if (loading) {
    return <LoadingSpinner fullScreen />
  }

  const statCards = [
    { label: 'Skills Offered', value: stats.skills_offered.toString(), icon: '🎯', gradient: 'from-pink-400 to-pink-600' },
    { label: 'Active Exchanges', value: stats.active_exchanges.toString(), icon: '🔄', gradient: 'from-brown-400 to-brown-600' },
    { label: 'Trust Score', value: Math.round(stats.trust_score).toString(), icon: '⭐', gradient: 'from-pink-500 to-brown-500' },
    { label: 'Completed', value: stats.completed_exchanges.toString(), icon: '✅', gradient: 'from-brown-500 to-pink-500' }
  ]

  const getNotifIcon = (type: string) => {
    switch (type) {
      case 'exchange_created': return '🤝'
      case 'exchange_request': return '📩'
      case 'exchange_completed': return '✅'
      case 'match_found': return '🎯'
      case 'message_received': return '💬'
      default: return '🔔'
    }
  }

  const getTimeAgo = (dateStr: string) => {
    const date = new Date(dateStr)
    const now = new Date()
    const diff = now.getTime() - date.getTime()
    const minutes = Math.floor(diff / 60000)
    const hours = Math.floor(minutes / 60)
    const days = Math.floor(hours / 24)

    if (days > 0) return `${days}d ago`
    if (hours > 0) return `${hours}h ago`
    if (minutes > 0) return `${minutes}m ago`
    return 'just now'
  }

  return (
    <DashboardLayout>
      {/* Welcome banner */}
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-8"
      >
        <h1 className="text-3xl font-bold gradient-text mb-1">
          Welcome back, {auth.getUser()?.name || 'User'}! 👋
        </h1>
        <p className="text-brown-600">Here's what's happening with your skill exchanges</p>
      </motion.div>

      {/* Stats Grid */}
      <div className="grid md:grid-cols-4 gap-6 mb-8">
        {statCards.map((stat, index) => (
          <StatCard
            key={stat.label}
            icon={stat.icon}
            value={stat.value}
            label={stat.label}
            gradient={stat.gradient}
            delay={index * 0.1}
          />
        ))}
      </div>

      {/* Quick Actions */}
      <GlassCard className="p-8 mb-8" hover={false}>
        <h2 className="text-2xl font-bold text-brown-900 mb-6 gradient-text">Quick Actions</h2>
        <div className="grid md:grid-cols-3 gap-6">
          <Link href="/skills">
            <GlassCard className="p-6 text-center cursor-pointer" gradient>
              <motion.div 
                className="text-5xl mb-3"
                animate={{ scale: [1, 1.1, 1] }}
                transition={{ duration: 2, repeat: Infinity }}
              >
                ➕
              </motion.div>
              <div className="font-bold text-brown-900 text-lg">Add Skills</div>
              <p className="text-sm text-brown-600 mt-2">Share your expertise</p>
            </GlassCard>
          </Link>
          
          <Link href="/matches">
            <GlassCard className="p-6 text-center cursor-pointer" gradient>
              <motion.div 
                className="text-5xl mb-3"
                animate={{ scale: [1, 1.1, 1] }}
                transition={{ duration: 2, repeat: Infinity, delay: 0.3 }}
              >
                🔍
              </motion.div>
              <div className="font-bold text-brown-900 text-lg">Find Matches</div>
              <p className="text-sm text-brown-600 mt-2">AI-powered matching</p>
            </GlassCard>
          </Link>
          
          <Link href="/exchanges">
            <GlassCard className="p-6 text-center cursor-pointer" gradient>
              <motion.div 
                className="text-5xl mb-3"
                animate={{ scale: [1, 1.1, 1] }}
                transition={{ duration: 2, repeat: Infinity, delay: 0.6 }}
              >
                📊
              </motion.div>
              <div className="font-bold text-brown-900 text-lg">View Exchanges</div>
              <p className="text-sm text-brown-600 mt-2">Track your progress</p>
            </GlassCard>
          </Link>
        </div>
      </GlassCard>

      {/* Recent Activity — REAL notifications from database */}
      <GlassCard className="p-8" hover={false}>
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-brown-900 gradient-text">Recent Activity</h2>
          {notifications.length > 0 && (
            <button
              onClick={async () => {
                const userData = auth.getUser()
                await api.markAllNotificationsRead(userData.id)
                setNotifications(prev => prev.map(n => ({ ...n, is_read: true })))
              }}
              className="text-sm text-pink-600 hover:text-pink-700 font-medium"
            >
              Mark all read
            </button>
          )}
        </div>
        <div className="space-y-4">
          {notifications.length === 0 ? (
            <div className="glass p-6 rounded-2xl text-center text-brown-600">
              <div className="text-4xl mb-3">🔔</div>
              <p>No activity yet. Start by adding skills and finding matches!</p>
            </div>
          ) : (
            notifications.slice(0, 5).map((notif, index) => (
              <motion.div
                key={notif.id}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.05 }}
                className={`glass p-4 rounded-2xl flex items-center gap-4 ${!notif.is_read ? 'border-l-4 border-pink-400' : ''}`}
              >
                <div className="text-3xl">{getNotifIcon(notif.type)}</div>
                <div className="flex-1">
                  <div className={`font-semibold ${!notif.is_read ? 'text-brown-900' : 'text-brown-700'}`}>
                    {notif.title}
                  </div>
                  <div className="text-sm text-brown-600">{notif.message}</div>
                </div>
                <div className="text-xs text-brown-500">{getTimeAgo(notif.created_at)}</div>
              </motion.div>
            ))
          )}
        </div>
      </GlassCard>
    </DashboardLayout>
  )
}
