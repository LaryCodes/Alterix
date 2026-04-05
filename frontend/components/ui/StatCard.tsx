'use client'

import { motion } from 'framer-motion'

interface StatCardProps {
  icon: string
  value: string | number
  label: string
  gradient?: string
  delay?: number
}

export default function StatCard({ icon, value, label, gradient, delay = 0 }: StatCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay }}
      whileHover={{ y: -5, scale: 1.02 }}
      className="glass-card p-6 rounded-3xl group relative overflow-hidden"
    >
      <div className="absolute inset-0 shimmer opacity-0 group-hover:opacity-100 transition-opacity" />
      <motion.div 
        className="text-5xl mb-3 relative z-10"
        animate={{ rotate: [0, 10, -10, 0] }}
        transition={{ duration: 3, repeat: Infinity, delay }}
      >
        {icon}
      </motion.div>
      <div className="text-4xl font-bold text-brown-900 mb-1 relative z-10">{value}</div>
      <div className="text-sm text-brown-600 relative z-10">{label}</div>
      
      {gradient && (
        <div className={`absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r ${gradient} opacity-60`} />
      )}
    </motion.div>
  )
}
