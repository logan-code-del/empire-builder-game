/**
 * Electric-SQL Client for Empire Builder
 * Handles real-time database synchronization
 */

const { Electric } = require('electric-sql');
const Database = require('better-sqlite3');
const WebSocket = require('ws');

class EmpireElectricClient {
    constructor() {
        this.db = null;
        this.electric = null;
        this.isConnected = false;
    }

    async initialize() {
        try {
            // Initialize SQLite database
            this.db = new Database('empire_electric.db');
            
            // Initialize Electric-SQL
            this.electric = await Electric(this.db, {
                url: process.env.ELECTRIC_URL || 'ws://localhost:5133',
                debug: true
            });

            // Set up real-time subscriptions
            await this.setupSubscriptions();
            
            this.isConnected = true;
            console.log('🔌 Electric-SQL client initialized successfully');
            
            return this.electric;
        } catch (error) {
            console.error('❌ Failed to initialize Electric-SQL:', error);
            throw error;
        }
    }

    async setupSubscriptions() {
        const { db } = this.electric;

        // Subscribe to empire changes
        const empireShape = await db.empires.sync();
        console.log('📡 Subscribed to empires table');

        // Subscribe to battle changes
        const battleShape = await db.battles.sync();
        console.log('⚔️ Subscribed to battles table');

        // Subscribe to messages
        const messageShape = await db.messages.sync();
        console.log('💬 Subscribed to messages table');

        // Subscribe to game events
        const eventShape = await db.game_events.sync();
        console.log('🎮 Subscribed to game events table');

        // Subscribe to resource transactions
        const transactionShape = await db.resource_transactions.sync();
        console.log('💰 Subscribed to resource transactions table');
    }

    // Empire operations
    async createEmpire(empireData) {
        const { db } = this.electric;
        
        try {
            const empire = await db.empires.create({
                data: {
                    id: empireData.id,
                    name: empireData.name,
                    ruler: empireData.ruler,
                    land: empireData.land || 2000,
                    resources: JSON.stringify(empireData.resources || {
                        gold: 10000, food: 5000, iron: 2000, oil: 1000, population: 1000
                    }),
                    military: JSON.stringify(empireData.military || {
                        infantry: 100, tanks: 10, aircraft: 5, ships: 8
                    }),
                    location: JSON.stringify(empireData.location || { lat: 0, lng: 0 }),
                    is_ai: empireData.is_ai || false,
                    cities: JSON.stringify(empireData.cities || {}),
                    buildings: JSON.stringify(empireData.buildings || {
                        farm: 0, mine: 0, oil_well: 0, bank: 0, factory: 0, 
                        barracks: 0, research_lab: 0, hospital: 0
                    })
                }
            });

            // Log creation event
            await this.logGameEvent(empire.id, 'empire_created', {
                empire_name: empire.name,
                ruler: empire.ruler
            });

            console.log(`🏰 Empire created: ${empire.name}`);
            return empire;
        } catch (error) {
            console.error('❌ Failed to create empire:', error);
            throw error;
        }
    }

    async updateEmpire(empireId, updates) {
        const { db } = this.electric;
        
        try {
            const empire = await db.empires.update({
                where: { id: empireId },
                data: {
                    ...updates,
                    updated_at: new Date().toISOString()
                }
            });

            console.log(`🔄 Empire updated: ${empireId}`);
            return empire;
        } catch (error) {
            console.error('❌ Failed to update empire:', error);
            throw error;
        }
    }

    async getEmpire(empireId) {
        const { db } = this.electric;
        
        try {
            const empire = await db.empires.findUnique({
                where: { id: empireId }
            });
            return empire;
        } catch (error) {
            console.error('❌ Failed to get empire:', error);
            throw error;
        }
    }

    async getAllEmpires() {
        const { db } = this.electric;
        
        try {
            const empires = await db.empires.findMany({
                orderBy: { created_at: 'desc' }
            });
            return empires;
        } catch (error) {
            console.error('❌ Failed to get empires:', error);
            throw error;
        }
    }

    // Battle operations
    async createBattle(battleData) {
        const { db } = this.electric;
        
        try {
            const battle = await db.battles.create({
                data: {
                    id: battleData.id,
                    attacker_id: battleData.attacker_id,
                    defender_id: battleData.defender_id,
                    attacking_units: JSON.stringify(battleData.attacking_units),
                    defending_units: JSON.stringify(battleData.defending_units),
                    status: 'active'
                }
            });

            // Log battle event
            await this.logGameEvent(battleData.attacker_id, 'battle_started', {
                defender_id: battleData.defender_id,
                battle_id: battle.id
            });

            console.log(`⚔️ Battle created: ${battle.id}`);
            return battle;
        } catch (error) {
            console.error('❌ Failed to create battle:', error);
            throw error;
        }
    }

    async completeBattle(battleId, result) {
        const { db } = this.electric;
        
        try {
            const battle = await db.battles.update({
                where: { id: battleId },
                data: {
                    result: JSON.stringify(result.outcome),
                    casualties: JSON.stringify(result.casualties),
                    resources_gained: JSON.stringify(result.resources_gained || {}),
                    land_gained: result.land_gained || 0,
                    status: 'completed',
                    completed_at: new Date().toISOString()
                }
            });

            // Log battle completion
            await this.logGameEvent(battle.attacker_id, 'battle_completed', {
                battle_id: battleId,
                result: result.outcome.winner
            });

            console.log(`🏆 Battle completed: ${battleId}`);
            return battle;
        } catch (error) {
            console.error('❌ Failed to complete battle:', error);
            throw error;
        }
    }

    // Message operations
    async sendMessage(fromEmpire, toEmpire, message, messageType = 'general') {
        const { db } = this.electric;
        
        try {
            const msg = await db.messages.create({
                data: {
                    id: `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
                    from_empire: fromEmpire,
                    to_empire: toEmpire,
                    message: message,
                    message_type: messageType,
                    read: false
                }
            });

            console.log(`💬 Message sent from ${fromEmpire} to ${toEmpire}`);
            return msg;
        } catch (error) {
            console.error('❌ Failed to send message:', error);
            throw error;
        }
    }

    // Game event logging
    async logGameEvent(empireId, eventType, eventData) {
        const { db } = this.electric;
        
        try {
            const event = await db.game_events.create({
                data: {
                    id: `event_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
                    empire_id: empireId,
                    event_type: eventType,
                    event_data: JSON.stringify(eventData)
                }
            });

            return event;
        } catch (error) {
            console.error('❌ Failed to log game event:', error);
            throw error;
        }
    }

    // Resource transaction logging
    async logResourceTransaction(empireId, transactionType, resources, reason) {
        const { db } = this.electric;
        
        try {
            const transaction = await db.resource_transactions.create({
                data: {
                    id: `tx_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
                    empire_id: empireId,
                    transaction_type: transactionType,
                    resources: JSON.stringify(resources),
                    reason: reason
                }
            });

            return transaction;
        } catch (error) {
            console.error('❌ Failed to log resource transaction:', error);
            throw error;
        }
    }

    // Real-time subscriptions for frontend
    async subscribeToEmpireChanges(empireId, callback) {
        const { db } = this.electric;
        
        try {
            const subscription = db.empires.liveUnique({
                where: { id: empireId }
            });

            subscription.subscribe(callback);
            console.log(`📡 Subscribed to empire changes: ${empireId}`);
            
            return subscription;
        } catch (error) {
            console.error('❌ Failed to subscribe to empire changes:', error);
            throw error;
        }
    }

    async subscribeToBattles(callback) {
        const { db } = this.electric;
        
        try {
            const subscription = db.battles.liveMany({
                where: { status: 'active' }
            });

            subscription.subscribe(callback);
            console.log('⚔️ Subscribed to active battles');
            
            return subscription;
        } catch (error) {
            console.error('❌ Failed to subscribe to battles:', error);
            throw error;
        }
    }

    async subscribeToMessages(empireId, callback) {
        const { db } = this.electric;
        
        try {
            const subscription = db.messages.liveMany({
                where: { 
                    OR: [
                        { to_empire: empireId },
                        { from_empire: empireId }
                    ]
                },
                orderBy: { created_at: 'desc' }
            });

            subscription.subscribe(callback);
            console.log(`💬 Subscribed to messages for empire: ${empireId}`);
            
            return subscription;
        } catch (error) {
            console.error('❌ Failed to subscribe to messages:', error);
            throw error;
        }
    }

    // Cleanup
    async disconnect() {
        if (this.db) {
            this.db.close();
        }
        this.isConnected = false;
        console.log('🔌 Electric-SQL client disconnected');
    }
}

// Export for use in Python via subprocess or HTTP API
if (require.main === module) {
    const client = new EmpireElectricClient();
    
    // Start the Electric-SQL client
    client.initialize().then(() => {
        console.log('🚀 Empire Builder Electric-SQL client is running');
        
        // Keep the process alive
        process.on('SIGINT', async () => {
            console.log('🛑 Shutting down Electric-SQL client...');
            await client.disconnect();
            process.exit(0);
        });
    }).catch(error => {
        console.error('💥 Failed to start Electric-SQL client:', error);
        process.exit(1);
    });
}

module.exports = EmpireElectricClient;