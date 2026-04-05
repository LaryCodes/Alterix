'use client'

import { motion } from 'framer-motion'
import Link from 'next/link'
import ThreeBackground from '@/components/three/ThreeBackground'

export default function LandingPage() {
  return (
    <main className="relative min-h-screen overflow-hidden">
      {/* Animated Gradient Background */}
      <div className="fixed inset-0 bg-gradient-to-br from-pink-50 via-cream-100 to-brown-100 bg-[length:200%_200%] animate-gradient" />
      
      {/* 3D Background */}
      <ThreeBackground />
      
      {/* Glassmorphic Header */}
      <motion.header 
        initial={{ y: -100, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.8 }}
        className="relative z-20 glass-strong border-b border-white/30"
      >
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <motion.h1 
              className="text-3xl font-bold gradient-text"
              whileHover={{ scale: 1.05 }}
            >
              Alterix
            </motion.h1>
            <div className="flex gap-3">
              <Link href="/login">
                <motion.button 
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="px-6 py-2 glass rounded-full text-brown-800 font-medium hover:glass-strong transition-all"
                >
                  Sign In
                </motion.button>
              </Link>
              <Link href="/register">
                <motion.button 
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="px-6 py-2 bg-gradient-to-r from-pink-500 to-brown-500 text-white rounded-full font-medium shadow-glass-lg hover:shadow-glass-xl transition-all"
                >
                  Get Started
                </motion.button>
              </Link>
            </div>
          </div>
        </div>
      </motion.header>
      
      {/* Content */}
      <div className="relative z-10">
        {/* Hero Section */}
        <section className="container mx-auto px-6 pt-32 pb-20">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-center"
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ duration: 0.8, delay: 0.2 }}
              className="inline-block mb-6"
            >
              <h1 className="text-8xl font-bold gradient-text mb-4">
                Alterix
              </h1>
              <div className="h-1 w-full bg-gradient-to-r from-transparent via-pink-400 to-transparent rounded-full" />
            </motion.div>
            
            <motion.p 
              className="text-3xl text-brown-800 mb-4 font-light"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.4 }}
            >
              The Intelligent Skill Exchange Network
            </motion.p>
            
            <motion.p 
              className="text-lg text-brown-600 mb-12 max-w-2xl mx-auto"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.6 }}
            >
              Exchange skills, learn from experts, and grow together with AI-powered matching
            </motion.p>
            
            <motion.div 
              className="flex gap-6 justify-center"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.8 }}
            >
              <Link href="/register">
                <motion.button 
                  whileHover={{ scale: 1.05, y: -2 }}
                  whileTap={{ scale: 0.95 }}
                  className="px-10 py-5 bg-gradient-to-r from-pink-500 via-pink-600 to-brown-500 text-white rounded-2xl font-semibold shadow-glass-xl hover:shadow-glass-xl transition-all text-lg relative overflow-hidden group"
                >
                  <span className="relative z-10">Get Started Free</span>
                  <div className="absolute inset-0 bg-gradient-to-r from-pink-400 to-brown-400 opacity-0 group-hover:opacity-100 transition-opacity" />
                </motion.button>
              </Link>
              
              <Link href="/login">
                <motion.button 
                  whileHover={{ scale: 1.05, y: -2 }}
                  whileTap={{ scale: 0.95 }}
                  className="px-10 py-5 glass-strong text-brown-800 rounded-2xl font-semibold border-2 border-white/40 hover:border-pink-300/60 transition-all text-lg"
                >
                  Sign In
                </motion.button>
              </Link>
            </motion.div>
          </motion.div>
        </section>

        {/* Features Section */}
        <section className="container mx-auto px-6 py-20">
          <motion.h2 
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-5xl font-bold text-center mb-16 gradient-text"
          >
            Powered by AI Agents
          </motion.h2>
          
          <div className="grid md:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: 0.2 * index }}
                whileHover={{ y: -10, scale: 1.02 }}
                className="group"
              >
                <div className="glass-card p-8 rounded-3xl transition-all duration-500 h-full relative overflow-hidden">
                  {/* Shimmer effect on hover */}
                  <div className="absolute inset-0 shimmer opacity-0 group-hover:opacity-100 transition-opacity" />
                  
                  <motion.div 
                    className="text-6xl mb-6 relative z-10"
                    animate={{ rotate: [0, 5, -5, 0] }}
                    transition={{ duration: 4, repeat: Infinity, delay: index * 0.5 }}
                  >
                    {feature.icon}
                  </motion.div>
                  <h3 className="text-2xl font-bold mb-4 text-brown-900 relative z-10">{feature.title}</h3>
                  <p className="text-brown-700 leading-relaxed relative z-10">{feature.description}</p>
                </div>
              </motion.div>
            ))}
          </div>
        </section>

        {/* Stats Section */}
        <section className="container mx-auto px-6 py-20">
          <div className="glass-strong rounded-3xl p-12">
            <div className="grid md:grid-cols-4 gap-8">
              {stats.map((stat, index) => (
                <motion.div
                  key={stat.label}
                  initial={{ opacity: 0, scale: 0.8 }}
                  whileInView={{ opacity: 1, scale: 1 }}
                  viewport={{ once: true }}
                  transition={{ delay: 0.1 * index }}
                  whileHover={{ scale: 1.1 }}
                  className="text-center p-6 rounded-2xl bg-gradient-to-br from-pink-400 via-pink-500 to-brown-500 text-white shadow-glass-lg relative overflow-hidden group"
                >
                  <div className="absolute inset-0 bg-gradient-to-br from-pink-300 to-brown-400 opacity-0 group-hover:opacity-100 transition-opacity" />
                  <div className="text-5xl font-bold mb-2 relative z-10">{stat.value}</div>
                  <div className="text-sm opacity-90 relative z-10">{stat.label}</div>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="container mx-auto px-6 py-20">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="glass-strong rounded-3xl p-16 text-center"
          >
            <h2 className="text-5xl font-bold mb-6 gradient-text">
              Ready to Start Exchanging?
            </h2>
            <p className="text-xl text-brown-700 mb-10 max-w-2xl mx-auto">
              Join thousands of learners and experts in the most intelligent skill exchange platform
            </p>
            <Link href="/register">
              <motion.button
                whileHover={{ scale: 1.05, y: -2 }}
                whileTap={{ scale: 0.95 }}
                className="px-12 py-6 bg-gradient-to-r from-pink-500 via-pink-600 to-brown-500 text-white rounded-2xl font-bold shadow-glass-xl hover:shadow-glass-xl transition-all text-xl"
              >
                Join Alterix Today
              </motion.button>
            </Link>
          </motion.div>
        </section>
      </div>
    </main>
  )
}

const features = [
  {
    icon: '🤖',
    title: 'AI-Powered Matching',
    description: 'Our intelligent agents find the perfect skill matches for you, including multi-hop exchange chains.'
  },
  {
    icon: '🔗',
    title: 'Multi-Party Chains',
    description: 'Exchange skills through connected networks. A teaches B, B teaches C, C teaches you.'
  },
  {
    icon: '⚖️',
    title: 'Fair Exchange',
    description: 'AI ensures balanced value in every exchange with our fairness validation system.'
  }
]

const stats = [
  { value: '10K+', label: 'Active Users' },
  { value: '50K+', label: 'Skills Exchanged' },
  { value: '95%', label: 'Success Rate' },
  { value: '4.9/5', label: 'User Rating' }
]
