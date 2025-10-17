"""
Example demonstrating the new URL features in pypresence
========================================================

This example shows how to use the new state_url, details_url,
large_url, and small_url parameters.

These URL parameters allow you to make text and images clickable
in Discord Rich Presence.
"""

import time

from pypresence import Presence
from pypresence.types import ActivityType

# Your Discord Application Client ID
client_id = "YOUR_CLIENT_ID_HERE"

# Initialize the presence client
RPC = Presence(client_id)

# Connect to Discord
RPC.connect()

print("Connected to Discord! Setting up Rich Presence with URLs...")

# Example 1: Basic state with clickable URL
RPC.update(
    state="Playing an awesome game",
    state_url="https://example.com/game",
    details="In the main menu",
)
print("Example 1: State with URL set")
time.sleep(5)

# Example 2: Both state and details with URLs
RPC.update(
    state="Currently Coding",
    state_url="https://github.com/your-username/your-repo",
    details="Working on pypresence",
    details_url="https://github.com/qwertyquerty/pypresence",
)
print("Example 2: State and details with URLs set")
time.sleep(5)

# Example 3: Images with clickable URLs
RPC.update(
    state="Streaming",
    large_image="streaming_large",  # Your uploaded image key
    large_text="Live Now!",
    large_url="https://twitch.tv/your-channel",  # Click the large image
    small_image="streaming_small",  # Your uploaded image key
    small_text="Online",
    small_url="https://youtube.com/your-channel",  # Click the small image
)
print("Example 3: Images with clickable URLs set")
time.sleep(5)

# Example 4: Everything together with buttons
RPC.update(
    state="Building Something Cool",
    state_url="https://github.com/your-username",
    details="pypresence with URL support",
    details_url="https://github.com/qwertyquerty/pypresence",
    large_image="project_logo",
    large_text="Project Logo",
    large_url="https://your-project-website.com",
    small_image="status_icon",
    small_text="Active",
    small_url="https://status.your-project.com",
    buttons=[
        {"label": "View Project", "url": "https://github.com/your-username/project"},
        {"label": "Documentation", "url": "https://docs.your-project.com"},
    ],
)
print("Example 4: Full rich presence with all URLs and buttons set")
time.sleep(5)

# Example 5: Using with activity types
RPC.update(
    activity_type=ActivityType.LISTENING,
    state="My Favorite Song",
    state_url="https://open.spotify.com/track/example",
    details="By My Favorite Artist",
    details_url="https://open.spotify.com/artist/example",
    large_image="album_cover",
    large_url="https://open.spotify.com/album/example",
)
print("Example 5: Listening activity with URLs set")
time.sleep(5)

# Keep the presence active
print("\nRich Presence active! Press Ctrl+C to exit...")
try:
    while True:
        time.sleep(15)
except KeyboardInterrupt:
    print("\nClosing connection...")
    RPC.close()
    print("Disconnected from Discord.")
