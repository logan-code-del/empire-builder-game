"""
Empire Builder - Alliance System
Handles alliance creation, management, diplomacy, and cooperative gameplay
"""

import sqlite3
import uuid
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from enum import Enum

class AllianceRole(Enum):
    LEADER = "leader"
    OFFICER = "officer"
    MEMBER = "member"

class AllianceInviteStatus(Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    DECLINED = "declined"
    EXPIRED = "expired"

class AllianceRelationType(Enum):
    NEUTRAL = "neutral"
    ALLIED = "allied"
    WAR = "war"
    NAP = "nap"  # Non-Aggression Pact

@dataclass
class Alliance:
    id: str
    name: str
    tag: str  # Short alliance tag (3-5 characters)
    description: str
    leader_id: str
    created_at: str
    member_count: int
    total_power: int
    is_recruiting: bool
    min_power_requirement: int
    alliance_color: str
    treasury_gold: int = 0
    treasury_food: int = 0
    treasury_iron: int = 0
    treasury_oil: int = 0

@dataclass
class AllianceMember:
    alliance_id: str
    empire_id: str
    role: AllianceRole
    joined_at: str
    contribution_gold: int = 0
    contribution_food: int = 0
    contribution_iron: int = 0
    contribution_oil: int = 0
    last_active: str = None

@dataclass
class AllianceInvite:
    id: str
    alliance_id: str
    empire_id: str
    invited_by: str
    status: AllianceInviteStatus
    created_at: str
    expires_at: str
    message: str = ""

@dataclass
class AllianceRelation:
    alliance1_id: str
    alliance2_id: str
    relation_type: AllianceRelationType
    created_at: str
    created_by: str
    expires_at: str = None

class AllianceDatabase:
    def __init__(self):
        self.init_alliance_db()
    
    def init_alliance_db(self):
        """Initialize alliance database tables"""
        conn = sqlite3.connect('empire_game.db')
        cursor = conn.cursor()
        
        # Alliances table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alliances (
                id TEXT PRIMARY KEY,
                name TEXT UNIQUE NOT NULL,
                tag TEXT UNIQUE NOT NULL,
                description TEXT,
                leader_id TEXT NOT NULL,
                created_at TEXT NOT NULL,
                is_recruiting BOOLEAN DEFAULT 1,
                min_power_requirement INTEGER DEFAULT 0,
                alliance_color TEXT DEFAULT '#007bff',
                treasury_gold INTEGER DEFAULT 0,
                treasury_food INTEGER DEFAULT 0,
                treasury_iron INTEGER DEFAULT 0,
                treasury_oil INTEGER DEFAULT 0,
                FOREIGN KEY (leader_id) REFERENCES empires (id)
            )
        ''')
        
        # Alliance members table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alliance_members (
                alliance_id TEXT NOT NULL,
                empire_id TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'member',
                joined_at TEXT NOT NULL,
                contribution_gold INTEGER DEFAULT 0,
                contribution_food INTEGER DEFAULT 0,
                contribution_iron INTEGER DEFAULT 0,
                contribution_oil INTEGER DEFAULT 0,
                last_active TEXT,
                PRIMARY KEY (alliance_id, empire_id),
                FOREIGN KEY (alliance_id) REFERENCES alliances (id),
                FOREIGN KEY (empire_id) REFERENCES empires (id)
            )
        ''')
        
        # Alliance invites table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alliance_invites (
                id TEXT PRIMARY KEY,
                alliance_id TEXT NOT NULL,
                empire_id TEXT NOT NULL,
                invited_by TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                created_at TEXT NOT NULL,
                expires_at TEXT NOT NULL,
                message TEXT,
                FOREIGN KEY (alliance_id) REFERENCES alliances (id),
                FOREIGN KEY (empire_id) REFERENCES empires (id),
                FOREIGN KEY (invited_by) REFERENCES empires (id)
            )
        ''')
        
        # Alliance relations table (for diplomacy between alliances)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alliance_relations (
                alliance1_id TEXT NOT NULL,
                alliance2_id TEXT NOT NULL,
                relation_type TEXT NOT NULL DEFAULT 'neutral',
                created_at TEXT NOT NULL,
                created_by TEXT NOT NULL,
                expires_at TEXT,
                PRIMARY KEY (alliance1_id, alliance2_id),
                FOREIGN KEY (alliance1_id) REFERENCES alliances (id),
                FOREIGN KEY (alliance2_id) REFERENCES alliances (id),
                FOREIGN KEY (created_by) REFERENCES empires (id)
            )
        ''')
        
        # Alliance messages/announcements table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alliance_messages (
                id TEXT PRIMARY KEY,
                alliance_id TEXT NOT NULL,
                sender_id TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at TEXT NOT NULL,
                is_announcement BOOLEAN DEFAULT 0,
                FOREIGN KEY (alliance_id) REFERENCES alliances (id),
                FOREIGN KEY (sender_id) REFERENCES empires (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_alliance(self, name: str, tag: str, description: str, leader_id: str, 
                       color: str = "#007bff") -> Optional[str]:
        """Create a new alliance"""
        conn = sqlite3.connect('empire_game.db')
        cursor = conn.cursor()
        
        try:
            # Check if name or tag already exists
            cursor.execute('SELECT id FROM alliances WHERE name = ? OR tag = ?', (name, tag))
            if cursor.fetchone():
                conn.close()
                return None  # Alliance name/tag already exists
            
            # Create alliance
            alliance_id = str(uuid.uuid4())
            
            cursor.execute('''
                INSERT INTO alliances (id, name, tag, description, leader_id, created_at, alliance_color)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                alliance_id, name, tag, description, leader_id,
                datetime.now().isoformat(), color
            ))
            
            # Add leader as first member
            cursor.execute('''
                INSERT INTO alliance_members (alliance_id, empire_id, role, joined_at)
                VALUES (?, ?, ?, ?)
            ''', (alliance_id, leader_id, AllianceRole.LEADER.value, datetime.now().isoformat()))
            
            conn.commit()
            conn.close()
            return alliance_id
            
        except sqlite3.IntegrityError:
            conn.close()
            return None
    
    def get_alliance(self, alliance_id: str) -> Optional[Alliance]:
        """Get alliance by ID"""
        conn = sqlite3.connect('empire_game.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT a.*, COUNT(am.empire_id) as member_count,
                   COALESCE(SUM(e.military_power), 0) as total_power
            FROM alliances a
            LEFT JOIN alliance_members am ON a.id = am.alliance_id
            LEFT JOIN empires e ON am.empire_id = e.id
            WHERE a.id = ?
            GROUP BY a.id
        ''', (alliance_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Alliance(
                id=row[0], name=row[1], tag=row[2], description=row[3],
                leader_id=row[4], created_at=row[5], is_recruiting=bool(row[6]),
                min_power_requirement=row[7], alliance_color=row[8],
                treasury_gold=row[9], treasury_food=row[10],
                treasury_iron=row[11], treasury_oil=row[12],
                member_count=row[13], total_power=row[14]
            )
        return None
    
    def get_alliance_by_name(self, name: str) -> Optional[Alliance]:
        """Get alliance by name"""
        conn = sqlite3.connect('empire_game.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT id FROM alliances WHERE name = ?', (name,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return self.get_alliance(row[0])
        return None
    
    def get_alliance_by_tag(self, tag: str) -> Optional[Alliance]:
        """Get alliance by tag"""
        conn = sqlite3.connect('empire_game.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT id FROM alliances WHERE tag = ?', (tag,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return self.get_alliance(row[0])
        return None
    
    def get_empire_alliance(self, empire_id: str) -> Optional[Alliance]:
        """Get the alliance that an empire belongs to"""
        conn = sqlite3.connect('empire_game.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT alliance_id FROM alliance_members WHERE empire_id = ?
        ''', (empire_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return self.get_alliance(row[0])
        return None
    
    def get_alliance_members(self, alliance_id: str) -> List[Dict[str, Any]]:
        """Get all members of an alliance with their empire info"""
        conn = sqlite3.connect('empire_game.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT am.*, e.name, e.ruler, e.military_power, e.land_area
            FROM alliance_members am
            JOIN empires e ON am.empire_id = e.id
            WHERE am.alliance_id = ?
            ORDER BY 
                CASE am.role 
                    WHEN 'leader' THEN 1 
                    WHEN 'officer' THEN 2 
                    ELSE 3 
                END,
                am.joined_at
        ''', (alliance_id,))
        
        members = []
        for row in cursor.fetchall():
            members.append({
                'alliance_id': row[0],
                'empire_id': row[1],
                'role': row[2],
                'joined_at': row[3],
                'contribution_gold': row[4],
                'contribution_food': row[5],
                'contribution_iron': row[6],
                'contribution_oil': row[7],
                'last_active': row[8],
                'empire_name': row[9],
                'ruler_name': row[10],
                'military_power': row[11],
                'land_area': row[12]
            })
        
        conn.close()
        return members
    
    def get_all_alliances(self) -> List[Alliance]:
        """Get all alliances"""
        conn = sqlite3.connect('empire_game.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT a.*, COUNT(am.empire_id) as member_count,
                   COALESCE(SUM(e.military_power), 0) as total_power
            FROM alliances a
            LEFT JOIN alliance_members am ON a.id = am.alliance_id
            LEFT JOIN empires e ON am.empire_id = e.id
            GROUP BY a.id
            ORDER BY total_power DESC
        ''')
        
        alliances = []
        for row in cursor.fetchall():
            alliances.append(Alliance(
                id=row[0], name=row[1], tag=row[2], description=row[3],
                leader_id=row[4], created_at=row[5], is_recruiting=bool(row[6]),
                min_power_requirement=row[7], alliance_color=row[8],
                treasury_gold=row[9], treasury_food=row[10],
                treasury_iron=row[11], treasury_oil=row[12],
                member_count=row[13], total_power=row[14]
            ))
        
        conn.close()
        return alliances
    
    def invite_to_alliance(self, alliance_id: str, empire_id: str, invited_by: str, 
                          message: str = "") -> Optional[str]:
        """Send an alliance invitation"""
        conn = sqlite3.connect('empire_game.db')
        cursor = conn.cursor()
        
        try:
            # Check if empire is already in an alliance
            cursor.execute('SELECT alliance_id FROM alliance_members WHERE empire_id = ?', (empire_id,))
            if cursor.fetchone():
                conn.close()
                return None  # Empire already in alliance
            
            # Check if there's already a pending invite
            cursor.execute('''
                SELECT id FROM alliance_invites 
                WHERE alliance_id = ? AND empire_id = ? AND status = 'pending'
            ''', (alliance_id, empire_id))
            if cursor.fetchone():
                conn.close()
                return None  # Invite already exists
            
            # Create invite
            invite_id = str(uuid.uuid4())
            expires_at = (datetime.now() + timedelta(days=7)).isoformat()
            
            cursor.execute('''
                INSERT INTO alliance_invites (id, alliance_id, empire_id, invited_by, 
                                            status, created_at, expires_at, message)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                invite_id, alliance_id, empire_id, invited_by,
                AllianceInviteStatus.PENDING.value, datetime.now().isoformat(),
                expires_at, message
            ))
            
            conn.commit()
            conn.close()
            return invite_id
            
        except sqlite3.IntegrityError:
            conn.close()
            return None
    
    def respond_to_invite(self, invite_id: str, accept: bool) -> bool:
        """Accept or decline an alliance invitation"""
        conn = sqlite3.connect('empire_game.db')
        cursor = conn.cursor()
        
        try:
            # Get invite details
            cursor.execute('''
                SELECT alliance_id, empire_id, status, expires_at
                FROM alliance_invites WHERE id = ?
            ''', (invite_id,))
            
            invite_data = cursor.fetchone()
            if not invite_data or invite_data[2] != 'pending':
                conn.close()
                return False
            
            alliance_id, empire_id, status, expires_at = invite_data
            
            # Check if invite has expired
            if datetime.now() > datetime.fromisoformat(expires_at):
                cursor.execute('''
                    UPDATE alliance_invites SET status = 'expired' WHERE id = ?
                ''', (invite_id,))
                conn.commit()
                conn.close()
                return False
            
            if accept:
                # Add empire to alliance
                cursor.execute('''
                    INSERT INTO alliance_members (alliance_id, empire_id, role, joined_at)
                    VALUES (?, ?, ?, ?)
                ''', (alliance_id, empire_id, AllianceRole.MEMBER.value, datetime.now().isoformat()))
                
                # Update invite status
                cursor.execute('''
                    UPDATE alliance_invites SET status = 'accepted' WHERE id = ?
                ''', (invite_id,))
            else:
                # Update invite status
                cursor.execute('''
                    UPDATE alliance_invites SET status = 'declined' WHERE id = ?
                ''', (invite_id,))
            
            conn.commit()
            conn.close()
            return True
            
        except sqlite3.IntegrityError:
            conn.close()
            return False
    
    def leave_alliance(self, empire_id: str) -> bool:
        """Leave current alliance"""
        conn = sqlite3.connect('empire_game.db')
        cursor = conn.cursor()
        
        try:
            # Check if empire is alliance leader
            cursor.execute('''
                SELECT a.id FROM alliances a
                JOIN alliance_members am ON a.id = am.alliance_id
                WHERE am.empire_id = ? AND am.role = 'leader'
            ''', (empire_id,))
            
            if cursor.fetchone():
                conn.close()
                return False  # Leaders cannot leave, must transfer leadership first
            
            # Remove from alliance
            cursor.execute('DELETE FROM alliance_members WHERE empire_id = ?', (empire_id,))
            
            conn.commit()
            conn.close()
            return True
            
        except sqlite3.Error:
            conn.close()
            return False
    
    def kick_member(self, alliance_id: str, empire_id: str, kicked_by: str) -> bool:
        """Kick a member from alliance"""
        conn = sqlite3.connect('empire_game.db')
        cursor = conn.cursor()
        
        try:
            # Check if kicker has permission (leader or officer)
            cursor.execute('''
                SELECT role FROM alliance_members 
                WHERE alliance_id = ? AND empire_id = ?
            ''', (alliance_id, kicked_by))
            
            kicker_role = cursor.fetchone()
            if not kicker_role or kicker_role[0] not in ['leader', 'officer']:
                conn.close()
                return False
            
            # Check target's role
            cursor.execute('''
                SELECT role FROM alliance_members 
                WHERE alliance_id = ? AND empire_id = ?
            ''', (alliance_id, empire_id))
            
            target_role = cursor.fetchone()
            if not target_role:
                conn.close()
                return False
            
            # Officers cannot kick other officers or leaders
            if kicker_role[0] == 'officer' and target_role[0] in ['leader', 'officer']:
                conn.close()
                return False
            
            # Cannot kick the leader
            if target_role[0] == 'leader':
                conn.close()
                return False
            
            # Remove member
            cursor.execute('''
                DELETE FROM alliance_members 
                WHERE alliance_id = ? AND empire_id = ?
            ''', (alliance_id, empire_id))
            
            conn.commit()
            conn.close()
            return True
            
        except sqlite3.Error:
            conn.close()
            return False
    
    def promote_member(self, alliance_id: str, empire_id: str, promoted_by: str, 
                      new_role: AllianceRole) -> bool:
        """Promote/demote a member"""
        conn = sqlite3.connect('empire_game.db')
        cursor = conn.cursor()
        
        try:
            # Check if promoter is leader
            cursor.execute('''
                SELECT role FROM alliance_members 
                WHERE alliance_id = ? AND empire_id = ?
            ''', (alliance_id, promoted_by))
            
            promoter_role = cursor.fetchone()
            if not promoter_role or promoter_role[0] != 'leader':
                conn.close()
                return False
            
            # Update member role
            cursor.execute('''
                UPDATE alliance_members SET role = ?
                WHERE alliance_id = ? AND empire_id = ?
            ''', (new_role.value, alliance_id, empire_id))
            
            conn.commit()
            conn.close()
            return True
            
        except sqlite3.Error:
            conn.close()
            return False
    
    def contribute_to_treasury(self, alliance_id: str, empire_id: str, 
                             gold: int = 0, food: int = 0, iron: int = 0, oil: int = 0) -> bool:
        """Contribute resources to alliance treasury"""
        conn = sqlite3.connect('empire_game.db')
        cursor = conn.cursor()
        
        try:
            # Update alliance treasury
            cursor.execute('''
                UPDATE alliances SET 
                    treasury_gold = treasury_gold + ?,
                    treasury_food = treasury_food + ?,
                    treasury_iron = treasury_iron + ?,
                    treasury_oil = treasury_oil + ?
                WHERE id = ?
            ''', (gold, food, iron, oil, alliance_id))
            
            # Update member contributions
            cursor.execute('''
                UPDATE alliance_members SET
                    contribution_gold = contribution_gold + ?,
                    contribution_food = contribution_food + ?,
                    contribution_iron = contribution_iron + ?,
                    contribution_oil = contribution_oil + ?
                WHERE alliance_id = ? AND empire_id = ?
            ''', (gold, food, iron, oil, alliance_id, empire_id))
            
            conn.commit()
            conn.close()
            return True
            
        except sqlite3.Error:
            conn.close()
            return False
    
    def get_empire_invites(self, empire_id: str) -> List[Dict[str, Any]]:
        """Get pending invites for an empire"""
        conn = sqlite3.connect('empire_game.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT ai.*, a.name, a.tag, e.name as inviter_name
            FROM alliance_invites ai
            JOIN alliances a ON ai.alliance_id = a.id
            JOIN empires e ON ai.invited_by = e.id
            WHERE ai.empire_id = ? AND ai.status = 'pending' AND ai.expires_at > ?
            ORDER BY ai.created_at DESC
        ''', (empire_id, datetime.now().isoformat()))
        
        invites = []
        for row in cursor.fetchall():
            invites.append({
                'id': row[0],
                'alliance_id': row[1],
                'empire_id': row[2],
                'invited_by': row[3],
                'status': row[4],
                'created_at': row[5],
                'expires_at': row[6],
                'message': row[7],
                'alliance_name': row[8],
                'alliance_tag': row[9],
                'inviter_name': row[10]
            })
        
        conn.close()
        return invites

# Global alliance database instance
alliance_db = AllianceDatabase()