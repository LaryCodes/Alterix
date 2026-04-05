'use client'

import { motion } from 'framer-motion'
import Button from '@/components/ui/Button'

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-pink-50 via-cream-100 to-brown-100 p-6">
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        className="glass-strong rounded-3xl p-12 text-center max-w-md shadow-glass-xl"
      >
        <div className="text-7xl mb-6">😵</div>
        <h2 className="text-3xl font-bold gradient-text mb-4">Something went wrong</h2>
        <p className="text-brown-600 mb-8">
          {error.message || 'An unexpected error occurred. Please try again.'}
        </p>
        <div className="flex gap-4 justify-center">
          <Button variant="primary" size="lg" onClick={reset}>
            Try Again
          </Button>
          <Button variant="secondary" size="lg" onClick={() => window.location.href = '/dashboard'}>
            Go Home
          </Button>
        </div>
      </motion.div>
    </div>
  )
}
