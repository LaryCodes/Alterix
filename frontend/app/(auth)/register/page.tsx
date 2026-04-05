'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { api } from '@/lib/api'
import { auth } from '@/lib/auth'
import Button from '@/components/ui/Button'

export default function RegisterPage() {
  const router = useRouter()
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: ''
  })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    
    if (formData.password.length < 8) {
      setError('Password must be at least 8 characters long')
      return
    }
    
    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match')
      return
    }

    setLoading(true)
    try {
      const response = await api.register(formData.name, formData.email, formData.password)
      auth.setToken(response.token)
      auth.setUser(response.user)
      router.push('/dashboard')
    } catch (err: any) {
      setError(err.message || 'Registration failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-pink-50 via-cream-100 to-brown-100 p-6 relative overflow-hidden">
      {/* Animated background elements */}
      <div className="absolute inset-0 overflow-hidden">
        <motion.div
          animate={{ 
            scale: [1, 1.2, 1],
            rotate: [0, 90, 0],
            opacity: [0.3, 0.5, 0.3]
          }}
          transition={{ duration: 20, repeat: Infinity }}
          className="absolute -top-20 -left-20 w-96 h-96 bg-gradient-to-br from-pink-300 to-pink-400 rounded-full blur-3xl"
        />
        <motion.div
          animate={{ 
            scale: [1.2, 1, 1.2],
            rotate: [90, 0, 90],
            opacity: [0.3, 0.5, 0.3]
          }}
          transition={{ duration: 15, repeat: Infinity }}
          className="absolute -bottom-20 -right-20 w-96 h-96 bg-gradient-to-br from-brown-300 to-brown-400 rounded-full blur-3xl"
        />
      </div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="w-full max-w-md relative z-10"
      >
        <motion.div 
          className="glass-strong rounded-3xl shadow-glass-xl p-10 relative overflow-hidden"
          whileHover={{ scale: 1.01 }}
        >
          {/* Decorative gradient border */}
          <div className="absolute inset-0 bg-gradient-to-br from-pink-400 via-transparent to-brown-400 opacity-20 rounded-3xl" />
          
          <div className="relative z-10">
            <motion.div
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ delay: 0.2 }}
              className="text-center mb-8"
            >
              <h1 className="text-4xl font-bold gradient-text mb-2">Join Alterix</h1>
              <p className="text-brown-600">Create your account and start exchanging skills</p>
            </motion.div>

            {error && (
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                className="mb-6 p-4 glass rounded-2xl border-2 border-pink-300"
              >
                <div className="flex items-center gap-2 text-pink-700">
                  <span className="text-xl">⚠️</span>
                  <span>{error}</span>
                </div>
              </motion.div>
            )}

            <form onSubmit={handleSubmit} className="space-y-5">
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.3 }}
              >
                <label className="block text-sm font-semibold text-brown-800 mb-2">
                  Full Name
                </label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({...formData, name: e.target.value})}
                  className="w-full px-5 py-3 glass rounded-2xl border-2 border-white/40 focus:border-pink-400 focus:ring-4 focus:ring-pink-100 transition-all text-brown-900 placeholder-brown-400"
                  placeholder="John Doe"
                  required
                />
              </motion.div>

              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.35 }}
              >
                <label className="block text-sm font-semibold text-brown-800 mb-2">
                  Email Address
                </label>
                <input
                  type="email"
                  value={formData.email}
                  onChange={(e) => setFormData({...formData, email: e.target.value})}
                  className="w-full px-5 py-3 glass rounded-2xl border-2 border-white/40 focus:border-pink-400 focus:ring-4 focus:ring-pink-100 transition-all text-brown-900 placeholder-brown-400"
                  placeholder="you@example.com"
                  required
                />
              </motion.div>

              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.4 }}
              >
                <label className="block text-sm font-semibold text-brown-800 mb-2">
                  Password
                </label>
                <input
                  type="password"
                  value={formData.password}
                  onChange={(e) => setFormData({...formData, password: e.target.value})}
                  className="w-full px-5 py-3 glass rounded-2xl border-2 border-white/40 focus:border-pink-400 focus:ring-4 focus:ring-pink-100 transition-all text-brown-900 placeholder-brown-400"
                  placeholder="••••••••"
                  required
                />
              </motion.div>

              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.45 }}
              >
                <label className="block text-sm font-semibold text-brown-800 mb-2">
                  Confirm Password
                </label>
                <input
                  type="password"
                  value={formData.confirmPassword}
                  onChange={(e) => setFormData({...formData, confirmPassword: e.target.value})}
                  className="w-full px-5 py-3 glass rounded-2xl border-2 border-white/40 focus:border-pink-400 focus:ring-4 focus:ring-pink-100 transition-all text-brown-900 placeholder-brown-400"
                  placeholder="••••••••"
                  required
                />
              </motion.div>

              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.5 }}
              >
                <Button
                  type="submit"
                  disabled={loading}
                  variant="primary"
                  size="lg"
                  fullWidth
                >
                  {loading ? (
                    <span className="flex items-center justify-center gap-2">
                      <motion.span
                        animate={{ rotate: 360 }}
                        transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                        className="inline-block w-5 h-5 border-2 border-white border-t-transparent rounded-full"
                      />
                      Creating Account...
                    </span>
                  ) : (
                    'Create Account'
                  )}
                </Button>
              </motion.div>
            </form>

            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.6 }}
              className="mt-8 text-center"
            >
              <p className="text-brown-600">
                Already have an account?{' '}
                <Link href="/login" className="text-pink-600 font-bold hover:text-pink-700 transition-colors">
                  Sign in
                </Link>
              </p>
            </motion.div>

            {/* Decorative elements */}
            <div className="absolute top-4 right-4 w-20 h-20 bg-gradient-to-br from-pink-300 to-transparent rounded-full blur-2xl opacity-50" />
            <div className="absolute bottom-4 left-4 w-20 h-20 bg-gradient-to-br from-brown-300 to-transparent rounded-full blur-2xl opacity-50" />
          </div>
        </motion.div>

        {/* Additional decorative card behind */}
        <div className="absolute inset-0 glass rounded-3xl transform translate-y-2 -z-10 opacity-50" />
      </motion.div>
    </div>
  )
}
