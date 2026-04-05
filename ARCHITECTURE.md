# Alterix - System Architecture Document

## Executive Summary
Alterix is an AI-powered skill exchange platform enabling direct swaps, paid learning, and multi-party exchange chains through intelligent agent coordination.

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                             │
│  Next.js 14 (App Router) + Tailwind + Framer Motion + Three.js  │
└────────────────────┬────────────────────────────────────────────┘
                     │ REST/WebSocket
┌────────────────────┴────────────────────────────────────────────┐
│                     API GATEWAY LAYER                           │
│              FastAPI (Python) - AI Orchestration                │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Agent Coordinator (Mediator Pattern)                    │   │
│  │  ├─ Matching Agent      ├─ Reputation Agent              │   │
│  │  ├─ Optimization Agent  ├─ Recommendation Agent          │   │ 
│  │  └─ Fairness Agent                                       │   │
│  └──────────────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────────────┘
                     │ gRPC/REST
┌────────────────────┴────────────────────────────────────────────┐
│                   CORE BUSINESS LAYER (JAVA)                    │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Exchange Engine (Chain of Responsibility)               │   │
│  │  Matching Engine (Strategy + Composite)                  │   │
│  │  Skill Valuation System (Command Pattern)                │   │
│  │  Trust Graph Builder (Builder + Composite)               │   │
│  │  System Core (Singleton)                                 │   │
│  └──────────────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────────────┘
                     │
┌────────────────────┴─────────────────────────────────────────────┐
│                     DATA LAYER                                   │
│  PostgreSQL (Relational) + Redis (Cache) + Vector DB (Embeddings)│
└──────────────────────────────────────────────────────────────────┘
```

## Layer Responsibilities

### 1. Client Layer (Next.js)
- Premium UI/UX with glassmorphism
- Real-time updates via WebSocket
- 3D landing page animations
- Responsive dashboard and chat interface

### 2. AI Orchestration Layer (FastAPI)
- Multi-agent coordination
- Real-time communication hub
- OpenAI integration
- WebSocket management

### 3. Core Business Layer (Java)
- Design pattern implementations
- Exchange matching algorithms
- Skill valuation logic
- Trust graph computation
- System architecture backbone

### 4. Data Layer
- PostgreSQL: Users, skills, exchanges, sessions
- Redis: Real-time data, caching
- Vector DB: Skill embeddings for AI matching

## Design Pattern Mapping

| Pattern | Module | Purpose |
|---------|--------|---------|
| Singleton | SystemCore | Single instance of core engine |
| Factory | UserFactory, SkillFactory | Object creation abstraction |
| Builder | ExchangeBuilder, TrustGraphBuilder | Complex object construction |
| Adapter | PaymentAdapter, NotificationAdapter | External service integration |
| Bridge | SkillMatchBridge | Decouple matching algorithms |
| Composite | ExchangeChainComposite | Multi-party exchange trees |
| Chain of Responsibility | MatchingPipeline | Sequential matching filters |
| Command | ValuationCommand | Encapsulate skill valuation |
| Observer | ExchangeObserver | Event notification system |
| Mediator | AgentMediator | Agent communication coordination |
| Strategy | MatchingStrategy | Pluggable matching algorithms |

## Multi-Agent Intelligence System

### Agent Architecture
```
AgentMediator (Coordinator)
    ├─ MatchingAgent: Finds optimal matches using graph algorithms
    ├─ OptimizationAgent: Selects best exchange paths (A→B→C)
    ├─ FairnessAgent: Validates value equality in exchanges
    ├─ ReputationAgent: Analyzes user trust scores
    └─ RecommendationAgent: Suggests skills and connections
```

### Agent Communication Flow
1. User request enters system
2. Mediator distributes to relevant agents
3. Agents process in parallel
4. Results aggregated and ranked
5. Best solution returned to user

## Data Flow: Complete Exchange Lifecycle

```
1. User Registration
   └─> UserFactory creates User entity
   └─> Profile stored in PostgreSQL
   └─> Skill embeddings generated

2. Skill Listing
   └─> SkillFactory creates Skill entity
   └─> Validation through Chain of Responsibility
   └─> Indexed in Vector DB

3. Match Request
   └─> Request enters MatchingPipeline (Chain)
   └─> Filters: Availability → Location → Skill Level
   └─> MatchingAgent finds candidates
   └─> OptimizationAgent ranks by multi-hop potential
   └─> FairnessAgent validates value balance

4. Exchange Creation
   └─> ExchangeBuilder constructs exchange object
   └─> For multi-party: ExchangeChainComposite builds graph
   └─> Observers notified (all participants)

5. Negotiation
   └─> WebSocket real-time chat
   └─> AI suggests negotiation points
   └─> Command pattern for valuation adjustments

6. Session Execution
   └─> Session scheduled
   └─> Observers track completion
   └─> ReputationAgent updates trust scores

7. Rating & Completion
   └─> Trust graph updated
   └─> RecommendationAgent learns from interaction
```

## API Structure

### FastAPI Endpoints
```
/api/v1/auth/*          - Authentication
/api/v1/users/*         - User management
/api/v1/skills/*        - Skill CRUD
/api/v1/matches/*       - AI matching
/api/v1/exchanges/*     - Exchange management
/api/v1/chat/*          - Real-time messaging
/api/v1/sessions/*      - Session scheduling
/api/v1/analytics/*     - User analytics
/ws/chat                - WebSocket chat
/ws/notifications       - WebSocket notifications
```

### Java Core Services (gRPC)
```
MatchingService         - Core matching logic
ExchangeService         - Exchange chain building
ValuationService        - Skill value computation
TrustService            - Trust graph operations
```

## Technology Integration Points

### Java ↔ FastAPI Communication
- gRPC for high-performance RPC calls
- Java services expose gRPC endpoints
- FastAPI acts as gRPC client
- Protobuf for serialization

### FastAPI ↔ Next.js Communication
- REST API for standard operations
- WebSocket for real-time features
- JWT authentication
- Server-Sent Events for notifications

## Scalability Considerations

1. **Horizontal Scaling**: Stateless services, load balancing
2. **Caching Strategy**: Redis for hot data, CDN for static assets
3. **Database Optimization**: Indexing, connection pooling, read replicas
4. **Async Processing**: Message queues for heavy computations
5. **Microservices Ready**: Clear service boundaries for future decomposition

## Security Architecture

- JWT-based authentication
- Role-based access control (RBAC)
- End-to-end encryption for chat
- Rate limiting on all endpoints
- Input validation at all layers
- SQL injection prevention
- XSS protection

## Monitoring & Observability

- Structured logging (ELK stack)
- Metrics collection (Prometheus)
- Distributed tracing (Jaeger)
- Health check endpoints
- Performance monitoring
