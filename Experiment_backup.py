from Agent.Brain import LearningAgent

def run_experiment(rewards):
    # Start with a fresh agent without loading or saving permanent memory
    agent = LearningAgent(use_saved_memory=False)
    action_counts = {
        "explore": 0,
        "rest": 0,
        "study": 0,
    }
    total_reward = 0
    total_experiences = 200
    print("AI AGENT PERFORMANCE EXPERIMENT")
    print("-" * 35)
    print("\nRewards used:", rewards)
    print("Starting scores:", agent.action_scores)
    for experience in range(1, total_experiences + 1):
        action = agent.choose_action()
        reward = rewards[action]
        agent.learn(action, reward)
        action_counts[action] += 1
        total_reward += reward
        # Display average reward every 20 experiences
        if experience % 20 == 0:
            average_reward = total_reward / experience
            print(
                f"After {experience:3} experiences | "
                f"Average reward: {average_reward:.2f}"
            )
    print("\nACTION STATISTICS")
    print("-" * 35)
    for action, count in action_counts.items():
        percentage = count / total_experiences * 100
        print(
            f"{action}: {count} times "
            f"({percentage:.1f}%)"
        )
    print("\nFINAL LEARNED SCORES")
    agent.show_knowledge()
if __name__ == "__main__":
    rewards = {
        "explore": 1,
        "rest": 0,
        "study": 10,
    }
    run_experiment(rewards)