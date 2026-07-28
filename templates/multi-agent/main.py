from dotenv import load_dotenv
from bindai import Agent
import os
import yaml

load_dotenv()

class MultiAgentSystem:
    def __init__(self, config_path):
        self.agents = {}
        self.agent_configs = {}
        self.conversation_history = {}  # Store history per agent
        self.load_agents(config_path)
    
    def load_agents(self, config_path):
        """Load multiple agents from YAML configuration"""
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        for agent_config in config['agents']:
            # Store config for later use
            name = agent_config['name']
            self.agent_configs[name] = agent_config
            
            # Create agent programmatically
            from bindai_provider_openai import OpenAIProvider, ProviderConfiguration
            
            # Extract model (remove provider prefix if present)
            model = agent_config['model']
            if ':' in model:
                model = model.split(':', 1)[1]  # Remove "openai:" prefix
            
            # Create provider
            provider_config = ProviderConfiguration(model=model)
            provider = OpenAIProvider(configuration=provider_config)
            
            # Create agent
            agent = Agent()
            agent.provider = provider
            
            # Set instructions
            try:
                agent.instructions = agent_config['instructions']
            except AttributeError:
                pass
            
            # Store agent
            self.agents[name] = agent
            # Initialize empty conversation history for this agent
            self.conversation_history[name] = []
            print(f"✅ Loaded agent: {name} (model: {model})")
    
    def chat_with_agent(self, agent_name, message):
        """Chat with a specific agent with memory"""
        if agent_name not in self.agents:
            return f"❌ Agent '{agent_name}' not found. Available: {', '.join(self.agents.keys())}"
        
        agent = self.agents[agent_name]
        instructions = self.agent_configs[agent_name].get('instructions', 'You are a helpful assistant.')
        
        # Add user message to history
        self.conversation_history[agent_name].append({"role": "user", "content": message})
        
        try:
            result = agent.chat(message)
            response = result.output
        except:
            result = agent.chat(message, system_prompt=instructions)
            response = result.output
        
        # Add assistant response to history
        self.conversation_history[agent_name].append({"role": "assistant", "content": response})
        
        return response
    
    def chat_with_context(self, agent_name, message, include_history=True, max_history=10):
        """Chat with context from conversation history"""
        if agent_name not in self.agents:
            return f"❌ Agent '{agent_name}' not found. Available: {', '.join(self.agents.keys())}"
        
        agent = self.agents[agent_name]
        instructions = self.agent_configs[agent_name].get('instructions', 'You are a helpful assistant.')
        
        # Build context from history if enabled
        if include_history and self.conversation_history[agent_name]:
            # Get last N messages from history
            history = self.conversation_history[agent_name][-max_history:]
            
            # Build context string
            context = "Previous conversation:\n"
            for entry in history:
                role = entry['role']
                content = entry['content']
                context += f"{role.capitalize()}: {content}\n"
            
            # Combine context with new message
            full_message = f"{context}\nUser: {message}"
        else:
            full_message = message
        
        # Add user message to history
        self.conversation_history[agent_name].append({"role": "user", "content": message})
        
        try:
            result = agent.chat(full_message)
            response = result.output
        except:
            result = agent.chat(full_message, system_prompt=instructions)
            response = result.output
        
        # Add assistant response to history
        self.conversation_history[agent_name].append({"role": "assistant", "content": response})
        
        return response
    
    def clear_history(self, agent_name=None):
        """Clear conversation history for an agent or all agents"""
        if agent_name:
            if agent_name in self.conversation_history:
                self.conversation_history[agent_name] = []
                return f"✅ Cleared conversation history for {agent_name}"
            else:
                return f"❌ Agent '{agent_name}' not found"
        else:
            # Clear all agents' history
            for name in self.conversation_history:
                self.conversation_history[name] = []
            return "✅ Cleared all conversation history"
    
    def get_history(self, agent_name, limit=None):
        """Get conversation history for an agent"""
        if agent_name not in self.conversation_history:
            return f"❌ Agent '{agent_name}' not found"
        
        history = self.conversation_history[agent_name]
        if limit:
            history = history[-limit:]
        
        if not history:
            return "No conversation history yet."
        
        result = f"📋 Conversation History for {agent_name}:\n"
        result += "=" * 40 + "\n"
        for entry in history:
            role = entry['role'].capitalize()
            content = entry['content']
            result += f"{role}: {content}\n"
            result += "-" * 40 + "\n"
        
        return result
    
    def list_agents(self):
        """List all available agents"""
        return list(self.agents.keys())
    
    def get_agent_info(self, agent_name):
        """Get information about a specific agent"""
        if agent_name in self.agent_configs:
            config = self.agent_configs[agent_name]
            history_count = len(self.conversation_history.get(agent_name, []))
            return f"Name: {config['name']}\nModel: {config['model']}\nHistory: {history_count} messages\nInstructions: {config['instructions'][:100]}..."
        return None

def main():
    # Clear screen (optional)
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Load multi-agent system
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "agents.yaml")
    
    if not os.path.exists(config_path):
        print(f"❌ Error: agents.yaml not found at {config_path}")
        print("Please create agents.yaml file first.")
        return
    
    print("🤖 Multi-Agent Chat System")
    print("=" * 50)
    
    # Initialize multi-agent system
    try:
        multi_agent = MultiAgentSystem(config_path)
    except Exception as e:
        print(f"❌ Error loading agents: {e}")
        return
    
    print(f"\n📋 Available agents: {', '.join(multi_agent.list_agents())}")
    print("\n💡 Commands:")
    print("  • 'list'           - List all available agents")
    print("  • 'switch <name>'  - Switch to another agent")
    print("  • 'info <name>'    - Show agent information")
    print("  • 'history'        - Show conversation history for current agent")
    print("  • 'history <name>' - Show conversation history for specific agent")
    print("  • 'clear'          - Clear history for current agent")
    print("  • 'clear all'      - Clear all conversation history")
    print("  • 'context on'     - Enable context from history")
    print("  • 'context off'    - Disable context from history")
    print("  • 'exit' / 'quit'  - Exit the chat")
    print("  • 'help'           - Show this help message")
    print("=" * 50)
    
    current_agent = multi_agent.list_agents()[0]  # Default to first agent
    use_context = True  # Context is enabled by default
    print(f"\n👉 Current agent: {current_agent}")
    print(f"📝 Context mode: {'ON' if use_context else 'OFF'}")
    print("Type your message to start chatting...\n")
    
    while True:
        try:
            user_input = input(f"[{current_agent}] You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in {"exit", "quit", "bye"}:
                print("👋 Goodbye! Thanks for chatting.")
                break
            
            if user_input.lower() == "help":
                print("\n💡 Commands:")
                print("  • 'list'           - List all available agents")
                print("  • 'switch <name>'  - Switch to another agent")
                print("  • 'info <name>'    - Show agent information")
                print("  • 'history'        - Show conversation history for current agent")
                print("  • 'history <name>' - Show conversation history for specific agent")
                print("  • 'clear'          - Clear history for current agent")
                print("  • 'clear all'      - Clear all conversation history")
                print("  • 'context on'     - Enable context from history")
                print("  • 'context off'    - Disable context from history")
                print("  • 'exit' / 'quit'  - Exit the chat")
                print("  • 'help'           - Show this help message")
                continue
            
            if user_input.lower() == "list":
                print(f"\n📋 Available agents: {', '.join(multi_agent.list_agents())}")
                print(f"👉 Current agent: {current_agent}")
                continue
            
            if user_input.lower().startswith("switch "):
                parts = user_input.split(" ", 1)
                if len(parts) == 2:
                    new_agent = parts[1].strip()
                    if new_agent in multi_agent.list_agents():
                        current_agent = new_agent
                        history_count = len(multi_agent.conversation_history.get(current_agent, []))
                        print(f"✅ Switched to agent: {current_agent}")
                        print(f"📝 History has {history_count} messages")
                    else:
                        print(f"❌ Agent '{new_agent}' not found.")
                        print(f"   Available: {', '.join(multi_agent.list_agents())}")
                continue
            
            if user_input.lower().startswith("info "):
                parts = user_input.split(" ", 1)
                if len(parts) == 2:
                    agent_name = parts[1].strip()
                    info = multi_agent.get_agent_info(agent_name)
                    if info:
                        print(f"\n📋 Agent Information:\n{info}")
                    else:
                        print(f"❌ Agent '{agent_name}' not found.")
                continue
            
            if user_input.lower() == "history" or user_input.lower().startswith("history "):
                if user_input.lower() == "history":
                    # Show history for current agent
                    history = multi_agent.get_history(current_agent)
                    print(f"\n{history}")
                else:
                    # Show history for specific agent
                    parts = user_input.split(" ", 1)
                    if len(parts) == 2:
                        agent_name = parts[1].strip()
                        history = multi_agent.get_history(agent_name)
                        print(f"\n{history}")
                continue
            
            if user_input.lower() == "clear":
                # Clear history for current agent
                result = multi_agent.clear_history(current_agent)
                print(result)
                continue
            
            if user_input.lower() == "clear all":
                # Clear all history
                result = multi_agent.clear_history()
                print(result)
                continue
            
            if user_input.lower() == "context on":
                use_context = True
                print("✅ Context mode enabled. Agent will remember conversation history.")
                continue
            
            if user_input.lower() == "context off":
                use_context = False
                print("❌ Context mode disabled. Agent will respond without history.")
                continue
            
            # Process message with current agent
            print(f"[{current_agent}] Thinking...", end="", flush=True)
            
            if use_context:
                # Use chat with context
                response = multi_agent.chat_with_context(current_agent, user_input)
            else:
                # Use regular chat without context
                response = multi_agent.chat_with_agent(current_agent, user_input)
            
            print("\r", end="")  # Clear the "Thinking..." line
            print(f"[{current_agent}] Assistant: {response}")
            
            # Show conversation count
            history_count = len(multi_agent.conversation_history.get(current_agent, []))
            print(f"📝 History: {history_count} messages")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye! Thanks for chatting.")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()