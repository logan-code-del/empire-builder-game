Development Guide
=================

This guide covers development setup, architecture, coding standards, and contribution guidelines for Empire Builder.

Development Environment Setup
------------------------------

Prerequisites
~~~~~~~~~~~~~

**Required Software:**
- Python 3.11+
- Git
- Code editor (VS Code recommended)
- Supabase account

**Recommended Tools:**
- Docker (for containerized development)
- Postman (for API testing)
- pgAdmin (for database management)

Initial Setup
~~~~~~~~~~~~~

1. **Fork and Clone**

   .. code-block:: bash

      # Fork the repository on GitHub
      git clone https://github.com/your-username/strategic-pro.git
      cd strategic-pro/empire

2. **Create Development Environment**

   .. code-block:: bash

      # Create virtual environment
      python -m venv empire-dev
      
      # Activate environment
      # Windows:
      empire-dev\Scripts\activate
      # macOS/Linux:
      source empire-dev/bin/activate

3. **Install Dependencies**

   .. code-block:: bash

      # Install main dependencies
      pip install -r requirements.txt
      
      # Install development dependencies
      pip install -r requirements-dev.txt  # If available

4. **Set Up Development Database**

   Create a separate Supabase project for development:
   - Use ``dev-empire-builder`` as project name
   - Run the schema from ``supabase_auth_schema_uuid.sql``
   - Configure ``.env`` with development credentials

5. **Configure Pre-commit Hooks**

   .. code-block:: bash

      pip install pre-commit
      pre-commit install

Project Architecture
--------------------

Directory Structure
~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   empire/
   ├── app_supabase.py          # Main Flask application
   ├── models_supabase.py       # Database models and game logic
   ├── auth_supabase.py         # Authentication system
   ├── ai_system.py             # AI opponents and automation
   ├── supabase_config.py       # Database configuration
   ├── templates/               # Jinja2 HTML templates
   │   ├── base.html           # Base template
   │   ├── dashboard.html      # Game dashboard
   │   ├── login.html          # Login page
   │   └── register.html       # Registration page
   ├── static/                  # Static assets
   │   ├── css/                # Stylesheets
   │   ├── js/                 # JavaScript files
   │   └── images/             # Image assets
   ├── tests/                   # Unit tests
   │   ├── test_auth.py        # Authentication tests
   │   ├── test_models.py      # Model tests
   │   └── test_api.py         # API tests
   ├── docs/                    # Documentation
   ├── debug_*.py              # Debug and testing scripts
   ├── requirements.txt        # Python dependencies
   ├── .env.template          # Environment template
   └── README.md              # Project README

Core Components
~~~~~~~~~~~~~~~

**app_supabase.py**
- Flask application factory
- Route definitions
- WebSocket event handlers
- Middleware configuration

**models_supabase.py**
- Database models (Empire, City, Unit, Battle)
- Game logic and business rules
- Data validation and processing
- Supabase integration

**auth_supabase.py**
- User authentication
- Session management
- Password hashing and verification
- Authorization decorators

**ai_system.py**
- AI opponent behavior
- Automated game actions
- Decision-making algorithms
- Performance optimization

**supabase_config.py**
- Database connection management
- Configuration loading
- Client initialization
- Error handling

Coding Standards
----------------

Python Style Guide
~~~~~~~~~~~~~~~~~~

**PEP 8 Compliance:**
- Line length: 88 characters (Black formatter)
- Indentation: 4 spaces
- Import organization: stdlib, third-party, local
- Function and variable names: snake_case
- Class names: PascalCase
- Constants: UPPER_CASE

**Type Hints:**

.. code-block:: python

   from typing import Optional, List, Dict, Any

   def create_empire(name: str, owner_id: str) -> Optional[str]:
       """Create a new empire and return its ID."""
       # Implementation
       return empire_id

**Docstrings:**

.. code-block:: python

   def calculate_battle_outcome(attacker: Army, defender: Army) -> BattleResult:
       """
       Calculate the outcome of a battle between two armies.
       
       Args:
           attacker: The attacking army
           defender: The defending army
           
       Returns:
           BattleResult containing winner, casualties, and loot
           
       Raises:
           ValueError: If armies are invalid or empty
       """
       # Implementation

**Error Handling:**

.. code-block:: python

   def get_empire_by_id(empire_id: str) -> Optional[Empire]:
       """Get empire by ID with proper error handling."""
       try:
           result = client.table('empires').select('*').eq('id', empire_id).execute()
           if result.data:
               return Empire.from_dict(result.data[0])
           return None
       except Exception as e:
           logger.error(f"Failed to get empire {empire_id}: {e}")
           return None

Database Design Patterns
~~~~~~~~~~~~~~~~~~~~~~~~~

**Model Classes:**

.. code-block:: python

   @dataclass
   class Empire:
       id: str
       name: str
       owner_id: str
       created_at: str
       resources: Dict[str, int]
       
       @classmethod
       def from_dict(cls, data: Dict[str, Any]) -> 'Empire':
           """Create Empire from database row."""
           return cls(
               id=data['id'],
               name=data['name'],
               owner_id=data['owner_id'],
               created_at=data['created_at'],
               resources=json.loads(data['resources'])
           )
       
       def to_dict(self) -> Dict[str, Any]:
           """Convert Empire to database format."""
           return {
               'id': self.id,
               'name': self.name,
               'owner_id': self.owner_id,
               'created_at': self.created_at,
               'resources': json.dumps(self.resources)
           }

**Database Operations:**

.. code-block:: python

   class EmpireDatabase:
       def __init__(self, client):
           self.client = client
       
       def create_empire(self, empire: Empire) -> bool:
           """Create new empire in database."""
           try:
               result = self.client.table('empires').insert(
                   empire.to_dict()
               ).execute()
               return bool(result.data)
           except Exception as e:
               logger.error(f"Failed to create empire: {e}")
               return False

Frontend Development
~~~~~~~~~~~~~~~~~~~~

**HTML Templates:**

.. code-block:: html

   <!-- Use semantic HTML -->
   <main class="dashboard">
       <section class="empire-overview">
           <h2>{{ empire.name }}</h2>
           <div class="resources">
               <span class="gold">{{ empire.resources.gold }}</span>
               <span class="food">{{ empire.resources.food }}</span>
           </div>
       </section>
   </main>

**JavaScript Standards:**

.. code-block:: javascript

   // Use modern ES6+ syntax
   class GameClient {
       constructor(apiUrl) {
           this.apiUrl = apiUrl;
           this.socket = io();
       }
       
       async getEmpire(empireId) {
           try {
               const response = await fetch(`${this.apiUrl}/empire/${empireId}`);
               return await response.json();
           } catch (error) {
               console.error('Failed to get empire:', error);
               return null;
           }
       }
   }

**CSS Organization:**

.. code-block:: css

   /* Use BEM methodology */
   .dashboard {
       display: grid;
       grid-template-columns: 1fr 3fr 1fr;
       gap: 1rem;
   }
   
   .dashboard__sidebar {
       background: var(--sidebar-bg);
   }
   
   .dashboard__main {
       padding: 1rem;
   }

Testing Guidelines
------------------

Test Structure
~~~~~~~~~~~~~~

**Unit Tests:**

.. code-block:: python

   import unittest
   from unittest.mock import patch, MagicMock
   from models_supabase import Empire, EmpireDatabase

   class TestEmpireDatabase(unittest.TestCase):
       def setUp(self):
           """Set up test fixtures."""
           self.mock_client = MagicMock()
           self.db = EmpireDatabase(self.mock_client)
       
       def test_create_empire_success(self):
           """Test successful empire creation."""
           # Arrange
           empire = Empire(
               id='test-id',
               name='Test Empire',
               owner_id='user-id',
               created_at='2024-01-01T00:00:00Z',
               resources={'gold': 1000}
           )
           self.mock_client.table.return_value.insert.return_value.execute.return_value.data = [empire.to_dict()]
           
           # Act
           result = self.db.create_empire(empire)
           
           # Assert
           self.assertTrue(result)
           self.mock_client.table.assert_called_with('empires')

**Integration Tests:**

.. code-block:: python

   class TestEmpireAPI(unittest.TestCase):
       def setUp(self):
           """Set up test client."""
           self.app = create_app(testing=True)
           self.client = self.app.test_client()
           self.ctx = self.app.app_context()
           self.ctx.push()
       
       def tearDown(self):
           """Clean up test context."""
           self.ctx.pop()
       
       def test_create_empire_endpoint(self):
           """Test empire creation API endpoint."""
           response = self.client.post('/api/empire', json={
               'name': 'Test Empire'
           })
           self.assertEqual(response.status_code, 201)

**Running Tests:**

.. code-block:: bash

   # Run all tests
   python -m unittest discover tests

   # Run specific test file
   python -m unittest tests.test_models

   # Run with coverage
   pip install coverage
   coverage run -m unittest discover tests
   coverage report

Mock and Fixtures
~~~~~~~~~~~~~~~~~

**Database Mocking:**

.. code-block:: python

   @patch('supabase_config.get_supabase_client')
   def test_with_mocked_db(self, mock_get_client):
       """Test with mocked database client."""
       mock_client = MagicMock()
       mock_get_client.return_value = mock_client
       
       # Test implementation
       result = some_database_operation()
       
       # Verify mock calls
       mock_client.table.assert_called_with('expected_table')

**Test Fixtures:**

.. code-block:: python

   class TestFixtures:
       @staticmethod
       def create_test_empire() -> Empire:
           """Create test empire fixture."""
           return Empire(
               id='test-empire-id',
               name='Test Empire',
               owner_id='test-user-id',
               created_at='2024-01-01T00:00:00Z',
               resources={'gold': 1000, 'food': 500, 'materials': 200}
           )

Debugging and Profiling
-----------------------

Debug Scripts
~~~~~~~~~~~~~

The project includes several debug scripts:

**debug_registration.py**
- Tests user registration flow
- Validates database connections
- Checks authentication system

**debug_login.py**
- Tests login functionality
- Validates session creation
- Checks password verification

**test_simple_connection.py**
- Basic connectivity tests
- Environment validation
- Supabase client testing

**Usage:**

.. code-block:: bash

   # Test registration system
   python debug_registration.py

   # Test login with specific credentials
   python debug_login.py

   # Test basic connectivity
   python test_simple_connection.py

Logging Configuration
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import logging

   # Configure logging
   logging.basicConfig(
       level=logging.INFO,
       format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
       handlers=[
           logging.FileHandler('empire.log'),
           logging.StreamHandler()
       ]
   )

   logger = logging.getLogger(__name__)

   # Usage in code
   logger.info("Empire created: %s", empire.name)
   logger.error("Failed to create empire: %s", str(e))

Performance Profiling
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import cProfile
   import pstats

   def profile_function():
       """Profile a specific function."""
       profiler = cProfile.Profile()
       profiler.enable()
       
       # Code to profile
       result = expensive_operation()
       
       profiler.disable()
       stats = pstats.Stats(profiler)
       stats.sort_stats('cumulative')
       stats.print_stats(10)  # Top 10 functions

Database Development
--------------------

Schema Management
~~~~~~~~~~~~~~~~~

**Migration Scripts:**
Create migration scripts for database changes:

.. code-block:: sql

   -- migrations/001_add_alliance_table.sql
   CREATE TABLE alliances (
       id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
       name VARCHAR(100) UNIQUE NOT NULL,
       leader_id UUID REFERENCES users(id),
       created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
       description TEXT
   );

**Schema Validation:**

.. code-block:: python

   def validate_schema():
       """Validate database schema matches expectations."""
       required_tables = ['users', 'empires', 'cities', 'battles']
       
       for table in required_tables:
           result = client.table(table).select('count').limit(1).execute()
           assert result.data is not None, f"Table {table} not found"

Local Development
~~~~~~~~~~~~~~~~~

**SQLite Fallback:**
For offline development, implement SQLite fallback:

.. code-block:: python

   def get_database_client():
       """Get database client with fallback."""
       try:
           return get_supabase_client()
       except Exception:
           logger.warning("Using SQLite fallback")
           return get_sqlite_client()

**Test Data Generation:**

.. code-block:: python

   def create_test_data():
       """Generate test data for development."""
       # Create test users
       test_users = [
           {'username': 'player1', 'email': 'player1@test.com'},
           {'username': 'player2', 'email': 'player2@test.com'}
       ]
       
       for user_data in test_users:
           create_test_user(user_data)

Deployment Considerations
-------------------------

Environment Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~

**Production Settings:**

.. code-block:: bash

   # .env.production
   DEBUG=False
   SECRET_KEY=production-secret-key-very-long-and-random
   SUPABASE_URL=https://prod-project.supabase.co
   SUPABASE_ANON_KEY=prod-anon-key
   SUPABASE_SERVICE_KEY=prod-service-key

**Docker Configuration:**

.. code-block:: dockerfile

   FROM python:3.11-slim

   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt

   COPY . .
   EXPOSE 5000

   CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app_supabase:app"]

Performance Optimization
~~~~~~~~~~~~~~~~~~~~~~~~

**Database Optimization:**
- Add indexes to frequently queried columns
- Use connection pooling
- Implement query result caching

**Application Optimization:**
- Use Redis for session storage
- Implement API rate limiting
- Add CDN for static assets

Contributing Workflow
---------------------

Development Process
~~~~~~~~~~~~~~~~~~~

1. **Create Feature Branch**

   .. code-block:: bash

      git checkout -b feature/alliance-system

2. **Implement Changes**
   - Write code following style guidelines
   - Add comprehensive tests
   - Update documentation

3. **Test Thoroughly**

   .. code-block:: bash

      # Run tests
      python -m unittest discover tests
      
      # Check code style
      black --check .
      flake8 .
      
      # Test manually
      python app_supabase.py

4. **Commit Changes**

   .. code-block:: bash

      git add .
      git commit -m "feat: add alliance system with member management"

5. **Push and Create PR**

   .. code-block:: bash

      git push origin feature/alliance-system

Pull Request Guidelines
~~~~~~~~~~~~~~~~~~~~~~~

**PR Description Template:**

.. code-block:: markdown

   ## Description
   Brief description of changes

   ## Changes Made
   - [ ] Feature implementation
   - [ ] Tests added
   - [ ] Documentation updated

   ## Testing
   - [ ] Unit tests pass
   - [ ] Integration tests pass
   - [ ] Manual testing completed

   ## Screenshots
   (If UI changes)

**Review Checklist:**
- Code follows style guidelines
- Tests cover new functionality
- Documentation is updated
- No breaking changes (or properly documented)
- Performance impact considered

This development guide provides the foundation for contributing to Empire Builder while maintaining code quality and project consistency.