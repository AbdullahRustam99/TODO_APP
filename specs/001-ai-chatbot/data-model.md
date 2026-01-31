# Data Model: AI Chatbot for Todo Management

## Conversation Entity

**Conversation**
- id: UUID (Primary Key)
- user_id: String (Foreign Key to user)
- created_at: DateTime
- updated_at: DateTime
- expires_at: DateTime (Set to 7 days after last activity)

**Message**
- id: UUID (Primary Key)
- conversation_id: UUID (Foreign Key to Conversation)
- role: String (enum: 'user', 'assistant')
- content: String (Text content of the message)
- timestamp: DateTime
- metadata: JSON (Additional data like tool_calls, etc.)

## TaskOperation Entity

**TaskOperation** (Virtual entity for tracking operations)
- id: UUID (Primary Key)
- conversation_id: UUID (Foreign Key to Conversation)
- operation_type: String (enum: 'add_task', 'list_tasks', 'complete_task', 'delete_task', 'update_task')
- operation_params: JSON (Parameters for the operation)
- result: JSON (Result of the operation)
- timestamp: DateTime

## Relationships

- Conversation (1) → Messages (Many)
- Conversation (1) → TaskOperations (Many)
- User (1) → Conversations (Many)

## Validation Rules

1. **Conversation Expiration**: All conversations must expire after 7 days of inactivity
2. **User Isolation**: Users can only access their own conversations and messages
3. **Message Content**: Content must be non-empty and less than 10,000 characters
4. **Operation Parameters**: Must match the expected schema for each operation type

## State Transitions

- Conversation starts when user initiates first chat
- Conversation updated with each message exchange
- Conversation expires after 7 days (handled by cleanup job)