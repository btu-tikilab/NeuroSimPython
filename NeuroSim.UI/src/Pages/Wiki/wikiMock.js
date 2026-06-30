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
      "A collection of candidate solutions evolved together during optimization.",
  },
  {
    term: "Fitness",
    def:
      "Measures how good a solution is for solving the optimization problem.",
  },
  {
    term: "Genome",
    def:
      "The encoded representation of a candidate solution.",
  },
  {
    term: "Selection",
    def:
      "Chooses the best individuals for reproduction.",
  },
  {
    term: "Crossover",
    def:
      "Combines two parent solutions to produce offspring.",
  },
  {
    term: "Mutation",
    def:
      "Introduces random changes to maintain diversity.",
  },
  {
    term: "Elitism",
    def:
      "Copies the best individuals directly into the next generation.",
  },
  {
    term: "Seeded RNG",
    def:
      "Uses a fixed random seed to reproduce identical experimental results.",
  },
];
export const OPERATORS = [

{
    name: "EdgeSwapCrossover",
    type: "Crossover",
    desc: "Randomly splits each parent's edge set and swaps halves. Produces two children that each inherit edges from both parents."
},

{
    name: "SubgraphSwapCrossover",
    type: "Crossover",
    desc: "Samples a random node subset S and swaps all edges involving those nodes. Preserves local graph structure."
},

{
    name: "UniformGraphCrossover",
    type: "Crossover",
    desc: "For each eligible edge, independently flips a coin to decide which parent's value is copied. Produces the highest genetic diversity among crossover operators."
},

{
    name: "EdgeFlipMutation",
    type: "Mutation",
    desc: "Toggles each eligible edge with probability mutation_rate. This operator is ergodic and can eventually reach any adjacency matrix."
},

{
    name: "NodeAttrFlipMutation",
    type: "Mutation",
    desc: "Flips each node's binary activation attribute with probability mutation_rate. Directly affects active_nodes fitness."
},

{
    name: "TournamentSelection",
    type: "Selection",
    desc: "Randomly samples k individuals and returns the fittest one. Small k maintains diversity while larger k speeds convergence."
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
