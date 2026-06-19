import hashlib
from typing import Dict, Optional, List
from utils import generate_id, validate_non_empty_string, format_timestamp

class User:
    """
    Represents a user within the Smart Task Manager system.
    """
    def __init__(self, username: str, role: str = "member", user_id: str = None, created_at: float = None):
        """
        Initializes a new User.
        """
        self.user_id = user_id if user_id else generate_id("user")
        self.username = validate_non_empty_string(username, "Username")
        self.role = role
        self.created_at = created_at if created_at else format_timestamp()

    def to_dict(self) -> Dict:
        """
        Serializes user object to dictionary format.
        """
        return {
            "user_id": self.user_id,
            "username": self.username,
            "role": self.role,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "User":
        """
        Deserializes a dictionary into a User object.
        """
        return cls(
            username=data.get("username", "Unknown"),
            role=data.get("role", "member"),
            user_id=data.get("user_id"),
            created_at=data.get("created_at")
        )

class UserManager:
    """
    Handles user sessions, roles, and in-memory user registry.
    This module encapsulates user-centric operations so the main application
    logic remains clean. Note: In a real system, authentication would be persistent.
    For this simulation, we hold users in memory.
    """
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.current_user: Optional[User] = None
        self._initialize_default_users()

    def _initialize_default_users(self):
        """
        Seeds the system with initial users to simulate a multi-team environment.
        """
        admin = User("AdminUser", role="admin", user_id="user_admin1")
        alice = User("Alice", role="member", user_id="user_alice1")
        bob = User("Bob", role="member", user_id="user_bob1")

        self.users[admin.username.lower()] = admin
        self.users[alice.username.lower()] = alice
        self.users[bob.username.lower()] = bob

    def register_user(self, username: str, role: str = "member") -> User:
        """
        Registers a new user in the system.
        """
        try:
            valid_name = validate_non_empty_string(username, "Username")
            if valid_name.lower() in self.users:
                raise ValueError("User already exists.")
            
            new_user = User(valid_name, role)
            self.users[valid_name.lower()] = new_user
            return new_user
        except Exception as e:
            raise Exception(f"Registration failed: {str(e)}")

    def login(self, username: str) -> bool:
        """
        Simulates a user login.
        """
        valid_name = username.strip().lower()
        if valid_name in self.users:
            self.current_user = self.users[valid_name]
            return True
        return False

    def logout(self) -> None:
        """
        Simulates a user logout, clearing the current session.
        """
        self.current_user = None

    def get_current_user(self) -> Optional[User]:
        """
        Returns the logged-in user, if any.
        """
        return self.current_user

    def get_all_users(self) -> List[User]:
        """
        Retrieves a list of all users registered in the system.
        """
        return list(self.users.values())

    def is_admin(self) -> bool:
        """
        Checks if the currently logged-in user has admin privileges.
        """
        if self.current_user and self.current_user.role == "admin":
            return True
        return False
    //this is user manager
//this file end hear
// this is useful
