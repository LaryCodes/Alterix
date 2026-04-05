'use client'

import { useState, useEffect, useRef } from 'react'
import { motion } from 'framer-motion'
import { auth } from '@/lib/auth'
import { api } from '@/lib/api'
import { useRouter, useParams } from 'next/navigation'
import DashboardLayout from '@/components/layout/DashboardLayout'
import LoadingSpinner from '@/components/ui/LoadingSpinner'
import Button from '@/components/ui/Button'

export default function ChatPage() {
  const router = useRouter()
  const params = useParams()
  const exchangeId = params.exchangeId as string
  const [messages, setMessages] = useState<any[]>([])
  const [newMessage, setNewMessage] = useState('')
  const [loading, setLoading] = useState(true)
  const [sending, setSending] = useState(false)
  const [exchange, setExchange] = useState<any>(null)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const currentUser = auth.getUser()

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  const loadMessages = async () => {
    try {
      const res = await api.getMessages(exchangeId)
      if (res.success) {
        setMessages(res.messages)
      }
    } catch (err) {
      console.error('Failed to load messages:', err)
    }
  }

  useEffect(() => {
    if (!auth.isAuthenticated()) {
      router.push('/login')
      return
    }

    const loadData = async () => {
      try {
        const [exchangeRes] = await Promise.all([
          api.getExchange(exchangeId),
        ])
        
        if (exchangeRes.success) {
          setExchange(exchangeRes.exchange)
        }
        
        await loadMessages()
      } catch (err) {
        console.error('Failed to load chat:', err)
      } finally {
        setLoading(false)
      }
    }

    loadData()

    // Poll for new messages every 5 seconds
    const interval = setInterval(loadMessages, 5000)
    return () => clearInterval(interval)
  }, [exchangeId, router])

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const sendMessage = async () => {
    if (!newMessage.trim()) return
    
    setSending(true)
    try {
      await api.sendMessage(exchangeId, newMessage.trim())
      setNewMessage('')
      await loadMessages()
    } catch (err) {
      console.error('Failed to send message:', err)
    } finally {
      setSending(false)
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  if (loading) {
    return <LoadingSpinner fullScreen />
  }

  const partner = exchange?.participants?.find((p: any) => p.id !== currentUser?.id)

  return (
    <DashboardLayout>
      {/* Chat Header */}
      <div className="glass-strong rounded-3xl p-4 mb-4 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <button onClick={() => router.push('/exchanges')} className="text-2xl hover:scale-110 transition-transform">
            ←
          </button>
          <div className="w-12 h-12 bg-gradient-to-br from-pink-400 to-brown-400 rounded-full flex items-center justify-center text-white text-xl font-bold">
            {(partner?.name || 'P').charAt(0).toUpperCase()}
          </div>
          <div>
            <h2 className="text-xl font-bold text-brown-900">Chat with {partner?.name || 'Partner'}</h2>
            <p className="text-sm text-brown-600">Exchange: {exchange?.type?.replace('_', ' ')}</p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <span className={`px-3 py-1 rounded-full text-xs font-bold ${
            exchange?.status === 'IN_PROGRESS' ? 'bg-blue-100 text-blue-700' : 
            exchange?.status === 'COMPLETED' ? 'bg-green-100 text-green-700' : 'bg-orange-100 text-orange-700'
          }`}>
            {exchange?.status?.replace('_', ' ')}
          </span>
        </div>
      </div>

      {/* Messages Area */}
      <div className="glass-strong rounded-3xl p-6 mb-4" style={{ height: 'calc(100vh - 320px)', overflowY: 'auto' }}>
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-brown-600">
            <div className="text-6xl mb-4">💬</div>
            <p className="text-lg">No messages yet</p>
            <p className="text-sm">Send a message to start the conversation!</p>
          </div>
        ) : (
          <div className="space-y-4">
            {messages.map((msg, index) => {
              const isMine = msg.sender_id === currentUser?.id
              const sender = msg.users || {}
              
              return (
                <motion.div
                  key={msg.id}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.03 }}
                  className={`flex ${isMine ? 'justify-end' : 'justify-start'}`}
                >
                  <div className={`max-w-[70%] ${isMine ? 'order-2' : 'order-1'}`}>
                    <div className={`px-5 py-3 rounded-2xl ${
                      isMine 
                        ? 'bg-gradient-to-r from-pink-500 to-brown-500 text-white rounded-br-md' 
                        : 'glass text-brown-900 rounded-bl-md'
                    }`}>
                      <p className="text-sm whitespace-pre-wrap">{msg.content}</p>
                    </div>
                    <div className={`text-xs text-brown-500 mt-1 ${isMine ? 'text-right' : 'text-left'}`}>
                      {sender.name && <span className="mr-2">{sender.name}</span>}
                      {new Date(msg.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </div>
                  </div>
                </motion.div>
              )
            })}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      {/* Message Input */}
      <div className="glass-strong rounded-3xl p-4 flex items-end gap-4">
        <textarea
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type a message..."
          className="flex-1 px-5 py-3 glass rounded-2xl border-2 border-white/40 focus:border-pink-400 text-brown-900 resize-none"
          rows={1}
          disabled={exchange?.status === 'COMPLETED' || exchange?.status === 'CANCELLED'}
        />
        <Button
          variant="primary"
          size="md"
          onClick={sendMessage}
          disabled={sending || !newMessage.trim() || exchange?.status === 'COMPLETED'}
        >
          {sending ? '...' : '📤 Send'}
        </Button>
      </div>
    </DashboardLayout>
  )
}
