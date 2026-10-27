export const WIKI_SECTIONS = [
  {
    id: "overview",
    label: "Overview",
  },
  {
    id: "ga",
    label: "Genetic Algorithms (GA)",
  },
  {
    id: "gp",
    label: "Genetic Programming (GP)",
  },
  {
    id: "es",
    label: "Evolution Strategies (ES)",
  },
  {
    id: "ep",
    label: "Evolutionary Programming (EP)",
  },
  {
    id: "concepts",
    label: "Key Concepts",
    hasArrow: true,
  },
  {
    id: "operators",
    label: "Operators",
    hasArrow: true,
  },
  {
    id: "guides",
    label: "Playground Guides",
    hasArrow: true,
  },
];

export const PARADIGM_CARDS = [
  {
    id: "ga",
    title: "Genetic Algorithms (GA)",
    icon: "🧬",
    color: "#6366F1",
    colorDim: "#EEF2FF",
    desc:
      "Population-based optimization using selection, crossover and mutation to evolve better solutions.",
    linkLabel: "Learn More →",
  },
  {
    id: "gp",
    title: "Genetic Programming (GP)",
    icon: "🌳",
    color: "#059669",
    colorDim: "#ECFDF5",
    desc:
      "Automatically evolves computer programs represented as syntax trees.",
    linkLabel: "Learn More →",
  },
  {
    id: "es",
    title: "Evolution Strategies (ES)",
    icon: "📈",
    color: "#D97706",
    colorDim: "#FFF7ED",
    desc:
      "Optimization technique focusing on mutation and self-adaptive strategy parameters.",
    linkLabel: "Learn More →",
  },
  {
    id: "ep",
    title: "Evolutionary Programming (EP)",
    icon: "⚙️",
    color: "#7C3AED",
    colorDim: "#F5F3FF",
    desc:
      "Evolutionary approach emphasizing mutation and behavioral adaptation.",
    linkLabel: "Learn More →",
  },
];

export const HOW_IT_WORKS = [
  {
    label: "Initialize",
    sub: "Create initial population",
  },
  {
    label: "Evaluate",
    sub: "Compute fitness values",
  },
  {
    label: "Select",
    sub: "Choose best individuals",
  },
  {
    label: "Crossover & Mutation",
    sub: "Generate offspring",
  },
  {
    label: "Replace",
    sub: "Build next generation",
  },
  {
    label: "Repeat",
    sub: "Continue until convergence",
  },
];

export const KEY_CONCEPTS = [
  {
    term: "Population",
    def:
      "A collection of candidate solutions (individuals) that exist at a particular stage (generation) of the genetic algorithm.",
    detailedDef: "Instead of working with a single solution, GAs simultaneously evaluate and evolve multiple solutions which helps maintain diversity and reduces the risk of getting trapped in local optima.\n\n• Population size significantly affects convergence behavior.\n• Larger populations increase exploration but raise computational cost.\n• Smaller populations converge faster but risk premature convergence.",
    image: "https://media.geeksforgeeks.org/wp-content/uploads/20251223154437017860/population.webp",
    practicalExample: "As illustrated in the diagram, a Population is initialized at \"Generation 0\". It is made up of multiple distinct candidate solutions, labeled here as \"Chromosome 1\" through \"Chromosome N\". Each of these chromosomes is evaluated independently, and the best ones are selected to breed the next generation of solutions."
  },
  {
    term: "Chromosome",
    def:
      "A complete candidate solution to the given optimization problem.",
    detailedDef: "A chromosome represents a complete candidate solution to the problem. It is a structured collection of genes that encodes all decision variables required to evaluate a solution using the fitness function.",
    image: "https://media.geeksforgeeks.org/wp-content/uploads/20251223154637456128/chromosome.webp",
    practicalExample: "As shown in the diagram, a Chromosome is made up of individual \"Genes\" (such as A1, A2, A3) which encode specific traits. The collective behavior of all these genes determines the quality of the chromosome."
  },
  {
    term: "Gene",
    def:
      "The fundamental unit of information in a candidate solution.",
    detailedDef: "In Genetic Algorithms, a gene is the smallest structural component of a candidate solution (chromosome). It represents a single parameter, variable, or trait of the problem being solved.\n\nDepending on the problem, a gene can be encoded as:\n• A Binary Bit (0 or 1)\n• A Real-Valued Number (e.g., 3.14)\n• A Character or Symbol (e.g., 'A')",
    image: "https://media.geeksforgeeks.org/wp-content/uploads/20251223154637456128/chromosome.webp",
    practicalExample: "Look at the diagram above. The entire array is the \"Chromosome\", but each individual slot (labeled A1, A2, A3, etc.) is a single Gene. \n\nFor example, if an algorithm is trying to guess the target word \"HELLO\", the entire string is the chromosome, and each individual letter ('H', 'E', 'L', 'L', 'O') is a gene. The algorithm might mutate the gene 'P' into 'L' to get closer to the target word."
  },
  {
    term: "Fitness Function",
    def:
      "A mathematical formulation that evaluates how well a chromosome solves the problem.",
    detailedDef: "The fitness function acts as the guiding force of the genetic algorithm by determining which individuals are more likely to reproduce.\n\n• Higher fitness implies better solution quality.\n• The fitness function is heavily problem-specific.\n• It can be designed for either maximization or minimization.",
    image: "https://www.tutorialspoint.com/genetic_algorithms/images/fitness_function.jpg",
    practicalExample: "Following the previous example of guessing the target word \"HELLO\": The Fitness Function could simply count how many letters are in the correct position.\n\n• The chromosome 'HALO_' has 1 correct letter ('H'), so its fitness score is 1.\n• The chromosome 'HELLP' has 4 correct letters ('H','E','L','L'), so its fitness score is 4.\n\nBecause 'HELLP' has a much higher fitness score, the algorithm will select it to survive and reproduce, while discarding 'HALO_'."
  },
  {
    term: "Selection",
    def:
      "The process of choosing chromosomes from the current population to act as parents.",
    detailedDef: "The goal is to give preference to fitter individuals while still maintaining population diversity. Common selection methods include:\n\n• Roulette Wheel Selection: Probability of selection is proportional to fitness.\n• Tournament Selection: Randomly selects a group and chooses the fittest among them.\n• Stochastic Universal Sampling: Uses multiple equally spaced pointers to reduce sampling bias.",
    image: "https://media.geeksforgeeks.org/wp-content/uploads/20251223154806452649/fitness_value_3.webp",
    practicalExample: "The diagram illustrates Tournament Selection: a small group of individuals is randomly picked from the population, and they \"compete\" based on their fitness. The one with the highest fitness value is selected as a parent for the next generation."
  },
  {
    term: "Crossover",
    def:
      "A genetic operator that combines genetic material from two parents to generate offspring.",
    detailedDef: "Crossover enables the algorithm to exploit existing high-quality building blocks. Types include:\n\n• One Point Crossover: A random point is chosen, and genes are mixed.\n• Multi Point Crossover: Multiple points are chosen for mixing.\n• Uniform Crossover: A coin flip decides which parent's gene is inherited for every position.",
    image: "https://media.geeksforgeeks.org/wp-content/uploads/20251223154903842734/crossover_point.webp",
    practicalExample: "In the One Point Crossover diagram, a specific crossover point is chosen. The offspring inherits the first part of its genes from Parent 1 and the second part from Parent 2, effectively combining their traits into a new candidate solution."
  },
  {
    term: "Mutation",
    def:
      "Introduces random changes in genes to maintain genetic diversity.",
    detailedDef: "Mutation helps prevent premature convergence and enables the exploration of new solutions. Types include:\n\n• Bit Flip Mutation: One or more random bits are flipped.\n• Swap Mutation: Two points are chosen and switched.\n• Scramble/Inversion: A segment is randomly scrambled or reversed.",
    image: "https://media.geeksforgeeks.org/wp-content/uploads/20251223155205004886/crossover_point_6.webp",
    practicalExample: "The diagram demonstrates Bit Flip Mutation for binary encoding. At a random position, a '0' is flipped to a '1' (or vice versa), introducing a completely new trait that wasn't necessarily present in the parents."
  },
  {
    term: "Termination Criteria",
    def:
      "Conditions under which the genetic algorithm stops executing.",
    detailedDef: "Proper termination prevents unnecessary computation while ensuring solution quality. Common conditions:\n\n• Maximum number of generations reached.\n• Desired or threshold fitness achieved.\n• No improvement in fitness for several generations.\n• Computational time limit exceeded.",
    image: "https://media.geeksforgeeks.org/wp-content/uploads/20251223154806452649/fitness_value_3.webp",
    practicalExample: "Imagine the algorithm is trying to find the highest point on a mountain. The algorithm might stop (terminate) when it reaches a specific altitude (Target Fitness), or it might stop if it has taken 1,000 steps without going any higher (No Improvement), or it might simply stop after exactly 5,000 steps (Maximum Generations) regardless of where it is."
  }
];
export const OPERATORS = [
  {
      name: "EdgeSwapCrossover",
      type: "Crossover",
      desc: "Randomly splits each parent's edge set and swaps halves. Produces two children that each inherit edges from both parents.",
      example: "Example: Parent A has edges (1-2, 2-3) and Parent B has edges (1-3, 3-4). The crossover might take edge 1-2 from A and 3-4 from B, creating Child 1 with edges (1-2, 3-4). This preserves large structural pieces from both parents."
  },
  {
      name: "SubgraphSwapCrossover",
      type: "Crossover",
      desc: "Samples a random node subset S and swaps all edges involving those nodes. Preserves local graph structure.",
      example: "Example: The algorithm selects nodes {2, 3} as the subset. All connections between node 2 and 3, as well as their connections to other nodes, are swapped between Parent A and Parent B. This is great for preserving clusters or 'communities' in the graph."
  },
  {
      name: "UniformGraphCrossover",
      type: "Crossover",
      desc: "For each eligible edge, independently flips a coin to decide which parent's value is copied. Produces the highest genetic diversity among crossover operators.",
      example: "Example: For every single possible connection in the graph (e.g., node 1 to node 2), a coin is flipped. Heads: Child gets Parent A's connection. Tails: Child gets Parent B's connection. This creates highly diverse, scattered offspring."
  },
  {
      name: "EdgeFlipMutation",
      type: "Mutation",
      desc: "Toggles each eligible edge with probability mutation_rate. This operator is ergodic and can eventually reach any adjacency matrix.",
      example: "Example: If the mutation rate is 1%, then for every possible edge, there is a 1% chance it flips. An existing edge might be deleted, or a non-existent edge might suddenly be created, introducing random new pathways."
  },
  {
      name: "NodeAttrFlipMutation",
      type: "Mutation",
      desc: "Flips each node's binary activation attribute with probability mutation_rate. Directly affects active_nodes fitness.",
      example: "Example: Instead of changing the edges (connections), this mutates the nodes themselves. A 'deactivated' node might suddenly turn 'active', changing how the overall graph scores in the fitness function."
  },
  {
      name: "TournamentSelection",
      type: "Selection",
      desc: "Randomly samples k individuals and returns the fittest one. Small k maintains diversity while larger k speeds convergence.",
      example: "Example: If tournament size is 3, three random graphs are picked from the population. The one with the highest fitness score wins the tournament and is selected to be a parent. This ensures good solutions are picked without perfectly sorting the entire population."
  }
];
export const PLAYGROUND_GUIDES = [
  {
    title: "GraphGA",
    steps: [
      "Choose the graph dataset.",
      "Select population size.",
      "Select crossover operator.",
      "Run the algorithm.",
      "Analyze the fitness graph."
    ]
  },
  {
    title: "BitGA",
    steps: [
      "Choose OneMax problem.",
      "Select population size.",
      "Select mutation rate.",
      "Run the algorithm.",
      "Observe convergence."
    ]
  }
];
