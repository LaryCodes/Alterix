# Alterix - Project Structure

```
alterix/
├── frontend/                          # Next.js Application
│   ├── app/
│   │   ├── (auth)/
│   │   │   ├── login/
│   │   │   └── register/
│   │   ├── (dashboard)/
│   │   │   ├── dashboard/
│   │   │   ├── skills/
│   │   │   ├── matches/
│   │   │   ├── exchanges/
│   │   │   ├── chat/
│   │   │   └── analytics/
│   │   ├── layout.tsx
│   │   └── page.tsx                   # Landing page with 3D
│   ├── components/
│   │   ├── ui/                        # Reusable UI components
│   │   ├── three/                     # Three.js 3D components
│   │   ├── animations/                # Framer Motion animations
│   │   ├── chat/                      # Chat interface
│   │   └── dashboard/                 # Dashboard components
│   ├── lib/
│   │   ├── api.ts                     # API client
│   │   ├── websocket.ts               # WebSocket client
│   │   └── utils.ts
│   ├── styles/
│   │   └── globals.css
│   └── package.json
│
├── backend/                           # FastAPI AI Layer
│   ├── app/
│   │   ├── agents/
│   │   │   ├── __init__.py
│   │   │   ├── base_agent.py
│   │   │   ├── matching_agent.py
│   │   │   ├── optimization_agent.py
│   │   │   ├── fairness_agent.py
│   │   │   ├── reputation_agent.py
│   │   │   ├── recommendation_agent.py
│   │   │   └── mediator.py            # Agent Mediator Pattern
│   │   ├── api/
│   │   │   ├── v1/
│   │   │   │   ├── auth.py
│   │   │   │   ├── users.py
│   │   │   │   ├── skills.py
│   │   │   │   ├── matches.py
│   │   │   │   ├── exchanges.py
│   │   │   │   ├── chat.py
│   │   │   │   └── sessions.py
│   │   │   └── websocket.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   └── grpc_client.py         # Java gRPC client
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── skill.py
│   │   │   ├── exchange.py
│   │   │   └── session.py
│   │   ├── services/
│   │   │   ├── openai_service.py
│   │   │   ├── embedding_service.py
│   │   │   └── notification_service.py
│   │   └── main.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── core-engine/                       # Java Core Business Logic
│   ├── src/
│   │   ├── main/
│   │   │   ├── java/
│   │   │   │   └── com/
│   │   │   │       └── alterix/
│   │   │   │           ├── core/
│   │   │   │           │   ├── SystemCore.java              # Singleton
│   │   │   │           │   ├── config/
│   │   │   │           │   └── exceptions/
│   │   │   │           ├── factory/
│   │   │   │           │   ├── UserFactory.java             # Factory
│   │   │   │           │   ├── SkillFactory.java            # Factory
│   │   │   │           │   └── AbstractEntityFactory.java
│   │   │   │           ├── builder/
│   │   │   │           │   ├── ExchangeBuilder.java         # Builder
│   │   │   │           │   ├── TrustGraphBuilder.java       # Builder
│   │   │   │           │   └── MatchCriteriaBuilder.java
│   │   │   │           ├── adapter/
│   │   │   │           │   ├── PaymentAdapter.java          # Adapter
│   │   │   │           │   ├── NotificationAdapter.java
│   │   │   │           │   └── ExternalServiceAdapter.java
│   │   │   │           ├── bridge/
│   │   │   │           │   ├── SkillMatchBridge.java        # Bridge
│   │   │   │           │   ├── MatchingAlgorithm.java
│   │   │   │           │   └── implementations/
│   │   │   │           ├── composite/
│   │   │   │           │   ├── ExchangeComponent.java       # Composite
│   │   │   │           │   ├── ExchangeChain.java
│   │   │   │           │   └── ExchangeLeaf.java
│   │   │   │           ├── chain/
│   │   │   │           │   ├── MatchingHandler.java         # Chain of Resp.
│   │   │   │           │   ├── AvailabilityFilter.java
│   │   │   │           │   ├── LocationFilter.java
│   │   │   │           │   ├── SkillLevelFilter.java
│   │   │   │           │   └── ReputationFilter.java
│   │   │   │           ├── command/
│   │   │   │           │   ├── Command.java                 # Command
│   │   │   │           │   ├── ValuationCommand.java
│   │   │   │           │   ├── CommandInvoker.java
│   │   │   │           │   └── commands/
│   │   │   │           ├── observer/
│   │   │   │           │   ├── ExchangeObserver.java        # Observer
│   │   │   │           │   ├── ExchangeSubject.java
│   │   │   │           │   └── observers/
│   │   │   │           ├── mediator/
│   │   │   │           │   ├── AgentMediator.java           # Mediator
│   │   │   │           │   ├── Agent.java
│   │   │   │           │   └── ConcreteMediator.java
│   │   │   │           ├── strategy/
│   │   │   │           │   ├── MatchingStrategy.java        # Strategy
│   │   │   │           │   ├── DirectMatchStrategy.java
│   │   │   │           │   ├── MultiHopStrategy.java
│   │   │   │           │   └── HybridMatchStrategy.java
│   │   │   │           ├── models/
│   │   │   │           │   ├── User.java
│   │   │   │           │   ├── Skill.java
│   │   │   │           │   ├── Exchange.java
│   │   │   │           │   ├── TrustScore.java
│   │   │   │           │   └── MatchResult.java
│   │   │   │           ├── services/
│   │   │   │           │   ├── MatchingService.java
│   │   │   │           │   ├── ExchangeService.java
│   │   │   │           │   ├── ValuationService.java
│   │   │   │           │   └── TrustService.java
│   │   │   │           └── grpc/
│   │   │   │               ├── MatchingServiceImpl.java
│   │   │   │               ├── ExchangeServiceImpl.java
│   │   │   │               └── server/
│   │   │   ├── proto/
│   │   │   │   ├── matching.proto
│   │   │   │   ├── exchange.proto
│   │   │   │   └── valuation.proto
│   │   │   └── resources/
│   │   │       └── application.properties
│   │   └── test/
│   │       └── java/
│   │           └── com/
│   │               └── alterix/
│   ├── pom.xml
│   └── Dockerfile
│
├── database/
│   ├── migrations/
│   ├── seeds/
│   └── schema.sql
│
├── docker-compose.yml
├── .env.example
└── README.md
```

## Module Descriptions

### Frontend (Next.js)
- **app/**: App router structure with route groups
- **components/ui/**: Glassmorphism cards, buttons, inputs
- **components/three/**: 3D animated elements for landing
- **components/animations/**: Framer Motion wrappers
- **lib/**: API client, WebSocket manager, utilities

### Backend (FastAPI)
- **agents/**: Multi-agent system with mediator coordination
- **api/v1/**: RESTful endpoints for all resources
- **core/**: Configuration, security, gRPC client
- **services/**: OpenAI integration, embeddings, notifications

### Core Engine (Java)
- **core/**: Singleton system core, configuration
- **factory/**: User and Skill object creation
- **builder/**: Complex object construction (exchanges, trust graphs)
- **adapter/**: External service integration layer
- **bridge/**: Matching algorithm abstraction
- **composite/**: Multi-party exchange tree structure
- **chain/**: Sequential matching filters pipeline
- **command/**: Skill valuation command pattern
- **observer/**: Event notification system
- **mediator/**: Agent coordination (used by FastAPI)
- **strategy/**: Pluggable matching algorithms
- **services/**: Business logic services
- **grpc/**: gRPC server implementations

## Design Pattern Usage Summary

Each pattern serves a specific architectural purpose:

1. **Singleton**: Ensures single instance of core system
2. **Factory**: Abstracts complex object creation
3. **Builder**: Constructs complex exchanges step-by-step
4. **Adapter**: Integrates external payment/notification services
5. **Bridge**: Separates matching interface from implementation
6. **Composite**: Represents multi-party exchange chains as trees
7. **Chain of Responsibility**: Filters matches through validation pipeline
8. **Command**: Encapsulates valuation operations
9. **Observer**: Notifies participants of exchange events
10. **Mediator**: Coordinates agent communication
11. **Strategy**: Allows runtime selection of matching algorithms
