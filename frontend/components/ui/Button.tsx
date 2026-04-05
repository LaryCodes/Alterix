'use client'

import { motion } from 'framer-motion'
import { ReactNode } from 'react'

interface ButtonProps {
  children: ReactNode
  onClick?: () => void
  variant?: 'primary' | 'secondary' | 'ghost'
  size?: 'sm' | 'md' | 'lg'
  disabled?: boolean
  type?: 'button' | 'submit' | 'reset'
  fullWidth?: boolean
  className?: string
}

export default function Button({ 
  children, 
  onClick, 
  variant = 'primary',
  size = 'md',
  disabled = false,
  type = 'button',
  fullWidth = false,
  className = ''
}: ButtonProps) {
  const baseClasses = 'font-bold rounded-2xl transition-all relative overflow-hidden group'
  
  const variantClasses = {
    primary: 'bg-gradient-to-r from-pink-500 via-pink-600 to-brown-500 text-white shadow-glass-lg hover:shadow-glass-xl',
    secondary: 'glass-strong text-brown-800 border-2 border-white/40 hover:border-pink-300/60',
    ghost: 'text-brown-700 hover:text-pink-600 hover:bg-white/30'
  }
  
  const sizeClasses = {
    sm: 'px-4 py-2 text-sm',
    md: 'px-6 py-3 text-base',
    lg: 'px-10 py-5 text-lg'
  }
  
  const widthClass = fullWidth ? 'w-full' : ''
  
  return (
    <motion.button
      whileHover={{ scale: disabled ? 1 : 1.02, y: disabled ? 0 : -2 }}
      whileTap={{ scale: disabled ? 1 : 0.98 }}
      onClick={onClick}
      type={type}
      disabled={disabled}
      className={`${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]} ${widthClass} ${className} ${
        disabled ? 'opacity-50 cursor-not-allowed' : ''
      }`}
    >
      <span className="relative z-10">{children}</span>
      {variant === 'primary' && !disabled && (
        <div className="absolute inset-0 bg-gradient-to-r from-pink-400 to-brown-400 opacity-0 group-hover:opacity-100 transition-opacity" />
      )}
    </motion.button>
  )
}
