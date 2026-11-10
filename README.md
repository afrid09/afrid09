# Hi, I'm Afrid 👋

**Backend Software Engineer · Distributed Systems & Reliability**

I'm a software engineer with 5+ years of experience building backend systems, event-driven microservices, and cloud-native platforms, including at Apple and Accenture.

I focus on systems that **don't lose or duplicate data**: idempotent workflows, the transactional outbox pattern, safe retries and dead-letter queues, careful database concurrency, and end-to-end tracing.

### 🔧 What I work on
- **Reliable data pipelines:** idempotent writes, transactional outbox, exactly-once-effect processing
- **Event-driven systems:** Kafka, AWS SQS/SNS, retries, DLQs, failure classification
- **Database correctness:** PostgreSQL row-level locking, savepoints, safe schema migrations
- **Observability:** OpenTelemetry distributed tracing across APIs and async workers
- **Cloud infrastructure:** AWS, Docker, Kubernetes, Terraform

### 🛠️ Tech stack
| Area | Tools |
|---|---|
| Languages | Java 17, Python, TypeScript, Go |
| Backend | Spring Boot, Spring Security, FastAPI, Pydantic, Node/Express, REST, gRPC, OpenAPI |
| Data | PostgreSQL, PostGIS, Oracle, MongoDB, Redis, Alembic |
| Messaging | Apache Kafka, AWS SQS/SNS, RabbitMQ, Kinesis |
| Cloud & DevOps | AWS (Lambda, Step Functions, EC2, S3, RDS), Docker, Kubernetes (EKS), Helm, Terraform, GitHub Actions |
| Observability | OpenTelemetry, Prometheus, Grafana, CloudWatch |

### 🚀 Featured projects
**[reliable-orders](https://github.com/afrid09/reliable-orders)**: an order service that never loses or duplicates data, even when clients retry, processes crash and Kafka redelivers. Idempotency keys enforced by PostgreSQL, a transactional outbox to Kafka, exactly-once effects on top of at-least-once delivery, retries with a dead-letter topic, and one OpenTelemetry trace across the async gap. Every guarantee is proven by tests against real Postgres and Kafka. *Java 17 · Spring Boot · Kafka · Testcontainers*

**[FieldFlow](https://github.com/afrid09/FieldFlow)**: multi-service agriculture platform with separate read and write services, an API gateway with WebSocket fan-out, a background enrichment worker and PostGIS geo queries. Ships with OpenTelemetry tracing, Prometheus/Grafana/Loki/Tempo, Kubernetes and Helm manifests, backups with restore validation, and runbooks. *TypeScript · Node · Next.js · PostGIS*

### 🌱 Currently
- Getting into open source in the **workflow orchestration** space (Cadence, Temporal)

### 🎓 Credentials
- M.S. Computer Science, Texas A&M University–Kingsville
- AWS Certified Solutions Architect – Associate · Certified Kubernetes Administrator (CKA) · Oracle Certified Professional Java SE Developer

### 📫 Connect
- LinkedIn: [linkedin.com/in/afrid-abdul-shaik](https://www.linkedin.com/in/afrid-abdul-shaik/)
