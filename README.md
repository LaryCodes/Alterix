# Alterix - AI-Powered Skill Exchange Platform

> A production-grade, intelligent skill exchange network enabling direct swaps, paid learning, and multi-party exchange chains through advanced AI agent coordination.

## 🎯 Vision

Alterix is not just a marketplace—it's an intelligent skill economy network that uses multi-agent AI systems to create optimal learning and exchange opportunities. The platform enables users to exchange skills through direct swaps or complex multi-hop chains (A → B → C → D), all validated for fairness by AI.

## 🏗️ Architecture Overview

### Three-Layer Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    CLIENT LAYER (Next.js)                   │
│  Premium UI/UX • Glassmorphism • 3D Animations • Real-time  │
└────────────────────────┬────────────────────────────────────┘
                         │ REST/WebSocket
┌────────────────────────┴────────────────────────────────────┐
│              AI ORCHESTRATION LAYER (FastAPI)               │
│  Multi-Agent System • OpenAI Integration • WebSocket Hub    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  AgentMediator (Mediator Pattern)                    │   │
│  │  ├─ MatchingAgent      ├─ ReputationAgent            │   │
│  │  ├─ OptimizationAgent  ├─ RecommendationAgent        │   │ 
│  │  └─ FairnessAgent                                    │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────────┬────────────────────────────────────┘
                         │ gRPC
┌────────────────────────┴────────────────────────────────────┐
│            CORE BUSINESS LAYER (Java)                       │
│  Design Patterns • Matching Engine • Exchange Logic         │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  11 Design Patterns Implemented:                     │   │
│  │  • Singleton    • Factory     • Builder              │   │
│  │  • Adapter      • Bridge      • Composite            │   │
│  │  • Chain        • Command     • Observer             │   │
│  │  • Mediator     • Strategy                           │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────┴────────────────────────────────────┐
│                    DATA LAYER                               │
│  PostgreSQL • Redis • Vector DB (Embeddings)                │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Tech Stack

### Frontend
- **Next.js 14** (App Router) - React framework
- **Tailwind CSS** - Utility-first styling
- **Framer Motion** - Smooth animations
- **Three.js** - 3D graphics and animations
- **TypeScript** - Type safety

### Backend (AI Layer)
- **FastAPI** - High-performance Python API
- **OpenAI SDK** - AI agent capabilities
- **WebSockets** - Real-time communication
- **gRPC** - High-performance RPC with Java

### Core Engine (Java)
- **Java 17** - Core business logic
- **Maven** - Dependency management
- **gRPC** - Service communication
- **SLF4J + Logback** - Logging

### Database
- **PostgreSQL** - Relational data
- **Redis** - Caching and real-time data
- **Vector DB** - Skill embeddings for AI

## 📋 Design Patterns Implementation

### 1. Singleton Pattern
**Location**: `core-engine/src/main/java/com/alterix/core/SystemCore.java`

**Purpose**: Ensures single instance of core system engine

**Usage**:
```java
SystemCore core = SystemCore.getInstance();
core.initialize();
```

### 2. Factory Pattern
**Location**: `core-engine/src/main/java/com/alterix/factory/`

**Purpose**: Abstracts complex object creation

**Usage**:
```java
UserFactory userFactory = new UserFactory();
User user = userFactory.create("user123", "John Doe", "john@example.com");

SkillFactory skillFactory = new SkillFactory();
Skill skill = skillFactory.createTechnicalSkill("skill456", "Java", SkillLevel.ADVANCED);
```

### 3. Builder Pattern
**Location**: `core-engine/src/main/java/com/alterix/builder/ExchangeBuilder.java`

**Purpose**: Constructs complex Exchange objects step-by-step

**Usage**:
```java
Exchange exchange = new ExchangeBuilder()
    .withId("exc_789")
    .withType(ExchangeType.DIRECT_SWAP)
    .addParticipant(user1)
    .addParticipant(user2)
    .addOffering(user1, skill1)
    .addOffering(user2, skill2)
    .scheduleAt(LocalDateTime.now().plusDays(7))
    .build();
```

### 4. Composite Pattern
**Location**: `core-engine/src/main/java/com/alterix/composite/`

**Purpose**: Represents multi-party exchange chains as tree structures

**Usage**:
```java
ExchangeChain chain = new ExchangeChain("chain_123");
chain.add(new ExchangeLeaf(exchangeAB));
chain.add(new ExchangeLeaf(exchangeBC));
chain.add(new ExchangeLeaf(exchangeCD));

if (chain.isValid()) {
    chain.execute(); // Executes entire chain
}
```

### 5. Chain of Responsibility Pattern
**Location**: `core-engine/src/main/java/com/alterix/chain/`

**Purpose**: Filters match candidates through validation pipeline

**Usage**:
```java
MatchingHandler availability = new AvailabilityFilter();
MatchingHandler reputation = new ReputationFilter();
MatchingHandler skillLevel = new SkillLevelFilter();

availability.setNext(reputation);
reputation.setNext(skillLevel);

List<User> filtered = availability.handle(requester, candidates, criteria);
```

### 6. Strategy Pattern
**Location**: `core-engine/src/main/java/com/alterix/strategy/`

**Purpose**: Allows runtime selection of matching algorithms

**Usage**:
```java
MatchingStrategy strategy = new DirectMatchStrategy();
// or
MatchingStrategy strategy = new MultiHopStrategy();

MatchResult result = strategy.findMatches(requester, candidates, skill);
```

### 7. Command Pattern
**Location**: `core-engine/src/main/java/com/alterix/command/`

**Purpose**: Encapsulates skill valuation operations with undo/redo

**Usage**:
```java
Command valuationCmd = new ValuationCommand(skill, newValue);
CommandInvoker invoker = new CommandInvoker();

invoker.executeCommand(valuationCmd);
invoker.undo(); // Revert valuation
invoker.redo(); // Reapply valuation
```

### 8. Observer Pattern
**Location**: `core-engine/src/main/java/com/alterix/observer/`

**Purpose**: Notifies participants of exchange events

**Usage**:
```java
ExchangeSubject subject = new ExchangeSubject(exchange);
subject.attach(new UserNotificationObserver(user1));
subject.attach(new UserNotificationObserver(user2));

subject.notifyExchangeCreated();
subject.notifyStatusChanged(oldStatus, newStatus);
```

### 9. Mediator Pattern
**Location**: `backend/app/agents/mediator.py`

**Purpose**: Coordinates communication between AI agents

**Usage**:
```python
mediator = AgentMediator()
result = await mediator.find_optimal_match(context)
```

### 10. Adapter Pattern
**Location**: `core-engine/src/main/java/com/alterix/adapter/`

**Purpose**: Integrates external services (payment, notifications)

**Usage**:
```java
PaymentAdapter payment = new PaymentAdapter(apiKey, gatewayUrl);
payment.connect();
payment.processPayment(userId, amount, "USD");
```

### 11. Bridge Pattern
**Location**: `core-engine/src/main/java/com/alterix/bridge/`

**Purpose**: Separates matching interface from algorithm implementation

**Usage**:
```java
SkillMatchBridge bridge = new SkillMatchBridge(new CollaborativeFilteringAlgorithm());
List<User> matches = bridge.findMatches(requester, allUsers);

// Switch algorithm at runtime
bridge.setAlgorithm(new ContentBasedAlgorithm());
```

## 🤖 Multi-Agent Intelligence System

### Agent Architecture

```
AgentMediator (Coordinator)
    ├─ MatchingAgent
    │   └─ Finds optimal direct matches
    │       • Skill compatibility scoring
    │       • Trust-based filtering
    │       • Reciprocal interest detection
    │
    ├─ OptimizationAgent
    │   └─ Discovers multi-hop paths
    │       • Graph traversal (DFS)
    │       • Path scoring algorithms
    │       • Chain feasibility analysis
    │
    ├─ FairnessAgent
    │   └─ Validates exchange balance
    │       • Skill valuation
    │       • Price recommendations
    │       • Fairness scoring
    │
    ├─ ReputationAgent
    │   └─ Analyzes trust and behavior
    │       • Trust score calculation
    │       • Fraud detection
    │       • Reputation trends
    │
    └─ RecommendationAgent
        └─ Suggests skills and connections
            • Collaborative filtering
            • Skill path recommendations
            • Personalized suggestions
```

### Agent Communication Flow

1. User request enters system
2. Mediator distributes to relevant agents
3. Agents process in parallel
4. Results aggregated and ranked
5. Best solution returned to user

## 🎨 UI/UX Design Philosophy

### Design Principles
- **Glassmorphism**: Soft, elegant glass-like surfaces
- **Light Palette**: Calming blues and purples
- **Smooth Animations**: Framer Motion for fluid transitions
- **3D Elements**: Three.js for engaging landing page
- **Minimal Friction**: Intuitive user flows

### Color Scheme
```
Primary: Blue (#0ea5e9 - #0c4a6e)
Accent: Purple (#d946ef - #701a75)
Background: Soft gradients with glassmorphism
Text: Dark gray for readability
```

### Key UI Components
- **Skill Cards**: Glassmorphic cards with hover effects
- **Match Results**: Animated list with score indicators
- **Chat Interface**: Clean, modern messaging
- **Dashboard**: Analytics with charts and graphs
- **Trust Visualization**: Interactive network graph

## 📦 Installation & Setup

### Prerequisites
- Node.js 18+
- Python 3.10+
- Java 17+
- Maven 3.8+
- PostgreSQL 14+
- Redis 7+

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
# Runs on http://localhost:3000
```

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
# Runs on http://localhost:8000
```

### Java Core Engine Setup
```bash
cd core-engine
mvn clean install
mvn exec:java -Dexec.mainClass="com.alterix.core.SystemCore"
```

### Database Setup
```sql
CREATE DATABASE alterix;
-- Run migrations from database/migrations/
```

### Environment Variables
```env
# Backend (.env)
DATABASE_URL=postgresql://user:pass@localhost:5432/alterix
REDIS_URL=redis://localhost:6379
OPENAI_API_KEY=your_key_here
JAVA_GRPC_HOST=localhost:50051

# Frontend (.env.local)
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🚀 Running the Full Stack

### Using Docker Compose
```bash
docker-compose up -d
```

### Manual Start
```bash
# Terminal 1: Java Core
cd core-engine && mvn exec:java

# Terminal 2: FastAPI Backend
cd backend && uvicorn app.main:app --reload

# Terminal 3: Next.js Frontend
cd frontend && npm run dev
```

## 📊 Project Structure

See [PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md) for detailed breakdown.

## 🔄 Complete Workflow

See [WORKFLOW.md](./WORKFLOW.md) for end-to-end user journey.

## 🏛️ System Architecture

See [ARCHITECTURE.md](./ARCHITECTURE.md) for technical details.

## 🧪 Testing

```bash
# Java tests
cd core-engine && mvn test

# Python tests
cd backend && pytest

# Frontend tests
cd frontend && npm test
```

## 📈 Performance Metrics

- **Match Finding**: < 500ms for direct matches
- **Multi-Hop Pathfinding**: < 2s for 4-hop chains
- **WebSocket Latency**: < 50ms
- **API Response Time**: < 200ms (p95)
- **Database Queries**: Optimized with indexes

## 🔒 Security

- JWT-based authentication
- End-to-end encrypted chat
- Rate limiting on all endpoints
- SQL injection prevention
- XSS protection
- CORS configuration
- Input validation at all layers

## 🌟 Premium Features

1. **Multi-Hop Exchange Engine**: Advanced pathfinding
2. **AI Negotiation Assistant**: Smart suggestions
3. **Trust Graph Visualization**: Interactive network view
4. **Analytics Dashboard**: Comprehensive insights
5. **Priority Matching**: Faster results
6. **Skill Valuation System**: Market-based pricing

## 📝 License

MIT License - See LICENSE file

## 👥 Contributing

This is a production-grade system. Contributions welcome following our coding standards.

## 📧 Contact

For questions or support, contact: support@alterix.com

---

**Built with ❤️ using Java, Python, and TypeScript**

**Alterix - Where Skills Meet Intelligence**
