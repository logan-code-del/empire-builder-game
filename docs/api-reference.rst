API Reference
=============

Empire Builder provides both REST API endpoints and WebSocket events for real-time interaction. This reference covers all available APIs for game integration and development.

REST API Endpoints
------------------

Authentication Endpoints
~~~~~~~~~~~~~~~~~~~~~~~~

**POST /register**

Create a new user account.

*Request Body:*

.. code-block:: json

   {
       "username": "string (3+ chars, unique)",
       "email": "string (valid email, unique)", 
       "password": "string (6+ chars)",
       "confirm_password": "string (must match password)"
   }

*Response (Success):*

.. code-block:: json

   {
       "success": true,
       "message": "Account created successfully"
   }

*Response (Error):*

.. code-block:: json

   {
       "error": "Error message"
   }

*Status Codes:*
- ``200``: Success
- ``400``: Validation error
- ``500``: Server error

**POST /login**

Authenticate user and create session.

*Request Body:*

.. code-block:: json

   {
       "username": "string",
       "password": "string",
       "remember_me": "boolean (optional)"
   }

*Response (Success):*

.. code-block:: json

   {
       "success": true,
       "message": "Login successful"
   }

*Response (Error):*

.. code-block:: json

   {
       "error": "Invalid username or password"
   }

*Status Codes:*
- ``200``: Success
- ``401``: Invalid credentials
- ``400``: Missing fields

**POST /logout**

End user session (requires authentication).

*Response:*

.. code-block:: json

   {
       "success": true,
       "message": "Logged out successfully"
   }

Game Data Endpoints
~~~~~~~~~~~~~~~~~~~

**GET /api/empire/<empire_id>**

Get empire information.

*Authentication:* Required

*Parameters:*
- ``empire_id``: UUID of the empire

*Response:*

.. code-block:: json

   {
       "id": "uuid",
       "name": "Empire Name",
       "owner_id": "uuid",
       "created_at": "2024-01-01T00:00:00Z",
       "resources": {
           "gold": 1000,
           "food": 500,
           "materials": 200
       },
       "cities": [
           {
               "id": "uuid",
               "name": "City Name",
               "population": 1000,
               "buildings": [...]
           }
       ],
       "military": {
           "total_units": 50,
           "units_by_type": {...}
       }
   }

**GET /api/empires**

List all empires (paginated).

*Authentication:* Required

*Query Parameters:*
- ``page``: Page number (default: 1)
- ``limit``: Items per page (default: 20, max: 100)
- ``sort``: Sort field (name, created_at, score)
- ``order``: Sort order (asc, desc)

*Response:*

.. code-block:: json

   {
       "empires": [...],
       "pagination": {
           "page": 1,
           "limit": 20,
           "total": 150,
           "pages": 8
       }
   }

**POST /api/empire**

Create a new empire.

*Authentication:* Required

*Request Body:*

.. code-block:: json

   {
       "name": "string (unique)",
       "starting_location": {
           "x": "number",
           "y": "number"
       }
   }

*Response:*

.. code-block:: json

   {
       "success": true,
       "empire": {
           "id": "uuid",
           "name": "Empire Name",
           "owner_id": "uuid",
           "created_at": "timestamp"
       }
   }

**PUT /api/empire/<empire_id>**

Update empire information.

*Authentication:* Required (must own empire)

*Request Body:*

.. code-block:: json

   {
       "name": "string (optional)",
       "description": "string (optional)"
   }

City Management Endpoints
~~~~~~~~~~~~~~~~~~~~~~~~~

**GET /api/empire/<empire_id>/cities**

Get all cities in an empire.

*Authentication:* Required

*Response:*

.. code-block:: json

   {
       "cities": [
           {
               "id": "uuid",
               "name": "string",
               "population": "number",
               "location": {"x": "number", "y": "number"},
               "buildings": [...],
               "production": {...}
           }
       ]
   }

**POST /api/empire/<empire_id>/cities**

Create a new city.

*Authentication:* Required (must own empire)

*Request Body:*

.. code-block:: json

   {
       "name": "string",
       "location": {
           "x": "number",
           "y": "number"
       }
   }

**GET /api/city/<city_id>/buildings**

Get all buildings in a city.

*Authentication:* Required

*Response:*

.. code-block:: json

   {
       "buildings": [
           {
               "id": "uuid",
               "type": "string",
               "level": "number",
               "production": "number",
               "upkeep": "number",
               "status": "string"
           }
       ]
   }

**POST /api/city/<city_id>/buildings**

Construct a new building.

*Authentication:* Required (must own city)

*Request Body:*

.. code-block:: json

   {
       "type": "string",
       "quantity": "number (optional, default: 1)"
   }

Military Endpoints
~~~~~~~~~~~~~~~~~~

**GET /api/empire/<empire_id>/military**

Get military information.

*Authentication:* Required

*Response:*

.. code-block:: json

   {
       "total_units": "number",
       "units_by_type": {
           "soldiers": 20,
           "archers": 15,
           "knights": 5
       },
       "armies": [
           {
               "id": "uuid",
               "name": "string",
               "location": {"x": "number", "y": "number"},
               "units": {...},
               "status": "string"
           }
       ]
   }

**POST /api/city/<city_id>/train**

Train military units.

*Authentication:* Required (must own city)

*Request Body:*

.. code-block:: json

   {
       "unit_type": "string",
       "quantity": "number"
   }

**POST /api/army/<army_id>/move**

Move an army.

*Authentication:* Required (must own army)

*Request Body:*

.. code-block:: json

   {
       "destination": {
           "x": "number",
           "y": "number"
       }
   }

Battle Endpoints
~~~~~~~~~~~~~~~~

**GET /api/battles**

Get battle history.

*Authentication:* Required

*Query Parameters:*
- ``empire_id``: Filter by empire
- ``status``: Filter by status (active, completed)
- ``limit``: Number of results

*Response:*

.. code-block:: json

   {
       "battles": [
           {
               "id": "uuid",
               "attacker_id": "uuid",
               "defender_id": "uuid",
               "location": {"x": "number", "y": "number"},
               "status": "string",
               "started_at": "timestamp",
               "result": "string (if completed)"
           }
       ]
   }

**POST /api/battle**

Initiate a battle.

*Authentication:* Required

*Request Body:*

.. code-block:: json

   {
       "army_id": "uuid",
       "target_type": "string (city, army)",
       "target_id": "uuid"
   }

**GET /api/battle/<battle_id>**

Get detailed battle information.

*Authentication:* Required (must be participant)

*Response:*

.. code-block:: json

   {
       "id": "uuid",
       "attacker": {...},
       "defender": {...},
       "rounds": [...],
       "status": "string",
       "result": "string"
   }

Leaderboard Endpoints
~~~~~~~~~~~~~~~~~~~~~

**GET /api/leaderboard**

Get global rankings.

*Authentication:* Optional

*Query Parameters:*
- ``type``: Ranking type (score, military, economic)
- ``limit``: Number of results (default: 50)

*Response:*

.. code-block:: json

   {
       "rankings": [
           {
               "rank": 1,
               "empire_id": "uuid",
               "empire_name": "string",
               "score": "number",
               "owner_username": "string"
           }
       ],
       "updated_at": "timestamp"
   }

WebSocket Events
----------------

Connection
~~~~~~~~~~

Connect to WebSocket endpoint: ``/socket.io/``

*Authentication:* Session-based (must be logged in)

Client Events (Sent to Server)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**join_empire**

Join empire-specific room for updates.

*Data:*

.. code-block:: json

   {
       "empire_id": "uuid"
   }

**leave_empire**

Leave empire room.

*Data:*

.. code-block:: json

   {
       "empire_id": "uuid"
   }

**request_update**

Request current game state.

*Data:*

.. code-block:: json

   {
       "type": "string (empire, city, battle)",
       "id": "uuid"
   }

Server Events (Sent to Client)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**empire_update**

Real-time empire data changes.

*Data:*

.. code-block:: json

   {
       "empire_id": "uuid",
       "changes": {
           "resources": {...},
           "population": "number",
           "military": {...}
       },
       "timestamp": "timestamp"
   }

**battle_start**

New battle notification.

*Data:*

.. code-block:: json

   {
       "battle_id": "uuid",
       "attacker": "string",
       "defender": "string",
       "location": {"x": "number", "y": "number"}
   }

**battle_update**

Battle progress updates.

*Data:*

.. code-block:: json

   {
       "battle_id": "uuid",
       "round": "number",
       "events": [...],
       "status": "string"
   }

**battle_end**

Battle completion notification.

*Data:*

.. code-block:: json

   {
       "battle_id": "uuid",
       "winner": "string",
       "casualties": {...},
       "loot": {...}
   }

**resource_update**

Resource production updates.

*Data:*

.. code-block:: json

   {
       "empire_id": "uuid",
       "resources": {
           "gold": "number",
           "food": "number", 
           "materials": "number"
       },
       "production_rates": {...}
   }

**construction_complete**

Building construction finished.

*Data:*

.. code-block:: json

   {
       "city_id": "uuid",
       "building": {
           "id": "uuid",
           "type": "string",
           "level": "number"
       }
   }

**unit_training_complete**

Military unit training finished.

*Data:*

.. code-block:: json

   {
       "city_id": "uuid",
       "units": {
           "type": "string",
           "quantity": "number"
       }
   }

Error Handling
--------------

HTTP Status Codes
~~~~~~~~~~~~~~~~~~

- ``200``: Success
- ``201``: Created
- ``400``: Bad Request (validation error)
- ``401``: Unauthorized (authentication required)
- ``403``: Forbidden (insufficient permissions)
- ``404``: Not Found
- ``409``: Conflict (duplicate resource)
- ``429``: Too Many Requests (rate limited)
- ``500``: Internal Server Error

Error Response Format
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

   {
       "error": "Error message",
       "code": "ERROR_CODE (optional)",
       "details": "Additional details (optional)"
   }

WebSocket Error Events
~~~~~~~~~~~~~~~~~~~~~~

**error**

General error notification.

*Data:*

.. code-block:: json

   {
       "message": "Error description",
       "code": "ERROR_CODE"
   }

Rate Limiting
-------------

API endpoints are rate limited to prevent abuse:

- **Authentication endpoints**: 5 requests per minute
- **Game data endpoints**: 60 requests per minute
- **Action endpoints**: 30 requests per minute
- **WebSocket connections**: 1 per user

Rate limit headers:
- ``X-RateLimit-Limit``: Request limit
- ``X-RateLimit-Remaining``: Remaining requests
- ``X-RateLimit-Reset``: Reset timestamp

SDK and Examples
----------------

JavaScript Client Example
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: javascript

   // REST API usage
   async function getEmpire(empireId) {
       const response = await fetch(`/api/empire/${empireId}`, {
           headers: {
               'Authorization': 'Bearer ' + sessionToken
           }
       });
       return await response.json();
   }

   // WebSocket usage
   const socket = io();
   
   socket.emit('join_empire', {empire_id: 'uuid'});
   
   socket.on('empire_update', (data) => {
       console.log('Empire updated:', data);
   });

Python Client Example
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import requests
   import socketio

   # REST API
   class EmpireClient:
       def __init__(self, base_url, session_token):
           self.base_url = base_url
           self.headers = {'Authorization': f'Bearer {session_token}'}
       
       def get_empire(self, empire_id):
           response = requests.get(
               f'{self.base_url}/api/empire/{empire_id}',
               headers=self.headers
           )
           return response.json()

   # WebSocket
   sio = socketio.Client()
   
   @sio.on('empire_update')
   def on_empire_update(data):
       print('Empire updated:', data)
   
   sio.connect('http://localhost:5000')
   sio.emit('join_empire', {'empire_id': 'uuid'})

This API reference provides comprehensive coverage of Empire Builder's programmatic interfaces, enabling integration with external tools, mobile applications, and automated systems.