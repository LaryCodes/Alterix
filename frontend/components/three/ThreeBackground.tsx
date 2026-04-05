'use client'

import { useRef, useMemo } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import * as THREE from 'three'

function FloatingShape({ position, geometry, color, speed, scale }: any) {
  const meshRef = useRef<THREE.Mesh>(null)
  
  useFrame((state) => {
    if (meshRef.current) {
      meshRef.current.position.y = position[1] + Math.sin(state.clock.elapsedTime * speed) * 0.8
      meshRef.current.position.x = position[0] + Math.cos(state.clock.elapsedTime * speed * 0.5) * 0.5
      meshRef.current.rotation.x += 0.003
      meshRef.current.rotation.y += 0.005
      meshRef.current.rotation.z += 0.002
    }
  })
  
  return (
    <mesh ref={meshRef} position={position} scale={scale}>
      {geometry}
      <meshStandardMaterial
        color={color}
        roughness={0.1}
        metalness={0.9}
        transparent
        opacity={0.7}
        emissive={color}
        emissiveIntensity={0.2}
      />
    </mesh>
  )
}

function ParticleField() {
  const particlesRef = useRef<THREE.Points>(null)
  
  const particles = useMemo(() => {
    const temp = []
    for (let i = 0; i < 100; i++) {
      const x = (Math.random() - 0.5) * 30
      const y = (Math.random() - 0.5) * 30
      const z = (Math.random() - 0.5) * 30
      temp.push(x, y, z)
    }
    return new Float32Array(temp)
  }, [])
  
  useFrame((state) => {
    if (particlesRef.current) {
      particlesRef.current.rotation.y = state.clock.elapsedTime * 0.05
    }
  })
  
  return (
    <points ref={particlesRef}>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          count={particles.length / 3}
          array={particles}
          itemSize={3}
        />
      </bufferGeometry>
      <pointsMaterial
        size={0.05}
        color="#fbcfe8"
        transparent
        opacity={0.6}
        sizeAttenuation
      />
    </points>
  )
}

function Scene() {
  const shapes = useMemo(() => [
    { 
      position: [-5, 2, -8], 
      geometry: <torusGeometry args={[1, 0.4, 16, 100]} />,
      color: '#fbcfe8', 
      speed: 0.4,
      scale: 1.2
    },
    { 
      position: [5, -2, -10], 
      geometry: <octahedronGeometry args={[1.5, 0]} />,
      color: '#bfa094', 
      speed: 0.5,
      scale: 1
    },
    { 
      position: [0, 4, -7], 
      geometry: <icosahedronGeometry args={[1, 0]} />,
      color: '#f9a8d4', 
      speed: 0.6,
      scale: 1.3
    },
    { 
      position: [-3, -3, -9], 
      geometry: <sphereGeometry args={[1, 32, 32]} />,
      color: '#d2bab0', 
      speed: 0.7,
      scale: 1.1
    },
    { 
      position: [4, 1, -6], 
      geometry: <torusKnotGeometry args={[0.8, 0.3, 100, 16]} />,
      color: '#fce7f3', 
      speed: 0.45,
      scale: 0.9
    },
    { 
      position: [-4, -1, -11], 
      geometry: <dodecahedronGeometry args={[1.2, 0]} />,
      color: '#977669', 
      speed: 0.55,
      scale: 1
    },
  ], [])
  
  return (
    <>
      <ambientLight intensity={0.6} />
      <pointLight position={[10, 10, 10]} intensity={1.5} color="#fbcfe8" />
      <pointLight position={[-10, -10, -10]} intensity={1} color="#bfa094" />
      <pointLight position={[0, 10, 5]} intensity={0.8} color="#f9a8d4" />
      <spotLight position={[5, 5, 5]} angle={0.3} penumbra={1} intensity={1} color="#fce7f3" />
      
      <ParticleField />
      
      {shapes.map((shape, index) => (
        <FloatingShape key={index} {...shape} />
      ))}
    </>
  )
}

export default function ThreeBackground() {
  return (
    <div className="fixed inset-0 -z-10 opacity-40">
      <Canvas camera={{ position: [0, 0, 12], fov: 60 }}>
        <Scene />
      </Canvas>
    </div>
  )
}
