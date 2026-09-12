import time
import math
import random

class Player:
    """Represents a simple player with a position."""
    def __init__(self, x, y):
        self.x = x
        self.y = y

class EnemyAI:
    """Simulates a basic enemy AI making decisions based on player proximity and health."""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 100
        self.aggro_range = 10.0 # Distance at which AI becomes aggressive
        self.flee_range = 3.0   # Distance at which AI tries to flee if low health

    def _simulate_complex_thought(self):
        """Simulates a computationally intensive task an AI might perform (e.g., pathfinding, target evaluation)."""
        # This loop adds artificial CPU load to mimic complex AI logic.
        # The article discusses CPU impact, so this simulates that aspect.
        result = 0.0
        for _ in range(1000): # A loop to add some CPU load
            result += math.sin(random.random()) * math.cos(random.random())
        return result

    def make_decision(self, player):
        """The core AI decision-making logic that we want to benchmark."""

        # Step 1: Simulate internal processing/thinking (CPU-bound operations)
        self._simulate_complex_thought() # This function call represents the 'cost' of AI thinking.

        # Step 2: Evaluate environment (e.g., distance to player)
        distance = math.sqrt((self.x - player.x)**2 + (self.y - player.y)**2)

        # Step 3: Make a decision based on evaluation
        if self.health < 30 and distance < self.flee_range:
            return "FLEE" # Low health, player too close
        elif distance < self.aggro_range:
            return "ATTACK" # Player in range
        else:
            return "PATROL" # No immediate threat, or player out of range

# --- Benchmark Setup ---
if __name__ == "__main__":
    # Initialize game entities
    player = Player(x=5, y=5)
    enemy_ai = EnemyAI(x=15, y=15)

    # Number of times to run the AI's decision logic for benchmarking.
    # A higher number gives more reliable average times but takes longer.
    NUM_ITERATIONS = 100000

    print(f"Benchmarking AI decision-making for {NUM_ITERATIONS} iterations...")

    # Record the start time using a high-resolution performance counter.
    # This is crucial for accurate benchmarking of short operations.
    start_time = time.perf_counter()

    # Run the AI decision loop multiple times to gather performance data.
    for i in range(NUM_ITERATIONS):
        # Simulate slight player movement and enemy health changes to vary AI decisions
        # and prevent caching effects from making the benchmark unrealistic.
        if i % 10000 == 0: # Update player/enemy state periodically
            player.x = random.uniform(0, 20)
            player.y = random.uniform(0, 20)
            enemy_ai.health = random.randint(10, 100)

        decision = enemy_ai.make_decision(player)
        # In a real game, 'decision' would trigger actions (e.g., move, attack animation).
        # For benchmarking, we only care about the time taken to make the decision itself.

    # Record the end time.
    end_time = time.perf_counter()

    # Calculate and display benchmark results.
    total_time = end_time - start_time
    avg_time_per_decision = total_time / NUM_ITERATIONS

    print("\n--- Benchmark Results ---")
    print(f"Total time for {NUM_ITERATIONS} decisions: {total_time:.4f} seconds")
    print(f"Average time per decision: {avg_time_per_decision * 1000000:.4f} microseconds")
    print(f"Decisions per second: {1 / avg_time_per_decision:.2f}")

    # Provide a simple interpretation of the results, relating to game performance.
    # A typical game runs at 60 FPS, meaning each frame has ~16.67 milliseconds (16670 microseconds).
    # The AI's decision time should be a tiny fraction of this to avoid impacting FPS.
    if avg_time_per_decision * 1000000 > 1000: # If decision takes more than 1 millisecond
        print("\nWarning: Average decision time is relatively high. This AI might impact game FPS.")
    else:
        print("\nNote: Average decision time seems reasonable for this simple AI.")
