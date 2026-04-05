'use client'

import { motion } from 'framer-motion'
import { ReactNode } from 'react'

interface EmptyStateProps {
  icon: string
  title: string
  description: string
  action?: ReactNode
}

export default function EmptyState({ icon, title, description, action }: EmptyStateProps) {
  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="glass-card text-center py-16 rounded-3xl"
    >
      <motion.div 
        className="text-8xl mb-6"
        animate={{ scale: [1, 1.1, 1] }}
        transition={{ duration: 2, repeat: Infinity }}
      >
        {icon}
      </motion.div>
      <p className="text-2xl text-brown-800 font-bold mb-2">{title}</p>
      <p className="text-brown-600 mb-6">{description}</p>
      {action && <div className="mt-6">{action}</div>}
    </motion.div>
  )
}
