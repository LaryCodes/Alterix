'use client'

import { motion } from 'framer-motion'
import { ReactNode } from 'react'

interface GlassCardProps {
  children: ReactNode
  className?: string
  hover?: boolean
  gradient?: boolean
  onClick?: () => void
}

export default function GlassCard({ 
  children, 
  className = '', 
  hover = true,
  gradient = false,
  onClick 
}: GlassCardProps) {
  const baseClasses = gradient ? 'glass-card' : 'glass'
  
  return (
    <motion.div
      whileHover={hover ? { y: -5, scale: 1.02 } : {}}
      whileTap={onClick ? { scale: 0.98 } : {}}
      className={`${baseClasses} rounded-3xl p-6 transition-all ${className} ${onClick ? 'cursor-pointer' : ''}`}
      onClick={onClick}
    >
      {children}
    </motion.div>
  )
}
