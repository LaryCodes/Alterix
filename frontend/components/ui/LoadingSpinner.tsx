'use client'

import { motion } from 'framer-motion'

interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg'
  fullScreen?: boolean
}

export default function LoadingSpinner({ size = 'md', fullScreen = false }: LoadingSpinnerProps) {
  const sizeClasses = {
    sm: 'w-8 h-8 border-2',
    md: 'w-16 h-16 border-4',
    lg: 'w-24 h-24 border-4'
  }

  const spinner = (
    <motion.div 
      animate={{ rotate: 360 }}
      transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
      className={`${sizeClasses[size]} border-pink-400 border-t-transparent rounded-full`}
    />
  )

  if (fullScreen) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-pink-50 via-cream-100 to-brown-100 flex items-center justify-center">
        {spinner}
      </div>
    )
  }

  return spinner
}
