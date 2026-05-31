import type { Lesson } from "@/lib/types";

/**
 * Pillar H: Reinforcement Learning. Ordered lesson curriculum per subsection.
 * Lesson order is the array order; prerequisites are bare ids within the same
 * subsection or "subId/lessonId" across subsections.
 */
export const H_CURRICULUM: Record<string, Lesson[]> = {
  H1: [
    {
      id: "mdp-formulation",
      title: "Markov decision processes and returns",
      goal: "Define an MDP by its states, actions, transitions, and rewards; write the discounted return and the state- and action-value functions of a policy.",
      prerequisites: ["A2/expectation", "A2/markov-chains"],
    },
    {
      id: "bellman-equations",
      title: "Bellman expectation and optimality equations",
      goal: "Derive the Bellman expectation equations from the recursive structure of the return, and state the Bellman optimality equations that characterize the optimal value function.",
      prerequisites: ["mdp-formulation"],
    },
    {
      id: "dynamic-programming",
      title: "Policy iteration and value iteration",
      goal: "Solve a known MDP exactly with policy evaluation, policy improvement, and value iteration, and prove each is a contraction that converges to the optimal value function.",
      prerequisites: ["bellman-equations"],
    },
    {
      id: "monte-carlo",
      title: "Monte Carlo prediction and control",
      goal: "Estimate value functions from complete sampled episodes without a model, and turn first-visit Monte Carlo evaluation into a control algorithm via epsilon-greedy improvement.",
      prerequisites: ["mdp-formulation", "A2/lln-clt"],
    },
    {
      id: "temporal-difference",
      title: "Temporal-difference learning and bootstrapping",
      goal: "Derive the TD(0) update from the Bellman expectation equation, understand bootstrapping as sampled dynamic programming, and place TD between Monte Carlo and DP on the bias-variance axis.",
      prerequisites: ["monte-carlo", "dynamic-programming"],
    },
    {
      id: "q-learning-sarsa",
      title: "Q-learning and SARSA",
      goal: "Derive the off-policy Q-learning and on-policy SARSA control updates, contrast their targets, and understand when each converges to the optimal action-value function.",
      prerequisites: ["temporal-difference"],
    },
  ],
  H2: [
    {
      id: "function-approximation",
      title: "Value function approximation and the deadly triad",
      goal: "Replace a value table with a parametric approximator trained by semi-gradient TD, and understand why function approximation, bootstrapping, and off-policy data together can diverge.",
      prerequisites: ["H1/q-learning-sarsa", "A3/sgd"],
    },
    {
      id: "dqn",
      title: "Deep Q-networks: replay and target networks",
      goal: "Stabilize Q-learning with a neural network using experience replay and a slowly-updated target network, and state the DQN loss and training loop.",
      prerequisites: ["function-approximation", "D1/backprop"],
    },
    {
      id: "dqn-improvements",
      title: "Double, dueling, and prioritized DQN",
      goal: "Fix Q-learning's maximization bias with Double DQN, separate state value from advantage with the dueling architecture, and weight replay by TD error, the pieces that compose Rainbow.",
      prerequisites: ["dqn"],
    },
    {
      id: "policy-gradient",
      title: "The policy gradient theorem and REINFORCE",
      goal: "Derive the policy gradient theorem with the log-derivative trick, obtain the REINFORCE estimator, and reduce its variance with a baseline.",
      prerequisites: ["H1/mdp-formulation", "A3/sgd"],
    },
    {
      id: "actor-critic",
      title: "Actor-critic and generalized advantage estimation",
      goal: "Replace the Monte Carlo return in REINFORCE with a learned critic, derive the advantage actor-critic update, and trade bias for variance with GAE(lambda).",
      prerequisites: ["policy-gradient", "function-approximation"],
    },
    {
      id: "ppo",
      title: "Trust regions and proximal policy optimization",
      goal: "Motivate the trust-region constraint behind TRPO, derive the PPO clipped surrogate objective, and understand why clipping keeps policy updates conservative.",
      prerequisites: ["actor-critic"],
    },
    {
      id: "ddpg-td3-sac",
      title: "Continuous control: DDPG, TD3, and SAC",
      goal: "Extend Q-learning to continuous actions with a deterministic actor (DDPG), correct overestimation with twin critics and target smoothing (TD3), and add entropy regularization for exploration (SAC).",
      prerequisites: ["ppo", "H1/q-learning-sarsa"],
    },
  ],
  H3: [
    {
      id: "dyna-q",
      title: "Dyna-Q: integrating planning and learning",
      goal: "Learn a model from experience and use it to generate simulated transitions that accelerate value learning, unifying model-free and model-based updates.",
      prerequisites: ["H1/q-learning-sarsa"],
    },
    {
      id: "mcts-alphazero",
      title: "Monte Carlo tree search and AlphaZero",
      goal: "Build a search tree with UCT selection and backpropagation, then replace rollouts and priors with a neural network trained by self-play, the AlphaZero loop.",
      prerequisites: ["H1/dynamic-programming", "H4/bandits-exploration"],
    },
    {
      id: "muzero",
      title: "MuZero: planning with a learned model",
      goal: "Remove AlphaZero's need for known dynamics by learning a latent transition model trained only to predict reward, value, and policy, enabling search without the true simulator.",
      prerequisites: ["mcts-alphazero"],
    },
    {
      id: "world-models-dreamer",
      title: "World models and Dreamer",
      goal: "Train a latent dynamics model from pixels and learn a policy entirely inside its imagined rollouts, backpropagating returns through the model (Dreamer).",
      prerequisites: ["dyna-q", "D4/vae"],
    },
  ],
  H4: [
    {
      id: "bandits-exploration",
      title: "Bandits: epsilon-greedy, UCB, and Thompson sampling",
      goal: "Formalize the exploration-exploitation tradeoff in the multi-armed bandit, derive the UCB confidence bonus and Thompson sampling, and compare their regret.",
      prerequisites: ["A2/bayes-rule", "H1/mdp-formulation"],
    },
    {
      id: "intrinsic-motivation",
      title: "Intrinsic motivation and random network distillation",
      goal: "Drive exploration in sparse-reward MDPs with intrinsic bonuses from prediction error and count-based novelty, and implement random network distillation.",
      prerequisites: ["bandits-exploration", "H2/dqn"],
    },
  ],
  H5: [
    {
      id: "imitation-learning",
      title: "Behavioral cloning and DAgger",
      goal: "Frame imitation as supervised learning on expert state-action pairs, diagnose the compounding-error problem from distribution shift, and fix it with the DAgger interactive correction loop.",
      prerequisites: ["H2/policy-gradient"],
    },
    {
      id: "inverse-rl",
      title: "Inverse RL and adversarial imitation",
      goal: "Recover a reward that explains expert behavior with maximum-entropy IRL, and connect the result to GAIL, which matches occupancy measures with a GAN-style discriminator.",
      prerequisites: ["imitation-learning", "A2/entropy"],
    },
    {
      id: "offline-rl",
      title: "Offline RL: CQL and IQL",
      goal: "Explain why standard Q-learning fails on a fixed dataset, then control the distribution shift with conservative Q-learning (CQL) and implicit Q-learning (IQL).",
      prerequisites: ["H2/ddpg-td3-sac"],
    },
    {
      id: "multi-agent-rl",
      title: "Multi-agent RL and self-play",
      goal: "Extend MDPs to stochastic games, see why independent learning is nonstationary, and use centralized-training-decentralized-execution and self-play to reach equilibria.",
      prerequisites: ["H2/policy-gradient"],
    },
    {
      id: "hierarchical-rl",
      title: "Hierarchical RL and the options framework",
      goal: "Define temporally-extended actions as options over a semi-MDP, write the intra-option value updates, and understand feudal goal-conditioned hierarchies.",
      prerequisites: ["H1/mdp-formulation", "H2/actor-critic"],
    },
  ],
  H6: [
    {
      id: "rl-as-llm-finetuning",
      title: "Language generation as an MDP",
      goal: "Cast autoregressive text generation as a token-level MDP, identify the policy, reward, and KL-to-reference penalty, and place the RLHF pipeline in this RL frame.",
      prerequisites: ["H2/ppo", "E4/ppo-rlhf"],
    },
    {
      id: "rlvr-reasoning",
      title: "RLVR: verifier rewards for reasoning",
      goal: "Replace a learned reward model with a programmatic verifier, optimize with a group-relative baseline (GRPO), and explain the R1-style emergence of long reasoning chains.",
      prerequisites: ["rl-as-llm-finetuning", "E4/grpo"],
    },
    {
      id: "reward-hacking",
      title: "Reward hacking and overoptimization",
      goal: "Explain why optimizing a proxy reward eventually degrades the true objective (Goodhart), quantify it with reward-model overoptimization scaling, and mitigate it with KL control and reward ensembles.",
      prerequisites: ["rl-as-llm-finetuning", "E4/reward-modeling"],
    },
  ],
};
