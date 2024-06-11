# train_ai_without_display.py
# Author: Henry Shi

from board import Board
from qlearning_agent import QLearningAgent

def train_agents_without_display(num_episodes=50000, max_steps=150):
    """
    Train two AI agents without visual display.

    Parameters:
    num_episodes (int): Number of training episodes.
    max_steps (int): Maximum steps per episode.
    """
    ai_agent_1 = QLearningAgent(actions=['flip', 'move'], player=1)
    ai_agent_2 = QLearningAgent(actions=['flip', 'move'], player=2)

    #load previous Q-tables
    try:
        ai_agent_1.load_q_table('ai_agent_1_q_table.pkl')
        ai_agent_2.load_q_table('ai_agent_2_q_table.pkl')
        print("Q-tables loaded successfully.")
    except FileNotFoundError:
        print("No previous Q-tables found, starting fresh.")

    for episode in range(num_episodes):
        board = Board()
        state_1 = ai_agent_1.get_state(board)
        state_2 = ai_agent_2.get_state(board)
        done = False
        step_count = 0

        while not done and step_count < max_steps:
            # AI 1 takes action
            action_1 = ai_agent_1.choose_action(state_1, board)
            next_state_1, reward_1, done_1, action_detail_1 = ai_agent_1.step(state_1, action_1, board, step_count)
            ai_agent_1.update_q_table(state_1, action_1, reward_1, next_state_1)

            if done_1:
                break

            # AI 2 takes action
            action_2 = ai_agent_2.choose_action(state_2, board)
            next_state_2, reward_2, done_2, action_detail_2 = ai_agent_2.step(state_2, action_2, board, step_count)
            ai_agent_2.update_q_table(state_2, action_2, reward_2, next_state_2)

            # Update states and check if the game is done
            state_1 = next_state_1
            state_2 = next_state_2
            done = done_1 or done_2

            step_count += 1

        if (episode + 1) % 1000 == 0:
            print(f"Episode {episode + 1}/{num_episodes} completed")

    ai_agent_1.save_q_table('ai_agent_1_q_table.pkl')
    ai_agent_2.save_q_table('ai_agent_2_q_table.pkl')

if __name__ == "__main__":
    train_agents_without_display()
