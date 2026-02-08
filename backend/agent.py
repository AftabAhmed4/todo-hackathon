"""
Gemini AI Agent Configuration for Todo Management.

Stateless AI agent that interprets natural language and executes MCP tools.
"""
import os
import json
from typing import List, Dict, Any, Optional
import google.generativeai as genai
from mcp_tools import (
    TOOLS,
    CreateTodoInput,
    ListTodosInput,
    UpdateTodoInput,
    DeleteTodoInput,
    CompleteTodoInput
)

from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

# Gemini client instance (initialized lazily)
_model: Optional[Any] = None


def get_gemini_model(tools=None):
    """
    Get or create Gemini model instance.

    Args:
        tools: Optional list of tools to configure the model with

    Returns:
        Gemini model instance

    Raises:
        ValueError: If GEMINI_API_KEY is not set
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set")
    genai.configure(api_key=api_key)

    # Create a new model instance with tools if provided
    if tools:
        return genai.GenerativeModel(
            'gemini-2.5-flash',
            tools=tools
        )
    else:
        return genai.GenerativeModel('gemini-2.5-flash')


# System prompt for the todo management assistant
SYSTEM_PROMPT = """You are a helpful todo management assistant. Your role is to help users manage their todo list through natural conversation.

You have access to the following tools:
- create_todo: Create a new todo item with a title and optional description
- list_todos: List all todos, optionally filtered by status (pending, in_progress, completed)
- update_todo: Update a todo's title and/or description
- delete_todo: Delete a todo permanently
- complete_todo: Mark a todo as completed or incomplete

When users ask you to perform actions, use the appropriate tool. Be conversational and friendly in your responses.

Examples:
- "Add a todo to buy groceries" → Use create_todo
- "Show me my todos" → Use list_todos
- "Mark todo 5 as done" → Use complete_todo with completed=true
- "Delete the first todo" → Use delete_todo
- "Change the title of todo 3 to 'Call dentist'" → Use update_todo

Always confirm actions and provide clear feedback about what was done.
"""


def convert_tools_to_gemini_format() -> List[Dict[str, Any]]:
    """
    Convert MCP tools to Gemini function calling format.

    Returns:
        List of tool definitions in Gemini format
    """
    gemini_tools = []

    for tool_name, tool_config in TOOLS.items():
        # Get the input schema
        input_schema = tool_config["input_schema"]
        schema_dict = input_schema.model_json_schema()

        # Extract properties and required fields
        properties = schema_dict.get("properties", {})
        required = schema_dict.get("required", [])

        # Convert Pydantic types to Gemini types
        gemini_properties = {}
        for prop_name, prop_schema in properties.items():
            prop_type = prop_schema.get("type", "string")

            # Map JSON Schema types to Gemini types
            type_mapping = {
                "string": "STRING",
                "integer": "INTEGER",
                "number": "NUMBER",
                "boolean": "BOOLEAN",
                "array": "ARRAY",
                "object": "OBJECT"
            }

            gemini_prop = {
                "type": type_mapping.get(prop_type, "STRING"),
                "description": prop_schema.get("description", "")
            }

            # Handle optional fields
            if "default" in prop_schema:
                gemini_prop["nullable"] = True

            gemini_properties[prop_name] = gemini_prop

        # Convert to Gemini function format
        gemini_tool = {
            "name": tool_name,
            "description": tool_config["description"],
            "parameters": {
                "type": "OBJECT",
                "properties": gemini_properties,
                "required": required
            }
        }

        gemini_tools.append(gemini_tool)

    return gemini_tools


def execute_tool(tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute a tool with the given arguments.

    Args:
        tool_name: Name of the tool to execute
        arguments: Dictionary of arguments for the tool

    Returns:
        Tool execution result
    """
    if tool_name not in TOOLS:
        return {
            "success": False,
            "error": f"Unknown tool: {tool_name}"
        }

    tool_config = TOOLS[tool_name]
    tool_function = tool_config["function"]
    input_schema = tool_config["input_schema"]

    try:
        # Validate and parse input
        input_data = input_schema(**arguments)

        # Execute the tool
        result = tool_function(input_data)

        return result
    except Exception as e:
        return {
            "success": False,
            "error": f"Tool execution error: {str(e)}"
        }


def run_agent(user_id: int, messages: List[Dict[str, str]], model_name: str = "gemini-1.5-flash") -> Dict[str, Any]:
    """
    Run the Gemini agent with conversation history.

    This is a stateless function that processes a conversation and returns the agent's response.

    Args:
        user_id: ID of the user (for tool execution context)
        messages: List of conversation messages [{"role": "user/assistant", "content": "..."}]
        model_name: Gemini model to use (default: gemini-1.5-flash)

    Returns:
        Dictionary with agent response and any tool calls made
    """
    try:
        # Convert tools to Gemini format
        tools = convert_tools_to_gemini_format()

        # Get Gemini model with tools configured
        model = get_gemini_model(tools=[{"function_declarations": tools}])

        # Build conversation history for Gemini
        # Gemini expects a different format - we'll use the chat interface
        chat_history = []
        for msg in messages[:-1]:  # Exclude the last message
            role = "user" if msg["role"] == "user" else "model"
            chat_history.append({
                "role": role,
                "parts": [msg["content"]]
            })

        # Start chat with history
        chat = model.start_chat(history=chat_history)

        # Get the last user message
        last_message = messages[-1]["content"] if messages else ""

        # Send message (tools are already configured in the model)
        response = chat.send_message(last_message)

        # Check if there are function calls
        try:
            # Check if response has function calls
            has_function_call = (
                response.candidates and
                len(response.candidates) > 0 and
                response.candidates[0].content.parts and
                len(response.candidates[0].content.parts) > 0 and
                hasattr(response.candidates[0].content.parts[0], 'function_call') and
                response.candidates[0].content.parts[0].function_call
            )

            if has_function_call:
                function_call = response.candidates[0].content.parts[0].function_call
                tool_name = function_call.name
                tool_arguments = dict(function_call.args)

                # Add user_id to arguments if not present
                if "user_id" not in tool_arguments:
                    tool_arguments["user_id"] = user_id

                # Execute the tool
                result = execute_tool(tool_name, tool_arguments)

                # Send the function response back to the model
                response = chat.send_message(
                    genai.protos.Content(
                        parts=[genai.protos.Part(
                            function_response=genai.protos.FunctionResponse(
                                name=tool_name,
                                response={"result": result}
                            )
                        )]
                    )
                )

                # Get the final text response
                final_response = response.text

                return {
                    "success": True,
                    "response": final_response,
                    "tool_calls": [{
                        "tool": tool_name,
                        "arguments": tool_arguments,
                        "result": result
                    }]
                }
            else:
                # No function call, just return the text response
                return {
                    "success": True,
                    "response": response.text,
                    "tool_calls": []
                }
        except AttributeError as e:
            # If there's an attribute error, just return the text response
            return {
                "success": True,
                "response": response.text if hasattr(response, 'text') else str(response),
                "tool_calls": []
            }

    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return {
            "success": False,
            "error": f"Agent execution error: {str(e)}\n{error_details}",
            "response": "I'm sorry, I encountered an error processing your request. Please try again."
        }
